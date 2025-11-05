
import pathlib, re, json, glob
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# -------- 路径 & 命名空间 --------
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "tei"
MAP_PATH = BASE_DIR.parent / "mappings" / "tei_mapping.json"
OUT_DIR  = BASE_DIR.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE    = "https://example.org/woolf/"
WOO     = Namespace("https://example.org/woolf-ontology#")
SCHEMA  = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF    = Namespace("http://xmlns.com/foaf/0.1/")
PROV    = Namespace("http://www.w3.org/ns/prov#")
EDM     = Namespace("http://www.europeana.eu/schemas/edm/")
GEO     = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

TEI_NS  = {"tei":"http://www.tei-c.org/ns/1.0"}

# -------- 通用工具 --------
def parse_xml(path):
    parser = etree.XMLParser(recover=False, huge_tree=True)
    try:
        return etree.parse(str(path), parser)
    except etree.XMLSyntaxError as e:
        raise RuntimeError(f"XML parse failed for {path}: {e}")

# turn names into slugs
def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")

def lit(s):
    return Literal(s) if s is not None else None

# 读取 mapping
MAPPING = json.loads(MAP_PATH.read_text(encoding="utf-8"))

# bind namespaces
def new_graph():
    g = Graph()
    g.bind("woolfo", WOO)
    g.bind("schema", SCHEMA)
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("prov", PROV)
    g.bind("edm", EDM)
    g.bind("geo", GEO)
    return g

g = new_graph()

# 你们的主角（也可以从 TEI 里抽）
VIRGINIA = URIRef(BASE + "person/virginia-woolf")
g.add((VIRGINIA, RDF.type, SCHEMA.Person))
g.add((VIRGINIA, SCHEMA.name, Literal("Virginia Woolf")))
g.add((VIRGINIA, OWL.sameAs, URIRef("https://dbpedia.org/page/Virginia_Woolf")))

# MAPPING
def add_refs(g, subject, urls):
    for u in urls:
        u = u.strip()
        if u:
            g.add((subject, RDFS.seeAlso, URIRef(u)))

def handle_element(g, subject, elem):
    tag = etree.QName(elem).localname
    pred = MAPPING["elements"].get(tag)

    # 特殊：地理坐标
    if pred == "__GEO__":
        text = " ".join(elem.itertext()).strip()
        parts = [p for p in re.split(r"[, ]+", text) if p]
        if len(parts) >= 2:
            g.add((subject, GEO.lat, Literal(parts[0], datatype=XSD.decimal)))
            g.add((subject, GEO.long, Literal(parts[1], datatype=XSD.decimal)))
        return

    # 特殊：WebResource
    if pred == "__WEBRESOURCE__":
        xml_id = elem.get("{http://www.w3.org/XML/1998/namespace}id") or f"res-{abs(hash(etree.tostring(elem)))}"
        res_uri = URIRef(BASE + f"resource/{slugify(xml_id)}")
        g.add((res_uri, RDF.type, EDM.WebResource))
        url = elem.get("url")
        if url:
            g.add((res_uri, SCHEMA.contentUrl, Literal(url)))
        # 尝试读取邻近标题/描述
        head = elem.getparent().xpath("string(tei:head)", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head.strip())))
        desc = elem.getparent().xpath("normalize-space(tei:figDesc)", namespaces=TEI_NS)
        if desc:
            g.add((res_uri, DCTERMS.description, Literal(desc)))
        # 处理 figDesc/ptr 链接
        ptr = elem.getparent().xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
        if ptr:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))
        return res_uri

    # 普通文本三元组
    if pred:
        text = " ".join(elem.itertext()).strip()
        if text:
            g.add((subject, URIRef(pred), Literal(text)))

    # 属性映射（@sameAs, @ref, @when）
    for attr_name, p in MAPPING.get("attributes", {}).items():
        if attr_name.startswith("@"):
            val = elem.get(attr_name[1:])
            if not val:
                continue
            if attr_name == "@ref":
                urls = val.split() if MAPPING.get("split_multi_ref") else [val]
                add_refs(g, subject, urls)
            elif attr_name == "@when":
                g.add((subject, URIRef(p), Literal(val)))
            else:
                g.add((subject, URIRef(p), URIRef(val)))

