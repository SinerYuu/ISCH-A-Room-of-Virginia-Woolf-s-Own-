# ISCH-A-Room-of-Virginia-Woolf-s-Own-

## About the Project
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
This metadata analysis identifies the descriptive standards used by institutions that preserve or provide Virginia Woolf-related materials. Most items follow Dublin Core, MODS/METS, or TEI, while web-based sources use Schema.org or custom schemas to ensure interoperability across linked-data environments. In the table below, all the standards explicitly stated by the institutions are marked with *.

| Item Name                         | Object Type                                              | Provider                             | Metadata Standard                              | Description                                                                                                                                                                                                                                                                                                          |
| --------------------------------- | -------------------------------------------------------- | ------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A Room of One's Own               | Printed Edition                                          | Internet Archive                     | Dublin Core*                                   | The schema of Internet Archive is based on Dublin Core.                                                                                                                                                                                                                                                              |
| A Room of One's Own               | Manuscript                                               | Cambridge University Digital Library | MODS / METS , TEI*                             | The data in CUDL is primarily in METS, MODS and TEI formats, and it's currently working on implementing the IIIF technology to expand user experience.                                                                                                                                                               |
| To the Lighthouse                 | Digital Scholarly Edition (Printed Edition + Manuscript) | Woolf Online                         | TEI (inferred)                                 | Although there is no explicit schema statement found, the project functions as a digital scholarly edition, offering transcriptions and multiple textual states (manuscript, typescript, proofs, and printed version). Its organization and structure are consistent with typical TEI P5 scholarly editing projects. |
| 1928 Diary                        | Manuscript                                               | The New York Public Library          | MODS / METS*                                   | NYPL uses MODS XML to describe bibliographic and technical metadata within METS packages.                                                                                                                                                                                                                            |
| From the Diary of Virginia Woolf  | Song Cycle                                               | The LiederNet Archive                | Not explicitly declared — custom schema likely | The LiederNet Archive presents structured metadata (composer, author, language, text first line) but no formal metadata standard is stated. Metadata fields appear to be system-defined for this specialised corpus of art-song texts.                                                                               |
| Hogarth Press                     | Publishing House                                         | Wikipedia                            | Schema.org*                                    | Wikipedia implements structured data on its article pages using Schema.org markup and links to Wikidata for entity metadata.                                                                                                                                                                                         |
| Mrs. Dalloway                     | Printed Edition                                          | Internet Archive                     | Dublin Core*                                   | The schema of Internet Archive is based on Dublin Core.                                                                                                                                                                                                                                                              |
| Orlando                           | Printed Edition                                          | Internet Archive                     | Dublin Core*                                   | The schema of Internet Archive is based on Dublin Core.                                                                                                                                                                                                                                                              |
| Picture of Virginia Woolf in 1902 | Photograph                                               | Wikimedia Commons                    | Dublin Core, Schema.org                        | Wikimedia Commons implements Wikibase structured data based on Schema.org and Dublin Core predicates (title, creator, license) with embedded EXIF technical metadata for media files.                                                                                                                                |
| Places Related to Virginia Woolf  | Maps                                                     | GeoNames                             | Dublin Core                                    | GeoNames Ontology uses Dublin Core metadata elements to describe the ontology and its metadata. The ontology defines its own RDF vocabulary for geospatial features.                                                                                                                                                 |
| The Hours                         | Movie                                                    | IMDb                                 | Schema.org                                     | Metadata is embedded as JSON-LD in webpages, following Schema.org’s Movie type (name, director, datePublished, genre) for search engine interoperability.                                                                                                                                                            |


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

<img width="2615" height="2227" alt="A room of Virginia Woolf&#39;s own" src="https://github.com/user-attachments/assets/38246184-f6a4-4947-a3ad-423bf4dce357" />

## Files Sturcture
```
ISCH-A-Room-of-Virginia-Woolf-s-Own/
├── data/
│   ├── tei              
│       ├── XXX.xml                                # tei annotation on items
│       ├── XXX.jpg                                # jpg items
│       └── ...
│   └── img
│       └──A Room of Virginia Woolf's Own.png      # the graffoo picture
├── output/
│   ├── woolf-full.rdf             # ontology in rdf (autogenerated by scripts/jsoncsv.py)
│   ├── woolf-full.ttl             # ontology in ttl (autogenerated by scripts/jsoncsv.py)
│   ├── XX.csv                     # csv of triples on each item (autogenerated by scripts/jsoncsv.py)
│   └── ... 
├── public/
│   ├── data/ 
│       ├── XXX.json               # additional .json files, for Front-End
│       ├── graph.json             # overview json of all items
│       └── ...
│   ├── images/ 
│       └──                        # the images used on final website
│   └── XXX.html                   # final html of website
└── scripts/
    ├── buil_full.py                # tei -> rdf
    ├── jsoncsv.py                  # rdf -> csv
    ├── tei_mapping.json            
    └── ...                         # additional .csv or .json files
```

## About the Team
| Name | Role | Responsibilities |
|------|--------------|------------------------------------|
| Peize Yu | Coordinator | XML/TEI documents, Metadata analysis |
| Yihua Li | Theorist | XML/TEI to RDF transformation, Theoretical/Conceptual model  |
| Jingtong Jiang | Designer | XML to HTML transformation, Webpage making |
