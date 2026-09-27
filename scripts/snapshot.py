#!/usr/bin/env python3
"""Weekly snapshot of first-year vs renewal list prices per TLD, and the README built from it.

Source: Porkbun's public pricing endpoint (no key). One registrar's list prices — not a
market average, and not a quote from any other registrar.

Usage: python3 scripts/snapshot.py        (run from the repo root)
"""
import csv
import datetime as dt
import json
import pathlib
import ssl
import urllib.request

API = "https://api.porkbun.com/api/json/v3/pricing/get"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SNAPS = DATA / "snapshots"
FIELDS = ["tld", "first_year_usd", "renewal_usd", "transfer_usd",
          "renewal_minus_first_year_usd", "renewal_to_first_year_ratio", "first_year_has_coupon"]
# Extensions people actually launch on; the README tables focus on these.
COMMON = ["com", "net", "org", "io", "ai", "app", "dev", "me", "xyz", "tech", "store", "shop",
          "online", "site", "so", "gg", "sh", "cc", "info", "biz", "us", "studio", "design",
          "agency", "cloud", "digital", "company", "space", "website", "live", "life", "world",
          "fun", "club", "blog", "news", "media", "email", "health", "finance", "money"]


def fetch():
    req = urllib.request.Request(API, data=b"{}", headers={"content-type": "application/json"})
    try:  # python.org builds on macOS ship without system CA roots
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        body = json.load(r)
    if body.get("status") != "SUCCESS":
        raise SystemExit(f"API error: {body}")
    return body["pricing"]


def to_rows(pricing):
    out = []
    for tld, p in sorted(pricing.items()):
        try:
            reg, ren = float(p["registration"]), float(p["renewal"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append({
            "tld": tld,
            "first_year_usd": f"{reg:.2f}",
            "renewal_usd": f"{ren:.2f}",
            "transfer_usd": p.get("transfer", ""),
            "renewal_minus_first_year_usd": f"{ren - reg:.2f}",
            "renewal_to_first_year_ratio": f"{ren / reg:.2f}" if reg > 0 else "",
            "first_year_has_coupon": "yes" if p.get("coupons") else "no",
        })
    return out


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def read_csv(path):
    with open(path, newline="") as f:
        return {r["tld"]: r for r in csv.DictReader(f)}


def ratio(r):
    return float(r["renewal_to_first_year_ratio"] or 0)


def table(rows):
    lines = ["| TLD | First year | Renewal | Renewal ÷ first year |", "|---|---:|---:|---:|"]
    for r in rows:
        lines.append(f"| .{r['tld']} | ${r['first_year_usd']} | ${r['renewal_usd']} | {ratio(r):.1f}× |")
    return "\n".join(lines)


def changes(prev, cur):
    out = []
    for tld, r in sorted(cur.items()):
        p = prev.get(tld)
        if p and (p["first_year_usd"], p["renewal_usd"]) != (r["first_year_usd"], r["renewal_usd"]):
            out.append(f"| .{tld} | ${p['first_year_usd']} → ${r['first_year_usd']} | "
                       f"${p['renewal_usd']} → ${r['renewal_usd']} |")
    return out


def readme(date, rows, change_lines, prev_date):
    by = {r["tld"]: r for r in rows}
    n2 = sum(1 for r in rows if ratio(r) >= 2)
    n5 = sum(1 for r in rows if ratio(r) >= 5)
    common = sorted((by[t] for t in COMMON if t in by), key=ratio, reverse=True)
    traps = [r for r in common if ratio(r) >= 1.5]
    flat = [r for r in common if ratio(r) <= 1.0]
    worst = sorted(rows, key=lambda r: float(r["renewal_minus_first_year_usd"]), reverse=True)[:15]
    if change_lines:
        ch = ("| TLD | First year | Renewal |\n|---|---|---|\n" + "\n".join(change_lines))
    elif prev_date:
        ch = f"No list-price changes since the {prev_date} snapshot."
    else:
        ch = "First snapshot — changes appear from next week."
    return f"""# TLD renewal prices: first year vs. renewal

Cheap first-year domain prices often hide a much higher renewal. This repo snapshots, every week,
the **first-year and renewal list price of {len(rows)} domain extensions** from one registrar's
public pricing endpoint, so the gap is easy to check before you register a name.

**Latest snapshot: {date}.** {n2} of {len(rows)} extensions renew at **2× or more** their
first-year price; {n5} renew at 5× or more.

> Source: Porkbun's public pricing API (`{API}`), list prices in USD, fetched as-is.
> One registrar's prices on one date — **not a market average** and not a quote from any other
> registrar. Promotional first-year prices change often; check the registrar before buying.
> Not affiliated with Porkbun.

## Popular extensions where renewal costs more than year one

{table(traps)}

## Popular extensions with the same price every year

{", ".join("." + r["tld"] for r in sorted(flat, key=lambda r: r["tld"]))}

## Largest renewal gaps in dollars (all extensions)

{table(worst)}

## Changes since the previous snapshot

{ch}

## Files

- [`data/latest.csv`](data/latest.csv) — the current snapshot
- [`data/snapshots/`](data/snapshots/) — one dated CSV per week, the full history
- Columns: `{"`, `".join(FIELDS)}`

Updated every Monday by a GitHub Action ([`scripts/snapshot.py`](scripts/snapshot.py)).

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — cite "TLD renewal prices
(github.com/AlonDrilich/tld-renewal-prices)". Code: MIT.

Browse and search the same data at **[namesale.store/renewal-prices](https://namesale.store/renewal-prices)**.
Maintained by [NameSale](https://namesale.store/), a marketplace of brandable domain names where
each listing shows its extension's yearly renewal next to the price.
"""


def main():
    SNAPS.mkdir(parents=True, exist_ok=True)
    date = dt.date.today().isoformat()
    rows = to_rows(fetch())
    if len(rows) < 300:
        raise SystemExit(f"Only {len(rows)} TLDs returned — refusing to overwrite the data")
    olds = sorted(p for p in SNAPS.glob("porkbun-*.csv") if p.stem != f"porkbun-{date}")
    prev, prev_date = ({}, None) if not olds else (read_csv(olds[-1]), olds[-1].stem[len("porkbun-"):])
    write_csv(SNAPS / f"porkbun-{date}.csv", rows)
    write_csv(DATA / "latest.csv", rows)
    change_lines = changes(prev, {r["tld"]: r for r in rows}) if prev else []
    (ROOT / "README.md").write_text(readme(date, rows, change_lines, prev_date))
    print(f"{len(rows)} TLDs, {len(change_lines)} changed since {prev_date}")


if __name__ == "__main__":
    main()
