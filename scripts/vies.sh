#!/usr/bin/env bash
# Verifică un cod de TVA în VIES (registrul UE). Utilizare: vies.sh RO12345678  |  vies.sh "IE 4276970QH"
set -euo pipefail
v="$(echo "${1:?cod TVA lipsa}" | tr -d ' .-' | tr '[:lower:]' '[:upper:]')"
cc="${v:0:2}"; nr="${v:2}"
curl -s "https://ec.europa.eu/taxation_customs/vies/rest-api/ms/$cc/vat/$nr" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(("VALID" if d.get("isValid") else "INVALID"), sys.argv[1], "|", d.get("name") or "-", "|", " ".join((d.get("address") or "-").split()))' "$cc$nr"
