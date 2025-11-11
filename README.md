# ISCH-A-Room-of-Virginia-Woolf-s-Own-

## About the Project
Group project for the course Information Science and Cultural Heritage at DHDK, UNIBO.

Virginia Woolf (1882 – 1941) was one of the foremost figures of English literary modernism — a novelist, essayist, and publisher whose life and works reshaped twentieth-century ideas of art, gender, and consciousness.

Born into a prominent intellectual family in London, she grew up surrounded by books, debates, and the early currents of feminism. Her home later became the center of the Bloomsbury Group, a circle of writers, artists, and thinkers who challenged Victorian conventions and redefined modern art and philosophy.

Woolf’s writing career began at the Hogarth Press, which she co-founded with her husband Leonard Woolf in 1917. Through this small independent press she published not only her own works but also experimental texts by T.S. Eliot, Freud, and Katherine Mansfield — making the Press itself an emblem of avant-garde literary culture.

Her major novels — *Mrs. Dalloway* (1925), *To the Lighthouse* (1927), *Orlando* (1928), and so many others — revolutionized narrative form with interior monologue and fluid time. Each work explores the subtle layers of human perception and the constraints imposed by gender, society, and history.

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

### Authority Control
The project adopts authority control practices to ensure consistent identification and referencing of entities.
Each person, place, and work was linked to external authority sources (DBpedia, Wikidata, VIAF, IMDb).
Internal TEI markup and RDF labels were also standardized to maintain controlled vocabularies within the dataset.
| Entity Type  | Local URI               | Authority Source |
| ------------ | ----------------------- | ---------------- |
| Person       | `person/virginia-woolf` | DBpedia, VIAF    |
| Work         | `work/mrs-dalloway`     | DBpedia          |
| Place        | `place/stives`          | GeoName, Wikidata|
| Organization | `org/hogarth-press`     | Wikidata         |
| Film         | `film/the-hours`        | IMDb             |


## Theoretical Model
the idea about ontology:
<img width="1103" height="701" alt="vw drawio" src="https://github.com/user-attachments/assets/800f1ed9-75d4-4275-94df-9b1df3c9b122" />

The project models the literary universe around the English writer Virginia Woolf as a network of interconnected entities, including people, works, places, publishers, adaptations, and visual resources.
Each entity is described according to existing metadata standards adopted by the cultural heritage institutions holding the items.
Each work (e.g.*To the Lighthouse*, *Mrs Dalloway*) has attributes such as title, creator, publication year, publisher, and related locations of creation and content.
The project introduces one custom property __woolf:hasManuscript__ to link works with their digital manuscripts (__edm:WebResource__).
The manuscripts are connected only to the works, and each page includes its own description and external digital link.
In the case of the diaries, this project treats the entire diary as a collection, while the 1928 diary is selected as a specific manuscript to be annotated in detail.
Places are linked to external authorities (Wikidata, GeoNames) via __owl:sameAs__, and those works linked to the places they were created or their content happened in through schema:contentLocation or schema:locationCreated.
Visual materials (portraits, facsimiles) use foaf:depicts to connect with the person entity.
Adaptations such as *The Hours* (film) or *From the Diaries of Virginia Woolf* (music composition) are connected to the original works through schema:basedOn or prov:wasDerivedFrom. *From the Diary of Virginia Woolf* is linked to the entire diary collection.
The model therefore integrates literary, biographical, and geographical information through Linked Open Data, reusing vocabularies such as schema.org, Dublin Core Terms, FOAF, PROV, EDM, and GEO.
Its conceptual structure is further represented in the Graffoo diagram and in RDF/OWL serializations (woolf-full.rdf, woolf-full.ttl).

