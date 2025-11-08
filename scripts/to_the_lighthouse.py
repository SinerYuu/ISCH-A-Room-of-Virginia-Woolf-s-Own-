# scripts/tei_text_to_rdf.py
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF
import pathlib, re

# Paths & Namespaces
BASE = "https://example.org/woolf/"
DATA = pathlib.Path("../data/tei/Text-To the lighthouse.xml")
OUT  = pathlib.Path("../output/text-to-the-lighthouse.rdf")

NS = {"tei": "http://www.tei-c.org/ns/1.0"}  
SCHEMA  = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
OWL     = Namespace("http://www.w3.org/2002/07/owl#")
RDFS    = Namespace("http://www.w3.org/2000/01/rdf-schema#")

def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

parser = etree.XMLParser(recover=False, huge_tree=True)
tree = etree.parse(str(DATA), parser)

# 取标题（XPath：/TEI/teiHeader/fileDesc/titleStmt/title）
title = tree.xpath("normalize-space(//tei:titleStmt/tei:title)", namespaces=NS) or "Untitled"
work_slug = slugify(title)                     # to-the-lighthouse
work_uri  = URIRef(BASE + f"work/{work_slug}") # https://example.org/woolf/work/to-the-lighthouse

# 取作者名（/titleStmt/author）
author_name = tree.xpath("normalize-space(//tei:titleStmt/tei:author)", namespaces=NS) or "Virginia Woolf"
author_uri  = URIRef(BASE + "person/virginia-woolf")

# 取出版者（/publicationStmt/publisher）
publisher = tree.xpath("normalize-space(//tei:publicationStmt/tei:publisher)", namespaces=NS)

# 取出版年（/sourceDesc//date）
date_text = tree.xpath("normalize-space(//tei:sourceDesc//tei:date)", namespaces=NS)

# 取外部链接（/sourceDesc//ref/@target），可能有“两个 URL 用空格隔开”
ref_targets = tree.xpath("//tei:sourceDesc//tei:ref/@target", namespaces=NS)
see_alsos = []
for t in ref_targets:
    see_alsos.extend(t.split())  # 按空格拆成多条

# ---------- 生成 RDF ----------
g = Graph()
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)

# 声明类型：Book（或 CreativeWork）
g.add((work_uri, RDF.type, SCHEMA.Book))
# 标题
g.add((work_uri, DCTERMS.title, Literal(title)))
# 作者（统一用 schema:creator）
g.add((work_uri, SCHEMA.creator, author_uri))
# 出版社（字面量即可）
if publisher:
    g.add((work_uri, DCTERMS.publisher, Literal(publisher)))
# 出版时间
if date_text:
    g.add((work_uri, DCTERMS.date, Literal(date_text)))
# 外部链接
for u in see_alsos:
    g.add((work_uri, RDFS.seeAlso, URIRef(u)))

# （可选）补作品情节地点：本例按常识——St Ives
st_ives_uri = URIRef(BASE + "place/st-ives")  # 你稍后由 Places TEI 生成
g.add((work_uri, SCHEMA.contentLocation, st_ives_uri))

# 作者节点（最少信息）
g.add((author_uri, RDF.type, SCHEMA.Person))
g.add((author_uri, SCHEMA.name, Literal(author_name)))

# ---------- 输出 ----------
OUT.parent.mkdir(parents=True, exist_ok=True)
g.serialize(destination=str(OUT), format="xml")
print("OK →", OUT)
