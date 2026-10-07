# Independent replication at MaxNb = 42: per-slot totals

The full-window replication (`code/replica_s1.py --full --max 42`, four
slots run in parallel on 2026-08-08) printed one `TOTALE` line per slot
at the end of its run. The stdout redirect of those runs failed (the
redirect file was empty), so these four lines were transcribed by the
author from the terminal scrollback of the four runs (the 127–129 line
from a screenshot). They are reproduced verbatim, in the original
Italian wording printed by the script ("insiemi candidati esaminati" =
candidate sets examined; "con almeno una partizione in righe" = with at
least one row partition):

```
TOTALE: 84948 insiemi candidati esaminati in 36841s; 11084 con almeno una partizione in righe.   [slot S1 112-126]
TOTALE: 76605 insiemi candidati esaminati in 31018s; 13130 con almeno una partizione in righe.   [slot S1 127-129]
TOTALE: 76605 insiemi candidati esaminati in 28984s; 8081  con almeno una partizione in righe.   [slot S1 130-132]
TOTALE: 84948 insiemi candidati esaminati in 30222s; 13690 con almeno una partizione in righe.   [slot S1 133-147]
```

| | examined | with at least one row partition | with a square |
|---|---|---|---|
| four slots | 323,106 | 45,985 | 4 |

Total machine time: 127,065 s (about 35.3 h over four parallel slots).

## Checks

1. **Against the JSON files.** The second number of each line equals the
   number of entries of the corresponding `replica-full-s1_*.json`
   (11,084 / 13,130 / 8,081 / 13,690): the JSON files record only the
   candidates with at least one row partition, 45,985 in all
   (`replica-full-verdetto.log`).
2. **Mirror identity (Remark 4 of the paper).** The map x ↦ 42 − x on the
   omitted 6-subsets of {1, …, 41} (42 belongs to every candidate set)
   sends stratum S1 to stratum 259 − S1 and preserves the candidacy
   conditions, so it pairs the slots 112–126 ↔ 133–147 and 127–129 ↔
   130–132: the examined counts must pair exactly, and they do
   (84,948 = 84,948 and 76,605 = 76,605). The partitionable counts do
   not pair (11,084 ≠ 13,690), as expected, because the map does not
   transport the semi-bimagic structure.
3. **The examined counts are recomputable in seconds** without the
   35-hour run: `code/count_candidates.py` enumerates the candidate sets
   of each slot with the same candidacy conditions and prints the four
   examined totals (`logs/count-candidates.log`).
