# Firma — date de identificare și reguli TVA

> NECONFIGURAT — rulează `/acte-lunare` și dă CUI-ul sau o factură (vezi „Configurare” în `SKILL.md`), ori completează de mână câmpurile `<…>`. Șterge rândul acesta când ai terminat.

## Identificare

| Câmp | Valoare |
|---|---|
| Denumire | `<DENUMIRE FIRMĂ SRL>` |
| CUI | `<CUI>` |
| Statut TVA | `<plătitoare (art. 316) / neplătitoare cu cod special (art. 317) / neplătitoare fără cod>` |
| Cod de TVA pentru facturile din UE | `<RO… sau „nu are”>` |
| Reg. Com. | `<J…>` |
| Sediu | `<adresa>` |
| Sediu vechi (dacă mai apare pe facturi) | `<adresa sau „—”>` — nu e o problemă, doar de semnalat |
| Bancă | `<banca, IBAN, conturile pe monede>` |
| Activitate | `<ce facturează firma, cui, în ce monedă, din ce program de facturare>` |

## Carduri
- **`<Mastercard …1234>`** = cardul firmei. Doar plățile de pe el contează.
- **`<Visa …5678>`** = card personal. Plățile și rambursările pe el **nu** sunt ale firmei — se ignoră. Șterge rândul dacă nu e cazul.

## Contabilul
- **`<Nume>`**, `<email>`. `<Cum facturează: ce scrie pe factură, suma, ziua, e-Factura sau PDF, când se plătește.>`
- `<Ce respinge: de regulă facturile emise pe persoană fizică.>`
- `<Ce cere mereu: de regulă bonul fiscal pentru plățile la benzinărie fără factură.>`
- `<Ce întocmește chiar el: stat de plată, ordine de plată pentru taxe, declarații — pentru acestea nu se caută documente.>`

## Reguli TVA — de știut când verifici o factură
Aplică secțiunea care corespunde rândului „Statut TVA” de mai sus. Totul se dă ca semnal, cu recomandarea de a confirma cu contabilul — nu ca sfat fiscal definitiv.

### Cum recunoști furnizorul
- **Stabilit în UE**: cod de TVA cu prefix de stat membru (IE, PL, DE…), valid în VIES. Irlanda (Dublin, IE…) **este** în UE.
- **Din afara UE** (SUA, UK): cod „EU372…” (schema OSS pentru furnizori non-UE), GB… sau niciun cod european. Marea Britanie și Irlanda de Nord nu sunt în UE.
- Uneori numele induce în eroare: o factură emisă pe o entitate americană poate purta un cod de TVA irlandez → se tratează ca UE. Codul bate numele.
- Verificare cod: `scripts/vies.sh <cod>`.
- Furnizorii români trimit e-Factura (SPV) pe CUI — corect, indiferent de statut.

### Firmă plătitoare de TVA (art. 316)
- Codul firmei este `RO<CUI>`. Ca să fie acceptat de furnizorii din UE trebuie să fie valid în VIES (firma înscrisă în Registrul operatorilor intracomunitari) — verifică o dată cu `scripts/vies.sh`.
- Furnizor din UE: factura ar trebui să poarte `RO<CUI>` și să nu aplice TVA (taxare inversă). Fără cod sau cu TVA străin → semnalează să fie adăugat codul în setările de facturare ale furnizorului.
- Furnizor din afara UE: nimic de verificat pe factură.

### Firmă neplătitoare, cu cod special (art. 317)
- Firma e înregistrată în scopuri de TVA doar pentru operațiuni intracomunitare. Codul special **poate fi diferit de CUI** — ia-l de pe certificatul de înregistrare și trece-l în tabelul de mai sus. `RO<CUI>` poate să nu fie valid în VIES.
- Furnizor din UE: factura ar trebui să poarte codul special și să nu aplice TVA (taxare inversă). Cu `RO<CUI>` sau fără cod → semnalează să fie schimbat în codul special.
- Furnizor din afara UE: codul nu e relevant pe factură, nimic de făcut.

### Firmă neplătitoare, fără cod special
- Furnizor din UE: fără un cod valid, furnizorul facturează de regulă cu TVA-ul țării lui. Achizițiile de servicii din UE cer, de regulă, înregistrarea conform art. 317 **înainte** de achiziție → dacă apar astfel de facturi, semnalează și recomandă discuția cu contabilul. Nu propune singur un cod.
- Furnizor din afara UE: nimic de verificat pe factură.
