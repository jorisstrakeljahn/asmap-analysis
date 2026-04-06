# First Kartograf Run (RPKI-only)

**Date:** 2026-04-06
**Epoch:** 1775508222 (2026-04-06 20:43:42 UTC)
**Kartograf:** v0.4.13
**rpki-client:** 9.7
**Setup:** Nix (`nix develop`)

## Results

| Phase | Duration | Details |
|-------|----------|---------|
| RPKI Download | 4:58 | 5 TALs fetched, then `rpki-client` bulk download |
| RPKI Validation | 1:22 | 357,720 ROA files, 1,431 batches |
| RPKI Parsing | 0:16 | 719,680 entries, 111,587 duplicates, 5 invalids |
| Sorting | 0:04 | — |
| **Total** | **6:41** | — |

**Result SHA-256:** `a322704842bd7bea18d1dbd41c46d3f1bec179cb095df6d4f7dc3793755c69f8`

## Observation: No progress feedback during RPKI download

The RPKI download phase (nearly 5 minutes) shows no progress indicator.
The message `"Downloading RPKI Data, this may take a while."` is printed,
then nothing until it finishes.

The validation phase right after _does_ use `tqdm` for progress
(`kartograf/rpki/fetch.py`, line 149). The download phase does not
(same file, lines 88-95) because `rpki-client` runs as an external
subprocess with `capture_output=True`.

Not a bug, but worth noting for dashboard/UX work later.
