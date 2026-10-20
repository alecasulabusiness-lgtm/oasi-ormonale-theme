# Migrazione delle pagine alla nuova identità

Home, Chi siamo, Lavora con noi e la cornice comune (header, footer) sono state ricostruite con sezioni native del tema, nello stile approvato (palette ufficiale borgogna, rosa e crema, con taglio clinico e premium). Tutte le altre pagine GemPages sono rimaste come erano.

## Cosa è stato rifatto

| Pagina | Template | Come si arriva |
| --- | --- | --- |
| Home | `templates/index.json` | `/` |
| Chi siamo | `templates/page.gp-template-586581486656815819.json` | `/pages/chi-siamo` |
| Lavora con noi | `templates/page.gp-template-586694286104331137.json` | `/pages/lavora-con-noi` |
| Header e footer | `sections/header-group.json`, `sections/footer-group.json` | tutte le pagine che usano il layout del tema |

I due template delle pagine interne hanno mantenuto il nome GemPages: così ogni pagina conserva il template assegnato e nello store non cambia niente. Il contenuto però è nativo, senza `gp-section-*` e senza il layout `theme.gempages.blank`.

Header e footer nuovi valgono per tutte le pagine che usano il layout del tema (`layout/theme.liquid`): le tre ricostruite, più prodotto, carrello, blog, ricerca e Contatti. Le pagine GemPages con layout `theme.gempages.blank` (landing, quiz, TYP) non li mostrano e tengono il loro header e il loro footer.

## Cosa non è stato toccato

- Tutte le altre pagine GemPages: Sensualità e le sue varianti, Celebrities, Quiz, VSL, TYP, Termini e condizioni, Protocollo Menopausa e le altre.
- Prodotti, carrello, checkout, email transazionali, blog.
- Le impostazioni Brand di Shopify (logo e colori usati da checkout ed email). Vanno aggiornate dall'admin, in Impostazioni > Brand.

## Sezioni nuove

| File | Uso |
| --- | --- |
| `sections/oasi-header.liquid` | Header con menu a tendina su mobile e pulsante principale |
| `sections/oasi-footer.liquid` | Footer a quattro colonne, testo legale e copyright |
| `sections/oasi-hero.liquid` | Apertura della home con foto e card del percorso |
| `sections/oasi-page-hero.liquid` | Apertura delle pagine interne |
| `sections/oasi-chips.liquid` | Fascia con le figure del team |
| `sections/oasi-method.liquid` | Il metodo: foto con testo sopra e riquadro laterale |
| `sections/oasi-split.liquid` | Testo con immagine, con elenco numerato o con spunte |
| `sections/oasi-statement.liquid` | Frase grande a tutta larghezza, con etichette facoltative |
| `sections/oasi-cards.liquid` | Card colorate (protocollo, posizioni aperte) |
| `sections/oasi-videos.liquid` | Griglia di video YouTube, caricati al click |
| `sections/oasi-team.liquid` | Le specialiste, con elenco |

Stile e script: `assets/oasi-brand.css`, `assets/oasi-videos.js`. Font Geologica e Niramit sono nel tema (`assets/*.woff2`, licenza OFL in `brand/fonts/`) e si caricano da `snippets/oasi-head.liquid`, incluso in `layout/theme.liquid`. I colori del tema (`config/settings_data.json`) sono quelli della palette ufficiale.

Ogni testo, immagine e link si cambia dall'editor del tema, sezione per sezione.

## Come sono stati ricostruiti i testi

I testi e i link vengono dai template GemPages originali, letti dal ramo `main` (copia del tema live al 20/10/2026) da `tools/build_templates.py`. Lo script ha asserzioni sulla posizione dei paragrafi: se un testo originale non è quello atteso si ferma. `tools/validate_templates.py` controlla che ogni impostazione e ogni blocco scritti nei template esistano negli schema delle sezioni.

Per rigenerare i template dalla radice della repo:

```
python3 tools/build_templates.py
python3 tools/validate_templates.py
```

