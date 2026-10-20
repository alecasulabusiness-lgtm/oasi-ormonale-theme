# Brand identity 2026

Fonte: `brand/OAS_B26_Guidelines.pdf`, 15 pagine, "Brand Guidelines | Oasi Ormonale - 2026". I nomi dei colori qui sotto sono descrittivi e li ho dati io: il documento riporta solo i codici.

## Palette (pag. 9)

| Colore | HEX | RGB | CMYK |
| --- | --- | --- | --- |
| Borgogna scuro | `#4b1c22` | 75 / 28 / 34 | 42 / 85 / 59 / 69 |
| Vino | `#65333c` | 101 / 51 / 60 | 39 / 76 / 49 / 53 |
| Rosa antico | `#db9aa8` | 219 / 154 / 168 | 13 / 48 / 22 / 1 |
| Rosa cipria | `#ebccd2` | 235 / 204 / 210 | 8 / 25 / 12 / 0 |
| Crema | `#f6ede4` | 246 / 237 / 228 | 4 / 8 / 11 / 0 |
| Marrone | `#9d7961` | 157 / 121 / 97 | 30 / 46 / 55 / 24 |

## Tipografia (pag. 12)

| Uso | Font | Genere |
| --- | --- | --- |
| Titolo principale | Geologica | sans-serif geometrico |
| Corpo del testo | Niramit | sans-serif umanistico |
| Corsivo | Brush Script MT | script, calligrafico |

Il corsivo compare nel documento in un solo punto, come sopratitolo ("Respiro visivo", pag. 7). Brush Script MT è un font commerciale che non si può incorporare liberamente in un sito: sul web va con `cursive` come alternativa, e si vede solo dove è installato. Geologica e Niramit sono su Google Fonts con licenza OFL.

## Logo

Il marchio è il pittogramma (un triangolo dai bordi arrotondati, vuoto al centro) sopra il logotipo "Oasi Ormonale". Il documento mostra tre versioni: bianco su borgogna (pag. 8), e le due monocromatiche, bianco su nero e nero su bianco (pag. 11).

- Area di rispetto: 15X su ogni lato (15X = 15 mm nel documento, pag. 10).
- Usi vietati (pag. 13): allungare, schiacciare, aggiungere ombre, sfumature, cornici, inclinare, cambiare colore, usare in outline, aggiungere frasi non previste, metterlo sopra un'immagine complessa.

## Tono visivo

- Pag. 3, logotipo: contrasto degli spessori ("unendo la forza alla delicatezza"), forme circolari e morbide, stile graziato ed elegante, con "autorevolezza clinica" e un "tocco premium".
- Pag. 6, pittogramma: "il flusso del cambiamento". Il passaggio morbido da una forma all'altra rappresenta le fasi della vita di una donna e dei suoi cicli ormonali.
- Pag. 7, "Respiro visivo / Benessere Clinico": un'animazione lenta e pulsante, che simula un respiro profondo, per accogliere chi arriva sul sito.
- Pag. 4, 14, 15: foto di donne adulte, luce naturale, abiti in toni vino e terra, carta goffrata e sigillata a secco su fondi borgogna e sabbia.

## Applicato nel tema (ramo `brand/nuova-identita`)

Logo nuovo in bianco e nero al posto del vecchio logo dorato:

- Header: logo nero. Gli header GemPages stanno su fondo `#D5D5D5`.
- Footer: logo bianco. I footer stanno su fondo nero.
- Header nativo del tema (prodotti, carrello, blog): `logo` nero, `logo_inverse` bianco, altezza 56 px su desktop e 40 su mobile, perché il logo nuovo è impilato e più alto del vecchio.
- Favicon: pittogramma bianco su quadrato nero con angoli arrotondati.
- Testo alternativo "Oasi Ormonale" sulle immagini del logo, che prima avevano `alt=""`.

Lo ha fatto `tools/apply_logo.py`: 49 file di sezioni e template più `config/settings_data.json`, 85 riferimenti sostituiti, nessun riferimento al vecchio logo rimasto. I file sono nei File di Shopify (Contenuti > File):

| File | Uso |
| --- | --- |
| `oasi-logo-black.svg` | header GemPages |
| `oasi-logo-white.svg` | footer GemPages |
| `oasi-logo-black.png`, `oasi-logo-white.png` | header nativo del tema (il selettore immagini del tema vuole PNG) |
| `oasi-favicon.png` | favicon |

Gli originali vettoriali sono in `brand/logo/`. Li ho estratti dalla pag. 8 del PDF con `pdftocairo -svg -f 8 -l 8 brand/OAS_B26_Guidelines.pdf page8.svg` e `tools/extract_logo.py`.

## Contrasti della palette

Rapporti di contrasto calcolati per le coppie che servono nel sito (soglia WCAG AA: 4,5:1 per il testo, 3:1 per testo grande e per elementi non testuali):

| Coppia | Rapporto | Esito |
| --- | --- | --- |
| Borgogna scuro su crema | 12,2 | ok |
| Vino su crema | 8,7 | ok |
| Crema su borgogna scuro | 12,2 | ok |
| Rosa cipria su borgogna scuro | 9,5 | ok |
| Rosa antico su borgogna scuro | 6,2 | ok |
| Borgogna scuro su rosa antico | 6,2 | ok |
| Borgogna scuro su rosa cipria | 9,5 | ok |
| Crema su vino | 8,7 | ok |
| Rosa cipria su vino | 6,7 | ok |
| Rosa antico su crema | 2,0 | no |
| Marrone su crema | 3,4 | solo testo grande |
| Crema o borgogna su marrone | 3,4 e 3,6 | solo testo grande |
| Nero su marrone | 5,3 | ok |

Il rosa antico non si usa per il testo su crema. Il marrone va bene per filetti e decorazioni, e come fondo regge solo testo nero o testo molto grande.

## Non ancora applicato

Font e palette. Dipendono dalla scelta tra la versione in bianco e nero e quella con borgogna e rosa. La bozza di confronto è nel canvas https://claude.ai/artifact/JnhF98FuZ6MnejLu13BY9b (privato: lo apre solo chi ha accesso).

I vecchi file del logo (`gempages_…-2ef090f0-….png` e `gempages_…-d7ce851e-….png`) restano nei File di Shopify: la repo non li usa più, ma li lascio dove sono finché il tema live li richiama.
