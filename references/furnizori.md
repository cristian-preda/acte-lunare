# Furnizori — cum apar în extras și de unde vine documentul

Nume scurt = numele folosit în denumirea fișierului (vezi `conventii.md`).

Catalogul comun pornește de la o firmă reală, în 2026. Entitățile, codurile de TVA și locul din care se descarcă facturile se pot schimba: ce scrie pe factură bate ce scrie aici.

## Catalog comun — plăți care au nevoie de document

| Descriere în extras | Nume scurt | Entitate / țară | Ritm | De unde iei documentul |
|---|---|---|---|---|
| `Anthropic* Claude Sub` | Anthropic | Anthropic, PBC; TVA IE4276970QH → UE | lunar, factura pe 1, plata ~2 | Gmail `from:mail.anthropic.com receipt` → link „Download invoice” (Stripe) |
| `Google*workspace <nume>` | Google Workspace | Google Cloud EMEA Ltd, IE → UE | factura lunară emisă în **ultima zi a lunii**, plătită ~2 luna următoare | **Nu vine pe mail.** admin.google.com → Facturare → documente/tranzacții → PDF (nume `<nr factura>.pdf`) |
| `Figma` | Figma | Figma, Inc., SUA (EU372054390) → non-UE | lunar | Gmail `from:figma "Receipt for subscription payment"` → linkul „receipt here” (click.figma.com) → `scripts/stripe_pdf.sh` urmează redirectul și ia factura |
| `X Corp. Paid Features` | X | X Internet Unlimited Co, IE → UE | lunar | Gmail `from:stripe.com "receipt from X"` → link „Download invoice” |
| `Paper.design` | Paper | Paper, SUA → non-UE | anual | Gmail `from:stripe.com Paper` → „Download invoice” |
| `Raycast.com` | Raycast | Raycast Technologies, UK → non-UE | anual | Gmail `from:raycast.com OR from:stripe.com Raycast`. Atenție: se emite ușor pe persoană fizică dacă datele firmei nu sunt trecute în cont |
| `Ntp*smartbill` | SmartBill | Intelligent IT SRL (RO) | anual | contul SmartBill (Contul meu → facturi) sau Gmail `smartbill factura`; factura `SBC…` |
| `Revolut Business Fee • <plan> plan fee` | Revolut | — | lunar | **Nu vine pe mail.** Export din Revolut Business: Transactions → filtru Type = Billing → Statement PDF (`transaction-statement_<de la>_<pana la>.pdf`) |
| `Mol …` | MOL | MOL Romania (RO) | ocazional | e-Factura în SPV (apare în arhiva de e-Facturi din programul de facturare) |
| `Omv …` | OMV | OMV Petrom (RO) | ocazional | **De regulă nu apare în SPV.** Bon fiscal cu CUI, de hârtie → se scanează sau fotografiază |
| `Ikea Romania …` | IKEA | IKEA Romania SA (RO) | ocazional | e-Factura SPV (vine și pe mail „Factura fiscală IKEA”) |
| `To <FIRMA> • <nr>` (transfer bancar) | numele firmei | RO | ocazional | e-Factura SPV; numărul din descriere poate fi de proformă (ex. `PF 1234`), factura reală are alt număr |
| plăți cu cardul la magazine online din UE | după caz | UE | ocazional | Gmail după numele magazinului; dacă nu există factură, se cere pe firmă (CUI + codul de TVA din `firma.md` — de confirmat cu contabilul la bunuri) |

## Furnizorii firmei (de completat)

Același format ca mai sus. Rândul de mai jos e un exemplu — înlocuiește-l.

| Descriere în extras | Nume scurt | Entitate / țară | Ritm | De unde iei documentul |
|---|---|---|---|---|
| `To <CONTABIL> • <serie> NNNN` | `<Contabil>` | contabilul (RO) | lunar, plătit luna următoare | e-Factura SPV, numărul e în descrierea plății |

## Încasări (documente în `Emise/`, de completat)

| Descriere în extras | Document |
|---|---|
| `Money added from <CLIENT> • <descriere>` | factura emisă din programul de facturare, `<SERIE>00NN`, către client, aceeași sumă, de regulă aceeași zi. Fișier SmartBill brut: `<CLIENT>__DD-MM-YYYY__<SERIE>00NN__SmartBill.pdf` |

## Fără document (le marchezi „nu necesită”)

| Descriere în extras | Ce e |
|---|---|
| `Main · USD –> Main · RON` (EXI/EXO) | schimb valutar intern; poate avea comision |
| `To BUGETUL GENERAL CONSOLIDAT • …` | contribuții salariale (CAS/CASS/impozit) și CAM |
| `To Trezorerie … • … TVA …` | plata TVA |
| `To <ANGAJAT> • SALARIU <LUNA>` | salariu (stat de plată de la contabil) |
| `Money added from <ASOCIAT> • creditare` | împrumut de la asociat |

## Documente care vin fără plată în aceeași lună
- Factura contabilului (se plătește luna următoare).
- Google Workspace din ultima zi a lunii (se plătește pe ~2 luna următoare). Plata de pe ~2 a lunii curente corespunde facturii din luna trecută, deja trimisă — **nu o duplica**.
