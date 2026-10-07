"""SEDUTA INVARIANTE 156x32 — censimento indipendente delle coppie
|G|=4 di [1..22]: carta d'identita (Bersaglio 1) e invariante del 32
(Bersaglio 2). MISURA, non teoria. Codice NUOVO, non riuso di
fresco_excl.py: censimento diretto a N=22 (ogni coppia same-bucket di
[1..N] con N<=22 e coppia di [1..22], quindi il livello 22 e
esaustivo), G contato per bucket di invarianti delle terne, non per
doppio ciclo con uguaglianze.

FACCE PRE-SCRITTE (stampate qui, prima di ogni calcolo):
 B1-a: atteso dal quadro: matrice d'incidenza congiunta (lato A, lato
       B, gemelle appaiate) IDENTICA a meno di rietichettatura delle
       4 gemelle su tutte le 156 coppie; se anche UNA differisce, la
       classe comune per incidenza e FALSIFICATA e si verbalizza coi
       membri.
 B1-b: distribuzione di (s1,s2) e taglie dei bucket a verbale
       (descrittiva, nessun atteso vincolante).
 B2-a: ri-misura indipendente del vaglio S1: OGNI coppia |G|=4 da
       ESATTAMENTE {misti 32, solo-N3 40, solo-N2 488, nulli 160} su
       720; una coppia con firma diversa FALSIFICA l'uniformita coi
       membri a verbale.
 B2-b (TEST pre-scritto): il conteggio dei misti e FUNZIONE della
       sola matrice d'incidenza normalizzata? Operativamente:
       (i) coppie reali con la stessa incidenza canonica devono avere
       gli stessi conteggi; (ii) il MODELLO ASTRATTO costruito dalla
       SOLA incidenza canonica (punti 0..5 senza aritmetica) deve
       riprodurre i conteggi contando le 720 biiezioni, su TUTTE le
       realizzazioni enumerate dell'incidenza. Se si, l'invariante
       candidato e l'incidenza e il 32 SI DERIVA da essa per
       conteggio (aritmetica finita); se no, controesempio coi
       membri. Idem per 40/488/160 (stesso costo).
 B2-c: struttura dei 32 misti (descrittiva): vettori k per gemella,
       tabella (kg,kh) su 720, gruppo di simmetria congiunto della
       configurazione, orbite dei misti, stabilizzatori,
       fattorizzazione del 32; ritratto orbitale confrontato su tutte
       le 156.
Log: logs/invariante-156.log
"""
import os
import time
from itertools import combinations, permutations
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "..", "logs")
OUT = []


def P(msg=""):
    OUT.append(msg)
    print(msg, flush=True)


P(__doc__)

P("SPECIFICA VERIFICATA (segni e convenzioni, prima del primo run):")
P("  bucket key = (s1, s2) = (somma, somma dei quadrati) della sestina")
P("  gemella = (TA, TB): TA in A, TB in B, |TA|=|TB|=3,")
P("            somma(TA) = somma(TB) e somma quadrati(TA) = (TB)")
P("  |G| = numero di gemelle; base = coppie DISGIUNTE same-bucket")
P("  accoppiamento = biiezione psi: A -> B, una per permutazione (720)")
P("  k(gemella) = |psi(TA) intersecato TB|; N3 = #{gemelle con k=3},")
P("  N2 = #{gemelle con k=2}; classi: misto (N3>0 e N2>0),")
P("  solo-N3 (N3>0, N2=0), solo-N2 (N2>0, N3=0), nullo (0,0)")
P("  cella (a,b) normalizzata = min((a,b), (3-a,3-b))")
P("  multiset con Counter; MAI sorted su collezioni di frozenset")
P("  (ordinamenti solo su tuple di interi, deterministici)")
P()

# ------------------------------------------------------------------
P("=" * 68)
P("CENSIMENTO INDIPENDENTE a N=22 (base coi membri)")
P("=" * 68)
t0 = time.time()
N = 22
bucket = defaultdict(list)
for S in combinations(range(1, N + 1), 6):
    bucket[(sum(S), sum(v * v for v in S))].append(S)
nsest = sum(len(v) for v in bucket.values())


def inv3(T):
    return (T[0] + T[1] + T[2], T[0] * T[0] + T[1] * T[1] + T[2] * T[2])


