# 📇 Narzędzia do kopii zapasowej i zarządzania kontaktami (VCF ⇄ CSV)

## 🧩 Opis projektu

To zestaw trzech narzędzi napisanych w Pythonie, które pozwalają na:

* konwersję kontaktów z formatu **VCF do CSV** (czytelnego i edytowalnego),
* łączenie wielu baz kontaktów i eliminację duplikatów po numerach telefonu,
* konwersję z powrotem z CSV do VCF (w wersjach 2.1 lub 3.0), z opcją eksportu jako zbiorczy plik, wiele osobnych plików lub plik .vcf.gz.

### Dla kogo?

Dla **serwisantów**, **techników GSM**, **osób robiących kopie zapasowe kontaktów** z telefonów starszych i nowszych, oraz **dla każdego, kto chce utrzymać porządek w kontaktach** i mieć je w jednym miejscu.

---

## 🛠 Skrypty w zestawie

### 1. `vcf_to_csv.py`

Konwertuje plik `.vcf` zawierający wiele kontaktów na plik `.csv`, zachowując:

* imiona i nazwiska,
* wiele numerów telefonu (do 5),
* notatki (NOTE),
* obsługę starszych formatów vCard 2.1, QUOTED-PRINTABLE,
* debugowanie pierwszych linii pliku.

### 2. `merge_contacts.py`

Łączy wiele plików `.csv` z kontaktami w jeden, usuwając duplikaty po numerze telefonu.

* zachowuje najdłuższe dostępne imię,
* scala notatki,
* tworzy jedną bazę bez powtórzeń,
* zapisuje wynik do `kontakty_final.csv`

### 3. `csv_to_vcf.py`

Eksportuje kontakty z `.csv` z powrotem do formatu `.vcf`, z możliwością:

* wyboru wersji VCF: `2.1` lub `3.0`,
* eksportu:

  * do jednego pliku `kontakty_export.vcf`,
  * do osobnych plików `.vcf` (dla każdego kontaktu),
  * do jednego spakowanego `kontakty_export.vcf.gz`,
* obsługi dodatkowych pól: `ORG`, `TITLE`, `ADR`, `NOTE`,
* logowania i ostrzeżeń dla pustych rekordów.

---

## 🏁 Jak uruchomić

### Wymagania

* Python 3.7+

### Instalacja:

```
git clone https://github.com/Eul33r/kontakty-tools.git
cd kontakty-tools
```

### Uruchamianie

```bash
python3 vcf_to_csv.py           # Konwersja VCF → CSV
python3 merge_contacts.py       # Łączenie CSV-ow
python3 csv_to_vcf.py           # Konwersja CSV → VCF z wyborem trybu
```

---

## 🧠 Co warto wiedzieć
* Jeśli przy eksporcie kontakty uległy zduplikowaniu, to duplikaty można usunąć unixowym poleceniem:
  `find . -name "* (1).vcf" -delete`
  Przy czym polecenie zakłada, że mamy duplikaty postaci OsobaX.vcf oraz OsobaX(1).vcf
* Jeśli nie wyeksportował się "zbiorczy" plik .vcf, tylko kilka z osobna, to łatwo je połączyć w jeden duży, poleceniem:
  `cat *.vcf > kontakty_razem.vcf`
* Programy uwzględniają niestandardowe pliki z eksportu starszych telefonów.
* Pliki CSV mogą być ręcznie edytowane (np. w Excelu) przed powrotnym eksportem.
* Tworzony jest osobny folder dla eksportów VCF, aby nie nadpisać danych.
* Wersje `VCF 2.1` i `3.0` są zgodne z wiekszością telefonów i Google Contacts.

---

## 📬 Kontakt / Wsparcie

Jeśli masz pytania lub chcesz zgłosić poprawkę, otwórz **Issue** lub napisz do autora repozytorium.

---

## 📄 Licencja

MIT – używaj dowolnie, ulepszaj, rozwijaj dalej.

---

Zbudowane przez technika, dla techników. Zadbaj o swoje kontakty jak profesjonalista. 🚀
