# acte-lunare

Skill pentru [Claude Code](https://claude.com/claude-code) care pregătește actele lunare ale firmei pentru contabil: fiecare linie din extrasul bancar primește documentul ei, denumit după data și suma din extras.

E făcut pentru o firmă mică din România, cu Revolut Business și Gmail. Îl instalezi, îi dai CUI-ul și îl adaptezi după cum lucrezi tu.

## Ce face

1. Citește extrasele lunii. Revolut Business are parser dedicat; alte bănci sunt citite direct din PDF, best-effort.
2. Potrivește fiecare tranzacție cu factura sau bonul din folderul lunii.
3. Caută în Gmail facturile care lipsesc și le descarcă (linkuri Stripe: Anthropic, Figma, X și altele).
4. Verifică facturile: să fie emise pe firmă, nu pe persoană fizică, și să aibă codul de TVA corect la furnizorii din UE.
5. Îți arată un raport și ce ar redenumi. Aplică doar după ce zici OK.
6. Face arhiva `.zip` și o ciornă de mail pentru contabil.

Îl poți rula din nou oricând adaugi un document (un bon scanat, o factură întârziată): îl așază la locul lui și reface arhiva.

O lună organizată arată așa:

```
09 Septembrie/
├─ Extrase/
│   ├─ Revolut RON - septembrie 2026.pdf
│   └─ Revolut USD - septembrie 2026.pdf
├─ Emise/
│   └─ 15.09.2026 Client - 3000 USD - factura ABC0012.pdf
└─ Primite/
    ├─ 02.09.2026 Anthropic - 541.20 RON - factura ABCD1234-0009.pdf
    ├─ 21.09.2026 Revolut - 200.00 RON - comision abonament.pdf
    └─ 29.09.2026 Figma - 105.59 RON - factura ABCD1234-0030.pdf
```

## Ce nu face

- Nu trimite mailuri. Lasă doar ciorne, iar arhiva o atașezi tu.
- Nu redenumește, nu mută și nu șterge nimic fără acordul tău.
- Nu dă verdicte fiscale. Semnalează ce pare în neregulă și îți spune să confirmi cu contabilul.

## Cerințe

- [Claude Code](https://claude.com/claude-code)
- Conectorul Gmail legat la contul tău Claude (claude.ai → Settings → Connectors). În Claude Code îl vezi cu `/mcp`. Fără el, skill-ul merge, dar facturile lipsă le cauți tu.
- `poppler`, pentru citirea PDF-urilor: `brew install poppler`
- `python3`, `curl`, `zip` — vin cu macOS

Testat doar pe macOS. Pe Linux ar trebui să meargă la fel; pe Windows, doar prin WSL.

## Instalare

```bash
git clone https://github.com/cristian-preda/acte-lunare.git ~/.claude/skills/acte-lunare
```

Fără git: descarcă ZIP-ul de pe GitHub (Code → Download ZIP) și dezarhivează-l în `~/.claude/skills/acte-lunare`, astfel încât `SKILL.md` să stea direct în folderul acela.

Deschide apoi o sesiune nouă de Claude Code.

## Configurare

Rulează `/acte-lunare`. La prima rulare îți cere **CUI-ul firmei sau o factură existentă** și ia singur din registrul ANAF denumirea, sediul, Reg. Com. și statutul de TVA. Apoi te întreabă doar ce nu poate afla:

- folderul în care ții contabilitatea (cu câte un folder pe an);
- numele și mailul contabilului;
- cardurile firmei și, dacă e cazul, cele personale de ignorat;
- codul special de TVA, dacă firma e neplătitoare, dar înregistrată pentru achiziții din UE (art. 317).

Răspunsurile ajung în `references/firma.md` și `references/conventii.md`. Le poți completa și de mână: câmpurile de umplut sunt marcate cu `<…>`.

## Utilizare

```
/acte-lunare pe septembrie
```

Alte moduri de a-l porni:

- „pregătește actele pe octombrie” — închiderea lunii, de la zero
- „am pus bonul de la benzinărie în folder, aranjează-l” — actualizare după ce ai adăugat documente
- „caută facturile lipsă în mail” — doar căutarea în Gmail

Înainte de rulare, pune extrasele lunii în folderul ei (Revolut Business: Statements → Account statement → luna, PDF, câte unul pe monedă).

## Personalizare

Tot ce ține de firma ta stă în trei fișiere text. Schimbă-le direct sau cere-i lui Claude s-o facă.

| Vrei să schimbi | Fișier |
|---|---|
| Datele firmei, cardurile, contabilul, regulile de TVA | `references/firma.md` |
| Folderele, regula de denumire, numele arhivei, modelul de mail | `references/conventii.md` |
| Furnizorii: cum apar în extras și de unde iei factura | `references/furnizori.md` |
| Pașii și regulile de lucru | `SKILL.md` |
| Parserul de extras, descărcarea facturilor, arhiva | `scripts/` |

`references/furnizori.md` vine cu un catalog de furnizori obișnuiți (Anthropic, Google Workspace, Figma, X, SmartBill, Revolut, MOL, OMV, IKEA). Adaugă-i pe ai tăi pe măsură ce apar.

## Atenție la datele tale

După configurare, copia ta conține datele firmei: CUI, IBAN, mailul contabilului. Dacă îți faci un fork public, nu urca fișierele din `references/` completate.

## Stare și licență

Proiect făcut o singură dată, pentru uz propriu, și pus aici ca punct de plecare. Nu e întreținut: fă-ți un fork și modifică-l cum ai nevoie.

Licență [MIT](LICENSE).
