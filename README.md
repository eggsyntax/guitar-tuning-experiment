# Guitar Tuning Direction Experiment

Does finishing a guitar string **up** to pitch keep it in tune better than finishing it
**down**? A small, controlled, single-guitar experiment testing the old lutherie maxim —
run over ~5 days on a [PRS SE McCarty 594 Singlecut](https://prsguitars.com/electrics/model/se_mccarty_594_singlecut_2023).

**Headline result:** modest but consistent support for the maxim. Strings finished up went
out of tune about **16 percentage points less often** (≈49% vs ≈65% chance of being out on
a given check) and drifted about **1.8 cents less** on average. The effect held in both
reversed-polarity runs and for 5 of 6 strings, is driven by *how often* a string goes out
(not *how far*), and survived a dependence-robust reanalysis (posterior probability the
maxim holds ≈ 0.99). Caveat: one guitar, five days — a case study, not a population estimate.

## Reports

- **[General-audience summary](REPORT_general.md)** — plain-language write-up (< 1000 words).
- **[Full technical report](REPORT_full.md)** — design, data translation, frequentist +
  Bayesian analysis, robustness, limitations.

The reports are also published as web pages (links to be added once the repo is public).

## Repository layout

```
data/      source PDFs + the tidy/wide analysis datasets (CSV)
scripts/   Python analysis (standard library only — no dependencies)
*.md       the two reports
*.html     web-page versions of the reports
```

## Reproducing the analysis

No third-party packages required — everything uses the Python standard library. Each script
finds `data/` relative to itself, so it can be run from anywhere:

```bash
python3 scripts/translate.py     # PDFs → data/tuning_data_tidy.csv (tidy long form)
python3 scripts/wide_view.py     # tidy → data/tuning_data_wide.csv + readable table
python3 scripts/freq_test.py     # frequentist: within-sweep permutation + string-level paired
python3 scripts/bayes.py         # Bayesian: Beta-Binomial (frequency) + Bayesian bootstrap (magnitude)
python3 scripts/robustness.py    # sweep-level cluster bootstrap (dependence check)
```

## Method in one paragraph

Each recorded reading is a moment a string was found >3 cents off pitch; by protocol every
reading implies a full six-string sweep (unlisted strings were in tune). On every sweep,
half the strings were finished up and half down (alternating), so environment cancels
*within* a sweep; the two runs swap which strings go which way, so string identity cancels
*across* runs. The primary unit is the within-sweep up-vs-down contrast, combined
equal-weight across the two runs, on two outcomes: frequency (binary) and magnitude (|cents|).

## Authors

Experiment design and data collection by **Egg Syntax**. Data analysis and writing by
**Claude Opus 4.8**.
