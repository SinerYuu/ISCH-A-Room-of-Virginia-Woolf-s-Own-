# export data

import json, csv
from pathlib import Path
from rdflib import RDF, RDFS, Namespace
from rdflib.namespace import DCTERMS
SCHEMA = Namespace("https://schema.org/")

def export_work_json(g, work_uri, pub_dir):
    """导出单个作品的 JSON-LD 文件给前端"""
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
        obj["creator"] = {
            "@id": str(creator),
            "name": g.value(creator, SCHEMA.name)
                    and str(g.value(creator, SCHEMA.name))
        }
    if loc:
        obj["contentLocation"] = {
            "@id": str(loc),
            "name": g.value(loc, SCHEMA.name)
                    and str(g.value(loc, SCHEMA.name))
        }
    if sameAs:
        obj["sameAs"] = [str(u) for u in sameAs]

    slug = str(work_uri).split("/")[-1]
    json_path = pub_dir / f"work-{slug}.json"
    json_path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Exported JSON → {json_path.name}")

def export_person_json(g, person_uri, pub_dir):
    name = g.value(person_uri, SCHEMA.name) or g.value(person_uri, DCTERMS.title)
    obj = {
        "@context": "https://schema.org",
        "@id": str(person_uri),
        "@type": "Person",
        "name": str(name) if name else ""
    }
    slug = str(person_uri).split("/")[-1]
    (pub_dir / f"person-{slug}.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def export_place_json(g, place_uri, pub_dir):
    name = g.value(place_uri, SCHEMA.name) or g.value(place_uri, DCTERMS.title)
    obj = {
        "@context": "https://schema.org",
        "@id": str(place_uri),
        "@type": "Place",
        "name": str(name) if name else "",
    }
    slug = str(place_uri).split("/")[-1]
    (pub_dir / f"place-{slug}.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def export_film_json(g, film_uri, pub_dir):
    title = g.value(film_uri, DCTERMS.title) or g.value(film_uri, SCHEMA.name)
    based_on = g.value(film_uri, SCHEMA.basedOn)
    obj = {
        "@context": "https://schema.org",
        "@id": str(film_uri),
        "@type": "Movie",
        "name": str(title) if title else "",
    }
    if based_on:
        obj["basedOn"] = {"@id": str(based_on)}
    slug = str(film_uri).split("/")[-1]
    (pub_dir / f"film-{slug}.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def export_collection_json(g, coll_uri, pub_dir):
    name = g.value(coll_uri, DCTERMS.title) or g.value(coll_uri, SCHEMA.name)
    obj = {
        "@context": "https://schema.org",
        "@id": str(coll_uri),
        "@type": "Collection",
        "name": str(name) if name else "",
    }
    slug = str(coll_uri).split("/")[-1]
    (pub_dir / f"collection-{slug}.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def export_graph_index(g, pub_dir):
    """导出 graph.json 给前端（作品总览）"""
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
    path = pub_dir / "graph.json"
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Exported graph.json → {path}")

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


def export_all(g, out_dir, pub_dir):
    """主调用函数，一次导出 JSON + CSV"""
    pub_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    for s, p, o in g.triples((None, RDF.type, SCHEMA.Book)):
        export_work_json(g, s, pub_dir)     # all works' json
    for s, p, o in g.triples((None, RDF.type, SCHEMA.Person)):
        export_person_json(g, s, pub_dir)   # VW
    for s, p, o in g.triples((None, RDF.type, SCHEMA.Place)):
        export_place_json(g, s, pub_dir)    # all places' json
    for s, p, o in g.triples((None, RDF.type, SCHEMA.Movie)):
        export_film_json(g, s, pub_dir)     # The Hours
    for s, p, o in g.triples((None, RDF.type, SCHEMA.Collection)):
        export_collection_json(g, s, pub_dir)  # diaries

    export_graph_index(g, pub_dir)  # graph.json
    export_csv(g, out_dir)

    print(f"Total triples: {len(g)}")
    print(f"Total works: {len(list(g.subjects(RDF.type, SCHEMA.Book)))}")
