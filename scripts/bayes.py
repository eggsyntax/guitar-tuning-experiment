#!/usr/bin/env python3
"""
Bayesian analysis. Two questions:
  (1) P(out | up)  vs  P(out | down)          -- Beta-Binomial
  (2) E[|cents| | up] vs E[|cents| | down]     -- Bayesian bootstrap of the mean

Each computed per (experiment x direction) cell, then the two experiments are
combined with EQUAL weight:  pop = 0.5*(Exp1 cell + Exp2 cell).
Difference is defined  down - up , so POSITIVE => up is more stable (maxim holds).
"""
import csv, random, statistics as st
from pathlib import Path
random.seed(20260821)
N = 200_000

DATA = Path(__file__).resolve().parent.parent / "data"
rows = list(csv.DictReader(open(DATA/"tuning_data_tidy.csv")))

# ---- collect per (exp, direction) ----
freq = {}   # (exp,dir) -> [out, inn]
mags = {}   # (exp,dir) -> list of |cents| (in-tune=0, measured out only; symbol-only dropped)
mags_out = {}  # conditional: out-of-tune measured only
for r in rows:
    key = (r["experiment"], r["tuned_direction"])
    f = freq.setdefault(key, [0, 0])
    if r["out_of_tune"] == "1": f[0] += 1
    else:                       f[1] += 1
    # magnitude
    if r["out_of_tune"] == "0":
        mags.setdefault(key, []).append(0.0)
    elif r["magnitude_quality"] != "unknown":
        v = abs(int(r["cents_signed"]))
        mags.setdefault(key, []).append(v)
        mags_out.setdefault(key, []).append(v)
    # symbol-only out => dropped from magnitude

def ci(draws, lo=5, hi=95):
    s = sorted(draws); n = len(s)
    return s[int(lo/100*n)], s[int(hi/100*n)]

def summ(draws):
    return st.mean(draws), *ci(draws), sum(d > 0 for d in draws)/len(draws)

# ---- (1) frequency: Beta-Binomial, equal-weight experiments ----
def beta_draw(cell):
    o, i = freq[cell]; return random.betavariate(1+o, 1+i)

p_up, p_dn, diff_f = [], [], []
for _ in range(N):
    up = 0.5*(beta_draw(("1","up"))   + beta_draw(("2","up")))
    dn = 0.5*(beta_draw(("1","down")) + beta_draw(("2","down")))
    p_up.append(up); p_dn.append(dn); diff_f.append(dn - up)

# ---- (2) magnitude: Bayesian bootstrap of the mean, equal-weight experiments ----
def bb_mean(cell):
    xs = mags[cell]; n = len(xs)
    w = [random.gammavariate(1, 1) for _ in range(n)]; s = sum(w)
    return sum(wi*xi for wi, xi in zip(w, xs)) / s

m_up, m_dn, diff_m = [], [], []
for _ in range(N):
    up = 0.5*(bb_mean(("1","up"))   + bb_mean(("2","up")))
    dn = 0.5*(bb_mean(("1","down")) + bb_mean(("2","down")))
    m_up.append(up); m_dn.append(dn); diff_m.append(dn - up)

print("raw cell counts (out / total), and mean|cents| (unconditional):")
for e in ("1","2"):
    for d in ("up","down"):
        o,i = freq[(e,d)]; mm = st.mean(mags[(e,d)])
        print(f"  Exp{e} {d:<4}: out {o:2d}/{o+i:2d} = {o/(o+i):.2f}   mean|c|={mm:.2f}")

print("\n=== (1) FREQUENCY  P(out|dir) ===")
mu,lo,hi,_ = summ(p_up); print(f"  P(out | up)   = {mu:.3f}   90% CI [{lo:.3f}, {hi:.3f}]")
mu,lo,hi,_ = summ(p_dn); print(f"  P(out | down) = {mu:.3f}   90% CI [{lo:.3f}, {hi:.3f}]")
mu,lo,hi,pg = summ(diff_f)
print(f"  diff (down-up)= {mu:+.3f}  90% CI [{lo:+.3f}, {hi:+.3f}]   P(up more stable)={pg:.3f}")

print("\n=== (2) MAGNITUDE  E[|cents| | dir]  (unconditional, in-tune=0) ===")
mu,lo,hi,_ = summ(m_up); print(f"  E|c| up   = {mu:.2f}   90% CI [{lo:.2f}, {hi:.2f}]")
mu,lo,hi,_ = summ(m_dn); print(f"  E|c| down = {mu:.2f}   90% CI [{lo:.2f}, {hi:.2f}]")
mu,lo,hi,pg = summ(diff_m)
print(f"  diff (down-up) = {mu:+.2f}  90% CI [{lo:+.2f}, {hi:+.2f}]   P(up drifts less)={pg:.3f}")

# secondary: conditional-on-out magnitude
print("\n(secondary) mean|cents| GIVEN out of tune, by cell:")
for e in ("1","2"):
    for d in ("up","down"):
        xs = mags_out.get((e,d),[])
        print(f"  Exp{e} {d:<4}: n={len(xs):2d}  mean={st.mean(xs):.2f}" if xs else f"  Exp{e} {d}: none")
