import csv
import quopri


input_file = "kontakty_osoby.vcf"
output_file = "kontakty_osoby.csv"

def parse_vcard(file_path):
    contacts = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        print("\n".join(lines[:20]))  # podgląd pierwszych 20 linii
        contact = {"name": "", "phones": [], "note": ""}
        for line in lines:
            line = line.strip()
            if line.lower().startswith("begin:vcard"):
                contact = {"name": "", "phones": []}
            elif line.lower().startswith("fn"):
                contact["name"] = line.split(":", 1)[-1].strip()


            elif line.lower().startswith("n") and "quoted-printable" in line.lower():

                # Obsługa N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:

                try:

                    encoded_value = line.split(":", 1)[-1].strip()

                    decoded_bytes = quopri.decodestring(encoded_value)

                    contact["name"] = decoded_bytes.decode("utf-8").strip()

                except Exception as e:

                    print(f"Błąd dekodowania QUOTED-PRINTABLE: {e}")

                    contact["name"] = ""


            elif line.lower().startswith("n:") and not contact["name"]:

                parts = line.split(":", 1)[-1].split(";")

                first = parts[1].strip() if len(parts) > 1 else ""

                last = parts[0].strip()

                contact["name"] = f"{first} {last}".strip()


            elif line.lower().startswith("note"):
                contact["note"] = line.split(":", 1)[-1].strip()
            elif line.lower().startswith("tel"):
                number = line.split(":", 1)[-1].strip()
                if "phones" in contact:
                    contact["phones"].append(number)

            elif line.lower().startswith("end:vcard"):
                if contact:
                    contacts.append(contact)
    return contacts


def write_to_csv(contacts, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Imię i nazwisko", "Numer telefonu 1", "Numer telefonu 2", "Numer telefonu 3", "Notatka"])

        for contact in contacts:
            row = [contact["name"]] + contact["phones"][:3]
            row += [""] * (3 - len(contact["phones"]))  # uzupełnij brakujące numery pustymi komórkami
            row.append(contact.get("note", ""))

            writer.writerow(row)

contacts = parse_vcard(input_file)
write_to_csv(contacts, output_file)

print(f"Zapisano {len(contacts)} kontaktów do pliku {output_file}")
