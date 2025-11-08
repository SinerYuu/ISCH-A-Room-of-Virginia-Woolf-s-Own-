# scripts/jsoncsv.py
import json, csv
from pathlib import Path
from rdflib import RDF, RDFS, Namespace
from rdflib.namespace import DCTERMS

SCHEMA = Namespace("https://schema.org/")
EDM    = Namespace("http://www.europeana.eu/schemas/edm/")

# ---- 各类型的最小导出函数 ----

def export_person(g, uri):
    name = g.value(uri, SCHEMA.name) or g.value(uri, DCTERMS.title)
    return {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Person",
        "name": str(name) if name else ""
    }

def export_book(g, uri):
    title   = g.value(uri, DCTERMS.title) or g.value(uri, SCHEMA.name)
    creator = g.value(uri, SCHEMA.creator)
    loc     = g.value(uri, SCHEMA.contentLocation)
    out = {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Book",
        "name": str(title) if title else ""
    }
    if creator:
        out["creator"] = {"@id": str(creator)}
    if loc:
        out["contentLocation"] = {"@id": str(loc)}
    return out

def export_place(g, uri):
    name = g.value(uri, SCHEMA.name) or g.value(uri, DCTERMS.title)
    return {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Place",
        "name": str(name) if name else ""
    }

def export_org(g, uri):
    name = g.value(uri, SCHEMA.name) or g.value(uri, DCTERMS.title)
    return {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Organization",
        "name": str(name) if name else ""
    }

def export_film(g, uri):
    title = g.value(uri, DCTERMS.title) or g.value(uri, SCHEMA.name)
    based = g.value(uri, SCHEMA.basedOn)
    obj = {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Movie",
        "name": str(title) if title else ""
    }
    if based:
        obj["basedOn"] = {"@id": str(based)}
    return obj

def export_music(g, uri):
    title = g.value(uri, DCTERMS.title) or g.value(uri, SCHEMA.name)
    src   = g.value(uri, RDFS.seeAlso)
    obj = {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "MusicComposition",
        "name": str(title) if title else ""
    }
    if src:
        obj["sameAs"] = [str(src)]
    return obj

def export_collection(g, uri):
    title = g.value(uri, DCTERMS.title) or g.value(uri, SCHEMA.name)
    return {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "Collection",
        "name": str(title) if title else ""
    }

def export_webresource(g, uri):
    title = g.value(uri, DCTERMS.title) or g.value(uri, SCHEMA.name)
    url   = g.value(uri, SCHEMA.contentUrl)
    see   = list(g.objects(uri, RDFS.seeAlso))
    obj = {
        "@context": "https://schema.org",
        "@id": str(uri),
        "@type": "MediaObject",
        "name": str(title) if title else ""
    }
    if url:
        obj["contentUrl"] = str(url)
    if see:
        obj["sameAs"] = [str(u) for u in see]
    return obj

# ---- 类型 → 导出函数 的映射 ----
EXPORTERS = {
    str(SCHEMA.Person):        export_person,
    str(SCHEMA.Book):          export_book,
    str(SCHEMA.Place):         export_place,
    str(SCHEMA.Organization):  export_org,
    str(SCHEMA.Film):          export_film,
    str(SCHEMA.Movie):         export_film,     # 兜底
    str(SCHEMA.MusicComposition): export_music,
    str(SCHEMA.Collection):    export_collection,
    str(EDM.WebResource):      export_webresource,
}

def export_graph_index(g, pub_dir: Path):
    items = []
    for s, _, o in g.triples((None, RDF.type, None)):
        name = g.value(s, SCHEMA.name) or g.value(s, DCTERMS.title)
        if not name:
            continue
        items.append({
            "@id": str(s),
            "@type": str(o).split("/")[-1],
            "name": str(name),
        })
    (pub_dir / "graph.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2), "utf-8"
    )

def export_csv(g, out_dir):
    """导出 triples.csv + 每个 item 一个 csv"""
    csv_all = out_dir / "triples.csv"
    with open(csv_all, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "predicate", "object"])
        for s, p, o in g:
            writer.writerow([str(s), str(p), str(o)])
    print(f"[OK] Exported triples.csv → {csv_all}")

    for s in g.subjects(RDF.type, None):
        triples = [(str(s), str(p), str(o)) for p, o in g.predicate_objects(s)]
        csv_path = out_dir / f"{str(s).split('/')[-1]}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["subject", "predicate", "object"])
            writer.writerows(triples)
    print(f"[OK] Exported per-item CSVs → {out_dir}")

def export_all(g, out_dir: Path, pub_dir: Path):
    pub_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 按图里真实出现的所有类型导出
    for s, _, o in g.triples((None, RDF.type, None)):
        o_str = str(o)
        if o_str in EXPORTERS:
            data = EXPORTERS[o_str](g, s)
            slug = s.split("/")[-1]
            # 给不同类型起不同前缀
            type_name = data["@type"].lower()
            (pub_dir / f"{type_name}-{slug}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
    export_graph_index(g, pub_dir)
    export_csv(g, out_dir)

    print(f"Total triples: {len(g)}")
    print(f"Total works: {len(list(g.subjects(RDF.type, SCHEMA.Book)))}")