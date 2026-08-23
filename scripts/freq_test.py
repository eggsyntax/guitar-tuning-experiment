#!/usr/bin/env python3
"""
Frequentist headline: does tuning UP give more stable tuning than DOWN?

Unit = within-sweep up-vs-down contrast. Sign convention: effect = down - up,
so POSITIVE effect = up is more stable (supports the maxim).

Two outcomes:
  frequency  : per group, fraction of strings out of tune   (all rows, incl. symbol-only)
  magnitude  : per group, mean |cents|, in-tune counted as 0 (measured rows only;
               symbol-only cells dropped; unconditional "how far from pitch")

Combine sweeps within an experiment (mean of per-sweep effects), then combine the
two experiments with EQUAL weight. p-value from within-sweep label permutation
(each sweep is exactly 3 up / 3 down; permute which 3 are 'up').
"""
import csv, random, itertools, statistics as st
from pathlib import Path
random.seed(20260821)

DATA = Path(__file__).resolve().parent.parent / "data"
rows = list(csv.DictReader(open(DATA/"tuning_data_tidy.csv")))

# index: sweeps[(exp,sid)] = list of dicts per string
from collections import defaultdict, OrderedDict
sw = OrderedDict()
for r in rows:
    sw.setdefault((r["experiment"], r["sweep_id"]), []).append(r)

def cell_mag(r):
    """|cents| for magnitude outcome, or None to drop (symbol-only out)."""
    if r["out_of_tune"] == "0":
        return 0.0
    if r["magnitude_quality"] == "unknown":
        return None
    return abs(int(r["cents_signed"]))

def group_stats(cells, labels, want):
    """cells: list of 6 rows; labels: list of 6 in {'up','down'} (permuted).
       return (up_metric, down_metric) or None if undefined."""
    up_vals, dn_vals = [], []
    for r, lab in zip(cells, labels):
        if want == "freq":
            v = 1.0 if r["out_of_tune"] == "1" else 0.0
        else:
            v = cell_mag(r)
            if v is None:
                continue
        (up_vals if lab == "up" else dn_vals).append(v)
    if not up_vals or not dn_vals:
        return None
    return st.mean(up_vals), st.mean(dn_vals)

def observed_labels(cells):
    return [r["tuned_direction"] for r in cells]

def combined_effect(assign, want):
    """assign: dict (exp,sid)->labels(6). Returns 0.5*(mean_eff_exp1+mean_eff_exp2)."""
    per_exp = {"1": [], "2": []}
    for key, cells in sw.items():
        gs = group_stats(cells, assign[key], want)
        if gs is None:
            continue
        up_m, dn_m = gs
        per_exp[key[0]].append(dn_m - up_m)          # down - up
    if not per_exp["1"] or not per_exp["2"]:
        return None
    return 0.5 * (st.mean(per_exp["1"]) + st.mean(per_exp["2"])), \
           st.mean(per_exp["1"]), st.mean(per_exp["2"])

def run(want, nperm=50000):
    obs_assign = {k: observed_labels(v) for k, v in sw.items()}
    obs, e1, e2 = combined_effect(obs_assign, want)
    # permutation: within each sweep pick 3 of 6 to be 'up'
    idx = list(range(6))
    ge_two = ge_one = 0
    for _ in range(nperm):
        perm = {}
        for k, cells in sw.items():
            ups = set(random.sample(idx, 3))
            perm[k] = ["up" if i in ups else "down" for i in range(6)]
        val = combined_effect(perm, want)
        if val is None:
            continue
        eff = val[0]
        if abs(eff) >= abs(obs) - 1e-12: ge_two += 1
        if eff >= obs - 1e-12: ge_one += 1
    return obs, e1, e2, (ge_two+1)/(nperm+1), (ge_one+1)/(nperm+1)

print("=== WITHIN-SWEEP CONTRAST (combined, equal-weight experiments) ===")
print("effect = down - up ; positive => UP more stable (supports maxim)\n")
for want, unit in [("freq","out-rate"), ("mag","mean |cents|")]:
    obs, e1, e2, p2, p1 = run(want)
    print(f"{want:5s} ({unit}):  Exp1 effect={e1:+.3f}  Exp2 effect={e2:+.3f}  combined={obs:+.3f}")
    print(f"        permutation p: two-sided={p2:.4f}   one-sided(up>down)={p1:.4f}\n")

# ---------- string-level paired (exact identity control, n=6) ----------
print("=== STRING-LEVEL PAIRED (each string: up-experiment vs down-experiment) ===")
# For each string, gather its rows split by which experiment it was up vs down.
by_str = defaultdict(lambda: {"up": [], "down": []})
for r in rows:
    by_str[int(r["string"])][r["tuned_direction"]].append(r)

def sign_test(diffs):
    pos = sum(d > 0 for d in diffs); neg = sum(d < 0 for d in diffs)
    n = pos + neg
    # two-sided exact binomial p at 0.5
    from math import comb
    k = min(pos, neg)
    p = sum(comb(n, i) for i in range(0, k+1)) / 2**n * 2 if n else 1.0
    return pos, neg, min(p, 1.0)

print("str  freq: out%(up) out%(down) diff   mag: |c|(up) |c|(down) diff")
fdiffs, mdiffs = [], []
for s in range(1, 7):
    up, dn = by_str[s]["up"], by_str[s]["down"]
    def outrate(g): return st.mean(1.0 if r["out_of_tune"]=="1" else 0.0 for r in g)
    def magmean(g):
        vals = [cell_mag(r) for r in g]; vals = [v for v in vals if v is not None]
        return st.mean(vals) if vals else float("nan")
    fu, fd = outrate(up), outrate(dn); fdiffs.append(fd - fu)
    mu, md = magmean(up), magmean(dn); mdiffs.append(md - mu)
    print(f" {s}        {fu:5.2f}    {fd:5.2f}   {fd-fu:+.2f}        {mu:4.1f}    {md:4.1f}   {md-mu:+.1f}")

fp = sign_test(fdiffs); mp = sign_test(mdiffs)
print(f"\nfreq diffs (down-up): {[round(d,2) for d in fdiffs]}")
print(f"   sign test: {fp[0]} of 6 favor up, p(two-sided)={fp[2]:.3f}   mean diff={st.mean(fdiffs):+.3f}")
print(f"mag  diffs (down-up): {[round(d,1) for d in mdiffs]}")
print(f"   sign test: {mp[0]} of 6 favor up, p(two-sided)={mp[2]:.3f}   mean diff={st.mean(mdiffs):+.2f}")
