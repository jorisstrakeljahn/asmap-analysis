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
vs the RPKI-only run. → Done, see `full-run.md`.

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
as the new AS, 764 times as the old AS).

**Update after full run:** AS834 shows almost identical numbers in the
full run diff (1,409 entries). Since the full run uses the same sources
as the baseline, this confirms AS834's changes are from time drift
(real reassignments), not source disagreements.

## What this means for the dashboard project

After completing the full run (see `full-run.md`), it turns out RPKI and
IRR/Routeviews almost never disagree on the same prefix. So the interesting
dashboard metric is not "source conflicts" but rather **RPKI coverage**:
which ASes and prefixes are only covered by IRR/Routeviews and not yet
by RPKI? Tracking this over time would show RPKI adoption progress.
