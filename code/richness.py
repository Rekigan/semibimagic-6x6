"""L'ipotesi della ricchezza: i 4 vincitori sono i candidati con PIU'
partizioni in righe?  E le 5 classi mod 7 sorelle, come sono andate?

Dati: i 4 JSON della replica --full (tutti i candidati con >=1 partizione,
campo intero S1 112-147, conteggio partizioni per ciascuno).
"""
import json, glob, os

L = os.path.join(os.path.dirname(__file__), "..", "logs")
entries = []
for f in sorted(glob.glob(os.path.join(L, "replica-full-s1_*.json"))):
    with open(f) as fh:
        entries.extend(json.load(fh))

WINNERS = {(19, 20, 21, 22, 23, 24), (4, 11, 18, 25, 32, 39),
           (7, 8, 21, 22, 35, 36), (10, 11, 12, 31, 32, 33)}

# --- le 5 classi mod 7 sorelle (r = 1,2,3,5,6; r=4 e' il vincitore) ---
print("le sei classi mod 7 (omissione dell'intera classe):")
idx = {tuple(e["omette"]): e for e in entries}
for r in (1, 2, 3, 4, 5, 6):
    O = tuple(sorted(r + 7 * k for k in range(6)))
    e = idx.get(O)
    S1 = (903 - sum(O)) // 6
    mirror = "auto-speculare" if r == 4 else f"specchio -> classe {(1 - r) % 7}"
    if e:
        print(f"  r={r}: S1={S1}  partizioni={e['partizioni']:>3}  "
              f"quadrato={'SI' if e['quadrato_esiste'] else 'NO'}   ({mirror})")
    else:
        print(f"  r={r}: S1={S1}  partizioni=  0  (non nel JSON)   ({mirror})")

# --- classifica per ricchezza di partizioni, campo intero ---
entries.sort(key=lambda e: -e["partizioni"])
print(f"\ntop 12 per numero di partizioni (su {len(entries)} candidati):")
for i, e in enumerate(entries[:12]):
    w = "  <-- VINCITORE" if tuple(e["omette"]) in WINNERS else ""
    sym = all((43 - v) in e["omette"] for v in e["omette"])
    print(f"  #{i+1:>2}  partizioni={e['partizioni']:>3}  s1={e['s1']}  "
          f"s2={e['s2']}  omette={e['omette']}  spec={'si' if sym else 'no'}{w}")

ranks = {}
for i, e in enumerate(entries):
    k = tuple(e["omette"])
    if k in WINNERS:
        ranks[k] = (i + 1, e["partizioni"])
print("\nrango dei 4 vincitori nella classifica di ricchezza:")
for k, (rk, p) in sorted(ranks.items(), key=lambda kv: kv[1][0]):
    print(f"  #{rk:>4} su {len(entries)}  (partizioni={p})  omette={list(k)}")

# vincitore piu' povero per partizioni TOTALI: {7,8,21,22,35,36} con 50
poorest = min(p for _, p in ranks.values())
above = [e for e in entries if e["partizioni"] > poorest and
         tuple(e["omette"]) not in WINNERS]
print(f"\nnon-vincitori con piu' partizioni del vincitore piu' povero "
      f"({poorest}): {len(above)}")
print("=> l'ipotesi 'vincono i piu' ricchi' e' "
      + ("FALSA: la ricchezza non basta" if above else "VERA"))
