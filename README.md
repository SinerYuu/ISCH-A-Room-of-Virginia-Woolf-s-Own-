# ISCH-A-Room-of-Virginia-Woolf-s-Own-
Group project for the course Information Science and Cultural Heritage at DHDK, UNIBO.

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