Attenzione: lo script sovrascrive i template. Le modifiche fatte dall'editor di Shopify dopo la pubblicazione vanno perse se lo si rilancia.

## Correzioni ai testi originali

| Pagina | Prima | Dopo |
| --- | --- | --- |
| Home | IL protocollo | Il protocollo |
| Home | alimenti da dimenitacare | alimenti da dimenticare |
| Home | l'alimentazione schemi | l'alimentazione a schemi |
| Chi siamo | La Prima realtà in italia | La prima realtà in Italia |
| Chi siamo | BENESSRE | BENESSERE |
| Lavora con noi | Ogni talento? un piano carriera personale, A cui NON poniamo alcun limite. | Ogni talento? Un piano carriera personale, a cui non poniamo alcun limite. |
| Lavora con noi | Fitness trainer: "protocolli nutrizionali personalizzati" | "protocolli di allenamento personalizzati" |

L'ultima riga è più di un refuso: nell'originale la card Fitness trainer ripeteva il testo della card Nutrizione. Ho riscritto solo la parola che cambia. Se esiste un testo ufficiale per quel ruolo, va sostituito nell'editor.

I titoli dei ruoli e dei valori erano scritti in maiuscolo continuo: ora hanno la sola iniziale maiuscola.

## Link

| Dove | Destinazione |
| --- | --- |
| Header: Chi siamo, Lavora con noi | `/pages/chi-siamo`, `/pages/lavora-con-noi` |
| Pulsanti "Scopri Oasi Ormonale" | `/pages/oasi-ormonale` |
| Home, pulsante del hero | `/#protocollo` (la sezione dei protocolli, nella stessa pagina) |
| Pulsanti WhatsApp | `https://wa.me/+393296912328` |
| Lavora con noi: "Scopri le posizioni aperte" | `/pages/lavora-con-noi#posizioni-aperte` |
| Lavora con noi: "Candidati ora", team clinico | form Typeform `medici`, `ixHaHSYX`, `gp3Pbk6b`, come nell'originale |
| Lavora con noi: "Candidati ora", marketing e vendite | form Typeform `EN8ghdhI` (Sales), `g19z7KgH` (Copywriters), `cS695Y16` (Advertiser). Scelti dal titolo del form: non stavano nel template originale |

## Da sapere

1. **Pagina I nostri brand rimossa.** Template cancellato dal tema, link tolti da header e footer. Nello store la pagina è stata messa in bozza e `/pages/i-nostri-brand` rimanda alla home. Per ripristinarla basta ripubblicarla da Pagine e togliere il reindirizzamento (Negozio online > Navigazione > Reindirizzamenti URL). Il Progetto Leonessa non ha più una pagina: il link a `/pages/progettoleonessa` dava comunque 404.
2. **Termini e Condizioni tolti dal sito.** Non compaiono più nel footer. Restano Privacy Policy e Cookie Policy (iubenda). Le pagine "Termini & Condizioni" nello store sono ancora pubblicate e raggiungibili dall'indirizzo diretto.
3. **Posizioni aperte.** Quattro ruoli clinici (Medico, Nutrizione, Fitness trainer, Endocrinologhe) e quattro di marketing e vendite (Consulente commerciale, Copywriter direct response, Social media manager, Media buyer). I testi dei ruoli di marketing sono quelli delle impostazioni GemPages. Social media manager non ha un form Typeform dedicato: il pulsante non compare finché non si incolla il link nel campo "Pulsante, link" della card.
4. **Video.** I quattro video YouTube di Chi siamo e della home partono al click, senza caricare YouTube prima.
5. **Foto.** Le foto sono quelle già nei File di Shopify, con una tinta borgogna applicata dal CSS: nessun file è stato modificato.
6. **Header senza ricerca e senza carrello.** L'header nativo di prima li aveva. Lo store ha un solo prodotto attivo ("TEST") e le pagine di vendita sono GemPages, quindi oggi non servono. Se un giorno si usano le pagine prodotto del tema, vanno aggiunti all'header.
