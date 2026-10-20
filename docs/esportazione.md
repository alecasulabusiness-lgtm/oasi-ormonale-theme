# Esportazione del tema live

## Origine

- Store: Oasi Ormonale, `oasiormonale.com` (`1fkjyx-xd.myshopify.com`)
- Tema: "Tema shopify LIVE", ruolo `MAIN`, base Horizon
- ID: `gid://shopify/OnlineStoreTheme/188342239575`
- Ultima modifica del tema prima e dopo l'esportazione: 2026-10-16T15:05:48Z (invariata, quindi nessuno ha modificato il tema mentre lo esportavo)
- Esportato il 2026-10-20 con la query `theme.files` dell'Admin API, un file alla volta, senza passare dall'editor

## Contenuto

690 file, lo stesso numero che Shopify elenca per il tema.

| Cartella | File |
| --- | --- |
| `assets` | 100 |
| `blocks` | 87 |
| `config` | 3 |
| `layout` | 6 |
| `locales` | 51 |
| `sections` | 253 |
| `snippets` | 120 |
| `templates` | 69 |
| radice (`AGENTS.md`) | 1 |

## Integrità

Shopify registra un checksum MD5 per ogni file. Confronto con i file scritti qui:

- 569 file coincidono byte per byte: 465 `.liquid`, 66 `.js`, 28 `.svg`, 4 `.css`, 1 `.ts`, 5 `.json`.
- 120 file `.json` hanno un MD5 diverso. L'API li restituisce in forma normalizzata (indentazione ed escape diversi, e quindi anche dimensione diversa da quella dichiarata). Tutti si leggono come JSON valido. I due file `locales/en.default.json` e `locales/en.default.schema.json` contengono commenti `//`, che Shopify accetta nei file delle traduzioni.
- Non ho verificato che quei 120 file abbiano lo stesso contenuto dell'originale campo per campo. La verifica prevista è un confronto tra il tema creato da questa repo e il tema live, dopo il collegamento a Shopify.
- `AGENTS.md`: 18586 byte, uguale alla dimensione dichiarata. Il checksum non è stato controllato.

## Cosa non c'è

- Prodotti, pagine, articoli del blog, menu e impostazioni dello store: non fanno parte del tema.
- Le immagini caricate in Contenuti > File, compresi il logo `Oasi_Ormonale.png` e il favicon `Oasi_Ormonale_fav.png`. Il tema li richiama per nome.
- I dati interni dell'app GemPages. I template e le sezioni che GemPages ha scritto nel tema ci sono, il resto no.
