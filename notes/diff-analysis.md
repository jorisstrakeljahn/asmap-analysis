# Diff: RPKI-only run vs March 2026 baseline

**My run:** 2026-04-06 (epoch 1775508222), RPKI-only, unfilled
**Baseline:** 2026-03-05 (epoch 1772726400), all sources, filled
**Tool:** `asmap-tool.py diff -i` (`-i` ignores unassigned ranges since my map is unfilled)

## Summary

- **16,821 differences** (13,113 IPv4 + 3,708 IPv6)
- My RPKI-only map has **719,680 entries**
- Baseline has **399,450 entries** (after decode)

## Interpretation

The large number of differences is expected. Two things are being compared
at once:

1. **Source difference**: My map uses only RPKI. The baseline uses RPKI + IRR
   + Routeviews. Where RPKI has no data for a prefix, the baseline fills it
   from IRR/Routeviews. Where RPKI disagrees with IRR/Routeviews, my map
   shows the RPKI answer.

2. **Time difference**: ~1 month apart. Prefixes get reassigned, new ROAs
   are published, old ones expire.

Separating these two effects would require a same-day full run (`./run map -irr -rv`)
vs the RPKI-only run.

## Top changed ASes

Most frequent AS on my RPKI side of the diff:

| AS | Count | Who |
|----|-------|-----|
| AS834 | 1,399 | SaskTel (Canada) |
| AS19905 | 558 | NTT South Africa |
| AS31713 | 394 | BEMTA (Turkey) |
| AS6939 | 300 | Hurricane Electric |
| AS22516 | 259 | Vivo (Brazil) |
| AS3257 | 228 | GTT Communications |

AS834 stands out — it appears most on both sides of the diff (1,399 times
as the new AS, 764 times as the old AS). This suggests a large block of
address space where RPKI and IRR/Routeviews disagree about ownership.

## What this means for the dashboard project

A useful dashboard metric: **breakdown of diff by source**. If Kartograf
tagged each entry with its source (RPKI/IRR/Routeviews), diffs could show
"these 800 changes are because RPKI disagrees with IRR" vs "these 200
changes are genuine reassignments over time". Currently that information
is lost in the final output.
