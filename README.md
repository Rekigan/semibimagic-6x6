# The smallest semi-bimagic square of order six — code and data

Code, raw logs and data supporting the paper

> Luca Cipolletta, *The smallest semi-bimagic square of order six*,
> preprint, Zenodo, 2026. https://doi.org/10.5281/zenodo.23024029

(the published PDF, version 1.0.0, is in `paper/`; `paper/main.tex` is its
source, see "Paper" below).

## The result in one paragraph

A 6×6 array of distinct positive integers is *semi-bimagic* if all rows and
all columns have the same sum S1 and the same sum of squares S2 (diagonals
free). Pfeffermann's square of 1894 uses entries up to 49. By exhaustive
enumeration, the smallest possible largest entry is **42**: such squares
exist with entries in [1, 42] and none exists with entries in [1, 41]. At
the optimum S1 = 129 is forced and exactly four 36-element sets admit a
square (S2 = 3659, 3671, 3691, 3799), all closed under x ↦ 43 − x. Every
exclusion 36–41 is confirmed by two algorithms with different hypotheses,
and the classification at 42 by two independent implementations over the
full admissible window S1 ∈ [112, 147].

## Requirements

Python 3 (tested with 3.9), standard library only. Run every command from
the repository root, e.g. `python code/verify_full.py`. Most scripts print
to stdout, captured with a redirect (`> logs/<name>`); the scripts of the
Section 7 table write their own log into `logs/`, and
`dump_partitions.py`, `middle.py` and `replica_s1.py` also write the data
or JSON files named in the tables.

## Layout

```
code/    enumeration and checking scripts (MIT License)
logs/    raw outputs of the runs cited in the paper (CC BY 4.0)
data/    machine-readable partitions of the optimal sets (CC BY 4.0)
paper/   the published PDF (v1.0.0) and its LaTeX source
MANIFEST-SHA256.txt   SHA-256 of every file in logs/, data/ and paper/
```

## From claims to files

Times are wall-clock on an ordinary laptop; the long runs were not repeated
for this release (their logs are the original outputs).

### Minimality and classification (Sections 4–5, Theorems 2–3)

| claim | command | log / output | time |
|---|---|---|---|
| MaxNb 36–38 excluded, set-sweep (no translation lemma) | `code/set_sweep.py 38 36` | `logs/blim3yxim.output` | ~7 min |
| MaxNb 36 excluded, bucket algorithm | `code/bucket_sweep.py 36 36` | `logs/groups36.log` | 2 s |
| MaxNb 36, brute-force sextets cross-check | `code/verify36.py` | `logs/verify36.log` | ~1 s |
| MaxNb 37–38 excluded, bucket | `code/bucket_sweep.py 37 38` | `logs/bn0vyvt60.output` | ~3 min |
| MaxNb 39 excluded, set-sweep / bucket | `code/set_sweep.py 39 39` / `code/bucket_sweep.py 39 39` | `logs/b62iegrr5.output` / `logs/groups39.log` | 11 min / 4 min |
| MaxNb 40–41 excluded, set-sweep (82,251 and 658,008 sets) | `code/set_sweep.py 41 40` | `logs/bz9px7zym.output` | ~7 h |
| MaxNb 40–41 excluded and first square at 42, bucket | `code/bucket_sweep.py 40 48` (stops at the first square) | `logs/bjzvtqu5c.output` | ~2.3 h |
| S1 = 129 forced at 42 (phase 1), all solutions mirror-closed (phase 2) | `code/centred.py` | `logs/b5zmw01yv.output` | ~4 h |
| the four sets: 24 extendable row partitions (8 / 8 / 4 / 4), all mirror-closed | `code/phase2.py` | `logs/b7x4hoknj.output` | ~1 h |
| independent replication, full window S1 ∈ [112, 147] | `code/replica_s1.py --full --max 42 --s1lo 112 --s1hi 126` (and 127–129, 130–132, 133–147) | `logs/replica-full-s1_*.json` (4 files) | ~8–10 h per slot |
| replication checked against the pre-registered conditions (four YES, negative control, squares valid) | `code/verify_full.py` | `logs/replica-full-verdetto.log` | 1 s |
| per-slot examined totals (84,948 / 76,605 / 76,605 / 84,948) and their mirror identity | `code/count_candidates.py` | `logs/count-candidates.log`, `logs/replica-full-totals.md` | 20 s |
| the 324 row partitions of the four sets (132 + 50 + 83 + 59), 24 extendable, as a machine-readable list (+ the 3459 negative control) | `code/dump_partitions.py` (writes `data/partitions-max42.json`) | `logs/dump-partitions.log` | 20 s |

