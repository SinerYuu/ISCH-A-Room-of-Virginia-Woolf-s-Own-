# scripts/tei_to_rdf.py
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from lxml import etree
import json, pathlib, re

import pathlib, os
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "tei"

places_file = DATA_DIR / "Places_related_to_Virginia_Woolf.xml"  # 用你的实际文件名


# ===== 0) 基本配置（命名空间、基 URI、常用实体） =====
BASE = "https://example.org/woolf/"     # 数据集的基地址（和本体的 IRI 区分开）
NS_WOOLFO = Namespace("https://example.org/woolf-ontology#")  # 你在 Protégé 定的
SCHEMA   = Namespace("https://schema.org/")
DCTERMS  = Namespace("http://purl.org/dc/terms/")
FOAF     = Namespace("http://xmlns.com/foaf/0.1/")
PROV     = Namespace("http://www.w3.org/ns/prov#")
EDM      = Namespace("http://www.europeana.eu/schemas/edm/")
GEO      = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# 常量：主人物（可根据需要补 sameAs）
VIRGINIA = URIRef(BASE + "person/virginia-woolf")

# 小工具：把标题变 slug 用来拼 URI
def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# ===== 1) 初始化 RDF 图谱 =====
g = Graph()
g.bind("woolfo", NS_WOOLFO)  # 你的本体（ObjectProperty/Manuscript 在这里）
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("prov", PROV)
g.bind("edm", EDM)
g.bind("geo", GEO)

# 先把 Virginia Woolf 节点建出来（真实项目可再补 label/sameAs）
g.add((VIRGINIA, RDF.type, SCHEMA.Person))
g.add((VIRGINIA, SCHEMA.name, Literal("Virginia Woolf")))

# ===== 2) 读取映射表 =====
mapping = json.load(open("../mappings/tei_mapping.json", "r", encoding="utf-8"))

# ===== 3) 解析“地点”TEI，建立 Place 字典（后续可复用） =====
def parse_places(tei_path: pathlib.Path):
    tree = etree.parse(str(tei_path))
    places = {}  # key: xml:id or label -> URI
    for place in tree.xpath("//tei:place", namespaces=TEI_NS):
        xml_id = place.get("{http://www.w3.org/XML/1998/namespace}id") or slugify(
            "".join(place.xpath("normalize-space(tei:placeName/text())", namespaces=TEI_NS)) or "place"
        )
        place_uri = URIRef(BASE + f"place/{xml_id}")
        g.add((place_uri, RDF.type, SCHEMA.Place))

        # 名称
        name = "".join(place.xpath("normalize-space(tei:placeName/text())", namespaces=TEI_NS))
        if name:
            g.add((place_uri, SCHEMA.name, Literal(name)))

        # sameAs（Wikidata）
        sameas = place.xpath("string(tei:placeName/@sameAs)", namespaces=TEI_NS)
        if sameas:
            g.add((place_uri, OWL.sameAs, URIRef(sameas)))

        # Geo 坐标
        geo_text = "".join(place.xpath("normalize-space(tei:location/tei:geo/text())", namespaces=TEI_NS))
        if geo_text and "," in geo_text:
            lat_str, lon_str = [x.strip() for x in geo_text.split(",", 1)]
            g.add((place_uri, GEO.lat, Literal(lat_str, datatype=XSD.decimal)))
            g.add((place_uri, GEO.long, Literal(lon_str, datatype=XSD.decimal)))

        # GeoNames / Wikidata idno
        for idno in place.xpath("tei:idno", namespaces=TEI_NS):
            t = idno.get("type", "").lower()
            val = "".join(idno.xpath("normalize-space(text())", namespaces=TEI_NS))
            if t == "geonames" and val:
                g.add((place_uri, OWL.sameAs, URIRef(f"https://www.geonames.org/{val}/")))
            if t == "wikidata" and val:
                g.add((place_uri, OWL.sameAs, URIRef(f"https://www.wikidata.org/wiki/{val}")))

        places[xml_id] = place_uri
    return places

places_file = pathlib.Path("../data/tei/Places_related_to_Virginia_Woolf.xml")
PLACES = parse_places(places_file)

# ===== 4) 解析“印刷文本”TEI（To the Lighthouse）→ 作为作品节点 =====
def parse_print_text(tei_path: pathlib.Path):
    tree = etree.parse(str(tei_path))
    title = tree.xpath("normalize-space(//tei:titleStmt/tei:title/text())", namespaces=TEI_NS) or "Untitled"
    work_slug = slugify(title)
    work_uri = URIRef(BASE + f"work/{work_slug}")
    g.add((work_uri, RDF.type, SCHEMA.Book))
    g.add((work_uri, DCTERMS.title, Literal(title)))

    # 作者（用 Virginia）
    g.add((work_uri, SCHEMA.creator, VIRGINIA))

    # 出版社 & 日期
    publisher = tree.xpath("normalize-space(//tei:publicationStmt/tei:publisher/text())", namespaces=TEI_NS)
    if publisher:
        g.add((work_uri, DCTERMS.publisher, Literal(publisher)))

    date = tree.xpath("normalize-space(//tei:sourceDesc/tei:bibl/tei:date/text())", namespaces=TEI_NS)
    if date:
        g.add((work_uri, DCTERMS.date, Literal(date)))

    # 情节地点：示范把 St Ives 绑到作品（若不想硬编码，可在 TEI 中加线索再解析）
    # 这里演示：如果存在 id 为 stives 的 Place，则挂载
    if "stives" in PLACES:
        g.add((work_uri, SCHEMA.contentLocation, PLACES["stives"]))

    return work_uri

