# ISCH-A-Room-of-Virginia-Woolf-s-Own-
Group project for the course Information Science and Cultural Heritage at DHDK, UNIBO.

    Virginia Woolf (1882 – 1941) was one of the foremost figures of English literary modernism — a novelist, essayist, and publisher whose life and works reshaped twentieth-century ideas of art, gender, and consciousness.
 Born into a prominent intellectual family in London, she grew up surrounded by books, debates, and the early currents of feminism. Her home later became the center of the Bloomsbury Group, a circle of writers, artists, and thinkers who challenged Victorian conventions and redefined modern art and philosophy.
    Woolf’s writing career began at the Hogarth Press, which she co-founded with her husband Leonard Woolf in 1917. Through this small independent press she published not only her own works but also experimental texts by T.S. Eliot, Freud, and Katherine Mansfield — making the Press itself an emblem of avant-garde literary culture.
    Her major novels — Mrs. Dalloway (1925), To the Lighthouse (1927), Orlando (1928), and so many others — revolutionized narrative form with interior monologue and fluid time. Each work explores the subtle layers of human perception and the constraints imposed by gender, society, and history.
    - Mrs Dalloway, set in post-war London, unfolds in a single day and probes the inner lives of ordinary citizens beneath the surface of urban routine.
    - To the Lighthouse reflects the memory of Woolf’s childhood summers in St Ives, translating personal loss into a meditation on art and transience.
    - Orlando playfully defies gender and time, inspired by her relationship with Vita Sackville-West, becoming a celebration of identity’s fluidity.
    - In A Room of One’s Own, Woolf transformed her Cambridge lectures into a manifesto for women’s intellectual independence — the foundation of feminist literary criticism.
    Yet behind this creative brilliance lay an ongoing struggle with mental illness. Between periods of intense productivity and silence, Woolf’s diaries reveal both vulnerability and resilience, her acute sensitivity to the modern world’s chaos. In 1941, amid the turmoil of World War II, she took her own life near her home in Rodmell, Sussex, leaving behind a body of work that continues to inspire and challenge readers.
    Virginia Woolf’s influence transcends literature; she stands as both writer and symbol — of modern consciousness, of feminist thought, and of the intertwined beauty and fragility of the creative mind.
    Picking up pieces of the iconic Virginia Woolf, "A Room of Virginia Woolf's Own" as an Information Science project intends to build a semantic and digital representation of the life, works, and cultural afterlives of Virginia Woolf, one of the most influential figures of English modernism. 
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
