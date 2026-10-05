#!/usr/bin/env bash
# Face arhiva curată a unei luni pentru contabil, lângă celelalte arhive din folderul anului.
#
# Utilizare: zip_luna.sh "<cale>/Contabilitate/2026/09 Septembrie" [prefix]
# Rezultat:  "<cale>/Contabilitate/2026/<prefix> Septembrie.zip" (suprascrie dacă există; prefix implicit: Acte)
# Exclude .DS_Store, __MACOSX și orice folder/fișier care începe cu "_".
set -euo pipefail
dir="${1:?folderul lunii lipsa}"; dir="${dir%/}"
prefix="${2:-Acte}"
[[ -d "$dir" ]] || { echo "EROARE: nu exista $dir" >&2; exit 1; }
parent="$(dirname "$dir")"; base="$(basename "$dir")"
luna="${base#* }"                       # "09 Septembrie" -> "Septembrie"
zipf="$parent/$prefix $luna.zip"
cd "$parent"
rm -f "$zipf"
zip -r -X -q "$zipf" "$base" -x "*.DS_Store" -x "*__MACOSX*" -x "$base/_*" -x "$base/*/_*"
echo "OK: $zipf ($(du -h "$zipf" | cut -f1))"
unzip -Z1 "$zipf" | grep -v '/$' | sed "s|^$base/|  |"