# xslt part

# place
def parse_places(path):
    tree = parse_xml(path)
    for place in tree.xpath("//tei:listPlace/tei:place", namespaces=TEI_NS):
        xml_id = place.get("{http://www.w3.org/XML/1998/namespace}id") or slugify(
            place.xpath("string(tei:placeName)", namespaces=TEI_NS)
        )
        uri = URIRef(BASE + f"place/{slugify(xml_id)}")
        g.add((uri, RDF.type, SCHEMA.Place))

        # name
        name = place.xpath("string(tei:placeName)", namespaces=TEI_NS).strip()
        if name:
            g.add((uri, SCHEMA.name, Literal(name)))

        # sameAs（Wikidata/GeoNames）
        sameas = place.xpath("string(tei:placeName/@sameAs)", namespaces=TEI_NS)
        if sameas:
            g.add((uri, OWL.sameAs, URIRef(sameas)))

        # Geo coordinates
        for geo in place.xpath("tei:location/tei:geo", namespaces=TEI_NS):
            handle_element(g, uri, geo)

        # other id（idno）
        for idno in place.xpath("tei:idno", namespaces=TEI_NS):
            t = (idno.get("type") or "").lower()
            val = " ".join(idno.itertext()).strip()
            if not val:
                continue
            if t == "geonames":
                g.add((uri, OWL.sameAs, URIRef(f"https://www.geonames.org/{val}/")))
            elif t == "wikidata":
                g.add((uri, OWL.sameAs, URIRef(f"https://www.wikidata.org/wiki/{val}")))

# text（Book/Essay）
def parse_text(path):
    tree = parse_xml(path)
    title = tree.xpath("normalize-space(//tei:titleStmt/tei:title)", namespaces=TEI_NS) or "Untitled"
    work_slug = slugify(title)
    work_uri = URIRef(BASE + f"work/{work_slug}")

    g.add((work_uri, RDF.type, SCHEMA.Book))
    g.add((work_uri, DCTERMS.title, Literal(title)))

    # author
    g.add((work_uri, SCHEMA.creator, VIRGINIA))

    # publisher & date
    publisher = tree.xpath("normalize-space(//tei:publicationStmt/tei:publisher)", namespaces=TEI_NS)
    if publisher:
        g.add((work_uri, DCTERMS.publisher, Literal(publisher)))
    date = tree.xpath("normalize-space(//tei:sourceDesc//tei:date)", namespaces=TEI_NS)
    if date:
        g.add((work_uri, DCTERMS.date, Literal(date)))

    # links: <sourceDesc>//ref/@target
    refs = tree.xpath("//tei:sourceDesc//tei:ref/@target", namespaces=TEI_NS)
    for r in refs:
        for u in (r.split() if MAPPING.get("split_multi_ref") else [r]):
            g.add((work_uri, RDFS.seeAlso, URIRef(u)))

    # ?///情节地点（如果在 TEI 中有线索；暂时示例：根据标题猜测）
    if "lighthouse" in work_slug and (BASE + "place/st-ives"):
        g.add((work_uri, SCHEMA.contentLocation, URIRef(BASE + "place/st-ives")))
    if "mrs-dalloway" in work_slug:
        g.add((work_uri, SCHEMA.contentLocation, URIRef(BASE + "place/london")))

    return work_uri

