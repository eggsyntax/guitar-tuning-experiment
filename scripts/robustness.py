#!/usr/bin/env python3
"""
Robustness pass: treat the SWEEP (not the individual string-observation) as the
independent unit, so within-sweep correlation can't masquerade as sample size.

- Frequentist: cluster bootstrap -- resample whole sweeps (with replacement,
  stratified by experiment), recompute the equal-weight combined effect.
- Bayesian: sweep-level Bayesian bootstrap -- Dirichlet weights over sweeps.

Point estimates are ~unchanged vs the naive versions; intervals widen and the
"probability the maxim holds" softens to an honest level.
Sign: down - up ; positive => up more stable.
"""
import csv, random, statistics as st
from pathlib import Path
random.seed(20260821)
B = 100_000
DATA = Path(__file__).resolve().parent.parent / "data"
rows = list(csv.DictReader(open(DATA/"tuning_data_tidy.csv")))

# ---- per-sweep aggregates ----
from collections import OrderedDict
sw = OrderedDict()
for r in rows:
    sw.setdefault((r["experiment"], r["sweep_id"]), []).append(r)

def sweep_rates(cells):
    up_out = dn_out = 0
    up_mag, dn_mag = [], []
    for r in cells:
        up = r["tuned_direction"] == "up"
        if r["out_of_tune"] == "1":
            (up_out if up else dn_out)  # counted below
        # frequency counts
        if r["out_of_tune"] == "1":
            if up: up_out += 1
            else:  dn_out += 1
        # magnitude values (in-tune=0, measured out=|c|, symbol-only=skip)
        if r["out_of_tune"] == "0":
            (up_mag if up else dn_mag).append(0.0)
        elif r["magnitude_quality"] != "unknown":
            (up_mag if up else dn_mag).append(abs(int(r["cents_signed"])))
    return {
        "up_rate": up_out/3.0, "dn_rate": dn_out/3.0,
        "up_mag": st.mean(up_mag) if up_mag else None,
        "dn_mag": st.mean(dn_mag) if dn_mag else None,
    }

agg = {"1": [], "2": []}
for (e, sid), cells in sw.items():
    agg[e].append(sweep_rates(cells))

def ci(draws, lo=5, hi=95):
    s = sorted(draws); n = len(s); return s[int(lo/100*n)], s[int(hi/100*n)]

# ---------- Frequentist cluster bootstrap ----------
def eq_combine(f):
    """f(list_of_sweeps)->value; equal-weight the two experiments."""
    return 0.5*(f(agg["1"]) + f(agg["2"]))

def resample(lst): return [random.choice(lst) for _ in lst]

def boot_effect(metric):
    reps = []
    for _ in range(B):
        rs = {e: resample(agg[e]) for e in ("1","2")}
        def eff(lst):
            if metric == "freq":
                ds = [s["dn_rate"]-s["up_rate"] for s in lst]
            else:
                ds = [s["dn_mag"]-s["up_mag"] for s in lst if s["up_mag"] is not None and s["dn_mag"] is not None]
            return st.mean(ds) if ds else 0.0
        reps.append(0.5*(eff(rs["1"]) + eff(rs["2"])))
    return reps

# ---------- Bayesian sweep-level bootstrap (rates & magnitudes) ----------
def dir_weights(n):
    w = [random.gammavariate(1,1) for _ in range(n)]; s = sum(w)
    return [x/s for x in w]

def wmean(vals, weights):
    pairs = [(v,w) for v,w in zip(vals,weights) if v is not None]
    s = sum(w for _,w in pairs)
    return sum(v*w for v,w in pairs)/s if s else None

def bayes_boot():
    P_up=[];P_dn=[];D_f=[];M_up=[];M_dn=[];D_m=[]
    for _ in range(B):
        pu=pd=mu=md=0.0
        for e in ("1","2"):
            n=len(agg[e]); w=dir_weights(n)
            pu += 0.5*wmean([s["up_rate"] for s in agg[e]], w)
            pd += 0.5*wmean([s["dn_rate"] for s in agg[e]], w)
            mu += 0.5*wmean([s["up_mag"] for s in agg[e]], w)
            md += 0.5*wmean([s["dn_mag"] for s in agg[e]], w)
        P_up.append(pu);P_dn.append(pd);D_f.append(pd-pu)
        M_up.append(mu);M_dn.append(md);D_m.append(md-mu)
    return P_up,P_dn,D_f,M_up,M_dn,D_m

print("=== FREQUENTIST cluster bootstrap (resample whole sweeps) ===")
for metric,label in [("freq","out-rate"),("mag","mean|cents|")]:
    reps = boot_effect(metric); lo,hi = ci(reps)
    print(f"  {label:12s} effect(down-up)= {st.mean(reps):+.3f}  90% CI [{lo:+.3f}, {hi:+.3f}]  P(>0)={sum(r>0 for r in reps)/len(reps):.3f}")

print("\n=== BAYESIAN sweep-level bootstrap ===")
P_up,P_dn,D_f,M_up,M_dn,D_m = bayes_boot()
def line(name,d,fmt="{:+.3f}"):
    lo,hi=ci(d); return f"  {name:16s} {st.mean(d):+.3f}  90% CI [{lo:+.3f}, {hi:+.3f}]"
print(f"  P(out|up)   = {st.mean(P_up):.3f}  90% CI {tuple(round(x,3) for x in ci(P_up))}")
print(f"  P(out|down) = {st.mean(P_dn):.3f}  90% CI {tuple(round(x,3) for x in ci(P_dn))}")
lo,hi=ci(D_f); print(f"  diff freq   = {st.mean(D_f):+.3f}  90% CI [{lo:+.3f}, {hi:+.3f}]  P(up more stable)={sum(x>0 for x in D_f)/len(D_f):.3f}")
print(f"  E|c| up     = {st.mean(M_up):.2f}  90% CI {tuple(round(x,2) for x in ci(M_up))}")
print(f"  E|c| down   = {st.mean(M_dn):.2f}  90% CI {tuple(round(x,2) for x in ci(M_dn))}")
lo,hi=ci(D_m); print(f"  diff mag    = {st.mean(D_m):+.2f}  90% CI [{lo:+.2f}, {hi:+.2f}]  P(up drifts less)={sum(x>0 for x in D_m)/len(D_m):.3f}")

print("\n(naive-for-comparison: freq diff CI [+0.015,+0.305] P=0.965 ; mag diff CI [+0.35,+3.19] P=0.980)")
