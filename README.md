# TLD renewal prices: first year vs. renewal

Cheap first-year domain prices often hide a much higher renewal. This repo snapshots, every week,
the **first-year and renewal list price of 531 top-level domains** (every IANA root-zone TLD it sells) from one registrar's
public pricing endpoint, so the gap is easy to check before you register a name.

**Latest snapshot: 2026-10-07.** 305 of 531 extensions renew at **2× or more** their
first-year price; 182 renew at 5× or more.

> Source: Porkbun's public pricing API (`https://api.porkbun.com/api/json/v3/pricing/get`), list prices in USD, fetched as-is.
> One registrar's prices on one date — **not a market average** and not a quote from any other
> registrar. Promotional first-year prices change often; check the registrar before buying.
> Not affiliated with Porkbun.

## Popular extensions where renewal costs more than year one

| TLD | First year | Renewal | Renewal ÷ first year |
|---|---:|---:|---:|
| .store | $2.57 | $43.77 | 17.0× |
| .shop | $2.06 | $31.41 | 15.2× |
| .online | $1.96 | $28.84 | 14.7× |
| .site | $1.96 | $28.84 | 14.7× |
| .world | $2.57 | $37.59 | 14.6× |
| .digital | $2.57 | $34.50 | 13.4× |
| .life | $2.57 | $34.50 | 13.4× |
| .space | $1.96 | $26.26 | 13.4× |
| .live | $2.57 | $31.41 | 12.2× |
| .fun | $2.57 | $31.41 | 12.2× |
| .website | $1.96 | $21.11 | 10.8× |
| .media | $4.63 | $40.68 | 8.8× |
| .finance | $6.69 | $58.19 | 8.7× |
| .blog | $2.57 | $21.11 | 8.2× |
| .agency | $3.60 | $27.29 | 7.6× |
| .company | $2.57 | $19.05 | 7.4× |
| .tech | $6.99 | $50.98 | 7.3× |
| .xyz | $2.04 | $14.21 | 7.0× |
| .info | $3.60 | $22.14 | 6.2× |
| .health | $10.81 | $62.31 | 5.8× |
| .cloud | $3.88 | $21.11 | 5.4× |
| .email | $5.66 | $28.32 | 5.0× |
| .design | $10.81 | $46.86 | 4.3× |
| .club | $4.12 | $15.96 | 3.9× |
| .studio | $11.84 | $41.71 | 3.5× |
| .news | $9.78 | $29.35 | 3.0× |
| .money | $10.81 | $31.41 | 2.9× |
| .biz | $6.69 | $19.05 | 2.9× |
| .cc | $3.40 | $8.55 | 2.5× |
| .io | $28.12 | $51.80 | 1.8× |
| .app | $8.75 | $14.93 | 1.7× |
| .us | $4.43 | $7.00 | 1.6× |
| .sh | $31.20 | $46.65 | 1.5× |

## Popular extensions with the same price every year

.ai, .com, .gg, .me, .net

## Largest renewal gaps in dollars (all extensions)

| TLD | First year | Renewal | Renewal ÷ first year |
|---|---:|---:|---:|
| .feedback | $9.27 | $309.47 | 33.4× |
| .movie | $36.56 | $309.47 | 8.5× |
| .watches | $52.01 | $257.98 | 5.0× |
| .realty | $93.20 | $288.88 | 3.1× |
| .casino | $7.72 | $143.67 | 18.6× |
| .creditcard | $5.66 | $129.25 | 22.8× |
| .travel | $15.96 | $129.25 | 8.1× |
| .investments | $8.24 | $114.83 | 13.9× |
| .doctor | $8.24 | $102.47 | 12.4× |
| .ceo | $9.78 | $103.50 | 10.6× |
| .energy | $11.84 | $102.47 | 8.7× |
| .gold | $5.66 | $92.17 | 16.3× |
| .credit | $6.69 | $92.17 | 13.8× |
| .loans | $10.81 | $93.20 | 8.6× |
| .rich | $78.99 | $160.71 | 2.0× |

## Changes since the previous snapshot

Moves under 10 cents or 1% are left out as currency noise.

| TLD | First year | Renewal |
|---|---|---|
| .democrat | $5.66 → $5.66 | $7.83 → $5.66 |
| .futbol | $5.66 → $5.66 | $7.83 → $5.66 |
| .republican | $5.66 → $5.66 | $7.83 → $5.66 |

## Files

- [`data/latest.csv`](data/latest.csv) — the current snapshot
- [`data/snapshots/`](data/snapshots/) — one dated CSV per week, the full history
- Also on Hugging Face: [AlonDrilichHF/tld-renewal-prices](https://huggingface.co/datasets/AlonDrilichHF/tld-renewal-prices) (latest snapshot)
- Columns: `tld`, `first_year_usd`, `renewal_usd`, `transfer_usd`, `renewal_minus_first_year_usd`, `renewal_to_first_year_ratio`, `first_year_has_coupon`

Updated every Monday by a GitHub Action ([`scripts/snapshot.py`](scripts/snapshot.py)).

## Daily watch: .com, .net, .org and .io

[`data/watch/changes.csv`](data/watch/changes.csv) is a change log, checked every day
([`scripts/watch.py`](scripts/watch.py)). It holds the first price seen for each registrar and
extension, then one row each time a first-year, renewal or transfer price changes, so the day a
registrar passed a registry price change through can be read from the file. It was started on
2026-10-10, ahead of Verisign's wholesale .com change on 2026-11-01. Sources are registrars with
a public pricing API that needs no key: Porkbun (USD) and OVHcloud (USD and EUR). Two registrars
are a sample, not a market.

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — cite "TLD renewal prices
(github.com/AlonDrilich/tld-renewal-prices)". Code: MIT.

Browse and search the same data at **[namesale.store/renewal-prices](https://namesale.store/renewal-prices)**.
Maintained by [NameSale](https://namesale.store/), a marketplace of brandable domain names where
each listing shows its extension's yearly renewal next to the price.
