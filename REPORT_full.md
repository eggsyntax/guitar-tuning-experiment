# Does finishing a tuning "up to pitch" make a guitar string more stable? — Full Report

*Single-guitar empirical study, 10–14 August 2026.*

**Authorship.** Experiment design and data collection by **Egg Syntax**. Data analysis and writing by **Claude Opus 4.8**.

**Instrument.** [PRS SE McCarty 594 Singlecut (2023)](https://prsguitars.com/electrics/model/se_mccarty_594_singlecut_2023)[^1] — a **stoptail (hardtail)**: no tremolo, which removes one common, large source of tuning instability. The features most plausibly relevant to tuning stability are its PRS synthetic nut (1‑11/16″ wide), vintage-style tuning machines, and its strings: Pyramid Pure Nickel Classics, round core, R450 Light gauge (.009–.042). (Body/neck woods, pickups, and fret details are omitted as unlikely to bear on the question.)

[^1]: A fantastic guitar that punches well above its price, and the one I play the most — which is why it's the instrument tested.

## 1. Question

A long-standing piece of guitar lore holds that a string will hold its tuning better if
you finish tuning it by moving **up** to the target pitch (approaching from flat) rather
than **down** (approaching from sharp). The stated mechanism is that coming down leaves
slack/an unseated string at the nut and tuning post, which later slips. Whether this is
still meaningfully true — with modern strings, nuts, and machine heads — is unclear. This
study tests it empirically on one guitar.

**Hypothesis (the "maxim"):** strings finished *up* to pitch go out of tune less often
and/or by less than strings finished *down* to pitch.

## 2. Design

The core problem is separating a *tuning-direction* effect from two nuisances:

1. **Environment** — temperature/humidity drift move all strings together and continuously.
2. **String identity** — strings differ physically (plain vs wound, gauge, nut friction),
   so some are intrinsically more stable regardless of how they were tuned.

The design handles both:

- **Alternating directions within the instrument.** On any given sweep, half the strings
  were finished up and half down, alternating by string number. Because all six are
  measured at the same instant, any environmental shift is *common-mode* and cancels when
  up-strings are compared to down-strings **within the same sweep**.
- **Reversed polarity across two experiments.** In **Experiment 1** the even strings
  (2/B, 4/D, 6/low-E) were finished up and the odds (1/high-E, 3/G, 5/A) down. In
  **Experiment 2** the assignment was reversed. If "up is more stable" appears in *both*
  experiments, it tracks direction; if instead the same physical strings always win, it is
  string identity. Combining the two experiments with **equal weight** cancels string
  identity (in Exp 1 the "up" group is wound-heavy; in Exp 2 the "down" group is — the
  confound flips sign and averages out).

Standard string numbering is used throughout: 1 = high E, 2 = B, 3 = G, 4 = D, 5 = A,
6 = low E.

## 3. Data collection and translation

The raw record is a timestamped log: each row is a moment at which one string was found
more than 3 cents off pitch, with the signed error in cents (− = flat, + = sharp). By
protocol, **every logged reading implies a full sweep** — all six strings were checked at
that time (± ~3 min) and any not listed were within ±3 cents (treated as "in tune"). This
rule was confirmed to hold for every reading, including single-string sweeps.

The two source spreadsheets were translated into a tidy long table
(`tuning_data_tidy.csv`), one row per (sweep × string), with explicit in-tune rows filled
in. Decisions made during translation:

- **Experiment 2 dates were a spreadsheet drag-fill artifact.** Within each block the
  time-of-day was identical to the second while the date incremented one day per row — an
  impossible pattern for real independent timestamps. Each identical-time block was
  collapsed to a single sweep on its first date. (One block whose dates were genuinely all
  the same was left untouched.) This puts Experiment 2 on 13–14 August and the whole study
  in a ~5-day window, consistent with the experimenter's recollection.
- **13 early "symbol-only" readings** recorded only direction (−/^), not magnitude. These
  are kept and flagged (`magnitude_quality = unknown`); they are valid out-of-tune events
  usable for the **frequency** analysis, and excluded only from the **magnitude** analysis.
- **One blank cell** (10 Aug 20:45, string 6) was interpolated to −6 cents (the mean of
  the other flat strings in that sweep) and flagged `interpolated`.

Final dataset: **23 sweeps, 138 string-observations** (69 finished up, 69 down).

## 4. Analysis

**Unit of analysis:** the *within-sweep* up-vs-down contrast (differences out both
environment and elapsed-time-since-last-tuning, since the compared strings share the same
sweep). Sweeps are combined within an experiment, then the two experiments are combined
**equal-weight**.

**Two outcomes:**

- **Frequency** — did the string go out of tune (binary). Uses all rows, including
  symbol-only.
- **Magnitude** — how far out, |cents|, with in-tune counted as 0 (unconditional expected
  absolute error). Uses measured rows only.

**Sign convention throughout:** effect = (down − up), so a **positive** number means
**up is more stable** (supports the maxim); a **negative** number means **down is more
stable** (contradicts it).

Raw cell rates (out of tune / total; mean |cents|):

| | out-rate | mean \|cents\| |
|---|---|---|
| Exp 1 up (2,4,6)   | 27/51 = 0.53 | 2.89 |
| Exp 1 down (1,3,5) | 31/51 = 0.61 | 3.80 |
| Exp 2 up (1,3,5)   |  8/18 = 0.44 | 3.56 |
| Exp 2 down (2,4,6) | 13/18 = 0.72 | 6.17 |

### 4.1 Frequentist

**Null hypothesis (H₀):** tuning direction has no effect on stability — a string is equally
likely to go out of tune, and drifts equally far, whether it was finished up or down. The
frequentist question is: *how likely are results at least this extreme if H₀ is true?* Each
p-value below is that probability; a small value is evidence against H₀ and in favor of a
real direction effect.

*Within-sweep contrast, equal-weight combined, p-value from a within-sweep label
permutation (each sweep splits exactly 3 up / 3 down; 50,000 permutations):*

| outcome | Exp 1 | Exp 2 | combined | p (1-sided) | p (2-sided) |
|---|---|---|---|---|---|
| frequency (out-rate) | +0.078 | +0.278 | **+0.178** | 0.029 | 0.058 |
| magnitude (mean \|cents\|) | +0.91 | +2.61 | **+1.76** | 0.015 | 0.032 |

Both effects are positive in **both** experiments.

*String-level paired test (each string compared to itself, up-experiment vs
down-experiment; n = 6; exact identity control):* **5 of 6 strings favor up on both
outcomes.** The two dissents are different strings on different metrics and both tiny
(string 6 on frequency, −0.09; string 5 on magnitude, −1.2 c); **no string is
consistently against the maxim.** Sign-test p = 0.22 (underpowered at n = 6); mean paired
difference +0.18 out-rate and +1.8 c.

### 4.2 Bayesian

*Beta-Binomial (uniform prior) for frequency; Bayesian bootstrap of the mean for
magnitude; each computed per experiment × direction and combined equal-weight
(200,000 draws).*

**Q1 — probability a string is out of tune:**

- P(out | up) = **0.49** (90% CrI 0.38–0.60)
- P(out | down) = **0.65** (0.55–0.75)
- difference +0.16 (0.02–0.31) → **P(up more stable) = 96.5%**

**Q2 — expected drift E|cents| (unconditional):**

- E|c| up = **3.2 c** (2.3–4.2)
- E|c| down = **5.0 c** (3.9–6.1)
- difference +1.8 c (0.35–3.19) → **P(up drifts less) = 98%**

**Mechanism note.** Conditional on a string *having gone out of tune*, the two directions
are similar in severity (Exp 1: 6.2 c up vs 7.0 c down; Exp 2: 8.0 vs 8.5) — small
differences relative to the spread, and not the driver. So the ~1.8 c unconditional
advantage comes almost entirely from up-strings going out **less often**, not from being
**less far out** when they do. Frequency is the mechanism; magnitude inherits it.

### 4.3 Robustness to correlated observations

The naive tests assume all 138 observations are independent; they are not (strings share a
neck and a moment; nearby sweeps share slow-moving state). A cluster/sweep-level bootstrap
(resampling **whole sweeps**, stratified by experiment) was run to check this.

The point estimates are unchanged, and — counterintuitively — the **difference** intervals
did not widen; they slightly **tightened**, and P(maxim) rose to **≈0.995** on both
outcomes:

| quantity | naive | sweep-clustered |
|---|---|---|
| diff, frequency | +0.16 [0.02, 0.31] | +0.18 [0.06, 0.29] |
| diff, magnitude | +1.8 [0.35, 3.19] | +1.8 [0.66, 2.70] |

**Why:** the within-sweep correlation is *positive* (a common shock moves all strings the
same way), and for a **difference** that shared movement cancels
(Var(down−up) = Var(down)+Var(up) − 2·Cov, Cov > 0). The naive model treated up and down
as independent and thereby *overstated* the difference's uncertainty. The dependence
weakens claims about the *absolute* rates (those marginal intervals are genuinely wide) but
**strengthens** the *comparative* claim, which is the one of interest. The result is
therefore not an artifact of pseudo-replication.

## 5. Limitations

- **One guitar, ~5 days.** The strongest limitation: this is a single instrument over a
  short window. The effect size and even its existence could differ across guitars,
  string brands, string age, and climates. This is a case study, not a population estimate.
- **Absolute rates are uncertain.** The comparative effect is well-supported, but the
  individual probabilities (≈49% vs ≈65%) have wide intervals.
- **Re-tuning carryover.** Strings were reset only to within 3 cents, not exactly to
  pitch, so a string could start a period already partway out. Expected to be minor;
  not modeled.
- **Uneven exposure between sweeps.** Intervals between sweeps varied (minutes to
  overnight). This cancels under the within-sweep contrast but would matter for any
  naive/pooled view; noted, not a threat to the primary analysis.
- **Mechanical coupling.** Retuning one string slightly detunes its neighbors through neck
  flex; mitigated by not always tuning in the same order.
- **"All-sharp"/"all-flat" sweeps** (large synchronized environmental moves) carry no
  up-vs-down information and act as ties; they neither bias nor help the paired contrast.
- **Symbol-only rows** contribute to frequency but not magnitude, so the two outcomes rest
  on slightly different subsets.

## 6. Conclusion

On this guitar, the data give **modest but consistent support for the maxim**: finishing a
string up to pitch made it go out of tune roughly **16 percentage points less often**
(≈49% vs ≈65% chance of being out on a given check) and drift about **1.8 cents less** on
average. The effect is positive in both reversed-polarity experiments and for five of six
strings, is driven by *frequency of going out* rather than severity, and *strengthens*
rather than dissolves when observations are conservatively clustered by sweep
(posterior probability the maxim holds ≈ 0.99). The main caveat is external validity: it is
one instrument over five days. Within those bounds, "tune up to pitch" earns its keep.

---

### Appendix: files

Data lives in `data/`, analysis code in `scripts/`. Each script resolves the data directory
relative to itself, so it can be run from anywhere (`python3 scripts/freq_test.py`).

- `data/tuning_data_tidy.csv` — analysis dataset (long form); `scripts/translate.py` — its generator.
- `data/tuning_data_wide.csv` / `scripts/wide_view.py` — human-readable sweeps × strings view.
- `scripts/freq_test.py` — frequentist within-sweep permutation + string-level paired test.
- `scripts/bayes.py` — Bayesian frequency (Beta-Binomial) and magnitude (Bayesian bootstrap).
- `scripts/robustness.py` — sweep-level cluster bootstrap.
- `data/*.pdf` — the original source spreadsheets.

*Companion: the [general-audience summary](REPORT_general.md). Source, data, and code: [github.com/eggsyntax/guitar-tuning-experiment](https://github.com/eggsyntax/guitar-tuning-experiment).*
