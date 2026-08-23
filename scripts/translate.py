#!/usr/bin/env python3
"""
Translate the two guitar-tuning PDFs into a tidy long CSV.

One row per (sweep, string). Each recorded out-of-tune reading implies a full
sweep in which every *other* string was checked and found in tune (|err|<=3c),
so we emit explicit in-tune rows too.

magnitude_quality:
  measured      - a real cents value was recorded
  unknown       - only a '-'/'^' symbol was recorded (direction known, magnitude not)
  interpolated  - value was missing in the source and estimated here
  (blank)       - string was in tune this sweep (magnitude simply <=3c, unknown exactly)
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

NOTE = {1: "E(high)", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E(low)"}

def direction(experiment, string):
    odd = (string % 2 == 1)          # strings 1,3,5 (treble E, G, A)
    if experiment == 1:              # "evens up": 2,4,6 up / 1,3,5 down
        return "up" if not odd else "down"
    else:                            # "odds up": 1,3,5 up / 2,4,6 down
        return "up" if odd else "down"

# Each sweep: (experiment, datetime, readings)
# readings maps string -> (cents:int|None, quality:str, note:str)
#   quality in {"measured","unknown","interpolated"}
# Strings absent from the dict were in tune.
M, U, I = "measured", "unknown", "interpolated"

sweeps = [
    # ---------- EXPERIMENT 1  (evens up) ----------
    (1, "2026-08-10 08:23:14", {3:(None,U,"")}),
    (1, "2026-08-10 08:39:30", {6:(None,U,""),5:(None,U,""),4:(None,U,""),3:(None,U,""),2:(None,U,""),1:(None,U,"")}),
    (1, "2026-08-10 09:58:09", {6:(None,U,""),5:(None,U,""),3:(None,U,""),2:(None,U,"")}),
    (1, "2026-08-10 12:25:41", {6:(None,U,""),5:(None,U,""),3:(-14,M,""),2:(-5,M,""),1:(-4,M,"")}),
    (1, "2026-08-10 13:45:27", {4:(-4,M,""),3:(-8,M,"")}),
    (1, "2026-08-10 15:55:56", {6:(-5,M,""),5:(-7,M,""),3:(-9,M,""),2:(-6,M,""),1:(-5,M,"")}),
    (1, "2026-08-10 20:45:16", {6:(-6,I,"interpolated: mean of the other flat strings in this sweep (s5=-8,s4=-4,s3=-6); source cell was blank"),5:(-8,M,""),4:(-4,M,""),3:(-6,M,"")}),
    (1, "2026-08-11 08:39:27", {6:(14,M,""),5:(11,M,""),4:(12,M,""),3:(14,M,""),2:(10,M,""),1:(6,M,"")}),
    (1, "2026-08-11 10:21:48", {5:(-5,M,""),4:(-4,M,""),3:(-11,M,""),2:(-5,M,"")}),
    (1, "2026-08-11 13:21:39", {4:(-4,M,""),3:(-6,M,""),2:(-4,M,""),1:(-5,M,"")}),
    (1, "2026-08-11 14:11:44", {3:(-4,M,""),5:(-5,M,""),6:(-7,M,"")}),
    (1, "2026-08-11 16:54:41", {3:(-5,M,"")}),
    (1, "2026-08-11 20:25:07", {5:(-6,M,""),4:(-6,M,""),3:(-9,M,""),2:(-5,M,""),1:(-4,M,"")}),
    (1, "2026-08-12 08:53:51", {6:(-4,M,""),4:(-6,M,""),2:(6,M,"")}),
    (1, "2026-08-12 13:14:38", {5:(4,M,""),3:(-4,M,"")}),
    (1, "2026-08-12 18:58:42", {6:(-8,M,""),3:(-7,M,"")}),
    (1, "2026-08-12 23:12:11", {6:(5,M,"")}),
    # ---------- EXPERIMENT 2  (odds up) ----------  dates collapsed to each block's first date
    (2, "2026-08-13 08:49:48", {6:(18,M,""),5:(9,M,""),4:(8,M,""),3:(10,M,""),2:(10,M,""),1:(4,M,"")}),
    (2, "2026-08-13 10:07:44", {6:(-5,M,""),4:(-7,M,""),3:(-5,M,""),2:(-6,M,"")}),
    (2, "2026-08-13 22:47:35", {4:(-8,M,""),2:(-5,M,"")}),
    (2, "2026-08-14 09:56:46", {6:(9,M,""),5:(11,M,""),3:(10,M,""),2:(5,M,"")}),
    (2, "2026-08-14 10:08:35", {2:(-6,M,""),5:(-7,M,"")}),
    (2, "2026-08-14 11:47:24", {4:(-16,M,""),3:(-8,M,""),2:(-8,M,"")}),
]

rows = []
for sid, (exp, dt, readings) in enumerate(sweeps, start=1):
    for s in range(1, 7):
        d = direction(exp, s)
        if s in readings:
            cents, qual, note = readings[s]
            if cents is None:                      # symbol-only
                err = ""  # sign carried below; filled from note dir? we stored direction via symbol
            out = 1
        else:
            cents, qual, note, out = None, "", "", 0
        # error sign
        if out == 1:
            if cents is not None:
                err = "sharp" if cents > 0 else "flat"
            else:
                err = ""  # placeholder, set from symbol map below
        else:
            err = ""
        rows.append([exp, sid, dt, s, NOTE[s], d, out,
                     "" if cents is None else cents, err, qual, note])

# Fill error_sign for the symbol-only (unknown-magnitude) rows from the source symbols.
# All 13 early Exp-1 symbol-only readings, keyed by (datetime, string) -> 'flat'/'sharp'.
symbol_dir = {
    ("2026-08-10 08:23:14",3):"flat",
    ("2026-08-10 08:39:30",6):"flat", ("2026-08-10 08:39:30",5):"flat", ("2026-08-10 08:39:30",4):"flat",
    ("2026-08-10 08:39:30",3):"flat", ("2026-08-10 08:39:30",2):"flat", ("2026-08-10 08:39:30",1):"flat",
    ("2026-08-10 09:58:09",6):"sharp", ("2026-08-10 09:58:09",5):"sharp",
    ("2026-08-10 09:58:09",3):"flat", ("2026-08-10 09:58:09",2):"flat",
    ("2026-08-10 12:25:41",6):"flat", ("2026-08-10 12:25:41",5):"flat",
}
for r in rows:
    if r[9] == "unknown":
        r[8] = symbol_dir[(r[2], r[3])]

header = ["experiment","sweep_id","datetime","string","note","tuned_direction",
          "out_of_tune","cents_signed","error_sign","magnitude_quality","notes"]

with open(DATA/"tuning_data_tidy.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(header); w.writerows(rows)

# ---- quick sanity summary ----
n_sweeps = len(sweeps)
n_rows = len(rows)
oot = sum(r[6] for r in rows)
unk = sum(1 for r in rows if r[9]=="unknown")
interp = sum(1 for r in rows if r[9]=="interpolated")
print(f"sweeps={n_sweeps}  string-observations={n_rows}  out_of_tune={oot}  in_tune={n_rows-oot}")
print(f"magnitude: measured={oot-unk-interp}  unknown(symbol-only)={unk}  interpolated={interp}")

# 2x2 counts: direction vs out_of_tune (excludes nothing; symbol-only count for frequency)
from collections import Counter
c = Counter()
for r in rows:
    c[(r[5], "out" if r[6] else "in")] += 1
print("\nfrequency table (all sweeps, all rows):")
for d in ("up","down"):
    o, i = c[(d,"out")], c[(d,"in")]
    tot = o+i
    print(f"  {d:>4}: out_of_tune={o:3d} / {tot:3d}  = {o/tot:5.1%}")
