# Oasi Ormonale: tema Shopify

Codice del tema dello store [oasiormonale.com](https://oasiormonale.com) (`1fkjyx-xd.myshopify.com`) e lavoro sulla nuova brand identity.

Il punto di partenza è il tema live "Tema shopify LIVE" (base Horizon), esportato dall'Admin API il 20/10/2026. Origine, conteggi e limiti dell'export sono in [docs/esportazione.md](docs/esportazione.md). Font e colori attuali, misurati dal codice, sono in [docs/identita-attuale.md](docs/identita-attuale.md).

## Rami

| Ramo | A cosa serve |
| --- | --- |
| `main` | Copia del tema live al momento dell'esportazione. Resta com'è e fa da riferimento per i confronti. |
| `brand/nuova-identita` | Ramo di lavoro per la nuova identità. È quello da collegare a Shopify. |

## Collegare il ramo a Shopify

1. Admin Shopify > Negozio online > Temi > Aggiungi tema > Connetti da GitHub.
2. Autorizza l'app Shopify GitHub sulla repo `oasi-ormonale-theme`, se non l'hai già fatto.
3. Scegli la repo e il ramo `brand/nuova-identita`.

Shopify crea un tema nuovo, non pubblicato, e il tema live resta intatto. Da lì i commit sul ramo arrivano nel tema, e le modifiche fatte nell'editor di Shopify tornano sul ramo come commit. Pubblicare il tema è un passaggio separato e si fa dall'admin.

Collega solo `brand/nuova-identita`. Con `main` collegato, le modifiche fatte nell'editor su quel tema finirebbero su `main`.

## Struttura

Le cartelle del tema stanno alla radice (`assets`, `blocks`, `config`, `layout`, `locales`, `sections`, `snippets`, `templates`), come richiede Shopify. `AGENTS.md` è la guida al tema che arriva con Horizon. Shopify ignora le cartelle fuori dalla struttura del tema, quindi `docs/`, `brand/` e `tools/` non entrano nel tema.

| Cartella | Contenuto |
| --- | --- |
| `docs/` | Esportazione, identità attuale, brand identity 2026 con i contrasti della palette |
| `brand/` | Guidelines in PDF e logo in vettoriale e PNG, bianco e nero |
| `tools/` | `apply_logo.py` (mette il logo nuovo nel tema), `extract_logo.py` (estrae il logo dal PDF) |

## Stato del ramo `brand/nuova-identita`

Fatto: logo nuovo in bianco e nero (header, footer, header nativo, favicon). Da decidere: palette e font, in bianco e nero oppure con borgogna e rosa. Dettagli in [docs/brand-identity.md](docs/brand-identity.md).

## GemPages

218 delle 253 sezioni e 56 dei 69 template vengono da GemPages (`gp-section-*`, `*.gp-template-*`, `*.gem-*`). Font e colori di quelle pagine sono scritti dentro i file. È probabile che ripubblicare una pagina dall'editor di GemPages rigeneri il suo file e cancelli le modifiche fatte qui; da verificare sul tema collegato.
