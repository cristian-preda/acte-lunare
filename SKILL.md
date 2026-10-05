---
name: acte-lunare
description: ON-DEMAND ONLY. This skill should be used only when the user explicitly invokes "/acte-lunare" or asks by name for the monthly accounting-documents routine (e.g. "pregătește actele pe octombrie", "rulează acte-lunare", "am pus bonul în folder, aranjează-l"). It prepares the monthly package that a Romanian company sends to its accountant: parses the Revolut Business statements (other banks are read best-effort), matches every statement line to an invoice/receipt in the month folder, searches Gmail for missing invoices (Stripe links and similar), flags wrong buyer/VAT data, renames everything to the "DD.MM.YYYY Furnizor - suma MONEDA - factura nr" convention, builds the zip and a Gmail draft for the accountant. Also re-runs later to file documents added to the folder, and on first run configures itself from the company's CUI or an existing invoice. Do NOT auto-invoke on generic keywords like factură, extras, contabilitate, TVA.
---

# Acte lunare pentru contabil

## Scop
Pregătește actele lunare ale firmei pentru contabil astfel încât fiecare linie din extrasul bancar să aibă documentul ei, ușor de găsit după dată și sumă. Muncă de rutină: inventar → potrivire extras ↔ documente → căutare în Gmail a ce lipsește → verificări → redenumire după convenție → arhivă + ciornă de mail.

Înainte de orice, citește:
- `references/firma.md` — datele firmei, codul de TVA, carduri, contabilul, reguli TVA UE/non-UE;
- `references/conventii.md` — unde stau folderele, regula de denumire, arhiva, modelul de mail;
- `references/furnizori.md` — cum apare fiecare furnizor în extras și de unde vine documentul.

Dacă `references/firma.md` conține încă marcajul `NECONFIGURAT`, fă întâi „Configurare”.

## Reguli
1. **Nimic nu se redenumește, mută sau șterge fără OK-ul utilizatorului.** Mai întâi raport + propunere, apoi aplicare. Excepție: documentele descărcate din Gmail se pot salva direct în `Primite/` cu numele final (sunt adăugiri, nu modificări).
2. **Gmail: doar citire și ciorne.** Nu trimite niciodată un mail. Ciorne noi doar pentru contabil sau pentru cererea unei facturi lipsă, când utilizatorul e de acord.
3. **Ștergeri permise doar:** arhiva de e-Facturi după extragere verificată și dubluri cu text identic. Documentele altei luni se mută în luna lor.
4. **Cardurile care nu sunt ale firmei** (listate în `firma.md`) — plățile și rambursările de pe ele se ignoră.
5. **Cazuri neobișnuite** (rambursări, note de credit, storno, plăți parțiale, documente contradictorii): oprește-te, descrie cazul cu cifre și întreabă cum se tratează. Nu le rezolva „din pix”.
6. Nu inventa sume sau numere. Un PDF fără text (`pdftotext` gol) e o scanare/poză: randează-l cu `pdftoppm -png -r 110 -f 1 -l 1 <pdf> <prefix>` și citește imaginea.
7. Sfaturile fiscale se dau ca semnal („de confirmat cu contabilul”), nu ca verdict.

## Configurare (prima rulare)
Scop: completează `references/firma.md` și tabelul „Setări” din `references/conventii.md` cu cât mai puține întrebări.

1. Cere **CUI-ul firmei sau o factură existentă** (emisă de firmă ori primită pe numele ei).
   - CUI → `scripts/anaf.sh <CUI>`: denumire, sediu, Reg. Com., CAEN, plătitoare de TVA sau nu.
   - Factură → `pdftotext -layout`, ia CUI-ul din blocul firmei (la o factură emisă e furnizorul, la una primită e cumpărătorul) și rulează tot `scripts/anaf.sh` pe el. De pe factură mai ies banca, IBAN-ul, programul de facturare și seria facturilor.
2. Întreabă, într-o singură rundă, doar ce nu se poate afla automat:
   - folderul de contabilitate (calea de bază, cu câte un folder pe an);
   - contabilul: nume, email și ce cere sau respinge de obicei;
   - cardurile firmei (ultimele 4 cifre) și cardurile personale de ignorat, dacă apar în aceleași mailuri;
   - doar dacă firma nu e plătitoare de TVA: are cod special de TVA (art. 317)? Dacă da, verifică-l cu `scripts/vies.sh <cod>`;
   - prefixul arhivei (implicit numele scurt al firmei) și semnătura de mail;
   - clienții recurenți și ce nu are nevoie de document (salarii, taxe, creditări).
