"""Sostituisce il vecchio logo dorato con il nuovo logo Oasi Ormonale in bianco e nero.

Header: logo nero (gli header GemPages stanno su fondo #D5D5D5).
Footer: logo bianco (i footer stanno su fondo nero).

Il vecchio logo è referenziato in due modi:
- URL completo nelle impostazioni dei template e nei default dello schema delle sezioni;
- nome file con il filtro `file_url` nell'HTML delle sezioni più vecchie.
Sostituire il nome file copre entrambi i casi. I nuovi file stanno nei File di Shopify
(Contenuti > File), vedi docs/brand-identity.md.

Lo script mette anche un testo alternativo ai tag <img> del logo, che prima avevano alt="".
È ripetibile: se non c'è più niente da cambiare non scrive nulla.

Uso, dalla radice della repo: python3 tools/apply_logo.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLACEMENTS = {
    # header
    "gempages_571219258252461280-2ef090f0-60c7-4ecc-8135-ae7a3885f3c9.png": "oasi-logo-black.svg",
    # footer
    "gempages_571219258252461280-d7ce851e-0c44-4d34-aaa9-34ddd775b51e.png": "oasi-logo-white.svg",
}
LOGO_MARKERS = (
    "oasi-logo-black.svg",
    "oasi-logo-white.svg",
    "ggbCLFKKpgP_srcSet_desktop_src",  # logo dell'header nella home
    "gglNKFWI2Va_srcSet_desktop_src_728777627",  # logo del footer globale
)
ALT = "Oasi Ormonale"
IMG_RE = re.compile(r"<img\b[^>]*>", re.S)


def add_alt(text: str) -> tuple[str, int]:
    count = 0

    def fix(m: re.Match) -> str:
        nonlocal count
        tag = m.group(0)
        if 'alt=""' in tag and any(k in tag for k in LOGO_MARKERS):
            count += 1
            return tag.replace('alt=""', f'alt="{ALT}"', 1)
        return tag

    return IMG_RE.sub(fix, text), count


def main() -> int:
    dry = "--dry-run" in sys.argv
    files_changed = replaced = alts = 0
    for folder, pattern in (("sections", "*.liquid"), ("snippets", "*.liquid"), ("templates", "*.json")):
        for path in sorted((ROOT / folder).glob(pattern)):
            text = path.read_text(encoding="utf-8")
            new = text
            for old, repl in REPLACEMENTS.items():
                n = new.count(old)
                if n:
                    new = new.replace(old, repl)
                    replaced += n
            if path.suffix == ".liquid":
                new, a = add_alt(new)
                alts += a
            if new != text:
                files_changed += 1
                if not dry:
                    path.write_text(new, encoding="utf-8")
    verb = "da modificare" if dry else "modificati"
    print(f"file {verb}: {files_changed} | riferimenti al logo sostituiti: {replaced} | testi alternativi aggiunti: {alts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
