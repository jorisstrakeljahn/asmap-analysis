# Full Kartograf Run (RPKI + IRR + Routeviews)

**Date:** 2026-04-06
**Epoch:** 1775509338 (2026-04-06 21:02:18 UTC)
**Kartograf:** v0.4.13
**rpki-client:** 9.7
**Setup:** Nix (`nix develop`)

## Results

| Phase | Duration | Details |
|-------|----------|---------|
| RPKI Download | 5:01 | Same 5 TALs as before |
| RPKI Validation | 1:36 | 357,734 ROA files |
| RPKI Parsing | 0:17 | 719,694 entries, 111,587 dupes, 5 invalids |
| IRR Parsing | 0:55 | 2,020,573 unique entries from all 5 RIRs |
| RPKI + IRR Merge | 1:35 | — |
| Routeviews Parsing | 0:21 | 1,336,942 entries |
| Routeviews Merge | 1:25 | — |
| Sorting | 0:04 | — |
| **Total** | **11:55** | — |

**Final entries:** 1,352,588 (vs 719,680 RPKI-only)
**Result SHA-256:** `5b4c87fd988b0e5f169fd63b4e85c48dc0c28c35483dd2ba718a433f251b2c5c`

## Comparison of all three diffs

| Comparison | Diff entries | Meaning |
|------------|-------------|---------|
| RPKI-only vs baseline (Mar 5) | 16,821 | Source difference + time drift (mixed) |
| Full run vs baseline (Mar 5) | 20,100 | Time drift only (same sources, ~1 month apart) |
| Full run vs RPKI-only | 316,863 | Source difference only (same day, ~20 min apart) |

## Key finding: RPKI and IRR/Routeviews almost never disagree

The diff between the full run and the RPKI-only run (same day, ~20 min
apart) shows:

- **316,862 entries only in the full run** (prefixes covered by IRR/Routeviews
  but not by RPKI — these are the coverage gaps that the additional sources fill)
- **1 actual reassignment** where both maps have the same prefix but
  mapped to a different AS: `82.39.232.0/23 AS20326 # was AS834`

This means: when RPKI covers a prefix, IRR and Routeviews almost always
agree with it. The sources complement each other (fill coverage gaps)
rather than contradict each other.

The RPKI download hashes between the two runs are different (20 min
apart), confirming that RPKI repositories update continuously. But
the practical impact is tiny — only 14 additional ROA files appeared,
and the resulting map changed by 1 entry.

## AS834 (SaskTel) is consistently the biggest mover

AS834 appears as the top changed AS in both diffs against the baseline:
- 1,399 entries in the RPKI-only diff
- 1,409 entries in the full run diff

The nearly identical count despite different source sets means these
changes are from the time difference (March → April), not from
source disagreements. A large block of address space was reassigned
to/from SaskTel in the past month.

## Source contribution breakdown

| Source | Raw entries | After merge |
|--------|------------|-------------|
| RPKI | 719,694 | 719,694 (base) |
| IRR | 2,020,573 | fills gaps only |
| Routeviews | 1,336,942 | fills remaining gaps |
| **Final** | — | **1,352,588** |

The jump from 719k to 1.35M shows that IRR and Routeviews add ~633k
prefixes that RPKI doesn't cover. They almost never override RPKI.

## What this means for the dashboard

The top ASes in the "only in file1" section of the full-vs-RPKI diff
are the prefixes that IRR/Routeviews contribute but RPKI doesn't cover.
The biggest are AS4134 (China Telecom), AS174 (Cogent), AS3549 (Level3)
— large networks that haven't fully adopted RPKI yet. Tracking RPKI
adoption per-AS over time would be a valuable dashboard metric.