tripledict = {}


def triples_of(S):
    d = tripledict.get(S)
    if d is None:
        d = defaultdict(list)
        for T in combinations(S, 3):
            d[inv3(T)].append(T)
        tripledict[S] = d
    return d


dist_G = Counter()
q4 = []
npairs = 0
for key in sorted(bucket):
    lst = bucket[key]
    if len(lst) < 2:
        continue
    for A, B in combinations(lst, 2):
        if set(A) & set(B):
            continue
        npairs += 1
        dA = triples_of(A)
        dB = triples_of(B)
        g = 0
        for kk, TAs in dA.items():
            TBs = dB.get(kk)
            if TBs:
                g += len(TAs) * len(TBs)
        dist_G[g] += 1
        if g == 4:
            gem = []
            for kk, TAs in dA.items():
                TBs = dB.get(kk)
                if TBs:
                    for TA in TAs:
                        for TB in TBs:
                            gem.append((TA, TB))
            q4.append((key, A, B, gem))

P(f"sestine di [1..22]: {nsest} (atteso C(22,6) = 74613)")
P(f"bucket: {len(bucket)}; coppie disgiunte same-bucket: {npairs}")
P(f"distribuzione |G|: {dict(sorted(dist_G.items()))}")
P(f"coppie |G|=4: {len(q4)}")

# ricontrollo per appartenenza: |G| ricalcolato col doppio ciclo
# diretto (secondo metodo) su TUTTE le coppie |G|=4
anom = 0
for key, A, B, gem in q4:
    g2 = 0
    for TA in combinations(A, 3):
        for TB in combinations(B, 3):
            if inv3(TA) == inv3(TB):
                g2 += 1
    if g2 != 4 or len(gem) != 4:
        anom += 1
        P(f"  <<< ANOMALIA: A={list(A)} B={list(B)} g2={g2}")
P(f"ricontrollo doppio-ciclo su {len(q4)} coppie: anomalie {anom}")

# appartenenza dei due membri documentati (8.16)
attesi = [((1, 3, 9, 10, 11, 14), (2, 5, 6, 7, 13, 15)),
          ((7, 11, 12, 16, 17, 21), (8, 9, 13, 15, 19, 20))]
presenti = {frozenset((A, B)) for key, A, B, gem in q4}
for pa, pb in attesi:
    c = frozenset((pa, pb)) in presenti
    P(f"membro documentato A={list(pa)} B={list(pb)}: "
      + ("PRESENTE" if c else "<<< ASSENTE"))
P(f"[censimento: {time.time()-t0:.1f}s]")
P()

# ------------------------------------------------------------------
P("=" * 68)
P("BERSAGLIO 1 — CARTA D'IDENTITA: gemelle, complementi, incidenza")
P("=" * 68)
t0 = time.time()


def comp(S, T):
    return tuple(v for v in S if v not in T)


def canon_joint(MA, MB):
    best = None
    for p in permutations(range(4)):
        t = (tuple(tuple(MA[p[i]][p[j]] for j in range(4))
                   for i in range(4)),
             tuple(tuple(MB[p[i]][p[j]] for j in range(4))
                   for i in range(4)))
        if best is None or t < best:
            best = t
    return best


def canon_side(M):
    best = None
    for p in permutations(range(4)):
        t = tuple(tuple(M[p[i]][p[j]] for j in range(4)) for i in range(4))
        if best is None or t < best:
            best = t
    return best


