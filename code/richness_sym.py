"""Classifica di ricchezza RISTRETTA agli insiemi speculari."""
import json, glob, os

L = os.path.join(os.path.dirname(__file__), "..", "logs")
entries = []
for f in sorted(glob.glob(os.path.join(L, "replica-full-s1_*.json"))):
    entries.extend(json.load(open(f)))

sym = [e for e in entries if all((43 - v) in e["omette"] for v in e["omette"])]
sym.sort(key=lambda e: -e["partizioni"])
print(f"candidati SPECULARI con >=1 partizione: {len(sym)}  "
      f"(su 382 attesi dal middle-number)")
print("top 8 per partizioni (tra gli speculari):")
for i, e in enumerate(sym[:8]):
    w = "  <-- VINCITORE" if e["quadrato_esiste"] else ""
    print(f"  #{i+1}  partizioni={e['partizioni']:>3}  s2={e['s2']}  "
          f"omette={e['omette']}{w}")
winners_ranks = [i + 1 for i, e in enumerate(sym) if e["quadrato_esiste"]]
print(f"\nranghi dei 4 vincitori tra gli speculari: {winners_ranks}")
