# ISCH-A-Room-of-Virginia-Woolf-s-Own-
Group project for the course Information Science and Cultural Heritage at DHDK, UNIBO.

## Metadata Analysis

## Theoretical Model
The project models the literary universe around the English writer Virginia Woolf as a network of interconnected entities, including people, works, places, publishers, adaptations, and visual resources.
Each entity is described according to existing metadata standards adopted by the cultural heritage institutions holding the items:

| Source  |	Metadata Format	| Standard |
|---------|-----------------|----------|
| DBpedia	| RDF/XML	| Dublin Core, FOAF |
| Woolf Online	| TEI P5	| TEI |
| Cambridge Digital Library	| XML |	MODS / TEI |
| Archive.org	| RDFa	| schema.org |
| Wikimedia Commons	| RDFa	| schema:MediaObject |

Each work (e.g. To the Lighthouse, Mrs Dalloway) has attributes such as title, creator, publication year, publisher, and related locations of creation and content.
The project introduces one custom property — woolf:hasManuscript — to link works with their digital manuscripts (edm:WebResource).
Places are linked to external authorities (Wikidata, GeoNames) via owl:sameAs, while visual materials (portraits, facsimiles) use foaf:depicts to connect with the person entity.
Adaptations such as The Hours (film) or From the Diaries of Virginia Woolf (music composition) are connected to the original works through schema:basedOn or prov:wasDerivedFrom.

The model therefore integrates literary, biographical, and geographical information through Linked Open Data, reusing vocabularies such as schema.org, Dublin Core Terms, FOAF, PROV, EDM, and GEO.
Its conceptual structure is further represented in the Graffoo diagram and in RDF/OWL serializations (woolf-full.rdf, woolf-full.ttl).

## Conceptual Model

## Front-End Data Guide

###  Data Location
All data are in `/public/data/`.

###  Files
- `graph.json` — overview of all items.
- `work-*.json` — works (books, essays).
- `person-virginia-woolf.json` — main author.
- `place-*.json` — related places.
- `film-*.json` — adaptations.
- `resource-*.json` — manuscripts and images.

###  Routing
| Page | Example URL | Data File Loaded |
|------|--------------|------------------|
| work.html | `?id=to-the-lighthouse` | `/data/work-to-the-lighthouse.json` |
| person.html | `?id=virginia-woolf` | `/data/person-virginia-woolf.json` |
| place.html | `?id=london` | `/data/place-london.json` |

###  JSON-LD Structure
| Key | Meaning |
|-----|----------|
| `@id` | local identifier |
| `@type` | entity type (Book, Person, Place...) |
| `name` / `title` | label |
| `creator` | nested person object |
| `contentLocation` | nested place object |
| `sameAs` / `seeAlso` | external links |
| `contentUrl` | direct link to image or web resource |

Front-end only needs to read these JSON files with `fetch()` and display them.