carte = []
viol_compl = 0
viol_dist = 0
for key, A, B, gem in q4:
    gset = set(gem)
    chiuso = all((comp(A, TA), comp(B, TB)) in gset for TA, TB in gem)
    if not chiuso:
        viol_compl += 1
        P(f"  <<< CHIUSURA COMPLEMENTO VIOLATA: A={list(A)} B={list(B)}")
    latiA = [TA for TA, TB in gem]
    latiB = [TB for TA, TB in gem]
    distinti = (len(set(latiA)) == 4 and len(set(latiB)) == 4)
    if not distinti:
        viol_dist += 1
        P(f"  <<< LATI NON DISTINTI: A={list(A)} B={list(B)}")
    # ordinamento deterministico: g = gemella con lato A lex-minimo;
    # h = lex-minima delle restanti (tuple di interi, niente frozenset)
    gemS = sorted(gem)
    g0 = gemS[0]
    g0b = (comp(A, g0[0]), comp(B, g0[1]))
    resto = [x for x in gemS if x != g0 and x != g0b]
    h0 = resto[0]
    h0b = (comp(A, h0[0]), comp(B, h0[1]))
    ordg = [g0, g0b, h0, h0b]
    if Counter(ordg) != Counter(gem):
        P(f"  <<< ORDINAMENTO INCOERENTE: A={list(A)} B={list(B)}")
    MA = [[len(set(ordg[i][0]) & set(ordg[j][0])) for j in range(4)]
          for i in range(4)]
    MB = [[len(set(ordg[i][1]) & set(ordg[j][1])) for j in range(4)]
          for i in range(4)]
    a_i = MA[0][2]
    b_i = MB[0][2]
    cella = min((a_i, b_i), (3 - a_i, 3 - b_i))
    carte.append({"key": key, "A": A, "B": B, "ordg": ordg,
                  "MA": MA, "MB": MB, "a": a_i, "b": b_i,
                  "cella": cella,
                  "cj": canon_joint(MA, MB),
                  "cA": canon_side(MA), "cB": canon_side(MB)})

P(f"chiusura per complemento: violazioni {viol_compl} su {len(q4)}")
P(f"lati (4 terne distinte per lato): violazioni {viol_dist}")
P()

# faccia B1-a: forme canoniche
cjs = Counter(c["cj"] for c in carte)
cAs = Counter(c["cA"] for c in carte)
cBs = Counter(c["cB"] for c in carte)
celle = Counter(c["cella"] for c in carte)
P(f"forme canoniche CONGIUNTE distinte: {len(cjs)} "
  f"(molteplicita: {sorted(cjs.values(), reverse=True)})")
P(f"forme canoniche per lato A: {len(cAs)}; per lato B: {len(cBs)}")
P(f"celle (a,b) normalizzate: {dict(sorted(celle.items()))}")
for cj, m in sorted(cjs.items()):
    P(f"  forma congiunta (x{m}):")
    P(f"    lato A: {cj[0]}")
    P(f"    lato B: {cj[1]}")
P("FACCIA B1-a: " + ("incidenza congiunta IDENTICA a meno di "
  "rietichettatura su tutte le coppie — classe comune per incidenza "
  "NON falsificata" if len(cjs) == 1 else
  "<<< PIU FORME DISTINTE: classe comune per incidenza FALSIFICATA, "
  "membri a verbale sopra"))
P()

# faccia B1-b: distribuzione (s1,s2) e taglie bucket
kct = Counter(c["key"] for c in carte)
P(f"bucket coinvolti: {len(kct)}; coppie per bucket: "
  f"{dict(Counter(kct.values()))}  [chiave = coppie nel bucket]")
P(f"s1 range: {min(k[0] for k in kct)}..{max(k[0] for k in kct)}; "
  f"s2 range: {min(k[1] for k in kct)}..{max(k[1] for k in kct)}")
P("distribuzione (s1,s2) -> (coppie |G|=4, taglia bucket a N=22):")
for k in sorted(kct):
    P(f"  {k}: ({kct[k]}, {len(bucket[k])})")
P(f"[B1: {time.time()-t0:.1f}s]")
P()

# ------------------------------------------------------------------
P("=" * 68)
P("BERSAGLIO 2 — SWEEP 720 PER COPPIA: firma, vettori k, tabella")
P("=" * 68)
t0 = time.time()

FIRMA_S1 = Counter({"solo-N2": 488, "nullo": 160, "solo-N3": 40,
                    "misto": 32})


def sweep(A, B, ordg):
    Al = list(A)
    TAs = [set(t[0]) for t in ordg]
    TBs = [set(t[1]) for t in ordg]
    cnt = Counter()
    kvec = Counter()
    cviol = 0
    misti = []
    for q in permutations(B):
        ks = []
        for i in range(4):
            TAi = TAs[i]
            TBi = TBs[i]
            k = 0
            for j in range(6):
                if Al[j] in TAi and q[j] in TBi:
                    k += 1
            ks.append(k)
        if ks[0] != ks[1] or ks[2] != ks[3]:
            cviol += 1
        n3 = sum(1 for k in ks if k == 3)
        n2 = sum(1 for k in ks if k == 2)
        if n3 > 0 and n2 > 0:
            cl = "misto"
            misti.append(q)
        elif n3 > 0:
            cl = "solo-N3"
        elif n2 > 0:
            cl = "solo-N2"
        else:
            cl = "nullo"
        cnt[cl] += 1
        kvec[tuple(ks)] += 1
    return cnt, kvec, cviol, misti


