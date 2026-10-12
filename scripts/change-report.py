#!/usr/bin/env python3
"""Read data/watch/changes.csv around a registry (wholesale) price change.

For every (source, TLD) it prints the last price seen before the event, then each change
observed on or after it, with the size of the move. For a TLD whose wholesale change is known
(--wholesale-delta, in USD) and a USD source, it also says how much of that change reached the
retail renewal and first-year price.

Dates are the day the watcher OBSERVED a price, not the day the registrar changed it: the
watcher runs about three times a day and GitHub delays its schedules, so read each date as
"on or before this day, and after the previous observation".

Usage (from the repo root):
  python3 scripts/change-report.py --event 2026-11-01 --tld com --wholesale-delta 0.71
  python3 scripts/change-report.py --csv path/to/changes.csv --through 2026-11-03

Output is Markdown on stdout. It states facts only; interpretation is for the person reading it.
"""
import argparse
import csv
import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
USD_SOURCES = {"porkbun", "ovh-we"}


def f(x):
    return float(x) if x not in ("", None) else None


def pct(a, b):
    return (b - a) / a * 100 if a else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(ROOT / "data" / "watch" / "changes.csv"))
    ap.add_argument("--event", default="2026-11-01", help="effective date of the wholesale change (UTC)")
    ap.add_argument("--tld", default="com", help="the TLD whose wholesale price changed")
    ap.add_argument("--wholesale-delta", type=float, default=0.71, help="wholesale change in USD")
    ap.add_argument("--through", default=None, help="last day the watcher is known to have run (YYYY-MM-DD)")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.csv)))
    if not rows:
        sys.exit("empty log")
    by = defaultdict(list)
    for r in rows:
        by[(r["source"], r["tld"])].append(r)
    through = a.through or max(r["observed_utc"] for r in rows)

    out = []
    out.append(f"# Price changes observed around {a.event}")
    out.append("")
    out.append(f"Log: `{pathlib.Path(a.csv).name}`, {len(rows)} rows. Observed through **{through}**. "
               f"Wholesale change under study: .{a.tld} +${a.wholesale_delta:.2f} on {a.event}.")
    out.append("")
    moved_any = False
    sources = sorted({s for s, _ in by})
    order = [a.tld] + sorted({t for _, t in by} - {a.tld})
    for tld in order:
        block = []
        for src in sources:
            seq = by.get((src, tld))
            if not seq:
                continue
            before = [r for r in seq if r["observed_utc"] < a.event]
            after = [r for r in seq if r["observed_utc"] >= a.event]
            base = before[-1] if before else seq[0]
            cur = seq[-1]
            cu = base["currency"]
            line = (f"| {src} | {cu} | {base['first_year']} / {base['renewal']} | "
                    f"{base['observed_utc']}{'' if before else ' (first seen after the event)'} |")
            if not after or (not before and len(seq) == 1):
                block.append(line + " no change observed |  |")
                continue
            moved_any = True
            chg = []
            prev = base
            for r in after:
                if r is base:
                    continue
                parts = []
                for k, label in (("first_year", "first year"), ("renewal", "renewal"), ("transfer", "transfer")):
                    p, n = f(prev[k]), f(r[k])
                    if p is not None and n is not None and abs(n - p) >= 0.005:
                        parts.append(f"{label} {p:.2f} → {n:.2f} ({n - p:+.2f}, {pct(p, n):+.1f}%)")
                if parts:
                    chg.append(f"{r['observed_utc']}: " + "; ".join(parts))
                prev = r
            note = ""
            if tld == a.tld and src in USD_SOURCES and a.wholesale_delta:
                dr = f(cur["renewal"]) - f(base["renewal"])
                dfy = f(cur["first_year"]) - f(base["first_year"])
                note = (f"renewal moved {dr:+.2f} = {dr / a.wholesale_delta * 100:.0f}% of the wholesale change; "
                        f"first year moved {dfy:+.2f} = {dfy / a.wholesale_delta * 100:.0f}%")
            block.append(line + f" {' | '.join(chg) if chg else 'no change observed'} | {note} |")
        if block:
            out.append(f"## .{tld}" + ("  (the wholesale change)" if tld == a.tld else "  (control)"))
            out.append("")
            out.append("| Source | Currency | Before: first year / renewal | Baseline seen | Changes observed | vs wholesale |")
            out.append("|---|---|---|---|---|---|")
            out.extend(block)
            out.append("")

    out.append("## Reading it")
    out.append("")
    if moved_any:
        out.append("- At least one source changed a price on or after the event; see the rows above.")
    else:
        out.append(f"- No price changed in any source through {through}. Registrars may pass a wholesale "
                   "change on later; keep the log running and re-run this report.")
    out.append("- Sources are two registrars with public APIs (Porkbun, OVHcloud), list prices only. "
               "A sample, not a market. EUR rows are not comparable to the USD wholesale figure.")
    out.append("- Controls (.org, .io, and .net, whose wholesale change is 2027-03-01) show whether the "
               "registrar changed prices generally in the same window.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
