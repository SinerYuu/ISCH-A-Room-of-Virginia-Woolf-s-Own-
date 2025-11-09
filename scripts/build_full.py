
import pathlib, re, json, glob
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

#path and prefixes
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "tei"
MAP_PATH = BASE_DIR/ "tei_mapping.json"
OUT_DIR  = BASE_DIR.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PUB_DIR  = BASE_DIR.parent / "public" / "data"
PUB_DIR.mkdir(parents=True, exist_ok=True)

BASE    = "https://example.org/woolf/"
WOO     = Namespace("https://example.org/woolf-ontology#")
SCHEMA  = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF    = Namespace("http://xmlns.com/foaf/0.1/")
PROV    = Namespace("http://www.w3.org/ns/prov#")
EDM     = Namespace("http://www.europeana.eu/schemas/edm/")
GEO     = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

TEI_NS  = {"tei":"http://www.tei-c.org/ns/1.0"}

# general tools
def parse_xml(path): # parse XML with lxml, once something wrong I can read the note
    parser = etree.XMLParser(recover=False, huge_tree=True)
    try:
        return etree.parse(str(path), parser)
    except etree.XMLSyntaxError as e:
        raise RuntimeError(f"XML parse failed for {path}: {e}")

# turn names into slugs
def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
#in case any NONE
def lit(s):
    return Literal(s) if s is not None else None

# read mapping
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

# MAPPING
def add_refs(g, subject, urls):
    for u in urls:
        u = u.strip()
        if u:
            g.add((subject, RDFS.seeAlso, URIRef(u)))

def handle_element(g, subject, elem):
    tag = etree.QName(elem).localname
    pred = MAPPING["elements"].get(tag)

    # geo location
    if pred == "__GEO__":
        text = " ".join(elem.itertext()).strip()
        parts = [p for p in re.split(r"[, ]+", text) if p]
        if len(parts) >= 2:
            g.add((subject, GEO.lat, Literal(parts[0], datatype=XSD.decimal)))
            g.add((subject, GEO.long, Literal(parts[1], datatype=XSD.decimal)))
        return

    # WebResource
    if pred == "__WEBRESOURCE__":
        xml_id = elem.get("{http://www.w3.org/XML/1998/namespace}id") or f"res-{abs(hash(etree.tostring(elem)))}"
        res_uri = URIRef(BASE + f"resource/{slugify(xml_id)}")
        g.add((res_uri, RDF.type, EDM.WebResource))
        url = elem.get("url")
        if url:
            g.add((res_uri, SCHEMA.contentUrl, Literal(url)))
        # name and desc
        head = elem.getparent().xpath("string(tei:head)", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head.strip())))
        desc = elem.getparent().xpath("normalize-space(tei:figDesc)", namespaces=TEI_NS)
        if desc:
            g.add((res_uri, DCTERMS.description, Literal(desc)))
        # original link -> ptr target
        ptr = elem.getparent().xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
        if ptr:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))
        return res_uri

    # general triple
    if pred:
        text = " ".join(elem.itertext()).strip()
        if text:
            g.add((subject, URIRef(pred), Literal(text)))

    # turn attributes into triples
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

### xslt part

#dictionary for specific triples
Work_Content_Place = {
    "to-the-lighthouse": "stives",
    "mrs-dalloway": "london",
    "orlando-a-biography": "london",
    "diaries": "london",
}

Work_Created_Place = {
    "to-the-lighthouse": "rodmell",
    "mrs-dalloway": "london",
    "orlando-a-biography": "london",
    "a-room-of-one-s-own": "london",
}

# Virginia Woolf entity (core)
VIRGINIA = URIRef(BASE + "person/virginia-woolf")
g.add((VIRGINIA, RDF.type, SCHEMA.Person))
g.add((VIRGINIA, SCHEMA.name, Literal("Virginia Woolf")))
g.add((VIRGINIA, OWL.sameAs, URIRef("https://dbpedia.org/page/Virginia_Woolf")))
g.add((VIRGINIA, SCHEMA.birthPlace, URIRef(BASE + "place/london")))
g.add((VIRGINIA, SCHEMA.deathPlace, URIRef(BASE + "place/rodmell")))
g.add((VIRGINIA, SCHEMA.birthDate, Literal("1882-01-25")))
g.add((VIRGINIA, SCHEMA.deathDate, Literal("1941-03-28")))

