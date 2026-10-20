"""Costruisce i template nativi di home, Chi siamo e Lavora con noi,
più i gruppi header e footer, partendo dai testi dei template GemPages originali.

I testi si leggono dalla versione del tema salvata nel ramo `main` (copia del tema live al 20/10/2026),
quindi lo script si può rilanciare in qualsiasi momento con lo stesso risultato.
Ogni paragrafo che si prende per posizione ha un'asserzione: se il testo originale non è quello atteso
lo script si ferma invece di scrivere una pagina sbagliata.

Correzioni ai testi originali (refusi e maiuscole), tutte elencate in CORREZIONI:
vedi docs/migrazione-pagine.md.

Uso, dalla radice della repo: python3 tools/build_templates.py
"""
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_BRANCH = "main"
WA = "https://wa.me/+393296912328"
PROTOCOLLO = "/pages/oasi-ormonale"
HEADER_NOTE = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""

CORREZIONI = []


# ---------- lettura dei template originali ----------
def orig(name):
    out = subprocess.run(
        ["git", "show", f"{BASE_BRANCH}:templates/{name}.json"],
        capture_output=True, text=True, cwd=ROOT, check=True,
    ).stdout
    out = re.sub(r"^\s*/\*.*?\*/", "", out, count=1, flags=re.S)
    return json.loads(out)


class Tpl:
    """Accesso alle impostazioni di un template originale per sezione (suffisso dell'id) e chiave."""

    def __init__(self, name):
        self.data = orig(name)
        self.by_suffix = {sid[-8:]: sid for sid in self.data["order"]}

    def get(self, suffix, key):
        sid = self.by_suffix[suffix]
        value = self.data["sections"][sid]["settings"][key]
        return value

    def keys(self, suffix, prefix):
        sid = self.by_suffix[suffix]
        return [k for k in self.data["sections"][sid]["settings"] if k.startswith(prefix)]


# ---------- pulizia dei testi ----------
def _inline(htm):
    """Normalizza l'HTML in linea: tiene solo strong, em, u, a e br."""
    htm = htm.replace("\xa0", " ").replace("&nbsp;", " ")
    htm = re.sub(r"<(/?)b(\s[^>]*)?>", r"<\1strong>", htm)
    htm = re.sub(r"<(/?)i(\s[^>]*)?>", r"<\1em>", htm)
    htm = re.sub(r"<(strong|em|u)\s[^>]*>", r"<\1>", htm)
    htm = re.sub(r"<br\s*/?>", "<br>", htm)
    # tiene solo i tag ammessi (e i link con href)
    def keep(m):
        tag = m.group(0)
        name = re.match(r"</?([a-zA-Z0-9]+)", tag).group(1).lower()
        if name in ("strong", "em", "u", "br"):
            return tag
        if name == "a" and not tag.startswith("</"):
            href = re.search(r'href="([^"]+)"', tag)
            return f'<a href="{href.group(1)}">' if href else ""
        if name == "a":
            return tag
        if name in ("p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6") and tag.startswith("</"):
            return "\x00"  # fine paragrafo
        return ""
    htm = re.sub(r"</?[a-zA-Z][^>]*>", keep, htm)
    htm = re.sub(r"\s+(</(?:strong|em|u)>)", r"\1 ", htm)
    htm = re.sub(r"(<(?:strong|em|u)>)\s+", r" \1", htm)
    htm = re.sub(r"[ \t]+", " ", htm)
    return htm.strip()


def paras(htm):
    """Elenco dei paragrafi (HTML in linea). Un <br><br> separa i paragrafi, un <br> va a capo."""
    htm = _inline(htm)
    out = []
    for chunk in htm.split("\x00"):
        for part in re.split(r"(?:<br>\s*){2,}", chunk):
            part = re.sub(r"^(?:\s|<br>)+|(?:\s|<br>)+$", "", part)
            part = re.sub(r"\s*<br>\s*", "<br>", part).strip()
            part = re.sub(r"<(strong|em|u)>\s*</\1>", "", part)
            if part:
                out.append(part)
    return out


