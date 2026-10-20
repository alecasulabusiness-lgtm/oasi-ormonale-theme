"""Controlla che i template e i gruppi usino solo impostazioni, blocchi e valori previsti dagli schemi delle sezioni oasi-*.

Uso, dalla radice della repo: python3 tools/validate_templates.py
Esce con codice 1 se trova anche un solo problema.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = [
    "templates/index.json",
    "templates/page.gp-template-586581486656815819.json",
    "templates/page.gp-template-586691149922567041.json",
    "templates/page.gp-template-586694286104331137.json",
    "sections/header-group.json",
    "sections/footer-group.json",
]


def schema_of(section_type):
    text = (ROOT / "sections" / f"{section_type}.liquid").read_text(encoding="utf-8")
    m = re.search(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", text, re.S)
    return json.loads(m.group(1))


def load(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", text, count=1, flags=re.S))


def check_value(setting, value, where, errors):
    t = setting["type"]
    if t in ("header", "paragraph"):
        errors.append(f"{where}: '{setting.get('id')}' non è un'impostazione")
    elif t == "select":
        allowed = [o["value"] for o in setting["options"]]
        if value not in allowed:
            errors.append(f"{where}: valore '{value}' non ammesso per {setting['id']} {allowed}")
    elif t == "range":
        lo, hi, step = setting["min"], setting["max"], setting.get("step", 1)
        if not (isinstance(value, (int, float)) and lo <= value <= hi and (value - lo) % step == 0):
            errors.append(f"{where}: {setting['id']}={value} fuori da {lo}-{hi} passo {step}")
    elif t == "checkbox":
        if not isinstance(value, bool):
            errors.append(f"{where}: {setting['id']} deve essere vero o falso")
    elif t == "richtext":
        if not (isinstance(value, str) and value.startswith("<p>") and value.endswith("</p>")):
            errors.append(f"{where}: {setting['id']} (richtext) deve essere racchiuso in <p>…</p>")
        elif re.search(r"<(?!/?(?:p|br|strong|em|u|a|ul|ol|li)\b)[a-z]", value):
            errors.append(f"{where}: {setting['id']} contiene tag non ammessi nel richtext")
    elif t == "image_picker":
        if not (isinstance(value, str) and value.startswith("shopify://shop_images/")):
            errors.append(f"{where}: {setting['id']} deve iniziare con shopify://shop_images/")
    elif t in ("text", "textarea", "url"):
        if not isinstance(value, str):
            errors.append(f"{where}: {setting['id']} deve essere testo")
        elif t == "text" and "\n" in value:
            errors.append(f"{where}: {setting['id']} (text) non può andare a capo")


def main():
    errors, counts = [], {}
    for path in TEMPLATES:
        data = load(path)
        for sid, sec in data["sections"].items():
            where = f"{path} [{sid}]"
            schema = schema_of(sec["type"])
            settings = {s["id"]: s for s in schema.get("settings", []) if "id" in s}
            for key, value in sec.get("settings", {}).items():
                if key not in settings:
                    errors.append(f"{where}: impostazione sconosciuta '{key}'")
                else:
                    check_value(settings[key], value, f"{where}.{key}", errors)
            blocks = sec.get("blocks", {})
            order = sec.get("block_order", [])
            if sorted(order) != sorted(blocks):
                errors.append(f"{where}: block_order non coincide con i blocchi")
            max_blocks = schema.get("max_blocks")
            if max_blocks and len(blocks) > max_blocks:
                errors.append(f"{where}: {len(blocks)} blocchi, massimo {max_blocks}")
            btypes = {b["type"]: b for b in schema.get("blocks", [])}
            for bid, block in blocks.items():
                if block["type"] not in btypes:
                    errors.append(f"{where}.{bid}: tipo di blocco sconosciuto '{block['type']}'")
                    continue
                bset = {s["id"]: s for s in btypes[block["type"]].get("settings", []) if "id" in s}
                for key, value in block.get("settings", {}).items():
                    if key not in bset:
                        errors.append(f"{where}.{bid}: impostazione sconosciuta '{key}'")
                    else:
                        check_value(bset[key], value, f"{where}.{bid}.{key}", errors)
            counts[sec["type"]] = counts.get(sec["type"], 0) + 1
        for sid in data.get("order", []):
            if sid not in data["sections"]:
                errors.append(f"{path}: '{sid}' è nell'ordine ma non nelle sezioni")
    print("sezioni controllate:", json.dumps(counts, ensure_ascii=False))
    if errors:
        print(f"\n{len(errors)} problemi:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("nessun problema")


if __name__ == "__main__":
    main()