# Manuscripts
def make_webresource_from_graphic(graphic_elem, parent_elem=None):
    """
    把 <graphic> 变成一个 edm:WebResource，返回它的 URI
    parent_elem 用来拿 head/figDesc/ptr 这种写在父节点上的信息
    """
    # 1) 先起一个稳定的 id
    xml_id = (
        graphic_elem.get("{http://www.w3.org/XML/1998/namespace}id")
        or (parent_elem is not None and parent_elem.get("{http://www.w3.org/XML/1998/namespace}id"))
        or f"res-{abs(hash(etree.tostring(graphic_elem)))}"
    )
    res_uri = URIRef(BASE + f"resource/{slugify(str(xml_id))}")
    g.add((res_uri, RDF.type, EDM.WebResource))

    # 2) 图片真实地址
    url = graphic_elem.get("url")
    if url:
        g.add((res_uri, SCHEMA.contentUrl, Literal(url)))

    # 3) 如果父节点有标题/描述/ptr，就挂上去
    if parent_elem is not None:
        head = parent_elem.xpath("string(tei:head)", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head.strip())))
        desc = parent_elem.xpath("normalize-space(tei:figDesc)", namespaces=TEI_NS)
        if desc:
            g.add((res_uri, DCTERMS.description, Literal(desc)))
        ptr = parent_elem.xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
        if ptr:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))

    return res_uri


def parse_manuscript(path):
    tree = parse_xml(path)
    if tree is None:
        return

    # 通过文件名推断对应作品
    fname = pathlib.Path(path).stem.lower()           # manuscript-a room of one's own
    work_part = fname.replace("manuscript-", "").strip()
    work_slug = slugify(work_part)
    work_uri  = URIRef(BASE + f"work/{work_slug}")
    g.add((work_uri, RDF.type, SCHEMA.Book))


    figures = tree.xpath("//tei:figure", namespaces=TEI_NS)

    for fig in figures:
        graphic = fig.find("tei:graphic", namespaces=TEI_NS)
        if graphic is None:
            continue
        webres = make_webresource_from_graphic(graphic, parent_elem=fig)
        g.add((work_uri, WOO.hasManuscript, webres))

# portrait - foaf:depicts
def parse_portrait(path):
    tree = parse_xml(path)
    graphic = tree.xpath("//tei:facsimile/tei:graphic", namespaces=TEI_NS)
    if not graphic:
        return
    g_res = graphic[0]
    url = g_res.get("url")

    res_uri = URIRef(BASE + "resource/portrait-woolf-1902")
    g.add((res_uri, RDF.type, EDM.WebResource))
    if url:
        g.add((res_uri, SCHEMA.contentUrl, Literal(url)))


    facs = g_res.getparent()  
    head = facs.xpath("string(tei:head)", namespaces=TEI_NS)
    if head:
        g.add((res_uri, DCTERMS.title, Literal(head.strip())))
    desc = facs.xpath("normalize-space(tei:desc)", namespaces=TEI_NS)
    if desc:
        g.add((res_uri, DCTERMS.description, Literal(desc)))
    ptr = facs.xpath("string(tei:ptr/@target)", namespaces=TEI_NS)
    if ptr:
        g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))
    
    g.add((res_uri, FOAF.depicts, VIRGINIA))
    g.add((VIRGINIA, FOAF.depiction, res_uri))

# Film: The Hours.xml
def parse_film(path):
    tree = parse_xml(path)
    title = tree.xpath("normalize-space(//tei:titleStmt/tei:title)", namespaces=TEI_NS) 
    film_uri = URIRef(BASE + f"film/{slugify(title)}")
    g.add((film_uri, RDF.type, SCHEMA.Film))
    g.add((film_uri, DCTERMS.title, Literal(title)))

    # basedOn：Mrs Dalloway
    mrs = URIRef(BASE + "work/mrs-dalloway")
    g.add((mrs, RDF.type, SCHEMA.Book))
    g.add((film_uri, SCHEMA.basedOn, mrs))

# Press
def parse_press(path):
    tree = parse_xml(path)
    name = tree.xpath("normalize-space(//tei:org/tei:orgName)", namespaces=TEI_NS) or "Hogarth Press"
    press_uri = URIRef(BASE + "org/hogarth-press")
    g.add((press_uri, RDF.type, SCHEMA.Organization))
    g.add((press_uri, SCHEMA.name, Literal(name)))
    g.add((press_uri, SCHEMA.founder, VIRGINIA))
    #location
    #location = tree.xpath("normalize-space(//tei:org/tei:address/tei:settlement)", namespaces=TEI_NS)
    #把这个也变成一个 Place 实体？，就像VIRGINA一样，挪到前面，因为后面每个都要用
    