## Conceptual Model
This model illustrates the main semantic relationships among the selected items. It identifies the roles of persons, creative works, and places, highlighting the interconnections of authorship, publication, and inspiration.
<img width="2615" height="2227" alt="A room of Virginia Woolf&#39;s own" src="https://github.com/user-attachments/assets/38246184-f6a4-4947-a3ad-423bf4dce357" />
### Class
```
Class: Person
    Explanation: Represents human individuals, such as authors, artists, or related historical figures.

Class: Place
    Explanation: Refers to geographical locations associated with people or works (e.g., birthplaces, residences, settings).

Class: Organization
    Explanation: Denotes publishing houses or institutions connected to the production of literary works.

Class: Book
    Explanation: Stands for individual literary works authored by Virginia Woolf.

Class: CreativeWork
    Explanation: Used for other types of creative outputs beyond books, such as diaries or manuscripts.

Class: Collection
    Explanation: Represents a group or compilation of creative works, such as *The Diary of Virginia Woolf* volumes.

Class: WebResource
    Explanation: Refers to digitized or online resources (e.g., manuscript images, portraits) connected to the works.

Class: Movie
    Explanation: Denotes filmic interpretations or adaptations inspired by Woolf’s writings.

Class: MusicComposition
    Explanation: Captures musical compositions based on Woolf’s works or life.
```
### Objext Properties
```
ObjectProperty: birthPlace
    Domain: Person
    Range: Place
    Explanation: Connects a person to the place where they were born.

ObjectProperty: deathPlace
    Domain: Person
    Range: Place
    Explanation: Links a person to their place of death.

ObjectProperty: creator
    Domain: Book
    Range: Person
    Explanation: Expresses authorship between a work and its creator.

ObjectProperty: publisher
    Domain: Book
    Range: Organization
    Explanation: Indicates the organization responsible for publishing a work.

ObjectProperty: hasPart
    Domain: Collection
    Range: CreativeWork
    Explanation: Specifies that a collection includes particular creative works.

ObjectProperty: hasManuscript
    Domain: Book
    Range: WebResource
    Explanation: Associates a published work with its surviving manuscript images.

ObjectProperty: depiction
    Domain: Person
    Range: WebResource
    Explanation: Connects a person to their visual representation (portrait).

ObjectProperty: depicts
    Domain: WebResource
    Range: Person
    Explanation: Reverse relation showing that a resource portrays a person.

ObjectProperty: contentLocation
    Domain: Book
    Range: Place
    Explanation: Links a literary work to the location where its story is set.

ObjectProperty: basedOn
    Domain: Movie
    Range: Book
    Explanation: Expresses that a film is inspired by a literary work.

ObjectProperty: wasDerivedFrom
    Domain: MusicComposition
    Range: Collection
    Explanation: Indicates a musical piece is derived from or inspired by a literary collection.
```
### DataProperties
```
DataProperty: name
    Domain: Person, Place, Organization
    Range: Literal
    Explanation: Records the proper name of individuals, locations, or institutions.

DataProperty: title
    Domain: Book, CreativeWork, Collection, Movie, MusicComposition, WebResource
    Range: Literal
    Explanation: Specifies the title of the creative or digital resource.

DataProperty: date
    Domain: Book, CreativeWork
    Range: Literal
    Explanation: Indicates the year of creation or publication.

DataProperty: birthDate
    Domain: Person
    Range: Literal
    Explanation: Records the date of birth of a person.

DataProperty: deathDate
    Domain: Person
    Range: Literal
    Explanation: Records the date of death of a person.

DataProperty: foundingDate
    Domain: Organization
    Range: Literal
    Explanation: Specifies when an organization was founded.

DataProperty: lat
    Domain: Place
    Range: Literal
    Explanation: Expresses the latitude coordinate of a location.

DataProperty: long
    Domain: Place
    Range: Literal
    Explanation: Expresses the longitude coordinate of a location.

DataProperty: contentUrl
    Domain: WebResource
    Range: Literal
    Explanation: Stores the link to the digital representation of a manuscript or image.
```
### Individuals (Selected Examples)
```
Individual: virginia-woolf
    Types: Person
    Facts:
        birthPlace london
        deathPlace rodmell
        depiction portrait-woolf-1902
        name "Virginia Woolf"
        birthDate "1882-01-25"
        deathDate "1941-03-28"
    Explanation: Central individual connecting the creative network of works, locations, and visual representations.

Individual: hogarth-press
    Types: Organization
    Facts:
        name "Hogarth Press"
    Explanation: Publishing house co-founded by Virginia Woolf, linking most of her works.

Individual: london
    Types: Place
    Facts:
        name "London"
        lat "51.50853"
        long "-0.12574"
    Explanation: Major geographic anchor representing Woolf’s birthplace and literary space.

Individual: rodmell
    Types: Place
    Facts:
        name "Rodmell"
        lat "50.83917"
        long "0.01588"
    Explanation: The location of Woolf’s final residence and death.

Individual: to-the-lighthouse
    Types: Book
    Facts:
        creator virginia-woolf
        publisher hogarth-press
        hasManuscript fig-lh-page1
        hasManuscript fig-lh-page2
        contentLocation st-ives
        title "Text of To the Lighthouse"
        date "1927"
    Explanation: A representative novel linking author, publisher, and manuscript sources.

Individual: a-room-of-one-s-own
    Types: Book
    Facts:
        creator virginia-woolf
        publisher hogarth-press
        title "Text of A Room of One’s Own"
        date "1929"
    Explanation: Canonical feminist essay emphasizing economic and intellectual independence.

Individual: the-diary-of-virginia-woolf
    Types: Collection
    Facts:
        title "The Diary of Virginia Woolf"
    Explanation: A compilation that serves as a narrative and inspirational source for later adaptations.

Individual: 1928-diary
    Types: CreativeWork
    Facts:
        title "1928 Diary"
    Explanation: One of Woolf’s diary entries, linked with WebResource facsimiles.

Individual: the-hours-virginia-woolf-s-modern-echo
    Types: Movie
    Facts:
        basedOn mrs-dalloway
        title "The Hours: Virginia Woolf’s Modern Echo"
    Explanation: Cinematic reinterpretation connecting Woolf’s life and her novel *Mrs Dalloway*.

Individual: from-the-diary-of-virginia-woolf
    Types: MusicComposition
    Facts:
        wasDerivedFrom the-diary-of-virginia-woolf
        title "From the Diary of Virginia Woolf"
    Explanation: A musical composition inspired by Woolf’s diary texts and emotional landscape.

Individual: fig-lh-page1
    Types: WebResource
    Facts:
        title "Manuscript Page 1 of To the Lighthouse"
        contentUrl "fig-lh-page1.jpg"
    Explanation: A digitized facsimile of Woolf’s handwritten manuscript page.
```
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
├── html/
│   ├── data/ 
│       ├── XXX.xml               # additional xml files
│       └── ...
│   ├── collection.html/           # final html     
│   └── combine_tei.xslt           # the file of xslt
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