### The squares, the collapse, Remark 20 (Sections 3, 5, 6, 8)

| claim | command | log / output | time |
|---|---|---|---|
| the S2-minimal square (42, 129, 3659) and its check | `code/best3659.py` | `logs/best3659.log` | 1 s |
| the (42, 129, 3799) square and the 26/28 square, checked by a checker calibrated on four historical squares (Pfeffermann, Boyer, Wroblewski, Morgenstern) | `code/verify42.py`, `code/verify26.py` (checker: `code/records.py`) | `logs/verify42.log`, `logs/verify26.log` | 1 s |
| 546 → 546 → 382 → 4 in the symmetric class | `code/middle.py` (writes `data/middle-number.json`) | `logs/bmlofdsyf.output` | ~11 min |
| 546 symmetric candidates, the 3459 negative control | `code/check_symmetric_candidates.py` | `logs/check-symmetric-candidates.log` | 1 s |
| residue class 4 (mod 7): S1(r) = 133 − r, S2(r) = 3815 − 35r − r² | `code/formula_check.py` | `logs/formula-check.log` | 1 s |
| Proposition 5 (lifting of the mirror symmetry): σ-orbits of the orthogonal pairs | `code/twin.py`, `code/sigma2.py` | `logs/twin-sigma.log`, `logs/sigma-struttura.log` | 3 s |
| Proposition 5, every orbit checked explicitly (plain and transposed complements) | `code/verify_lifting.py` | `logs/verify-lifting.log` | 3 s |
| Remark 20: richness does not decide survival (197, 326, ranks 1/8/18/24) | `code/richness.py`, `code/richness_sym.py` | `logs/richness.log`, `logs/richness-sym.log` | 1 s |

### Twin triples and the free census (Section 7)

| claim | command (writes its own log) | log | time |
|---|---|---|---|
| twin census, realization check, exhaustive 32,400 sweep | `code/seduta_g.py` | `logs/seduta-g.log` | 9 s |
| the 1,200-pair dichotomy | `code/selezione_j3.py` | `logs/selezione-j3.log` | 3 s |
| pre-registered shuffle (3,600 pairings) | `code/m5_predizioni.py` | `logs/m5-predizioni.log` | 5 s |
| wide screen: 388,800 pairings, no pairing solves both systems | `code/screen_388800.py` (stdout) | `logs/screen-388800.log` | 2 min |
| independent re-implementation of the bijection check | `code/terza_biunivocita.py` | `logs/terza-biunivocita.log` | 12 s |
| the 1,078-pair uniqueness screen | `code/terza_vaglio_unicita.py` | `logs/terza-vaglio-unicita.log` | 5 s |
| case-analysis census (Proposition 18) | `code/residuo_ab.py` | `logs/residuo-ab.log` | 5 s |
| free census over [1, 22] and refutation sweep | `code/fresco_vaglio.py`, `code/fresco_excl.py` | `logs/fresco-vaglio.log`, `logs/fresco-excl.log` | 15 s each |
| four-twin census to N = 26: incidence forms and alignment | `code/invariante_156.py`, `code/invariante_n24.py`, `code/salita_n26.py` | `logs/invariante-156.log`, `logs/invariante-n24.log`, `logs/salita-n26.log` | 10–25 s each |
| the quadruple generator | `code/halfsum_generatore.py` | `logs/halfsum-generatore.log` | 1 s |
| the abstract-model alignment tables | `code/modello_tabella_fine.py` | `logs/modello-tabella-fine.log` | 2 s |
| complementation check at \|G\| = 2 | `code/cintura_finale.py` | `logs/cintura-finale.log` | 7 s |