firme_diverse = 0
kvec_forme = Counter()
compl_viol_tot = 0
sweep_res = []
for c in carte:
    cnt, kvec, cviol, misti = sweep(c["A"], c["B"], c["ordg"])
    sweep_res.append((cnt, kvec, misti))
    compl_viol_tot += cviol
    if sum(cnt.values()) != 720:
        P(f"  <<< SOMMA NON 720: A={list(c['A'])} B={list(c['B'])}")
    if cnt != FIRMA_S1:
        firme_diverse += 1
        P(f"  <<< FIRMA DIVERSA: A={list(c['A'])} B={list(c['B'])} "
          f"{dict(cnt)}")
    kvec_forme[tuple(sorted(kvec.items()))] += 1

P(f"coppie con firma diversa da {dict(FIRMA_S1)}: {firme_diverse} "
  f"su {len(carte)}")
P("FACCIA B2-a: " + ("firma {misti 32, solo-N3 40, solo-N2 488, "
  "nulli 160} RI-MISURATA IDENTICA su tutte le coppie (vaglio S1 "
  "riprodotto con codice indipendente)" if firme_diverse == 0 else
  "<<< UNIFORMITA FALSIFICATA, membri a verbale sopra"))
P(f"gemelle complementari con k uguale: violazioni {compl_viol_tot} "
  f"su {720*len(carte)} (aritmetica del complemento: attesa 0)")
P(f"firme FINI (Counter dei vettori k) distinte: {len(kvec_forme)}")
if len(kvec_forme) == 1:
    kv = list(kvec_forme)[0]
    P("  firma fine unica; tabella (kg,kh) su 720 [kg = k della "
      "coppia {g,gbar}, kh = k della coppia {h,hbar}]:")
    tab = {}
    for ks, n in kv:
        tab[(ks[0], ks[2])] = tab.get((ks[0], ks[2]), 0) + n
    P("        kh=0   kh=1   kh=2   kh=3")
    for kg in range(4):
        riga = "  ".join(f"{tab.get((kg, kh), 0):5d}" for kh in range(4))
        P(f"  kg={kg}  {riga}")
    m_ = tab.get((3, 2), 0) + tab.get((2, 3), 0)
    n3_ = (tab.get((3, 0), 0) + tab.get((3, 1), 0) + tab.get((0, 3), 0)
           + tab.get((1, 3), 0) + tab.get((3, 3), 0))
    n2_ = (tab.get((2, 0), 0) + tab.get((2, 1), 0) + tab.get((0, 2), 0)
          + tab.get((1, 2), 0) + tab.get((2, 2), 0))
    nul_ = sum(n for (kg, kh), n in tab.items()
               if kg not in (2, 3) and kh not in (2, 3))
    P(f"  ricontrollo per appartenenza dalla tabella: misti {m_}, "
      f"solo-N3 {n3_}, solo-N2 {n2_}, nulli {nul_} (somma "
      f"{m_+n3_+n2_+nul_})")
P(f"[B2 sweep: {time.time()-t0:.1f}s]")
P()

# ------------------------------------------------------------------
P("-" * 68)
P("B2-c — STRUTTURA: gruppo di simmetria congiunto e orbite dei misti")
P("-" * 68)
t0 = time.time()


def aut_side(S, tris):
    frs = [frozenset(t) for t in tris]
    idx = {f: i for i, f in enumerate(frs)}
    Sl = list(S)
    auts = []
    for p in permutations(Sl):
        m = dict(zip(Sl, p))
        pi = []
        ok = True
        for i in range(4):
            im = frozenset(m[x] for x in frs[i])
            jj = idx.get(im)
            if jj is None:
                ok = False
                break
            pi.append(jj)
        if ok:
            auts.append((m, tuple(pi)))
    return auts


