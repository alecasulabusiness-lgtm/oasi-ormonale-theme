"""Isola il logo Oasi Ormonale (pittogramma + logotipo) dalla pagina 8 delle guidelines.

La pagina 8 è il logo bianco su fondo borgogna, in vettoriale. Lo script tiene
i tracciati bianchi che fanno parte del logo, scarta il fondo e la riga di piè
di pagina, e scrive le versioni pulite in <cartella_uscita>.

Uso: python3 -I extract_logo.py <page8.svg> <cartella_uscita>
"""
import re
import sys
from pathlib import Path

WHITE = 'fill="rgb(100%, 100%, 100%)"'
PATH_RE = re.compile(r"<path\b([^>]*?)/>", re.S)
NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def bbox(d: str):
    nums = [float(n) for n in NUM_RE.findall(d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    svg = src.read_text(encoding="utf-8")

    shapes = []
    for m in PATH_RE.finditer(svg):
        attrs = m.group(1)
        if WHITE not in attrs:
            continue
        d = re.search(r'\bd="([^"]+)"', attrs).group(1)
        x0, y0, x1, y1 = bbox(d)
        if (y1 - y0) < 1.5 or (x1 - x0) > 400:  # riga del piè di pagina
            continue
        shapes.append({"d": d, "box": (x0, y0, x1, y1)})

    mark = [s for s in shapes if (s["box"][3] - s["box"][1]) > 100]
    word = [s for s in shapes if s not in mark]
    print(f"tracciati: {len(shapes)} (pittogramma {len(mark)}, logotipo {len(word)})")
    if len(mark) != 1 or len(word) != 13:
        print("ATTENZIONE: conteggio inatteso, controllare a mano")

    def union(items):
        return (
            min(i["box"][0] for i in items), min(i["box"][1] for i in items),
            max(i["box"][2] for i in items), max(i["box"][3] for i in items),
        )

    def write(name, items, fill, pad=0.0):
        x0, y0, x1, y1 = union(items)
        x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
        w, h = x1 - x0, y1 - y0
        paths = "\n".join(
            f'  <path fill-rule="nonzero" d="{i["d"]}"/>' for i in items
        )
        text = (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="{x0:.3f} {y0:.3f} {w:.3f} {h:.3f}" '
            f'width="{w:.1f}" height="{h:.1f}" role="img" aria-label="Oasi Ormonale" '
            f'fill="{fill}">\n{paths}\n</svg>\n'
        )
        (out / name).write_text(text, encoding="utf-8")
        print(f"{name}: {w:.1f} x {h:.1f} (rapporto {w / h:.3f})")

    for tag, fill in (("white", "#ffffff"), ("black", "#000000")):
        write(f"oasi-logo-{tag}.svg", shapes, fill)
        write(f"oasi-pictogram-{tag}.svg", mark, fill)
        write(f"oasi-logotype-{tag}.svg", word, fill)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
