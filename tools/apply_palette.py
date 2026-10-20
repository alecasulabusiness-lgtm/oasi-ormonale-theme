"""Porta gli schemi colore e gli angoli del tema Horizon sulla palette della guida (docs/brand-identity.md).

Serve alle pagine native (prodotto, carrello, blog, ricerca): le sezioni oasi-* usano direttamente
assets/oasi-brand.css. Rilanciabile: riscrive sempre gli stessi valori.

Uso, dalla radice della repo: python3 tools/apply_palette.py
"""
import json
import re
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "config" / "settings_data.json"
BURG, WINE, ROSE, BLUSH, CREAM, WHITE = "#4b1c22", "#65333c", "#db9aa8", "#ebccd2", "#f6ede4", "#ffffff"
CLEAR = "rgba(0,0,0,0)"


def light(bg, secondary_bg):
    """Fondo chiaro, testo borgogna."""
    return {
        "background": bg, "foreground_heading": BURG, "foreground": WINE, "primary": BURG, "primary_hover": WINE,
        "border": "#4b1c2229", "shadow": BURG,
        "primary_button_background": BURG, "primary_button_text": CREAM, "primary_button_border": BURG,
        "primary_button_hover_background": WINE, "primary_button_hover_text": CREAM, "primary_button_hover_border": WINE,
        "secondary_button_background": secondary_bg, "secondary_button_text": BURG, "secondary_button_border": secondary_bg,
        "secondary_button_hover_background": ROSE, "secondary_button_hover_text": BURG, "secondary_button_hover_border": ROSE,
        "input_background": WHITE, "input_text_color": BURG, "input_border_color": "#4b1c2240", "input_hover_background": WHITE,
        "variant_background_color": WHITE, "variant_text_color": BURG, "variant_border_color": "#4b1c2233",
        "variant_hover_background_color": BLUSH, "variant_hover_text_color": BURG, "variant_hover_border_color": ROSE,
        "selected_variant_background_color": BURG, "selected_variant_text_color": CREAM, "selected_variant_border_color": BURG,
        "selected_variant_hover_background_color": WINE, "selected_variant_hover_text_color": CREAM, "selected_variant_hover_border_color": WINE,
    }


def dark(bg):
    """Fondo borgogna o trasparente su immagine, testo crema."""
    return {
        "background": bg, "foreground_heading": CREAM, "foreground": BLUSH, "primary": CREAM, "primary_hover": BLUSH,
        "border": "#f6ede440", "shadow": BURG,
        "primary_button_background": CREAM, "primary_button_text": BURG, "primary_button_border": CREAM,
        "primary_button_hover_background": BLUSH, "primary_button_hover_text": BURG, "primary_button_hover_border": BLUSH,
        "secondary_button_background": WINE, "secondary_button_text": CREAM, "secondary_button_border": WINE,
        "secondary_button_hover_background": ROSE, "secondary_button_hover_text": BURG, "secondary_button_hover_border": ROSE,
        "input_background": WINE, "input_text_color": CREAM, "input_border_color": "#f6ede440", "input_hover_background": WINE,
        "variant_background_color": WINE, "variant_text_color": CREAM, "variant_border_color": "#f6ede433",
        "variant_hover_background_color": BURG, "variant_hover_text_color": CREAM, "variant_hover_border_color": ROSE,
        "selected_variant_background_color": CREAM, "selected_variant_text_color": BURG, "selected_variant_border_color": CREAM,
        "selected_variant_hover_background_color": BLUSH, "selected_variant_hover_text_color": BURG, "selected_variant_hover_border_color": BLUSH,
    }


SCHEMES = {
    "scheme-1": light(CREAM, BLUSH),
    "scheme-2": light(WHITE, BLUSH),
    "scheme-3": light(BLUSH, CREAM),
    "scheme-4": light(ROSE, CREAM),
    "scheme-5": dark(BURG),
    "scheme-6": dark(CLEAR),
    "scheme-58084d4c-a86e-4d0a-855e-a0966e5043f7": light(CLEAR, BLUSH),
}
CURRENT = {
    "button_border_radius_primary": 100,
    "button_border_radius_secondary": 100,
    "inputs_border_radius": 16,
    "card_corner_radius": 16,
    "product_corner_radius": 20,
}


def main():
    raw = PATH.read_text(encoding="utf-8")
    m = re.match(r"^(\s*/\*.*?\*/\s*)", raw, re.S)
    header = m.group(1) if m else ""
    data = json.loads(raw[len(header):])
    cur = data["current"]
    for sid, values in SCHEMES.items():
        assert sid in cur["color_schemes"], f"schema mancante: {sid}"
        settings = cur["color_schemes"][sid]["settings"]
        assert set(values) == set(settings), f"{sid}: chiavi diverse da quelle del tema: {set(values) ^ set(settings)}"
        cur["color_schemes"][sid]["settings"] = values
    for key, value in CURRENT.items():
        assert key in cur, f"impostazione mancante: {key}"
        cur[key] = value
    PATH.write_text(header + json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"schemi aggiornati: {len(SCHEMES)}; impostazioni: {', '.join(f'{k}={v}' for k, v in CURRENT.items())}")


if __name__ == "__main__":
    main()
