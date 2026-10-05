# Convenții — foldere, denumiri, arhivă, mail

## Setări
Se completează la configurare (vezi `SKILL.md`). Restul fișierului se referă la ele prin numele din stânga.

| Setare | Valoare |
|---|---|
| Calea de bază | `<CALEA DE BAZĂ>` — folderul care conține câte un folder pe an |
| Prefix | `<PREFIX>` — numele scurt al firmei, folosit în numele arhivei și în subiectul mailului |
| Mail contabil | `<EMAIL CONTABIL>` |
| Semnătură | `<nume, telefon, email — cum semnezi mailurile>` |
| Stil mail | scurt, politicos `<+ preferințe: cu sau fără diacritice, formula de adresare>` |

## Unde
Rădăcina: `<Calea de bază>/<AN>/`. Poate fi orice folder local sau sincronizat (Google Drive, iCloud, Dropbox), de exemplu `~/Library/CloudStorage/GoogleDrive-<email>/My Drive/Firma/Contabilitate/2026/`.

Folderul lunii: `<NN> <Luna>` — `01 Ianuarie`, `02 Februarie`, `03 Martie`, `04 Aprilie`, `05 Mai`, `06 Iunie`, `07 Iulie`, `08 August`, `09 Septembrie`, `10 Octombrie`, `11 Noiembrie`, `12 Decembrie`. Dacă nu există, creează-l.

## Structura țintă a unei luni
```
<NN> <Luna>/
├─ Extrase/
│   ├─ Revolut RON - <luna> <an>.pdf
│   └─ Revolut USD - <luna> <an>.pdf      (câte unul pe monedă; altă bancă → numele ei)
├─ Emise/
│   └─ DD.MM.YYYY <Client> - <suma> <MONEDA> - factura <SERIE>00NN.pdf
└─ Primite/
    └─ DD.MM.YYYY <Furnizor> - <suma> <MONEDA> - <tip> <numar>.pdf
```
Luna în numele extrasului se scrie cu literă mică (`septembrie 2026`).

## Regula de denumire a documentelor
`DD.MM.YYYY <Furnizor> - <suma> <MONEDA> - <tip> <numar>.pdf`

- **Data și suma se iau din linia de extras** pe care o acoperă documentul, exact cum apar acolo (data din extras, suma în moneda contului). Scopul: contabilul vede linia în extras și găsește fișierul din ochi. Ex.: plata Figma de 105.59 RON din 29.09 → `29.09.2026 Figma - 105.59 RON - factura ABCD1234-0030.pdf`, chiar dacă factura e în EUR și datată 28.09.
- Încasările: data și suma din extras → în `Emise/`.
- Documente fără plată în luna respectivă (factura contabilului, facturile emise în ultima zi): **data și suma de pe factură**, în moneda facturii. Nu se pun în folder separat.
- Suma: punct zecimal, fără separator de mii, două zecimale (`2364.58`, `3010.00`); sumele întregi din `Emise/` pot rămâne fără zecimale (`3000 USD`).
- `<Furnizor>`: numele scurt din `furnizori.md`; pentru furnizori noi, numele comercial scurt (ex. `Dedeman`, `eMAG`).
- `<tip>`: `factura`, `factura avans`, `bon fiscal`, `comision abonament` (bancă), `chitanta`.
- Data în format românesc `DD.MM.YYYY` — într-o lună se sortează corect cronologic.
- Fișierele cu nume conform: regex `^\d{2}\.\d{2}\.\d{4} .+ - .+ - .+\.(pdf|jpg|jpeg|png|heic)$`.
- **Subfolderele cu nume conform** (cazuri speciale rezolvate cu utilizatorul, ex. `02.09.2026 Furnizor - 500.00 RON - TVA rambursat ulterior/` cu documente numerotate `0 Nota explicativa.pdf`, `1 Factura …`) acoperă linia lor din extras și **se lasă neatinse**, inclusiv fișierele din ele.

## Curățenie
- Arhiva de e-Facturi primite din programul de facturare (SmartBill: `e-Facturi furnizori - [..] - [..] - PDF_SMARTBILL.zip`, plus folderul dezarhivat): extrage PDF-urile, redenumește-le în `Primite/`, apoi șterge zip-ul și folderul gol — **doar după** ce ai verificat că toate PDF-urile din zip sunt în `Primite/`. Exporturile din alte programe se tratează la fel.
- Dubluri: șterge doar dacă textul (`pdftotext`) e identic cu o copie care rămâne. Documentele altei luni se mută în folderul lunii lor, nu se șterg.
- `.DS_Store` se ignoră.

## Arhiva pentru contabil
`scripts/zip_luna.sh "<folderul lunii>" "<Prefix>"` → `<AN>/<Prefix> <Luna>.zip`, lângă arhivele lunilor trecute. Refă arhiva după orice modificare a folderului.

## Mailul către contabil (ciornă, nu se trimite niciodată automat)
- Către: adresa din „Mail contabil”; subiect: `<Prefix> acte <luna>` (luna cu literă mică).
- Stilul din „Stil mail”.
- **Conectorul Gmail nu poate atașa zip-ul** (fișierele se trimit inline în base64, prea mari) → ciorna fără atașament; spune-i utilizatorului să atașeze `<Prefix> <Luna>.zip` înainte de trimitere.
- Dacă există deja o ciornă pentru luna respectivă (`in:draft subject:"<Prefix> acte <luna>"`), actualizeaz-o cu `update_draft` în loc să creezi alta.

Model:
```
Buna ziua,

Atasez arhiva cu actele pe <luna>.

<doar daca e cazul: 1-2 randuri despre ceva neobisnuit, ex. un document care vine ulterior>

Multumesc!

<Semnătură>
```
La prima lună trimisă cu structura aceasta, adaugă 2-3 rânduri care o explică (Extrase / Emise / Primite, fișiere denumite după data și suma din extras). Lunile următoare nu mai au nevoie.
