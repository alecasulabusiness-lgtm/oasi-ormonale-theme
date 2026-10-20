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
| `docs/` | Esportazione, identità attuale, brand identity 2026 con i contrasti della palette, migrazione delle pagine |
| `brand/` | Guidelines in PDF e logo in vettoriale e PNG, bianco e nero |
| `tools/` | `build_templates.py` (ricostruisce home e pagine interne dai testi originali), `validate_templates.py` (controlla i template contro gli schema delle sezioni), `apply_palette.py` (palette ufficiale in `config/settings_data.json`), `apply_logo.py` (mette il logo nuovo nel tema), `extract_logo.py` (estrae il logo dal PDF) |

## Stato del ramo `brand/nuova-identita`

Pronto da pubblicare. Contiene la nuova identità (palette ufficiale borgogna, rosa e crema; Geologica e Niramit; logo nuovo) applicata a home, Chi siamo, I nostri brand, Lavora con noi, header e footer. Cosa è cambiato, i link, le correzioni ai testi e i punti da sapere sono in [docs/migrazione-pagine.md](docs/migrazione-pagine.md).

## Pubblicare

1. Admin Shopify > Negozio online > Temi.
2. Sul tema `oasi-ormonale-theme/brand/nuova-identita` > Pubblica.

Da quel momento il ramo `brand/nuova-identita` è il tema live: ogni push su quel ramo va in produzione. Per lavorare su altro, crea un ramo nuovo e collegalo come tema separato.

Le pagine GemPages non rifatte (Sensualità, Celebrities, quiz, TYP e le altre) non cambiano.

## GemPages

Le pagine GemPages hanno font e colori scritti dentro i file (`gp-section-*`, `*.gp-template-*`, `*.gem-*`). Le quattro pagine ricostruite non usano più GemPages. Se si ripubblica una di quelle pagine dall'editor di GemPages, GemPages può rigenerare il suo template e cancellare la versione nativa: per modificarle si usa l'editor del tema.