def orbite_misti(c, misti):
    A, B = c["A"], c["B"]
    autA = aut_side(A, [t[0] for t in c["ordg"]])
    autB = aut_side(B, [t[1] for t in c["ordg"]])
    byA = defaultdict(list)
    for m, pi in autA:
        byA[pi].append(m)
    byB = defaultdict(list)
    for m, pi in autB:
        byB[pi].append(m)
    joint = []
    for pi, mas in byA.items():
        if pi in byB:
            for ma in mas:
                ainv = {v: k for k, v in ma.items()}
                for mb in byB[pi]:
                    joint.append((ainv, mb))
    Al = list(A)
    posA = {x: j for j, x in enumerate(Al)}
    mset = set(misti)
    fuori = 0
    seen = set()
    taglie = []
    for q in misti:
        if q in seen:
            continue
        orb = set()
        for ainv, mb in joint:
            q2 = tuple(mb[q[posA[ainv[x]]]] for x in Al)
            orb.add(q2)
        fuori += len(orb - mset)
        orb &= mset
        seen |= orb
        taglie.append(len(orb))
    return (len(autA), len(autB), len(joint), tuple(sorted(taglie)),
            fuori)


ritratti = Counter()
for c, (cnt, kvec, misti) in zip(carte, sweep_res):
    r = orbite_misti(c, misti)
    ritratti[r] += 1