# Press
HPRESS = URIRef(BASE + "org/hogarth-press")
g.add((HPRESS, OWL.sameAs, URIRef("https://en.wikipedia.org/wiki/Hogarth_Press")))
g.add((HPRESS, SCHEMA.url, Literal("https://en.wikipedia.org/wiki/Hogarth_Press")))
def parse_press(path):
    tree = parse_xml(path)
    name = tree.xpath("normalize-space(//tei:org/tei:orgName)", namespaces=TEI_NS) or "Hogarth Press"
    g.add((HPRESS, RDF.type, SCHEMA.Organization))
    g.add((HPRESS, SCHEMA.name, Literal(name)))
    g.add((HPRESS, SCHEMA.founder, VIRGINIA))
    g.add((HPRESS, SCHEMA.location, URIRef(BASE + "place/london")))
    date = tree.xpath("normalize-space(//tei:org//tei:date)", namespaces=TEI_NS)
    if date:
        g.add((HPRESS, SCHEMA.foundingDate, Literal(date)))

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

        # idno -> authority control
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
    slug = slugify(title)
    for prefix in ("text-of-", "text-", "textof-"):
        if slug.startswith(prefix):
            work_slug = slug[len(prefix):]
            break
    work_uri = URIRef(BASE + f"work/{work_slug}")
    g.add((work_uri, RDF.type, SCHEMA.Book))
    # title - clean prefixes
    for prefix in ("Text of ", "Text - ", "Text ", "Text: "):
        if title.lower().startswith(prefix.lower()):
            clean_title = title[len(prefix):].strip()
            break
    clean_title = clean_title.strip('\'"“”‘’')
    g.add((work_uri, DCTERMS.title, Literal(clean_title)))
    # author & Publisher
    g.add((work_uri, SCHEMA.creator, VIRGINIA))
    g.add((work_uri, DCTERMS.publisher, HPRESS))
    # date
    date = tree.xpath("normalize-space(//tei:sourceDesc//tei:date)", namespaces=TEI_NS)
    if date:
        g.add((work_uri, DCTERMS.date, Literal(date)))
    # links: <sourceDesc>//ref/@target
    refs = tree.xpath("//tei:sourceDesc//tei:ref/@target", namespaces=TEI_NS)
    for r in refs:
        for u in (r.split() if MAPPING.get("split_multi_ref") else [r]):
            g.add((work_uri, RDFS.seeAlso, URIRef(u)))
    # location (created and content)
    content_place = Work_Content_Place.get(work_slug)
    if content_place:
        g.add((work_uri, SCHEMA.contentLocation, URIRef(BASE + f"place/{content_place}")))
    creation_place = Work_Created_Place.get(work_slug)
    if creation_place:
        g.add((work_uri, SCHEMA.locationCreated, URIRef(BASE + f"place/{creation_place}")))
    print("WORK SLUG →", work_slug)
    print("   content place?", Work_Content_Place.get(work_slug))

    return work_uri

# Manuscripts
def parse_manuscript(path):
    tree = parse_xml(path)
    # belong to which work
    fname = pathlib.Path(path).stem.lower()
    work_part = fname.replace("manuscript-", "").strip()
    work_slug = slugify(work_part)
    work_uri = URIRef(BASE + f"work/{work_slug}")
    # every single page - figure
    figures = tree.xpath("//tei:figure", namespaces=TEI_NS)
    for fig in figures:
        fig_id = fig.get("{http://www.w3.org/XML/1998/namespace}id")
        res_uri = URIRef(BASE + f"resource/{slugify(fig_id)}")
        g.add((res_uri, RDF.type, EDM.WebResource))
        # title
        head = fig.xpath("string(tei:head)", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head.strip())))
        # description
        desc = fig.xpath("normalize-space(tei:figDesc/text())", namespaces=TEI_NS)
        if desc:
            g.add((res_uri, DCTERMS.description, Literal(desc)))
        # picture url
        graphic = fig.find("tei:graphic", namespaces=TEI_NS)
        if graphic is not None:
            img_file = graphic.get("url")
            if img_file:
                g.add((res_uri, SCHEMA.contentUrl, Literal(img_file)))
        # original link -> ptr target
        ptr_target = fig.xpath("string(tei:figDesc/tei:ptr/@target)", namespaces=TEI_NS)
        if ptr_target:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr_target)))
        # manuscript belongs to which book
        g.add((work_uri, WOO.hasManuscript, res_uri))

