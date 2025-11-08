# scripts/build_full.py
import re, pathlib, glob
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "tei"
OUT_DIR  = BASE_DIR.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Namespaces
BASE    = "https://example.org/woolf/"
WOO     = Namespace("https://example.org/woolf-ontology#")
SCHEMA  = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF    = Namespace("http://xmlns.com/foaf/0.1/")
PROV    = Namespace("http://www.w3.org/ns/prov#")
EDM     = Namespace("http://www.europeana.eu/schemas/edm/")
GEO     = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
TEI_NS  = {"tei":"http://www.tei-c.org/ns/1.0"}

def parse_xml(path):
    parser = etree.XMLParser(recover=False, huge_tree=True)
    return etree.parse(str(path), parser)

# ---- 你的具体解析函数（只示意，保持和你之前的函数名一致） ----
def parse_places(g, path):
    parser = etree.XMLParser(recover=False, huge_tree=True)
    try:
        return etree.parse(str(path), parser)
    except etree.XMLSyntaxError as e:
def parse_text(g, path): ...
def parse_manuscript(g, path): ...
def parse_portrait(g, path): ...
def parse_film(g, path): ...
def parse_press(g, path): ...
def parse_diaries(g, path): ...
def parse_from_diaries(g, path): ...
# ------------------路由--------------------------------------

def route_file(g, path: pathlib.Path):
    name = path.name.lower()
    if name.startswith("places"):
        return parse_places(g, path)
    if name.startswith("text-"):
        return parse_text(g, path)
    if name.startswith("manuscript-"):
        return parse_manuscript(g, path)
    if name.startswith("picture"):
        return parse_portrait(g, path)
    if name.startswith("the hours"):
        return parse_film(g, path)
    if name.startswith("hogarth press"):
        return parse_press(g, path)
    if "from the diaries" in name:
        return parse_from_diaries(g, path)
    if name.startswith("dair") or name.startswith("diar"):  # 兼容 Diaries/Daires
        return parse_diaries(g, path)
    if name.startswith("orlando") or name.startswith("mrs dalloway"):
        return parse_text(g, path)   # 文本类，仍走 parse_text
    # 默认兜底
    return parse_text(g, path)

def build():
    g = Graph()
    for pref, ns in [("woolfo",WOO), ("schema",SCHEMA), ("dcterms",DCTERMS),
                     ("foaf",FOAF), ("prov",PROV), ("edm",EDM), ("geo",GEO)]:
        g.bind(pref, ns)

    # 遍历 data/tei 下所有 xml
    for path in sorted(DATA_DIR.glob("*.xml")):
        route_file(g, path)

    g.serialize(destination=str(OUT_DIR / "woolf-full.rdf"), format="xml")
    g.serialize(destination=str(OUT_DIR / "woolf-full.ttl"), format="turtle")
    print("OK → output/woolf-full.rdf & woolf-full.ttl")

if __name__ == "__main__":
    build()