P(f"ritratti orbitali distinti su {len(carte)} coppie: {len(ritratti)}")
for r, m in sorted(ritratti.items()):
    nA, nB, nJ, taglie, fuori = r
    P(f"  (x{m}) |Aut_A|={nA} |Aut_B|={nB} |congiunto|={nJ} "
      f"orbite misti {list(taglie)} fuori-misti {fuori}")
    if len(taglie) > 0 and nJ > 0:
        stab = [nJ // t for t in taglie]
        P(f"        stabilizzatori per orbita: {stab}; "
          f"32 = " + " + ".join(str(t) for t in taglie))
P(f"[B2-c: {time.time()-t0:.1f}s]")
P()

# coppia campione: dettaglio dei 32 misti
camp = None
for c, res in zip(carte, sweep_res):
    if c["A"] == (1, 3, 9, 10, 11, 14):
        camp = (c, res)
        break
if camp is None:
    camp = (carte[0], sweep_res[0])
c, (cnt, kvec, misti) = camp
P(f"COPPIA CAMPIONE: A={list(c['A'])} B={list(c['B'])} "
  f"key={c['key']}")
for nome, gg in zip(("g   ", "gbar", "h   ", "hbar"), c["ordg"]):
    P(f"  {nome}: A-lato {list(gg[0])}  B-lato {list(gg[1])}  "
      f"inv {inv3(gg[0])}")
P(f"  a=|gA int hA|={c['a']}  b=|gB int hB|={c['b']}  "
  f"cella {c['cella']}")
P(f"  firma: {dict(cnt)}")
P("  i 32 misti (q = immagine di A ordinata; ks per gemella "
  "g,gbar,h,hbar):")
Al = list(c["A"])
TAs = [set(t[0]) for t in c["ordg"]]
TBs = [set(t[1]) for t in c["ordg"]]
for q in misti:
    ks = []
    for i in range(4):
        k = sum(1 for j in range(6) if Al[j] in TAs[i] and q[j] in TBs[i])
        ks.append(k)
    P(f"    {list(q)}  ks={ks}")
P()

# ------------------------------------------------------------------
P("-" * 68)
P("B2-b — MODELLO ASTRATTO DALLA SOLA INCIDENZA (test pre-scritto)")
P("-" * 68)
t0 = time.time()

if len(cjs) == 1:
    MAc, MBc = list(cjs)[0]

    def realizzazioni(M):
        # tutte le quaterne ordinate di terne di {0..5} con matrice
        # d'incidenza M (T2 e T4 forzati dai complementi se
        # M[0][1] = M[2][3] = 0)
        out = []
        univ = set(range(6))
        for T1t in combinations(range(6), 3):
            T1 = set(T1t)
            T2 = univ - T1
            for T3t in combinations(range(6), 3):
                T3 = set(T3t)
                T4 = univ - T3
                cand = [T1, T2, T3, T4]
                if all(len(cand[i] & cand[j]) == M[i][j]
                       for i in range(4) for j in range(4)):
                    out.append(cand)
        return out

    def conta_modello(RA, RB):
        base = list(range(6))
        cnt = Counter()
        for q in permutations(base):
            n3 = n2 = 0
            for i in range(4):
                k = sum(1 for j in range(6)
                        if j in RA[i] and q[j] in RB[i])
                if k == 3:
                    n3 += 1
                elif k == 2:
                    n2 += 1
            if n3 and n2:
                cnt["misto"] += 1
            elif n3:
                cnt["solo-N3"] += 1
            elif n2:
                cnt["solo-N2"] += 1
            else:
                cnt["nullo"] += 1
        return cnt

    RAs = realizzazioni([list(r) for r in MAc])
    RBs = realizzazioni([list(r) for r in MBc])
    P(f"realizzazioni astratte dell'incidenza canonica: lato A "
      f"{len(RAs)}, lato B {len(RBs)}")
    conteggi = Counter()
    prove = 0
    for RB in RBs:
        conteggi[tuple(sorted(conta_modello(RAs[0], RB).items()))] += 1
        prove += 1
    for RA in RAs:
        conteggi[tuple(sorted(conta_modello(RA, RBs[0]).items()))] += 1
        prove += 1
    P(f"conteggi distinti su {prove} combinazioni (A canonico x "
      f"tutte le B, B canonico x tutte le A): {len(conteggi)}")
    for cc, m in sorted(conteggi.items()):
        P(f"  (x{m}) {dict(cc)}")
    unico = (len(conteggi) == 1)
    coincide = unico and Counter(dict(list(conteggi)[0])) == FIRMA_S1
    P("FACCIA B2-b: " + (
        "il conteggio e FUNZIONE della sola incidenza canonica sulle "
        "realizzazioni enumerate, e il modello RIPRODUCE "
        "{misti 32, solo-N3 40, solo-N2 488, nulli 160}: l'invariante "
        "candidato e l'incidenza; 32/40/488/160 SI DERIVANO da essa "
        "per conteggio finito" if coincide else
        "<<< il modello NON riproduce la firma (o conteggi non "
        "unici): controesempio a verbale sopra"))
else:
    P("piu forme canoniche distinte: test modello eseguito per forma")
    P("<<< vedi faccia B1-a: si verbalizza coi membri")
P(f"[B2-b: {time.time()-t0:.1f}s]")
P()

# ------------------------------------------------------------------
P("=" * 68)
P("TABELLA COMPLETA — le 156 coppie coi membri (carta d'identita)")
P("=" * 68)
P("colonne: idx | (s1,s2) | A | B | gemelle g,gbar,h,hbar "
  "(lato A / lato B) | (a,b) | firma")
for i, (c, (cnt, kvec, misti)) in enumerate(zip(carte, sweep_res), 1):
    P(f"[{i:3d}] {c['key']} A={list(c['A'])} B={list(c['B'])}")
    for nome, gg in zip(("g   ", "gbar", "h   ", "hbar"), c["ordg"]):
        P(f"      {nome} {list(gg[0])} / {list(gg[1])}")
    P(f"      (a,b)=({c['a']},{c['b']}) cella {c['cella']} firma "
      f"{{misti {cnt['misto']}, solo-N3 {cnt['solo-N3']}, "
      f"solo-N2 {cnt['solo-N2']}, nulli {cnt['nullo']}}}")

# ------------------------------------------------------------------
P()
P("=" * 68)
P("VERDETTO DELLA SEDUTA (B1 + B2)")
P("=" * 68)
P(f"base: {len(q4)} coppie |G|=4 di [1..22], censimento indipendente "
  f"(distribuzione |G| {dict(sorted(dist_G.items()))} su {npairs} "
  f"coppie)")
P(f"B1-a: forme d'incidenza congiunte distinte: {len(cjs)}")
P(f"B2-a: coppie con firma diversa da 32/40/488/160: {firme_diverse}")
P(f"B2-b: vedi faccia sopra")
P(f"B2-c: ritratti orbitali distinti: {len(ritratti)}")

with open(os.path.join(LOGS, "invariante-156.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