# portrait - foaf:depicts
def parse_portrait(path):
    tree = parse_xml(path)
    graphic = tree.xpath("//tei:facsimile/tei:graphic", namespaces=TEI_NS)
    if not graphic:
        print(f"[WARN] Portrait: No <graphic> found in {path}")
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
    g.add((film_uri, RDF.type, SCHEMA.Movie))
    g.add((film_uri, DCTERMS.title, Literal(title)))
    # basedOn：Mrs Dalloway
    mrs = URIRef(BASE + "work/mrs-dalloway")
    g.add((film_uri, SCHEMA.basedOn, mrs))    

# Diary & From the Diaries（简化示例）
def parse_diaries(path):
    tree = parse_xml(path)
    # two titles
    coll_title = tree.xpath("normalize-space(//tei:titleStmt/tei:title)", namespaces=TEI_NS)
    main_title = tree.xpath("normalize-space(//tei:sourceDesc//tei:title)", namespaces=TEI_NS)

    diary_slug = slugify(main_title)   # "1928 Diary" -> "1928-diary" -> "1928-diary"（前面有数字也行）
    diary_uri = URIRef(BASE + f"work/{diary_slug}")
    g.add((diary_uri, RDF.type, SCHEMA.CreativeWork))
    g.add((diary_uri, DCTERMS.title, Literal(main_title)))

    # Abstract collection: all diaries -- so that From the Diaries can refer to it
    coll_slug = slugify(coll_title)
    coll_uri = URIRef(BASE + f"work/{coll_slug}")
    g.add((coll_uri, RDF.type, SCHEMA.Collection))
    g.add((coll_uri, DCTERMS.title, Literal(coll_title)))
    g.add((coll_uri, SCHEMA.creator, VIRGINIA))

    g.add((coll_uri, DCTERMS.hasPart, diary_uri))
    g.add((diary_uri, DCTERMS.isPartOf, coll_uri))

    # date
    date = tree.xpath("normalize-space(//tei:sourceDesc//tei:date)", namespaces=TEI_NS)
    if date:
        g.add((diary_uri, DCTERMS.date, Literal(date)))
    # ref target: source
    src = tree.xpath("string(//tei:sourceDesc//tei:ref/@target)", namespaces=TEI_NS)
    if src:
        g.add((diary_uri, RDFS.seeAlso, URIRef(src)))
    # publisher: NYPL
    publ = tree.xpath("normalize-space(//tei:publicationStmt/tei:publisher)", namespaces=TEI_NS)
    if publ:
        g.add((diary_uri, DCTERMS.publisher, Literal(publ)))

    # facsimile (the picture has its own url so)
    facs = tree.xpath("//tei:facsimile", namespaces=TEI_NS)
    for fac in facs:
        res_uri = URIRef(BASE + f"resource/{diary_slug}-facsimile")
        g.add((res_uri, RDF.type, EDM.WebResource))

        head = fac.xpath("string(tei:head)", namespaces=TEI_NS)
        if head:
            g.add((res_uri, DCTERMS.title, Literal(head.strip())))

        graphic = fac.find("tei:graphic", namespaces=TEI_NS)
        if graphic is not None:
            img = graphic.get("url")
            if img:
                g.add((res_uri, SCHEMA.contentUrl, Literal(img)))
        # ptr
        ptr = fac.xpath("string(tei:ptr/@target)", namespaces=TEI_NS)
        if ptr:
            g.add((res_uri, RDFS.seeAlso, URIRef(ptr)))
        # has manuscript
        g.add((diary_uri, WOO.hasManuscript, res_uri))
    
def parse_from_diaries(path):
    tree = parse_xml(path)
    title = tree.xpath("normalize-space(//tei:titleStmt/tei:title)", namespaces=TEI_NS) or "From the Diaries of Virginia Woolf"
    work_slug = slugify(title)
    work_uri = URIRef(BASE + f"work/{work_slug}")
    g.add((work_uri, RDF.type, SCHEMA.MusicComposition))
    g.add((work_uri, DCTERMS.title, Literal(title)))
    # source
    coll_uri = URIRef(BASE + "work/the-diary-of-virginia-woolf")
    g.add((work_uri, PROV.wasDerivedFrom, coll_uri))

# routing: which parser to use
def route_file(path: pathlib.Path):
    name = path.name.lower()
    if name.startswith("hogarth press"):
        return parse_press(path)
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
    if "from the diaries" in name:
        return parse_from_diaries(path)
    # Diaries
    return parse_diaries(path)

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

from jsoncsv import export_all


if __name__ == "__main__":
    build()
    export_all(g, OUT_DIR, PUB_DIR) 