Shared module: `code/semibimagic.py` (sextet enumeration, row partitions,
column extension).

## About the logs

- **Original raw outputs.** Every log cited by name in the paper is the
  original output of its run, byte for byte; the SHA-256 of each file is in
  `MANIFEST-SHA256.txt`. The opaque names (`b5zmw01yv.output`, …) are the
  task identifiers of the original runs, cited in the paper's tables, and
  are kept unchanged.
- **Language.** The original runs were documented in Italian: many script
  headers and log banners are Italian, and they mention internal notebook
  entries (session names, section numbers such as "8.15", "verbale") that
  are not part of this release. Nothing in them is needed to run or check
  the code.
- **Added for this release (2026-10-07).** Some results of the paper had a
  script but no stored output; their logs were generated for this release
  from the scripts in `code/`: `best3659.log`, `verify42.log`,
  `verify26.log`, `formula-check.log`, `richness.log`, `richness-sym.log`,
  `dump-partitions.log`, `verify-lifting.log`; `check-symmetric-candidates.log`
  replaces an earlier output of the same check whose wording referred to
  internal notes (the numbers are unchanged). Two scripts are new:
  `screen_388800.py` re-creates the wide exclusion screen of Section 7 (the
  original screen was run ad hoc with the same `hom_aff` routine as
  `m5_predizioni.py` and not kept as a script), and `count_candidates.py`
  recomputes the per-slot totals of the replication.
  `replica-full-totals.md` records the four final lines of the replication
  runs, whose stdout redirect had failed.
- **Re-run check for this release.** All scripts that run in under a few
  minutes were re-run from a clean copy of this repository and their output
  compared line by line with the stored logs, machine-time figures
  excluded: identical everywhere, except one line in each of
  `invariante-n24.log` and `salita-n26.log` that reports a ratio of
  measured running times. The data files regenerated by
  `dump_partitions.py` and `middle.py` are identical to those in `data/`.
  The multi-hour runs were not repeated.
- **Changes to the scripts for this release.** Absolute local paths were
  replaced by paths relative to the script (eight scripts), and
  `dump_partitions.py` prints the relative path of the file it writes.
  Wording that referred to internal notes was made neutral, without
  touching any computation: the docstrings of `verify_full.py` and
  `replica_s1.py`, and the printed reference lines of `dump_partitions.py`
  and of `check_symmetric_candidates.py` (renamed from an internal name).
  `verify_lifting.py` is the independent check written on 2026-08-08, with
  an English first line. No other change. Script headers that are echoed
  into the original logs were left as they are, so that a re-run
  reproduces those logs.

## Paper

`paper/smallest-semibimagic-square-order-six-v1.0.0.pdf` is identical to
the file of the Zenodo record (MD5 1bdca3e517382823486b0bbc215bec77). Its
Data availability section still shows the placeholder "[REPOSITORY]";
`paper/main.tex` is the same source with editorial comments removed, the
placeholder replaced by the address of this repository, one sentence
pointing to this README and a statement on the use of AI tools, for the
next version of the record.

## Use of AI tools

The computations and the writing of the code in this repository were
done with AI tools, under the direction and verification of the author.

## Citation, license, contact

Please cite the paper (see `CITATION.cff`). Code: MIT License. Logs, data
and paper: CC BY 4.0. See `LICENSE`.

Contact: Luca Cipolletta, OGS@Noiellelab.com.