ttl_text_file = pathlib.Path("../data/tei/Text-To the lighthouse.xml")
WORK_TTL = parse_print_text(ttl_text_file)

# ===== 5) 解析“手稿图像”TEI：figure → WebResource，并挂到作品 =====
def parse_manuscript_images(tei_path: pathlib.Path, work_uri: URIRef):
    tree = etree.parse(str(tei_path))
    for fig in tree.xpath("//tei:figure", namespaces=TEI_NS):
        xml_id = fig.get("{http://www.w3.org/XML/1998/namespace}id") or slugify(
            fig.xpath("string(tei:head/text())", namespaces=TEI_NS) or "ms"
        )
        res_uri = URIRef(BASE + f"resource/{xml_id}")
        g.add((res_uri, RDF.type, EDM.WebResource))

        # 标题和描述
        head = fig.xpath("string(tei:head/text())", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head)))
        desc = fig.xpath("normalize-space(tei:figDesc/text())", namespaces=TEI_NS)
        if desc:
            g.add((res_uri, DCTERMS.description, Literal(desc)))

        # 图像 URL
        graphic_url = fig.xpath("string(tei:graphic/@url)", namespaces=TEI_NS)
        if graphic_url:
            g.add((res_uri, SCHEMA.contentUrl, Literal(graphic_url)))

        # 原始来源链接
        ptr = fig.xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
        if ptr:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))

        # 建立 作品 → 手稿 的连边（使用自定义属性）
        g.add((work_uri, NS_WOOLFO.hasManuscript, res_uri))

ms_file = pathlib.Path("../data/tei/Manuscript-To_the_lighthouse.xml")
parse_manuscript_images(ms_file, WORK_TTL)

# ===== 6) 解析“肖像照片”TEI：建 WebResource，并让人物 foaf:depiction 指向它 =====
def parse_portrait(tei_path: pathlib.Path):
    tree = etree.parse(str(tei_path))
    fig = tree.xpath("//tei:figure", namespaces=TEI_NS)
    if not fig:
        return
    fig = fig[0]
    xml_id = fig.get("{http://www.w3.org/XML/1998/namespace}id") or "fig-woolf-1902"
    res_uri = URIRef(BASE + f"resource/{xml_id}")
    g.add((res_uri, RDF.type, EDM.WebResource))

    title = fig.xpath("string(tei:head/text())", namespaces=TEI_NS)
    if title:
        g.add((res_uri, DCTERMS.title, Literal(title)))

    img = fig.xpath("string(tei:graphic/@url)", namespaces=TEI_NS)
    if img:
        g.add((res_uri, SCHEMA.contentUrl, Literal(img)))

    link = fig.xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
    if link:
        g.add((res_uri, RDFS.seeAlso, URIRef(link)))

    # 人物 → 肖像
    g.add((VIRGINIA, FOAF.depiction, res_uri))

portrait_file = pathlib.Path("../data/tei/Picture_of_Virginia_Woolf.xml")
parse_portrait(portrait_file)

# ===== 7) （可选）补充“文化再诠释”关系示例：电影 basedOn 小说 =====
def add_adaptations():
    mrs_dalloway = URIRef(BASE + "work/mrs-dalloway")
    g.add((mrs_dalloway, RDF.type, SCHEMA.Book))
    g.add((mrs_dalloway, DCTERMS.title, Literal("Mrs Dalloway")))
    g.add((mrs_dalloway, SCHEMA.creator, VIRGINIA))

    the_hours = URIRef(BASE + "film/the-hours")
    g.add((the_hours, RDF.type, SCHEMA.Film))
    g.add((the_hours, DCTERMS.title, Literal("The Hours")))
    g.add((the_hours, SCHEMA.basedOn, mrs_dalloway))

add_adaptations()

# ===== 8) 输出 RDF/XML（交作业用）与 Turtle（自检用） =====
pathlib.Path("../output").mkdir(parents=True, exist_ok=True)
g.serialize(destination="../output/woolf.rdf", format="xml")
g.serialize(destination="../output/woolf.ttl", format="turtle")

print("Done. Files saved to output/woolf.rdf and output/woolf.ttl")



#批量读取TEI
import glob
tei_files = glob.glob(str(DATA_DIR / "*.xml"))

for path in tei_files:
    fname = pathlib.Path(path).name
    if "Places" in fname:
        parse_places(path)
    elif "Manuscript" in fname:
        parse_manuscript_images(path, corresponding_work_uri)
    elif "Picture" in fname:
        parse_portrait(path)
    elif "Text-" in fname:
        parse_print_text(path)
    elif "Hours" in fname:
        parse_film(path)  # 你可以写一个小函数



# graph.json
PUB_DIR = BASE_DIR.parent / "public" / "data"
PUB_DIR.mkdir(parents=True, exist_ok=True)

# 生成各种 JSON-LD
(export 函数略)
(path := PUB_DIR / f"work-{slug}.json").write_text(json_str, "utf-8")

# 也可以把 output/graph.json 复制到 public/data
import shutil
shutil.copy(OUT_DIR / "graph.json", PUB_DIR / "graph.json")