3. Scrie valorile în `references/firma.md` și în „Setări” din `references/conventii.md`, șterge rândul `NECONFIGURAT`, arată un rezumat și cere confirmarea.
4. `references/furnizori.md`: catalogul comun rămâne cum e. Secțiunile firmei (furnizori proprii, încasări, fără document) se completează cu răspunsurile de mai sus și, după fiecare lună închisă, cu furnizorii recurenți noi găsiți în extras — propune rândurile, nu le adăuga fără OK.
5. Verifică uneltele: `command -v pdftotext pdftoppm python3 curl zip`. Ce lipsește se instalează cu `brew install poppler` (macOS) sau `apt install poppler-utils` (Linux).

## Alege modul
- **A. Închiderea lunii** — utilizatorul cere actele pe o lună („pe octombrie”; fără lună = luna trecută) și folderul nu e încă organizat (extrasele au nume brute, fișierele nu respectă convenția).
- **B. Actualizare** — luna e deja organizată (`Extrase/` există, majoritatea fișierelor respectă convenția) și utilizatorul a adăugat documente noi („am pus bonul de la benzinărie”, „mai verifică o dată folderul”).
- **Doar Gmail** — „caută facturile lipsă în mail”: pașii A1–A3, apoi raport scurt.

## A. Închiderea lunii

### A1. Inventar
1. Stabilește folderul lunii (vezi `conventii.md`) și listează tot: `find "<folder>" -not -name .DS_Store`.
2. Extrasele: caută `*account-statement*.pdf` (numele brut Revolut) sau alte PDF-uri de extras în rădăcină, apoi `Extrase/*.pdf`. Dacă lipsesc, cere utilizatorului să le descarce (Revolut Business: Statements → Account statement → luna, PDF, câte unul pe monedă) și oprește-te.
3. Rulează parserul pe toate extrasele:
   ```
   python3 scripts/extras_revolut.py "<extras RON>.pdf" "<extras USD>.pdf"
   ```
   Fiecare cont trebuie să aibă `Verificare totaluri: OK`. Dacă apare `DIFERENTA`, citește extrasul direct (`pdftotext -layout`) și corectează manual lista. Pentru date structurate folosește `--json`.
4. **Altă bancă decât Revolut Business** (parserul nu afișează niciun cont): citește extrasul cu `pdftotext -layout` și construiește de mână aceeași listă — dată, descriere, ieșire sau intrare, suma originală la plățile în valută. Verifică singur totalurile: sold inițial + intrări − ieșiri = sold final. Dacă nu se închid, spune-o și nu merge mai departe pe o listă incompletă. Menționează în raport că extrasul a fost citit fără parser.
5. Documentele: pentru fiecare PDF din `Emise/`, `Primite/` (inclusiv subfoldere) și din arhiva de e-Facturi a programului de facturare (`unzip -l`, apoi extrage într-un folder temporar), rulează `pdftotext -layout` și notează: furnizor, număr, dată, total + monedă, cumpărătorul (denumire, CUI/cod TVA).

### A2. Potrivire extras ↔ documente
Pentru fiecare linie din extras, caută documentul:
- factură în RON: totalul = suma din extras;
- factură în valută: totalul = suma originală din extras (`orig 20.00 EUR`);
- data facturii ≤ data plății, de regulă la 0–3 zile (datele din extrasul Revolut sunt UTC);
- transferurile au în descriere numărul facturii sau al proformei (proforma ≠ factura);
- liniile „fără document” din `furnizori.md` (schimb valutar, taxe, salarii, creditări) → „nu necesită”;
- plata unei facturi emise luna trecută și deja trimisă (ex. Google Workspace: factura din ultima zi a lunii, plata pe ~2) → „inclusă luna trecută”, nu o duplica.
Notează separat documentele fără plată în lună (factura contabilului, facturile din ultima zi). Sunt normale, intră în `Primite/` fără alt marcaj.

### A3. Gmail pentru ce lipsește
Fără conector Gmail, pasul acesta devine o listă cu ce are de căutat utilizatorul și unde. Altfel, pentru fiecare linie fără document:
1. Caută cu interogarea din `furnizori.md`, într-o fereastră de la ~5 zile înainte de începutul lunii până azi (`after:YYYY/MM/DD`).
2. Citește mesajul cu `get_message` (format `PLAIN_TEXT`) și ia linkul „Download invoice” (`https://pay.stripe.com/invoice/.../pdf?s=em`). Pentru Figma, ia linkul „receipt here” (click.figma.com). Descarcă:
   ```
   scripts/stripe_pdf.sh "<link>" "<folder>/Primite/<nume final>.pdf"
   ```
   Verifică ce afișează scriptul: numărul facturii, totalul, cumpărătorul.
