# Identità visiva attuale, misurata dal codice

Questi dati vengono dal codice del tema esportato il 2026-10-20. Il sito renderizzato non l'ho visto: i conteggi sono occorrenze nel codice e non dicono quanta superficie occupa ogni colore o font.

## Impostazioni del tema (`config/settings_data.json`)

- Font: Inter (testo, titoli), Bricolage Grotesque (accento)
- Schemi colore: bianco e nero
- Logo: `Oasi_Ormonale.png`, favicon: `Oasi_Ormonale_fav.png`

## Dentro i file GemPages

226 file (`sections/gp-section-*` e `snippets/gp-*`) hanno font e colori scritti nel file e non presi dalle impostazioni del tema.

Font più usati, per numero di occorrenze di `font-family`:

| Font | Occorrenze |
| --- | --- |
| Montserrat | 1867 |
| Cormorant Garamond | 831 |
| Anton | 58 |
| Geologica | 57 |
| Cormorant Unicase | 48 |
| Lora | 17 |
| Inter | 17 |

Colori HEX più frequenti:

| Colore | Occorrenze |
| --- | --- |
| `#121212` | 2022 |
| `#F4F4F4` | 1709 |
| `#000000` | 1445 |
| `#FFFFFF` | 1373 |
| `#E4BB7A` | 876 |
| `#BEA35F` | 572 |
| `#151515` | 387 |
| `#FCE19A` | 266 |
| `#C5453F` | 149 |
| `#DEB42F` | 135 |

## Cosa comporta per il restyling

218 delle 253 sezioni e 56 dei 69 template vengono da GemPages, e quei file pesano 15 MB dei 21 totali. Cambiare le impostazioni del tema modifica header, footer e poco altro. Per cambiare l'aspetto delle pagine bisogna intervenire su questi file, oppure sostituire le pagine GemPages con sezioni native del tema.

GemPages scrive questi file nel tema quando si pubblica una pagina dal suo editor. Non l'ho verificato, ma è probabile che una ripubblicazione sovrascriva le modifiche fatte qui sullo stesso file.
