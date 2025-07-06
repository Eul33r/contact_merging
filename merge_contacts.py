import csv
from collections import defaultdict

# Lista plików wejściowych CSV do scalenia
input_files = [
    "kontakty_osoby1.csv",
    "kontakty_osoby2.csv",
    # w razie potrzeby dodaj tu kolejne pliki do połączenia
]

output_file = "kontakty_final.csv"

# Mapa: numer telefonu → kontakt
phone_to_contact = {}
merged_contacts = {}

def normalize_number(number):
    return number.replace(" ", "").replace("-", "").strip()

def add_contact(name, phones, note):
    global phone_to_contact, merged_contacts

    # Znajdź, czy któryś z numerów już istnieje
    found_key = None
    for phone in phones:
        norm = normalize_number(phone)
        if norm in phone_to_contact:
            found_key = phone_to_contact[norm]
            break

    if found_key:
        # Uzupełniamy istniejący kontakt
        contact = merged_contacts[found_key]
        for phone in phones:
            norm = normalize_number(phone)
            if norm and norm not in contact["phones"]:
                contact["phones"].append(norm)
                phone_to_contact[norm] = found_key

        # Wybierz dłuższe imię
        if len(name.strip()) > len(contact["name"].strip()):
            contact["name"] = name.strip()

        # Dołącz notatkę
        if note:
            if contact["note"]:
                if note not in contact["note"]:
                    contact["note"] += "; " + note
            else:
                contact["note"] = note

    else:
        # Tworzymy nowy kontakt
        contact_id = len(merged_contacts)
        merged_contacts[contact_id] = {
            "name": name.strip(),
            "phones": [normalize_number(p) for p in phones if p.strip()],
            "note": note.strip() if note else ""
        }
        for phone in phones:
            norm = normalize_number(phone)
            if norm:
                phone_to_contact[norm] = contact_id


# Wczytanie danych z plików
for file in input_files:
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            name = row[0]
            phones = row[1:6]  # kolumny z numerami
            note = row[6] if len(row) > 6 else ""
            add_contact(name, phones, note)

# Zapis do pliku wynikowego
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Imię i nazwisko", "Numer 1", "Numer 2", "Numer 3", "Numer 4", "Numer 5", "Notatka"])

    for c in merged_contacts.values():
        row = [c["name"]] + c["phones"][:5]
        row += [""] * (5 - len(c["phones"]))  # uzupełnij puste kolumny
        row.append(c["note"])
        writer.writerow(row)

print(f"Zapisano scalone kontakty do pliku: {output_file}")
