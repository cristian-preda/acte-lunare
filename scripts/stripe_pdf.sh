#!/usr/bin/env bash
# Descarcă PDF-ul unei facturi Stripe pornind de la un link din email.
#
# Utilizare: stripe_pdf.sh "<url>" "<fisier_iesire.pdf>"
#
# Acceptă:
#  - link direct "Download invoice":  https://pay.stripe.com/invoice/acct_.../pdf?s=em
#  - link direct de credit note:      https://pay.stripe.com/credit_notes/acct_.../pdf?s=em
#  - link de chitanță (receipt):      https://dashboard.stripe.com/receipts/invoices/.../pdf?s=em
#  - link de tracking care duce la o pagină de chitanță Stripe (ex. click.figma.com/...):
#    urmează redirecturile și ia de pe pagină linkul pay.stripe.com/invoice/.../pdf
# Iese cu cod 1 dacă rezultatul nu e un PDF valid.
set -euo pipefail
url="${1:?url lipsa}"; out="${2:?fisier iesire lipsa}"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

fetch() { curl -sL --max-redirs 10 -A "Mozilla/5.0" -o "$2" -w "%{url_effective}" "$1"; }

final="$(fetch "$url" "$tmp/r")"
if ! head -c 5 "$tmp/r" | grep -q '%PDF'; then
  # pagină HTML (chitanță Stripe) -> caută linkul facturii PDF
  inv="$(grep -oE 'https://pay\.stripe\.com/invoice/[^"'"'"' <>]+/pdf[^"'"'"' <>]*' "$tmp/r" | head -1 | sed 's/&amp;/\&/g' || true)"
  if [[ -z "$inv" ]]; then
    echo "EROARE: nu am gasit link de factura PDF pe pagina $final" >&2; exit 1
  fi
  fetch "$inv" "$tmp/r" >/dev/null
fi
head -c 5 "$tmp/r" | grep -q '%PDF' || { echo "EROARE: rezultatul nu e PDF" >&2; exit 1; }
mv "$tmp/r" "$out"
echo "OK: $out"
pdftotext -layout "$out" - 2>/dev/null | grep -v '^\s*$' | grep -E 'Invoice number|Credit Note|Receipt number|Date (of issue|issued)|Total|Amount (due|paid)|VAT|TIN |Bill to' | head -12 || true