# Diary & From the Diaries（简化示例）
def parse_diaries(path):
    diary_uri = URIRef(BASE + "work/diaries")
    tree = parse_xml(path)
    g.add((diary_uri, RDF.type, SCHEMA.CreativeWork))
    g.add((diary_uri, DCTERMS.title, Literal("Diaries")))
    g.add((diary_uri, SCHEMA.creator, VIRGINIA))
    date = tree.xpath("normalize-space(//tei:sourceDesc//tei:date)", namespaces=TEI_NS)
    g.add((diary_uri, DCTERMS.date, Literal(date)))
    # links(target)
    #refs = tree.xpath("//tei:sourceDesc//tei:ref/@target", namespaces=
    #dcterms:seeAlso); dcterms:publisher




    
def parse_from_diaries(path):
    work_uri = URIRef(BASE + "work/from-the-diaries-of-virginia-woolf")
    g.add((work_uri, RDF.type, SCHEMA.MusicComposition))
    g.add((work_uri, DCTERMS.title, Literal("From the Diaries of Virginia Woolf")))
    # 来源
    diary_uri = URIRef(BASE + "work/diaries")
    g.add((work_uri, PROV.wasDerivedFrom, diary_uri))

# routing
def route_file(path: pathlib.Path):
    name = path.name.lower()
    if name.startswith("places"):
        return parse_places(path)
    if name.startswith("text-") or name in ("orlando.xml", "mrs dalloway.xml"):
        return parse_text(path)
    if name.startswith("manuscript-"):
        return parse_manuscript(path)
    if name.startswith("picture"):
        return parse_portrait(path)
    if name.startswith("the hours"):
        return parse_film(path)
    if name.startswith("hogarth press"):
        return parse_press(path)
    if "from the diaries" in name:
        return parse_from_diaries(path)
    if "dair" in name:
        return parse_diaries(path)
    # 兜底：按文本解析
    return parse_text(path)

def build():
    files = sorted(DATA_DIR.glob("*.xml"))
    if not files:
        raise SystemExit(f"No TEI files in {DATA_DIR}")
    for p in files:
        print("→", p.name)
        route_file(p)

    g.serialize(destination=str(OUT_DIR / "woolf-full.rdf"), format="xml")
    g.serialize(destination=str(OUT_DIR / "woolf-full.ttl"), format="turtle")
    print("\nDone → output/woolf-full.rdf & woolf-full.ttl")

if __name__ == "__main__":
    build()

# generate json files in /public/data/
import json
PUB_DATA = BASE_DIR.parent / "public" / "data"
PUB_DATA.mkdir(parents=True, exist_ok=True)

def export_work_json(g, work_uri):
    # 取基本字段
    name = g.value(work_uri, DCTERMS.title) or g.value(work_uri, SCHEMA.name)
    creator = g.value(work_uri, SCHEMA.creator)
    loc = g.value(work_uri, SCHEMA.contentLocation)
    sameAs = list(g.objects(work_uri, RDFS.seeAlso))

    obj = {
        "@context": "https://schema.org",
        "@id": str(work_uri),
        "@type": "Book",
        "name": str(name) if name else "",
    }

    if creator:
        obj["creator"] = {"@id": str(creator), "name": g.value(creator, SCHEMA.name) and str(g.value(creator, SCHEMA.name))}
    if loc:
        obj["contentLocation"] = {"@id": str(loc), "name": g.value(loc, SCHEMA.name) and str(g.value(loc, SCHEMA.name))}
    if sameAs:
        obj["sameAs"] = [str(u) for u in sameAs]

    slug = str(work_uri).split("/")[-1]
    (PUB_DATA / f"work-{slug}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def export_graph_index(g):
    items = []
    for s, p, o in g.triples((None, RDF.type, None)):
        name = g.value(s, SCHEMA.name) or g.value(s, DCTERMS.title)
        if not name:
            continue
        items.append({
          "@id": str(s),
          "@type": str(o).split("/")[-1],
          "name": str(name),
        })
    (PUB_DATA / "graph.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


# 所有作品都导出
for s, p, o in g.triples((None, RDF.type, SCHEMA.Book)):
    export_work_json(g, s)