3. Conectorul Gmail **nu poate descărca atașamente**. Dacă factura e doar atașament, fără link, dă-i utilizatorului subiectul, data și `viewUrl` ca s-o salveze el.
4. Documente care nu vin pe mail: Google Workspace (admin.google.com), comisionul băncii (export din aplicație), bonuri de benzinărie (hârtie). Spune exact de unde se iau.
5. Comerciant necunoscut în extras: caută în Gmail după nume și după sumă, în jurul datei (confirmări de comandă, livrări), ca să afli magazinul. Dacă factura nu există, propune o ciornă de cerere a facturii pe firmă.

### A4. Verificări
- Cumpărătorul e firma (denumirea și CUI-ul din `firma.md`), nu utilizatorul ca persoană fizică. Contabilii resping de regulă facturile pe persoană fizică.
- Codul de TVA de pe factură, după regulile din `firma.md` pentru statutul firmei: furnizor din UE cu cod greșit sau fără cod → semnalează să fie schimbat în setările de facturare ale furnizorului. Furnizor din afara UE → nimic de făcut.
- Plăți de pe carduri care nu sunt ale firmei → ignoră-le.
- Documente din altă lună sau dubluri prezente în folder.

### A5. Raport + propunere (în chat, apoi așteaptă OK)
```
## <Luna an> — <N> tranzacții · <M> cu document · <K> lipsă
| Data | Extras | Sumă | Document | Stare |      ← ✅ găsit · ⏳ lipsă · — nu necesită · ↩ luna trecută
### Ce lipsește și de unde îl iei
### De semnalat                                  ← date greșite pe facturi, coduri TVA, cazuri neobișnuite
### Ce aș redenumi / muta / șterge               ← tabel vechi → nou
```
Ține raportul scurt. Fără observații evidente.

### A6. Aplicare (după OK)
1. `mkdir -p Extrase` și mută extrasele: `Revolut RON - <luna> <an>.pdf` etc.
2. Redenumește cu `mv -n` (nu suprascrie), după regula din `conventii.md`. Extrage PDF-urile din arhiva de e-Facturi direct cu numele final, verifică că toate sunt în `Primite/`, apoi șterge arhiva și folderul dezarhivat.
3. Listează rezultatul final.
4. Arhiva: `scripts/zip_luna.sh "<folderul lunii>" "<Prefix>"`.
5. Ciorna pentru contabil, după modelul din `conventii.md`. Dacă există deja o ciornă pentru luna respectivă, actualizeaz-o. Spune-i utilizatorului că zip-ul trebuie atașat manual. Dacă mai lipsesc documente, spune că după adăugarea lor rulează modul B, care reface arhiva.

## B. Actualizare (documente adăugate ulterior)
1. Găsește fișierele care nu respectă convenția (regex în `conventii.md`): extrase brute în rădăcină, PDF-uri sau poze noi (`.jpg/.png/.heic` pentru bonuri), arhive de e-Facturi noi, documente din altă lună. Subfolderele cu nume conform (cazuri speciale) se sar.
2. Rulează din nou A1.3 și A2 pe lună, ca să știi ce linii din extras erau fără document. Leagă fișierele noi de ele.
3. Propune redenumirile (vechi → nou) și ce rămâne lipsă. Așteaptă OK, apoi aplică. Pozele își păstrează extensia; doar numele urmează convenția.
4. Dacă `<AN>/<Prefix> <Luna>.zip` există, refă-l cu `scripts/zip_luna.sh`. Dacă există ciornă pentru contabil, amintește-i utilizatorului să atașeze noul zip, nu pe cel vechi.

## Scripturi
| Script | Ce face |
|---|---|
| `scripts/extras_revolut.py <pdf…> [--json]` | Tranzacțiile din extrasele Revolut Business, cronologic, cu suma originală la plățile în valută și verificarea totalurilor față de soldul din extras. Suportă mai multe conturi în același PDF. |
| `scripts/stripe_pdf.sh <url> <out.pdf>` | Descarcă factura PDF dintr-un link Stripe sau dintr-un link de tracking către o chitanță Stripe (Figma). Afișează numărul, totalul și cumpărătorul. |
| `scripts/anaf.sh <CUI>` | Datele publice ale firmei din registrul ANAF: denumire, sediu, Reg. Com., CAEN, plătitoare de TVA sau nu. |
| `scripts/vies.sh <cod TVA>` | Verifică un cod de TVA în VIES (valid/invalid, denumire, adresă). |
| `scripts/zip_luna.sh <folder luna> [prefix]` | Face `<Prefix> <Luna>.zip` curat (fără `.DS_Store`, `__MACOSX` sau foldere `_*`) în folderul anului. |

Necesită `python3`, `pdftotext`/`pdftoppm` (poppler), `curl` și `zip`, plus conectorul Gmail pentru pasul A3 și pentru ciornă.
