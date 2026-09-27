# TLD renewal prices: first year vs. renewal

Cheap first-year domain prices often hide a much higher renewal. This repo snapshots, every week,
the **first-year and renewal list price of 897 domain extensions** from one registrar's
public pricing endpoint, so the gap is easy to check before you register a name.

**Latest snapshot: 2026-09-27.** 331 of 897 extensions renew at **2× or more** their
first-year price; 181 renew at 5× or more.

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
| .space | $1.96 | $26.26 | 13.4× |
| .digital | $2.57 | $33.47 | 13.0× |
| .world | $2.57 | $33.47 | 13.0× |
| .fun | $2.57 | $31.41 | 12.2× |
| .life | $2.57 | $29.35 | 11.4× |
| .website | $1.96 | $21.11 | 10.8× |
| .live | $2.57 | $26.26 | 10.2× |
| .blog | $2.57 | $21.11 | 8.2× |
| .media | $4.63 | $36.56 | 7.9× |
| .finance | $6.69 | $52.01 | 7.8× |
| .tech | $6.99 | $50.98 | 7.3× |
| .agency | $3.60 | $25.23 | 7.0× |
| .xyz | $2.04 | $14.21 | 7.0× |
| .company | $2.57 | $16.99 | 6.6× |
| .info | $3.60 | $22.14 | 6.2× |
| .health | $10.81 | $62.31 | 5.8× |
| .cloud | $3.88 | $21.11 | 5.4× |
| .email | $5.66 | $25.23 | 4.5× |
| .design | $10.81 | $46.86 | 4.3× |
| .club | $4.12 | $15.96 | 3.9× |
| .biz | $6.69 | $19.05 | 2.9× |
| .studio | $11.84 | $32.44 | 2.7× |
| .news | $9.78 | $26.26 | 2.7× |
| .money | $10.81 | $28.32 | 2.6× |
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
| .movie | $36.56 | $278.58 | 7.6× |
| .watches | $52.01 | $257.98 | 5.0× |
| .realty | $93.20 | $288.88 | 3.1× |
| .creditcard | $5.66 | $129.25 | 22.8× |
| .casino | $7.72 | $129.25 | 16.7× |
| .travel | $15.96 | $118.95 | 7.5× |
| .investments | $8.24 | $103.50 | 12.6× |
| .ceo | $9.78 | $103.50 | 10.6× |
| .doctor | $8.24 | $93.20 | 11.3× |
| .loans | $10.81 | $93.20 | 8.6× |
| .rich | $78.99 | $160.71 | 2.0× |
| .energy | $11.84 | $93.20 | 7.9× |
| .gold | $5.66 | $82.90 | 14.7× |
| .host | $4.63 | $81.87 | 17.7× |

## Changes since the previous snapshot

First snapshot — changes appear from next week.

## Files

- [`data/latest.csv`](data/latest.csv) — the current snapshot
- [`data/snapshots/`](data/snapshots/) — one dated CSV per week, the full history
- Columns: `tld`, `first_year_usd`, `renewal_usd`, `transfer_usd`, `renewal_minus_first_year_usd`, `renewal_to_first_year_ratio`, `first_year_has_coupon`

Updated every Monday by a GitHub Action ([`scripts/snapshot.py`](scripts/snapshot.py)).

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — cite "TLD renewal prices
(github.com/AlonDrilich/tld-renewal-prices)". Code: MIT.

Browse and search the same data at **[namesale.store/renewal-prices](https://namesale.store/renewal-prices)**.
Maintained by [NameSale](https://namesale.store/), a marketplace of brandable domain names where
each listing shows its extension's yearly renewal next to the price.