def rich(htm_or_paras):
    ps = htm_or_paras if isinstance(htm_or_paras, list) else paras(htm_or_paras)
    return "".join(f"<p>{p}</p>" for p in ps)


def plain(htm):
    htm = re.sub(r"<br\s*/?>", " ", htm.replace("\x00", " "))
    htm = re.sub(r"<[^>]+>", "", htm)
    return re.sub(r"\s+", " ", html.unescape(htm).replace("\xa0", " ")).strip()


def strip_end(text):
    return re.sub(r"[;.]\s*$", "", text.strip())


def cap(text):
    text = text.strip()
    return text[:1].upper() + text[1:] if text else text


def fix(text, old, new, where):
    if old in text:
        CORREZIONI.append((where, old, new))
        return text.replace(old, new)
    return text


def img(url):
    name = url.split("?")[0].rsplit("/", 1)[-1]
    return f"shopify://shop_images/{name}"


def expect(cond, msg):
    if not cond:
        raise SystemExit(f"ASSERZIONE FALLITA: {msg}")


# ---------- costruzione ----------
class Page:
    def __init__(self):
        self.sections = {}
        self.order = []

    def add(self, sid, type_, settings=None, blocks=None):
        settings = {k: v for k, v in (settings or {}).items() if v not in (None, "", [])}
        entry = {"type": type_, "settings": settings}
        if blocks:
            entry["blocks"] = {}
            entry["block_order"] = []
            for i, (btype, bsettings) in enumerate(blocks, 1):
                bid = f"{sid}_{i}"
                entry["blocks"][bid] = {
                    "type": btype,
                    "settings": {k: v for k, v in bsettings.items() if v not in (None, "")},
                }
                entry["block_order"].append(bid)
        self.sections[sid] = entry
        self.order.append(sid)

    def write(self, path):
        data = {"sections": self.sections, "order": self.order}
        Path(ROOT / path).write_text(HEADER_NOTE + json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_home():
    t = Tpl("index")
    p = Page()
    W = "home"

    # 1. hero
    intro_text = rich(paras(t.get("62439889", "ggMfso5R6pk_text")))
    intro_text = fix(intro_text, "IL protocollo", "Il protocollo", W)
    p.add("hero", "oasi-hero", {
        "eyebrow": "Il 1° Protocollo in Italia Specializzato nel Benessere Ormonale",
        "heading": plain(t.get("62374353", "ggEhDqGUFVQ_text")),
        "text": intro_text,
        "primary_label": "Scopri Oasi Ormonale",
        "primary_url": PROTOCOLLO,
        "secondary_label": "Come funziona",
        "secondary_url": "/#protocollo",
        "image": img(t.get("61981137", "ggtEPg21BZZ_srcSet_desktop_src")),
    })

    # 2. professioniste (chip)
    chips = [strip_end(plain(t.get("62177745", k))) for k in sorted(t.keys("62177745", "ggoNX3BMPKd_childItem_"))]
    expect(len(chips) == 5, "home: attese 5 professioniste")
    p.add("team_strip", "oasi-chips", {"label": "Professioniste del Benessere Ormonale", "padding_top": 72, "padding_bottom": 24},
          [("chip", {"text": c}) for c in chips])

    # 3. il metodo
    lines = re.split(r"<br\s*/?>", t.get("61915601", "ggA2aMIWSMr_text"))
    expect(len(lines) == 2, "home: il kicker doveva avere due righe")
    long_text = paras(t.get("61915601", "ggdj1I5UnSw_text"))
    expect(len(long_text) == 6, f"home: attesi 6 paragrafi nel testo del metodo, trovati {len(long_text)}")
    expect(long_text[0].startswith("Perché alcune donne"), "home: primo paragrafo del metodo")
    expect(long_text[5].startswith("Riducono"), "home: ultimo paragrafo del metodo")
    side = fix(long_text[5], "alimenti da dimenitacare", "alimenti da dimenticare", W)
    side = fix(side, "l’alimentazione schemi", "l’alimentazione a schemi", W)
    p.add("method", "oasi-method", {
        "label": "Il metodo",
        "heading": strip_end(plain(lines[0])) + ".",
        "heading_fade": plain(lines[1]),
        "anchor": "metodo",
        "image": img(t.get("61915601", "gga0mPstFYE_srcSet_desktop_src")),
        "card_title": plain(long_text[0]),
        "card_intro": plain(long_text[1]) + " " + plain(long_text[2]) + " I tuoi ormoni decidono:",
        "side_label": "Cosa fanno gli approcci tradizionali",
        "side_text": plain(side),
        "side_centre": plain(t.get("61915601", "ggqyqK4Co5B_text")),
        "button_label": "Scopri Oasi Ormonale",
        "button_url": PROTOCOLLO,
    }, [("chip", {"text": c}) for c in (
        "se ingrassi o dimagrisci", "se ti senti energica o spossata", "se dormi bene o male", "se ti gonfi o ti senti leggera")])
    expect("se ingrassi o dimagrisci" in plain(long_text[3]), "home: le frasi dei chip devono stare nel testo originale")

    # 4. approccio (split bianco, numerato)
    ap = paras(t.get("61981137", "ggqDNFkBFwu_text"))
    expect(len(ap) == 9, f"home: attesi 9 paragrafi nell'approccio, trovati {len(ap)}")
    expect(plain(ap[0]).startswith("Basta schemi"), "home: apertura dell'approccio")
    expect(plain(ap[7]).startswith("Mettiamo TE"), "home: chiusura dell'approccio")
    p.add("approach", "oasi-split", {
        "tone": "white",
        "image": img(t.get("62439889", "ggnj68vZxPR_srcSet_desktop_src")),
        "image_side": "left",
        "eyebrow": "Il nostro approccio",
        "heading": strip_end(plain(ap[0])) + ".",
        "body": rich([ap[1]]),
        "list_style": "numbered",
        "outro": rich(["<strong>" + ap[7] + "</strong> " + ap[8]]),
        "button_label": "Scopri Oasi Ormonale",
        "button_url": WA,
        "padding_top": 96, "padding_bottom": 96,
    }, [
        ("item", {"text": rich([ap[2] + "<br>" + ap[3]])}),
        ("item", {"text": rich([ap[4]])}),
        ("item", {"text": rich([ap[5]])}),
        ("item", {"text": rich([ap[6]])}),
    ])

    # 5. frase centrale (liberare le donne)
    p.add("statement", "oasi-statement", {
        "tone": "light",
        "kicker": plain(t.get("62505425", "ggdD9tO8yXN_text")),
        "heading_before": "Oasi Ormonale nasce per",
        "highlight": "liberare le donne",
        "heading_after": "dal “terrorismo nutrizionale”,",
        "text": "<p>fornendo un approccio</p>",
    }, [("pill", {"text": cap(w)}) for w in ("funzionante", "personalizzato", "sostenibile", "scientifico")])
    expect("funzionante" in plain(t.get("62505425", "ggDBxaTMnUi_text")), "home: aggettivi della frase centrale")

    # 6. protocollo (4 card)
    cards = []
    for tag, title_key, text_key in (
        ("Analisi", "gg_MAt1XZ3N_text", "ggg1KvgO37B_text"),
        ("Strategia", "gglO8b5Sw0I_text", "ggmKi9Oyn_a_text"),
        ("Supporto", "ggPw3Dk-tfr_text", "ggcACmhezra_text"),
        ("Risultati", "ggpIZt_vcYD_text", "ggN-DiLLQZR_text"),
    ):
        cards.append(("card", {"tag": tag, "title": cap(plain(t.get("62046673", title_key)).lower()), "text": rich(t.get("62046673", text_key))}))
    p.add("protocol", "oasi-cards", {
        "tone": "light", "card_style": "palette", "show_numbers": True, "show_shapes": True,
        "anchor": "protocollo",
        "label": "Il protocollo",
        "heading": plain(t.get("62046673", "ggQ-Q4gw1tK_text")),
        "intro": plain(t.get("62046673", "ggHj9Ne7-W6_text")),
        "padding_top": 40, "padding_bottom": 112,
    }, cards)

    # 7. le specialiste (sezione scura)
    sp = paras(t.get("62177745", "ggE-1PDtlQG_text"))
    expect(len(sp) == 3, f"home: attesi 3 paragrafi nel testo delle specialiste, trovati {len(sp)}")
    roles = [strip_end(plain(t.get("62177745", k))) for k in sorted(t.keys("62177745", "ggoNX3BMPKd_childItem_"))]
    p.add("specialists", "oasi-team", {
        "anchor": "specialiste",
        "label": "Le specialiste",
        "heading": "Le specialiste che ti seguiranno?",
        "lead": "<p>Non solo figure esperte, ma donne che hanno già affrontato il percorso prima di te e che comprendono perfettamente la tua situazione.</p>",
        "body": rich(sp),
        "button_label": "Conosci le professioniste",
        "button_url": WA,
    }, [("role", {"text": r}) for r in roles])
    expect("figure esperte" in plain(t.get("62112209", "ggpYqSEKPec_text")), "home: testo delle specialiste")

    # 8. video e storie
    p.add("stories", "oasi-videos", {
        "tone": "light",
        "label": "Le storie",
        "heading": plain(t.get("62243281", "gg8x7TtjFG3_text")),
        "heading_fade": plain(t.get("62243281", "ggGwjzGo_Lq_text")),
        "intro": plain(t.get("62243281", "ggODEHFoO4X_text")),
        "padding_top": 112, "padding_bottom": 96,
    }, VIDEOS)

    # 9. garanzia (split morbido, immagine a destra, elenco con spunta)
    g = paras(t.get("62308817", "ggnAup0ONH4_text"))
    expect(len(g) == 8, f"home: attesi 8 paragrafi nella garanzia, trovati {len(g)}")
    expect(g[0].startswith("Il tuo percorso") and g[7].startswith("Perché, chi"), "home: estremi del testo della garanzia")
    p.add("guarantee", "oasi-split", {
        "tone": "soft",
        "image": img(t.get("62308817", "ggP9DOPBV3F_srcSet_desktop_src")),
        "image_side": "right",
        "image_badge": "100% soddisfatta o rimborsata",
        "eyebrow": "La garanzia",
        "kicker": plain(t.get("62308817", "ggvB7lfWRxy_text")),
        "heading": plain(t.get("62308817", "gg5Jw9Ktryc_text")),
        "subheading": plain(t.get("62308817", "gg18MC6qzjI_text")),
        "body": rich([g[0], g[1]]),
        "list_style": "check",
        "outro": rich([g[6] + " " + g[7]]),
        "outro_style": "text",
        "button_label": "Scopri Oasi Ormonale",
        "button_url": WA,
    }, [
        ("item", {"text": rich([g[2]])}),
        ("item", {"text": rich([g[3] + " " + g[5]])}),
        ("item", {"text": rich([g[4]])}),
    ])
    p.write("templates/index.json")


VIDEOS = []


def collect_videos():
    """Quattro video YouTube con le loro frasi, nello stesso ordine del sito attuale."""
    t = Tpl("index")
    sid = "62243281"
    ytk = [k for k in t.keys(sid, "gg") if k.endswith("_youtubeUrl")]
    texts = [k for k in t.keys(sid, "gg") if k.endswith("_text") and k in (
        "ggqLQdDa0BL_text", "gg-tqiqqHEB_text", "ggZlvEPEFnb_text", "ggcPfnz8zxQ_text")]
    expect(len(ytk) == 4 and len(texts) == 4, "home: attesi 4 video con 4 frasi")
    quotes = {
        "ggqLQdDa0BL_text": ("Da stanca e senza energie a rinata", "Monica ce l'ha fatta!"),
        "gg-tqiqqHEB_text": ("Meno 6 kg e di nuovo taglia 42", "Cristina svela perché Oasi non è una dieta qualunque!"),
        "ggZlvEPEFnb_text": ("Mi hanno sempre detto che all’endometriosi non c’è soluzione. Oasi mi ha aiutata!", ""),
        "ggcPfnz8zxQ_text": ("-7 kg, -14 cm in vita e -13 cm sui fianchi, senza patire la fame", "Il percorso di Antonella"),
    }
    for yk, tk in zip(ytk, texts):
        original = plain(t.get(sid, tk))
        quote, who = quotes[tk]
        expect(quote.split(",")[0][:18].lower() in original.lower(), f"video: la frase '{quote[:30]}' non è nel testo originale")
        VIDEOS.append(("video", {"video_url": t.get(sid, yk), "quote": quote, "who": who}))


def build_chi_siamo():
    t = Tpl("page.gp-template-586581486656815819")
    p = Page()
    W = "chi siamo"
    heading = fix(plain(t.get("41291723", "ggEhDqGUFVQ_text")), "La Prima realtà in italia", "La prima realtà in Italia", W)
    p.add("hero", "oasi-page-hero", {
        "eyebrow": "Chi siamo", "heading": heading, "text": rich(t.get("41291723", "ggxmisnvFl4_text")),
    })

    p.add("intro", "oasi-split", {
        "tone": "light",
        "image": img(t.get("40701899", "ggnj68vZxPR_srcSet_desktop_src")), "image_side": "left",
        "heading": "Oasi Ormonale",
        "body": rich(t.get("40701899", "ggMfso5R6pk_text")),
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    })
    expect(plain(t.get("40701899", "ggMfso5R6pk_text")).startswith("Nasce da una necessità concreta"), "chi siamo: apertura del testo intro")

    who = paras(t.get("40832971", "ggdj1I5UnSw_text"))
    p.add("who", "oasi-split", {
        "tone": "dark",
        "image": img(t.get("40832971", "gga0mPstFYE_srcSet_desktop_src")), "image_side": "right",
        "eyebrow": cap(plain(t.get("40832971", "ggqyqK4Co5B_text")).rstrip("?")),
        "heading": plain(t.get("40832971", "ggA2aMIWSMr_text")),
        "body": rich(who),
        "button_label": "Scopri Oasi Ormonale", "button_url": WA,
    })

    p.add("team_title", "oasi-statement", {
        "tone": "light",
        "kicker": cap(plain(t.get("40767435", "ggdD9tO8yXN_text")).lower()),
        "heading_before": plain(t.get("40767435", "ggAHouq8Z7f_text")),
        "padding_top": 96, "padding_bottom": 24,
    })

    items = [strip_end(plain(t.get("40898507", k))) for k in sorted(t.keys("40898507", "ggoNX3BMPKd_childItem_"))]
    expect(len(items) == 3, "chi siamo: attesi 3 profili del team")
    p.add("team", "oasi-split", {
        "tone": "white",
        "body": rich(t.get("40898507", "ggqDNFkBFwu_text")),
        "list_style": "check",
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    }, [("item", {"text": rich([i])}) for i in items])

    stat = plain(t.get("41029579", "ggKu4PReshF_text"))
    stat = fix(stat, "BENESSRE", "BENESSERE", W)
    p.add("stat", "oasi-statement", {
        "tone": "dark",
        "heading_before": cap(stat.lower().replace("oasi ormonale", "Oasi Ormonale")),
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    })

    p.add("stories", "oasi-videos", {
        "tone": "light", "label": "Le storie",
        "heading": plain(t.get("41160651", "ggpwkNE3zi4_text")),
        "heading_fade": plain(t.get("41160651", "ggemhsXZD8S_text")),
        "intro": plain(t.get("41160651", "ggEmo0sKGz__text")),
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    }, VIDEOS)

    p.add("plan", "oasi-split", {
        "tone": "soft",
        "kicker": plain(t.get("41226187", "ggvB7lfWRxy_text")),
        "heading": cap(plain(t.get("41226187", "gg5Jw9Ktryc_text"))).replace("oasi ormonale", "Oasi Ormonale"),
        "body": rich(t.get("41226187", "ggnAup0ONH4_text")),
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    })

    p.add("future", "oasi-split", {
        "tone": "white",
        "eyebrow": cap(plain(t.get("82108867", "ggY4knyK01F_text"))),
        "heading": plain(t.get("82108867", "ggmHj8KkKOQ_text")),
        "body": rich(t.get("82108867", "ggY66W3N5SE_text")),
        "button_label": "Scopri Oasi Ormonale", "button_url": PROTOCOLLO,
    })
    p.write("templates/page.oasi-chi-siamo.json")


def build_lavora():
    t = Tpl("page.gp-template-586694286104331137")
    p = Page()
    W = "lavora con noi"
    ANCHOR = "/pages/lavora-con-noi#posizioni-aperte"
    p.add("hero", "oasi-page-hero", {
        "eyebrow": "Lavora con noi",
        "heading": cap(plain(t.get("22230401", "ggEhDqGUFVQ_text"))),
        "text": rich(t.get("22230401", "ggxmisnvFl4_text")),
        "image": img(t.get("22230401", "ggvzVrofcz-_background_desktop_image_src")),
    })
    p.add("intro", "oasi-split", {
        "tone": "light",
        "image": img(t.get("21837185", "ggnj68vZxPR_srcSet_desktop_src")), "image_side": "left",
        "eyebrow": "La missione",
        "body": rich(t.get("21837185", "ggMfso5R6pk_text")),
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    })

    # posizioni aperte: team clinico, poi marketing e vendite (queste ultime stanno nelle impostazioni GemPages ma il sito attuale non le stampa)
    pos = [
        ("ggqWGAkCyM5_text", "ggGG3S9Or58_text", "https://oasiormonale.typeform.com/medici"),
        ("ggc4jHEXXpL_text", "ggLa3IoypIK_text", "https://oasiormonale.typeform.com/to/ixHaHSYX"),
        ("gg65dtbSsMN_text", "ggOSilkE30e_text", "https://oasiormonale.typeform.com/to/gp3Pbk6b"),
        ("ggPGcggxcG0_text", "ggkVnFmjWJf_text", "https://oasiormonale.typeform.com/medici"),
    ]
    cards = []
    for tk, dk, url in pos:
        parts = [plain(x) for x in re.split(r"<br\s*/?>", t.get("21771649", tk))]
        expect(len(parts) == 2 and parts[0].upper() == "TEAM", f"lavora: formato inatteso del ruolo {parts}")
        body = t.get("21771649", dk)
        if parts[1].lower() == "fitness trainer":
            body = fix(body, "protocolli nutrizionali personalizzati", "protocolli di allenamento personalizzati", W + " (Fitness trainer)")
        cards.append(("card", {"tag": cap(parts[0].lower()), "title": cap(parts[1].lower()), "text": rich(body),
                               "button_label": "Candidati ora", "button_url": url}))
    p.add("positions", "oasi-cards", {
        "tone": "light", "card_style": "palette", "show_numbers": True, "show_shapes": True,
        "anchor": "posizioni-aperte",
        "heading": cap(plain(t.get("21771649", "ggqyqK4Co5B_text")).lower()),
        "intro": plain(t.get("21771649", "ggA2aMIWSMr_text")),
        "padding_top": 96, "padding_bottom": 56,
    }, cards)

    # Link di candidatura: non stanno nel template originale. Sono i form Typeform di Oasi Ormonale scelti dal titolo.
    # Social media manager non ha un form dedicato: senza link il pulsante non compare.
    mkt = [
        ("gg2NEveP-sU_text", "gg_u6iz2DC7_text", "Vendite", "https://oasiormonale.typeform.com/to/EN8ghdhI"),
        ("ggplv5Q0Tg7_text", "gg5_Fbh7Ejc_text", "Marketing", "https://oasiormonale.typeform.com/to/g19z7KgH"),
        ("ggcXIX59jXv_text", "ggOhBO2VXod_text", "Comunicazione", ""),
        ("ggHCIRPvH0q_text", "ggakGEFqjIO_text", "Marketing", "https://oasiormonale.typeform.com/to/cS695Y16"),
    ]
    mkt_cards = []
    for tk, dk, tag, url in mkt:
        title = " ".join(plain(x) for x in re.split(r"<br\s*/?>", t.get("21771649", tk)))
        mkt_cards.append(("card", {"tag": tag, "title": cap(title.lower()), "text": rich(t.get("21771649", dk)),
                                   "button_label": "Candidati ora", "button_url": url}))
    p.add("positions_marketing", "oasi-cards", {
        "tone": "light", "card_style": "palette", "show_numbers": True, "show_shapes": True,
        "heading": cap(plain(t.get("21771649", "gg150PlM363_text")).lower()).replace(" & ", " e "),
        "padding_top": 24, "padding_bottom": 112,
    }, mkt_cards)

    cultura = paras(t.get("21968257", "ggqDNFkBFwu_text"))
    cult_items = [rich(t.get("21968257", k)) for k in sorted(t.keys("21968257", "ggoNX3BMPKd_childItem_"))]
    expect(len(cult_items) == 5, "lavora: attese 5 voci di cultura")
    p.add("culture", "oasi-split", {
        "tone": "dark",
        "image": img(t.get("21968257", "ggtEPg21BZZ_srcSet_desktop_src")), "image_side": "right",
        "heading": cap(plain(t.get("21968257", "ggPN2c9CWLG_text"))),
        "body": rich(cultura),
        "list_style": "numbered",
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    }, [("item", {"text": c}) for c in cult_items])

    p.add("crusade", "oasi-split", {
        "tone": "white",
        "image": img(t.get("29722081", "ggwgN3zbB7o_srcSet_desktop_src")), "image_side": "left",
        "heading": cap(plain(t.get("29722081", "ggusg5IMsNm_text"))),
        "body": rich(t.get("29722081", "ggOuHQXXHPR_text")),
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    })

    p.add("career", "oasi-split", {
        "tone": "soft",
        "image": img(t.get("87728279", "ggXBlh7Hzaq_srcSet_desktop_src")), "image_side": "right",
        "eyebrow": "La crescita",
        "heading": fix(cap(plain(t.get("87728279", "ggrdp2hqFpy_text"))), "Ogni talento? un piano", "Ogni talento? Un piano", W),
        "heading_fade": fix(fix(plain(t.get("87728279", "ggpRJxnUcuC_text")), "A cui NON", "a cui non", W), "A cui non", "a cui non", W),
        "lead": rich(t.get("87728279", "ggH3QmnXyaJ_text")),
        "body": rich(t.get("87728279", "ggIrPSbOMlf_text")),
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    })

    vals = []
    for tk, dk in (("ggD8x-VdWf7_childItem_0", "ggnAup0ONH4_text"), ("ggOweVQ-lrZ_childItem_0", "ggr6LW0_7IX_text"),
                   ("ggyKivNWRXm_childItem_0", "gg5-wDtynjN_text"), ("ggNAmwZZUYY_childItem_0", "ggxTPAcKJwy_text"),
                   ("ggSyH4pfFI2_childItem_0", "gg7653PJCdE_text")):
        vals.append(("item", {"title": cap(plain(t.get("14074310", tk)).lower()), "text": rich(t.get("14074310", dk))}))
    p.add("values", "oasi-split", {
        "tone": "white",
        "image": img(t.get("14074310", "ggrZpm5To5k_srcSet_desktop_src")), "image_side": "left",
        "heading": "I nostri valori",
        "list_style": "numbered",
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    }, vals)

    p.add("final", "oasi-split", {
        "tone": "dark",
        "image": img(t.get("09370866", "ggZQsixUwgW_srcSet_desktop_src")), "image_side": "right",
        "heading": cap(plain(t.get("09370866", "ggnA99LLetJ_text"))),
        "body": rich(t.get("09370866", "ggMfXtUfp5w_text")),
        "button_label": "Scopri le posizioni aperte", "button_url": ANCHOR,
    })
    p.write("templates/page.oasi-lavora-con-noi.json")


def build_groups():
    t = Tpl("index")
    legal = plain(t.get("461672-1", "ggypewUmpks_text_547674795"))
    expect(legal.startswith("I risultati conseguibili") and legal.endswith("mera proiezione indicativa."), "footer: testo legale")
    copyright_ = plain(t.get("461672-1", "ggcF30HUJp__text"))

    header = {
        "type": "header",
        "name": "Header",
        "sections": {
            "oasi_header": {
                "type": "oasi-header",
                "blocks": {
                    "link_1": {"type": "link", "settings": {"label": "Chi siamo", "url": "/pages/chi-siamo"}},
                    "link_2": {"type": "link", "settings": {"label": "Lavora con noi", "url": "/pages/lavora-con-noi"}},
                },
                "block_order": ["link_1", "link_2"],
                "settings": {"cta_label": "Scopri Oasi Ormonale", "cta_url": PROTOCOLLO},
            }
        },
        "order": ["oasi_header"],
    }
    footer = {
        "type": "footer",
        "name": "Footer",
        "sections": {
            "oasi_footer": {
                "type": "oasi-footer",
                "blocks": {
                    "col_1": {"type": "column", "settings": {
                        "title": "Navigazione rapida",
                        "label_1": "Home", "url_1": "/",
                        "label_2": "Chi Siamo", "url_2": "/pages/chi-siamo"}},
                    "col_2": {"type": "column", "settings": {
                        "title": "Risorse",
                        "label_1": "Lavora con noi", "url_1": "/pages/lavora-con-noi",
                        "label_2": "Contattaci via email", "url_2": "mailto:ufficio@oasiormonale.com?subject=Richiesta%20di%20Contatto"}},
                    "col_3": {"type": "column", "settings": {
                        "title": "Legale",
                        "label_1": "Privacy Policy", "url_1": "https://www.iubenda.com/privacy-policy/12323298",
                        "label_2": "Cookie Policy", "url_2": "https://www.iubenda.com/privacy-policy/12323298/cookie-policy"}},
                },
                "block_order": ["col_1", "col_2", "col_3"],
                "settings": {
                    "tagline": "Il 1° Protocollo in Italia Specializzato nel Benessere Ormonale",
                    "legal": legal,
                    "copyright": copyright_,
                },
            }
        },
        "order": ["oasi_footer"],
    }
    for name, data in (("header-group", header), ("footer-group", footer)):
        (ROOT / "sections" / f"{name}.json").write_text(
            HEADER_NOTE + json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    collect_videos()
    build_home()
    build_chi_siamo()
    build_lavora()
    build_groups()
    print("template scritti: index, chi-siamo, lavora-con-noi, header-group, footer-group")
    print("\nCorrezioni ai testi originali:")
    for where, old, new in CORREZIONI:
        print(f"  [{where}] '{old}' -> '{new}'")


if __name__ == "__main__":
    main()
