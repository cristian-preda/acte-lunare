#!/usr/bin/env python3
"""Extrage tranzacțiile din extrase Revolut Business (PDF) într-o listă curată.

Utilizare:
  extras_revolut.py <extras.pdf> [<extras2.pdf> ...] [--json]

Un PDF poate conține mai multe conturi (ex. EUR + RON în același fișier); fiecare
secțiune "Currency XXX" e tratată separat. Pentru fiecare cont verifică suma
intrărilor/ieșirilor față de "Balance summary" și raportează OK / DIFERENȚĂ.
Tranzacțiile sunt listate cronologic (cele mai vechi primele), ca ordinea fișierelor.
"""
import json
import re
import subprocess
import sys

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
OUT_TYPES = {"CAR", "MOS", "EXO", "FEE", "ATM"}
IN_TYPES = {"MOA", "MOR", "EXI"}
SYM = {"$": "USD", "€": "EUR", "£": "GBP"}

AMT = r"-?\s?(?:[$€£]\s?)?\d{1,3}(?:[   ]\d{3})*\.\d{2}(?:\s?[A-Z]{3})?"
TX_START = re.compile(r"^\s{1,6}(\d{1,2}) ([A-Za-z]{3,5}) (\d{4})\s{2,}([A-Z]{3})\s{2,}(.*)$")
AMT_RE = re.compile(AMT)


def num(s):
    s = s.replace(" ", "").replace(" ", "").replace(" ", "")
    s = re.sub(r"[A-Z]{3}|[$€£]", "", s)
    return float(s)


def cur_of(s):
    m = re.search(r"[A-Z]{3}", s)
    if m:
        return m.group(0)
    for k, v in SYM.items():
        if k in s:
            return v
    return ""


def parse(path):
    text = subprocess.run(["pdftotext", "-layout", path, "-"],
                          capture_output=True, text=True, check=True).stdout
    accounts, acc, tx, col_in = [], None, None, None

    def close_tx():
        nonlocal tx
        if tx and acc is not None:
            tx["description"] = " ".join(tx["description"].split())
            acc["transactions"].append(tx)
        tx = None

    for line in text.splitlines():
        m = re.search(r"Currency\s+([A-Z]{3})\s*$", line)
        if m:
            close_tx()
            acc = {"file": path, "currency": m.group(1), "summary": {}, "transactions": []}
            accounts.append(acc)
            continue
        if acc is None:
            continue
        for key, label in (("opening", "Opening balance"), ("in", "Money in"),
                           ("out", "Money out"), ("closing", "Closing balance")):
            if re.match(rf"^\s*{label}\s{{2,}}", line) and key not in acc["summary"]:
                a = AMT_RE.findall(line)
                if a:
                    acc["summary"][key] = abs(num(a[-1]))
        if "Date (UTC)" in line and "Money in" in line:
            col_in = line.index("Money in")
            continue
        if re.match(r"^\s*Transaction types", line):
            close_tx()
            continue
        m = TX_START.match(line)
        if m:
            close_tx()
            d, mon, y, typ, rest = m.groups()
            amts = [(x.group(0), x.end()) for x in AMT_RE.finditer(line)]
            desc = rest
            if amts:
                desc = line[m.start(5):line.find(amts[0][0], m.start(5))]
            out_v = in_v = bal = None
            if amts:
                bal = num(amts[-1][0])
                if len(amts) >= 2:
                    v, end = num(amts[-2][0]), amts[-2][1]
                    if typ in OUT_TYPES:
                        out_v = abs(v)
                    elif typ in IN_TYPES:
                        in_v = abs(v)
                    elif col_in is not None and end > col_in:
                        in_v = abs(v)
                    else:
                        out_v = abs(v)
            tx = {"date": f"{int(d):02d}.{MONTHS[mon[:3].lower()]:02d}.{y}", "type": typ,
                  "description": desc, "out": out_v, "in": in_v, "balance": bal,
                  "currency": acc["currency"], "orig": None, "fee": None, "id": None,
                  "counterparty": None}
            continue
        if tx is None:
            continue
        s = line.strip()
        if not s:
            continue
        if s.startswith("ID:"):
            tx["id"] = s[3:].strip()
        elif s.startswith(("To account:", "From account:")):
            tx["counterparty"] = s.split(":", 1)[1].strip()
        elif s.startswith("FX Rate"):
            f = re.search(r"Fee:\s*(" + AMT + ")", s)
            if f:
                tx["fee"] = f.group(1).strip()
            a = AMT_RE.findall(re.sub(r"Fee:\s*" + AMT, "", s))
            if a:
                tx["orig"] = f"{abs(num(a[-1])):.2f} {cur_of(a[-1])}".strip()
        elif s.startswith(("Report lost", "+370", "Get help", "Scan the QR", "©")) or "Revolut Bank UAB" in s:
            continue
        elif len(line) - len(line.lstrip()) > 30 and len(s) < 90:
            tx["description"] += " " + s
    close_tx()

    for acc in accounts:
        acc["transactions"].reverse()
        acc["total_out"] = round(sum(t["out"] or 0 for t in acc["transactions"]), 2)
        acc["total_in"] = round(sum(t["in"] or 0 for t in acc["transactions"]), 2)
        sm = acc["summary"]
        acc["check"] = ("OK" if abs(acc["total_out"] - sm.get("out", 0)) < 0.01
                        and abs(acc["total_in"] - sm.get("in", 0)) < 0.01 else "DIFERENTA")
    return accounts


def fmt(v):
    return "" if v is None else f"{v:,.2f}".replace(",", " ")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    accounts = [a for p in args for a in parse(p)]
    if "--json" in sys.argv:
        print(json.dumps(accounts, ensure_ascii=False, indent=1))
        return
    for acc in accounts:
        sm = acc["summary"]
        print(f"\n=== {acc['currency']}  ({acc['file'].split('/')[-1]})")
        print(f"Sold initial {fmt(sm.get('opening'))} | intrari {fmt(sm.get('in'))} | "
              f"iesiri {fmt(sm.get('out'))} | sold final {fmt(sm.get('closing'))}")
        if not acc["transactions"]:
            print("(fara tranzactii)")
        for i, t in enumerate(acc["transactions"], 1):
            amt = f"-{fmt(t['out'])}" if t["out"] is not None else f"+{fmt(t['in'])}"
            extra = " | ".join(x for x in (t["orig"] and f"orig {t['orig']}",
                                           t["fee"] and f"fee {t['fee']}") if x)
            print(f"{i:>2}. {t['date']}  {t['type']}  {amt:>13} {t['currency']}  "
                  f"{t['description'][:60]}" + (f"  [{extra}]" if extra else ""))
        print(f"Verificare totaluri: {acc['check']} (iesiri {fmt(acc['total_out'])}, "
              f"intrari {fmt(acc['total_in'])})")


if __name__ == "__main__":
    main()
