#!/usr/bin/env python3
"""Pivot the tidy CSV into a human-readable sweeps x strings view.

Cell encoding:
  .      in tune (|err| <= 3c)
  -14    measured cents (sign = flat/sharp)
  f?/s?  symbol-only: direction known, magnitude unknown
  -6*    interpolated value
"""
import csv, collections
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

rows = list(csv.DictReader(open(DATA/"tuning_data_tidy.csv")))

def cell(r):
    if r["out_of_tune"] == "0":
        return "."
    q = r["magnitude_quality"]
    if q == "measured":
        c = int(r["cents_signed"]); return f"{c:+d}"
    if q == "interpolated":
        c = int(r["cents_signed"]); return f"{c:+d}*"
    # unknown (symbol only)
    return "s?" if r["error_sign"] == "sharp" else "f?"

sweeps = collections.OrderedDict()
for r in rows:
    key = (r["experiment"], r["sweep_id"], r["datetime"])
    sweeps.setdefault(key, {})[int(r["string"])] = r

# ---- wide CSV ----
with open(DATA/"tuning_data_wide.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["experiment","sweep_id","date","time","s1","s2","s3","s4","s5","s6","n_out","pattern"])
    for (exp, sid, dt), d in sweeps.items():
        date, time = dt.split(" ")
        cells = [cell(d[s]) for s in range(1,7)]
        n_out = sum(1 for s in range(1,7) if d[s]["out_of_tune"]=="1")
        signs = {d[s]["error_sign"] for s in range(1,7) if d[s]["out_of_tune"]=="1"}
        pattern = ("all-sharp" if n_out==6 and signs=={"sharp"} else
                   "all-flat"  if n_out==6 and signs=={"flat"}  else
                   "mixed" if signs=={"sharp","flat"} else
                   ("sharp" if signs=={"sharp"} else "flat" if signs=={"flat"} else ""))
        w.writerow([exp, sid, date, time] + cells + [n_out, pattern])

# ---- pretty console table (grouped by experiment, with U/D header) ----
DIR = {1:"D U D U D U", 2:"U D U D U D"}  # per-string up/down by experiment
LABEL = {1:"EXPERIMENT 1  (evens up: strings 2,4,6 = UP)",
         2:"EXPERIMENT 2  (odds up: strings 1,3,5 = UP)"}
for exp in ("1","2"):
    print("\n" + LABEL[int(exp)])
    print(f"  {'date':<10} {'time':<8}  dir:  " + "   ".join(DIR[int(exp)].split()))
    print(f"  {'':<10} {'':<8}       " + "  ".join(f"s{i}" for i in range(1,7)) + "   n_out pattern")
    for (e, sid, dt), d in sweeps.items():
        if e != exp: continue
        date, time = dt.split(" ")
        cells = [cell(d[s]) for s in range(1,7)]
        n_out = sum(1 for s in range(1,7) if d[s]["out_of_tune"]=="1")
        signs = {d[s]["error_sign"] for s in range(1,7) if d[s]["out_of_tune"]=="1"}
        pattern = ("ALL sharp" if n_out==6 and signs=={"sharp"} else
                   "ALL flat"  if n_out==6 and signs=={"flat"}  else
                   "mixed" if signs=={"sharp","flat"} else
                   ("sharp" if signs=={"sharp"} else "flat" if signs=={"flat"} else ""))
        print(f"  {date:<10} {time:<8}       " + "".join(f"{c:>4}" for c in cells) + f"   {n_out:>3}  {pattern}")

print("\nlegend:  . = in tune   -14 = measured cents   f?/s? = symbol-only (dir known, mag unknown)   -6* = interpolated")
