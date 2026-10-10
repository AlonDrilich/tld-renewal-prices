#!/usr/bin/env python3
"""Daily watch of a few TLDs at registrars with a public, key-free pricing API.

Why: on 2026-11-01 Verisign's wholesale .com price goes from $10.26 to $10.97 (+7%). The weekly
snapshot would show that a retail price moved, but not on which day. This log records the first
observation of each (source, TLD) and then one row every time any of its three prices changes,
so the day a registrar passed a registry change through can be read straight from the file.

Sources (list prices, no key needed):
  porkbun   USD  https://api.porkbun.com/api/json/v3/pricing/get
  ovh-we    USD  OVHcloud public order catalog, subsidiary WE (rest of the world)
  ovh-ie    EUR  OVHcloud public order catalog, subsidiary IE

Two registrars are a sample, not a market. A row is written only on change; the Action's run
history shows the daily checks in between.

Usage: python3 scripts/watch.py        (run from the repo root)
"""
import csv
import datetime as dt
import gzip
import json
import pathlib
import ssl
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "watch" / "changes.csv"
FIELDS = ["observed_utc", "source", "currency", "tld", "first_year", "renewal", "transfer"]
TLDS = ["com", "net", "org", "io"]  # .com/.net are Verisign's; .org and .io are controls
UA = "tld-renewal-prices/1.0 (+https://github.com/AlonDrilich/tld-renewal-prices)"


def ssl_ctx():
    try:  # python.org builds on macOS ship without system CA roots
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def fetch(url, data=None):
    headers = {"User-Agent": UA, "Accept-Encoding": "gzip"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=120, context=ssl_ctx()) as r:
        body = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
    return json.loads(body)


def money(v):
    return f"{float(str(v).replace(',', '')):.2f}"


def porkbun():
    pricing = fetch("https://api.porkbun.com/api/json/v3/pricing/get", b"{}")["pricing"]
    for tld in TLDS:
        p = pricing.get(tld)
        if p:
            yield "porkbun", "USD", tld, money(p["registration"]), money(p["renewal"]), money(p["transfer"])


def ovh(host, subsidiary, source):
    cat = fetch(f"https://{host}/1.0/order/catalog/public/domain?ovhSubsidiary={subsidiary}")
    currency = cat["locale"]["currencyCode"]
    plans = {p["planCode"]: p for p in cat["plans"]}
    for tld in TLDS:
        plan = plans.get(tld)
        if not plan:
            continue
        # Standard (non-premium) prices, in 1e-8 units of the currency.
        price = {(q["mode"], tuple(q["capacities"])): q["price"] / 1e8 for q in plan["pricings"]}
        first = price.get(("create-default", ("installation", "renew")))
        renew = price.get(("create-default", ("renew",)))
        transfer = price.get(("transfer-default", ("installation", "renew")))
        if first is None or renew is None:
            continue
        yield source, currency, tld, money(first), money(renew), money(transfer) if transfer is not None else ""


def main():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(LOG.open())) if LOG.exists() else []
    last = {(r["source"], r["tld"]): r for r in rows}  # later rows win
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    seen, failed = [], []
    for name, gen in (("porkbun", porkbun),
                      ("ovh-we", lambda: ovh("ca.api.ovh.com", "WE", "ovh-we")),
                      ("ovh-ie", lambda: ovh("eu.api.ovh.com", "IE", "ovh-ie"))):
        try:
            seen.extend(gen())
        except Exception as e:  # one source being down must not lose the others
            failed.append(f"{name}: {e}")

    added = []
    for source, currency, tld, first, renew, transfer in seen:
        prev = last.get((source, tld))
        if prev and (prev["first_year"], prev["renewal"], prev["transfer"]) == (first, renew, transfer):
            continue
        added.append({"observed_utc": today, "source": source, "currency": currency, "tld": tld,
                      "first_year": first, "renewal": renew, "transfer": transfer})

    if added:
        with LOG.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows + added)
    for a in added:
        print("changed" if (a["source"], a["tld"]) in last else "first seen", a)
    print(f"watch {today}: {len(seen)} prices read, {len(added)} rows written")
    for f in failed:
        print("FAILED", f)
    if failed and not seen:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
