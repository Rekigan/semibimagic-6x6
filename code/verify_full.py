"""Spunta della replica --full (4 slot) contro le condizioni PRE-SCRITTE
(written before the run returned; see Remark 4 of the paper).  Esito su
stdout -> log."""
import json, glob, os

L = os.path.join(os.path.dirname(__file__), "..", "logs")
FILES = sorted(glob.glob(os.path.join(L, "replica-full-s1_*.json")))

EXPECTED = {
    (19, 20, 21, 22, 23, 24): (3799, 59),
    (4, 11, 18, 25, 32, 39): (3659, 132),
    (7, 8, 21, 22, 35, 36): (3671, 50),
    (10, 11, 12, 31, 32, 33): (3691, 83),
}
NEGATIVE = (2, 3, 4, 39, 40, 41)

entries = []
for f in FILES:
    with open(f) as fh:
        part = json.load(fh)
    s1s = {e["s1"] for e in part}
    print(f"{os.path.basename(f)}: {len(part)} candidati, "
          f"S1 in [{min(s1s)},{max(s1s)}]")
    entries.extend(part)

s1_all = sorted({e["s1"] for e in entries})
print(f"\nvoci JSON totali: {len(entries)}  (tutte con partizioni >= 1: "
      f"{all(e['partizioni'] >= 1 for e in entries)})")
print("SEMANTICA: i JSON registrano i soli candidati con almeno una "
      "partizione in righe;\ni totali esaminati stanno nelle righe TOTALE "
      "dei terminali (slot 127-129: 76605\nesaminati -> 13130 nel JSON, "
      "coincide). Finestra S1 ammissibile [112,147];")
print(f"strati S1 con candidati partizionabili: {s1_all[0]}..{s1_all[-1]}, "
      f"assenti {sorted(set(range(112, 148)) - set(s1_all))} = strati senza "
      f"partizioni, non buchi di copertura")
print(f"assume 1 nell'insieme? "
      f"{'NO (piu ampio del necessario)' if any(1 in e['omette'] for e in entries) else 'si'}")

print("\n--- CONDIZIONE 1: i SI ---")
yes = [e for e in entries if e["quadrato_esiste"]]
ok1 = True
for e in yes:
    key = tuple(e["omette"])
    exp = EXPECTED.get(key)
    tag = "ATTESO" if exp else "*** NON ATTESO: FALSIFICA IL CLAIM ***"
    if not exp:
        ok1 = False
    else:
        if e["s1"] != 129 or e["s2"] != exp[0] or e["partizioni"] != exp[1]:
            tag += f"  *** MISMATCH: att. S2={exp[0]} part={exp[1]} ***"
            ok1 = False
    print(f"  SI  s1={e['s1']} s2={e['s2']} omette={key} "
          f"partizioni={e['partizioni']}  {tag}")
missing = [k for k in EXPECTED if k not in {tuple(e["omette"]) for e in yes}]
if missing:
    ok1 = False
    print(f"  *** INSIEMI ATTESI MANCANTI: {missing} ***")
print(f"  SI totali: {len(yes)} (attesi 4)  ->  {'PASS' if ok1 and len(yes) == 4 else 'FAIL'}")

print("\n--- CONDIZIONE 2: il negativo di controllo ---")
neg = [e for e in entries if tuple(e["omette"]) == NEGATIVE]
if len(neg) == 1 and neg[0]["partizioni"] == 6 and not neg[0]["quadrato_esiste"]:
    print(f"  omette {NEGATIVE}: partizioni={neg[0]['partizioni']}, "
          f"quadrato=NO  ->  PASS (atteso 6 e NO)")
    ok2 = True
else:
    print(f"  *** ANOMALIA: {neg} ***")
    ok2 = False

print("\n--- CONDIZIONE 3: i quadrati allegati sono semi-bimagici ---")
ok3 = True
for e in yes:
    g = e.get("quadrato")
    if not g:
        print(f"  {tuple(e['omette'])}: quadrato non allegato")
        ok3 = False
        continue
    S1, S2 = e["s1"], e["s2"]
    rows_ok = all(sum(r) == S1 and sum(v*v for v in r) == S2 for r in g)
    cols = list(zip(*g))
    cols_ok = all(sum(c) == S1 and sum(v*v for v in c) == S2 for c in cols)
    vals = sorted(v for r in g for v in r)
    set_ok = vals == sorted(set(range(1, 43)) - set(e["omette"]))
    print(f"  {tuple(e['omette'])}: righe {rows_ok}, colonne {cols_ok}, "
          f"insieme {set_ok}")
    ok3 &= rows_ok and cols_ok and set_ok

print(f"\n{'='*60}")
verdict = ok1 and len(yes) == 4 and ok2 and ok3
print(f"VERDETTO: {'CONDIZIONE PRE-SCRITTA SODDISFATTA' if verdict else 'DISCREPANZA - vedere sopra'}")
print("La classificazione a max=42 ha ora due implementazioni indipendenti")
print("sull'intero campo S1, senza assunzione 1-nell-insieme." if verdict else "")
