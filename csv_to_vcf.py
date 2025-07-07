import csv
import os
import re
import gzip
from datetime import datetime

# === Ustawienia wejściowe ===
input_csv = "kontakty_final.csv"

# === Zapytaj użytkownika o wersję VCF ===
vcard_version = input("Wybierz wersję VCARD (2.1 lub 3.0): ").strip()
if vcard_version not in ["2.1", "3.0"]:
    print("\n❌ Błędna wersja. Dozwolone: 2.1 lub 3.0")
    exit(1)

# === Zapytaj użytkownika o tryb eksportu ===
export_mode = input("Wybierz tryb eksportu [single, multi, gzip]: ").strip()
if export_mode not in ["single", "multi", "gzip"]:
    print("\n❌ Błędny tryb eksportu. Dozwolone: single, multi, gzip")
    exit(1)

# === Nazwa folderu wynikowego ===
out_dir = f"export_vcf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(out_dir, exist_ok=True)

# === Zmienna pomocnicza do zapisu zbiorczego ===
if export_mode == "single" or export_mode == "gzip":
    vcf_entries = []


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip() or "kontakt_bez_nazwy"


def create_vcard(data, version):
    lines = ["BEGIN:VCARD", f"VERSION:{version}"]

    name = data.get("name", "Brak nazwy")
    lines.append(f"FN:{name}")

    for phone in data.get("phones", []):
        if version == "2.1":
            lines.append(f"TEL;CELL:{phone}")
        else:
            lines.append(f"TEL;TYPE=CELL:{phone}")

    if data.get("note"):
        lines.append(f"NOTE:{data['note']}")
    if data.get("org"):
        lines.append(f"ORG:{data['org']}")
    if data.get("title"):
        lines.append(f"TITLE:{data['title']}")
    if data.get("adr"):
        lines.append(f"ADR:;;;;{data['adr']};;;")

    lines.append("END:VCARD")
    return "\n".join(lines)


# === Główna funkcja ===
def csv_to_vcf(csv_path):
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)

        field_map = {
            "name": 0,
            "phones": [1, 2, 3, 4, 5],
            "note": headers.index("Notatka") if "Notatka" in headers else None,
            "org": headers.index("ORG") if "ORG" in headers else None,
            "title": headers.index("TITLE") if "TITLE" in headers else None,
            "adr": headers.index("ADR") if "ADR" in headers else None,
        }

        for row_num, row in enumerate(reader, start=2):
            name = row[field_map["name"]].strip()
            phones = [row[i].strip() for i in field_map["phones"] if i < len(row) and row[i].strip()]
            note = row[field_map["note"]].strip() if field_map["note"] is not None and len(row) > field_map["note"] else ""
            org = row[field_map["org"]].strip() if field_map["org"] is not None and len(row) > field_map["org"] else ""
            title = row[field_map["title"]].strip() if field_map["title"] is not None and len(row) > field_map["title"] else ""
            adr = row[field_map["adr"]].strip() if field_map["adr"] is not None and len(row) > field_map["adr"] else ""

            data = {
                "name": name,
                "phones": phones,
                "note": note,
                "org": org,
                "title": title,
                "adr": adr
            }

            print(f"[DEBUG] Kontakt #{row_num - 1}")
            print(f"  Imię i nazwisko: {name}")
            print(f"  Numery telefonów: {phones}")
            print(f"  ORG: {org} | TITLE: {title} | ADR: {adr}")
            print(f"  Notatka: {note}\n")

            vcard_text = create_vcard(data, vcard_version)

            if export_mode == "multi":
                filename = sanitize_filename(name) + ".vcf"
                with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as out:
                    out.write(vcard_text)
            else:
                vcf_entries.append(vcard_text)

        # Zapis trybu single lub gzip
        if export_mode == "single":
            with open(os.path.join(out_dir, "kontakty_export.vcf"), "w", encoding="utf-8") as f:
                f.write("\n".join(vcf_entries))
        elif export_mode == "gzip":
            with gzip.open(os.path.join(out_dir, "kontakty_export.vcf.gz"), "wt", encoding="utf-8") as f:
                f.write("\n".join(vcf_entries))

        print(f"\n✅ Eksport zakończony. Pliki zapisane w katalogu: {out_dir}")


# === Start ===
csv_to_vcf(input_csv)
