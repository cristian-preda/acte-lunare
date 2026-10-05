#!/usr/bin/env bash
# Datele publice ale unei firme din registrul ANAF, după CUI. Utilizare: anaf.sh 12345678  |  anaf.sh RO12345678
set -euo pipefail
cui="$(echo "${1:?CUI lipsa}" | tr -d ' .-' | tr '[:lower:]' '[:upper:]')"; cui="${cui#RO}"
[[ "$cui" =~ ^[0-9]{2,10}$ ]] || { echo "EROARE: CUI invalid: $1" >&2; exit 1; }
curl -s -m 30 -X POST "https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva" \
  -H "Content-Type: application/json" -d "[{\"cui\": $((10#$cui)), \"data\": \"$(date +%F)\"}]" \
  | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit("EROARE: ANAF nu a raspuns cu date (serviciu indisponibil sau prea multe cereri) - incearca din nou")
if not d.get("found"):
    sys.exit("EROARE: CUI negasit in registrul ANAF: " + sys.argv[1])
f = d["found"][0]
g, t = f.get("date_generale") or {}, f.get("inregistrare_scop_Tva") or {}
da = lambda v: "DA" if v else "NU"
tva = da(t.get("scpTVA"))
if t.get("scpTVA"):
    start = [p.get("data_inceput_ScpTVA") for p in t.get("perioade_TVA") or [] if p.get("data_inceput_ScpTVA")]
    tva += " - cod RO%s" % g.get("cui") + (" (din %s)" % start[-1] if start else "")
print("Denumire:", g.get("denumire") or "-")
print("CUI:", g.get("cui") or "-")
print("Reg. Com.:", g.get("nrRegCom") or "-")
print("Sediu:", " ".join((g.get("adresa") or "-").split()))
print("CAEN:", g.get("cod_CAEN") or "-")
print("Platitoare de TVA:", tva)
print("TVA la incasare:", da((f.get("inregistrare_RTVAI") or {}).get("statusTvaIncasare")))
print("Inactiva:", da((f.get("stare_inactiv") or {}).get("statusInactivi")))
print("Stare:", g.get("stare_inregistrare") or "-")
' "$cui"
