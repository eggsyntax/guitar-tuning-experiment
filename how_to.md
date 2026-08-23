# How to run this experiment on your own guitar

This guide walks you through repeating the experiment yourself — recording the data and
then analyzing it — even if you've never written a line of code or taken a statistics
class. Take it one step at a time; none of it is hard, it's just a bit fiddly.

If you want to see what the finished thing looks like first, read the
[general-audience summary](https://claude.ai/code/artifact/b12ce579-4f74-4c3a-8a56-0e0531d4c0a0).

---

## The idea, in one minute

Guitarists are often told to always finish tuning a string by turning the peg so the pitch
rises *up* to correct, never *down*. We want to test, on your guitar, whether that actually
keeps it in tune better. The catch is that guitars drift out of tune for lots of reasons
(mostly temperature and humidity), so a fair test has to separate "tuned up vs down" from
all that noise. Two simple tricks do it:

1. On any given check, **half your strings are set up and half down** (alternating). Since
   they're all checked at the same moment, the weather affects both groups equally and
   cancels out.
2. You run the whole thing **twice, swapping which strings go which way**. That cancels out
   the fact that some individual strings are just naturally more stable than others.

That's the entire design. The rest is bookkeeping.

---

## What you'll need

- **A guitar** (any kind).
- **A tuner that shows "cents"** — the fine-grained measure of how sharp or flat a note is.
  Most clip-on tuners and phone tuner apps show a needle or a number in cents. You want one
  that shows the actual number (e.g. "+7" or "−4"), not just a green light.
- **Somewhere to log readings** — a free Google Sheet is ideal, but even paper works.
- **(Only for the analysis step) a computer** with Python installed. This is free and
  covered in Part 2. You can also skip the DIY analysis entirely and hand your data to an
  AI assistant (also in Part 2).

A quick vocabulary note: a note is **sharp** (♯) when it's too high and **flat** (♭) when
it's too low. **Cents** measure how far off it is — 100 cents is one semitone (one fret).
Most people start to hear that something's off around 3–5 cents.

---

## Part 1 — Recording your data

### Step 1: Learn "finishing up" vs "finishing down"

- **Finishing up:** bring the string to pitch while the pitch is *rising*. If you overshoot
  and go sharp, don't just ease back — go clearly flat first, then turn the peg so the pitch
  climbs up into tune. The last motion is upward.
- **Finishing down:** the opposite. Come to pitch while the pitch is *falling* — go a bit
  sharp, then lower it into tune. The last motion is downward.

Practice each a couple of times so it feels natural.

### Step 2: Decide your up/down assignment

Guitar strings are numbered 1 (thinnest, high E) to 6 (thickest, low E). For your **first
run**, pick one of these and stick with it:

- **Even strings up, odd strings down:** strings 2, 4, 6 finished up; strings 1, 3, 5
  finished down.

(That's the assignment used in the original study's first run. Either choice is fine, as
long as you swap it for the second run.)

### Step 3: Set up your log

Make three columns:

| Date & time | String # | Cents off |
|---|---|---|
| 2026-08-10 14:05 | 3 | −8 |
| 2026-08-10 14:06 | 5 | −5 |

- **Date & time:** when you did the check.
- **String #:** which string (1–6).
- **Cents off:** how far off it was, **with a sign** — `+` for sharp, `−` for flat. Always
  record the sign; it matters.

### Step 4: Tune up once to start

Tune the whole guitar to pitch, finishing each string in its assigned direction (Step 2).
Now leave it alone to drift.

### Step 5: Do "sweeps"

Whenever you come back to the guitar (a few times a day is great), do a **sweep**:

- Check **all six strings** with your tuner.
- For any string that's **more than 3 cents off**, write one row: the time, the string
  number, and the cents (with sign).
- For strings that are **within 3 cents, write nothing.** This is the one rule that makes
  the whole thing work: *a string with no row for that sweep is assumed to have been fine.*
  So you must genuinely check all six every time, even if you only end up writing down one
  or two.
- Then **re-tune** any out-of-tune string — in its assigned direction from Step 2 — and
  carry on.

Do this over about a week. More sweeps = a clearer result. The original study had 23 sweeps
across both runs.

### Step 6: Swap and run it again

After about a week, start **Run 2**: flip the assignment (now odd strings 1, 3, 5 finished
**up**, even strings 2, 4, 6 finished **down**). Keep logging in the same way — just start a
new sheet or clearly mark where Run 2 begins. Another week or so.

That's the data collection. A few tips:

- Use the **same tuner** throughout, and try to hold the guitar the same way each time.
- You don't need to control the room — changing weather is fine, the design handles it.
- If you're ever unsure whether a string is 2 or 4 cents off, it's okay to skip it; just be
  consistent about your 3-cent cutoff.

---

## Part 2 — Analyzing your data

You have two paths. Pick whichever suits you.

### Path A — Hand it to an AI assistant (easiest, no coding)

Honestly, the simplest route today: export your spreadsheet (File → Download → CSV in
Google Sheets), then give it, along with the link to this project's repository
(<https://github.com/eggsyntax/guitar-tuning-experiment>), to an AI coding assistant and ask
it to "run the same analysis as this repo on my data." It can adapt the scripts to your
readings and explain the results. Everything below is what it would be doing.

### Path B — Run it yourself

**1. Install Python.** Go to <https://www.python.org/downloads/>, download the latest
version for your system, and install it (the default options are fine). You don't need to
learn Python — just have it installed.

**2. Get the project files.** On the repository page, click the green **Code** button →
**Download ZIP**, then unzip it. You'll get a folder with `data/` and `scripts/` inside.

**3. Put your data in.** The analysis reads one file, `data/tuning_data_tidy.csv`, which
lists every string on every sweep (including the in-tune ones). You don't build that by
hand — a script called `scripts/translate.py` builds it for you from a short list of your
readings.

Open `scripts/translate.py` in any text editor and find the part that looks like a list of
sweeps. Each line records one sweep: the run number, the date and time, and the strings that
were off (with their cents). For example, this line —

```
(1, "2026-08-10 15:55:56", {6:(-5,M,""),5:(-7,M,""),3:(-9,M,""),2:(-6,M,""),1:(-5,M,"")}),
```

— means: Run 1, at that time, strings 6/5/3/2/1 were off by −5/−7/−9/−6/−5 cents, and (since
string 4 isn't listed) string 4 was in tune. The `M` just means "measured normally." Replace
the existing lines with your own readings in the same shape, keeping Run 1 and Run 2 rows
labeled `1` and `2` in the first slot. (This is the one fiddly step — and exactly the kind of
thing Path A's AI assistant can do for you if you'd rather not.)

**4. Run the scripts.** Open your computer's terminal (Terminal on Mac, Command Prompt on
Windows), navigate into the project folder, and run these one at a time. Each prints its
results right in the terminal.

Build your dataset from the readings you just entered:

```bash
python3 scripts/translate.py
```

Get the plain "how often did strings go out of tune" comparison and the frequentist test:

```bash
python3 scripts/freq_test.py
```

Get the Bayesian version (probabilities and ranges):

```bash
python3 scripts/bayes.py
```

(There are two more, `wide_view.py` for a readable table of your data and `robustness.py`
for a dependence check, if you want them.)

### Reading the results

The scripts compare your up-tuned and down-tuned strings. The key number is an **effect**,
defined as `down − up`:

- A **positive** effect means the strings you finished **up** were more stable — support for
  the maxim.
- A **negative** effect means the ones you finished **down** were more stable.

`freq_test.py` reports this for how *often* strings went out of tune and for how *far*, along
with a **p-value** — roughly, how surprising your result would be if tuning direction made no
difference at all. Smaller means more surprising (a value below ~0.05 is the usual rough
threshold for "probably not just luck"). `bayes.py` reports the **probability that tuning up
is genuinely more stable**, plus the estimated chance each way and a range of uncertainty.

### A note on interpreting it

One guitar over a week or two is a fun, real experiment — but it's a *case study*, not the
final word. Don't be surprised if your result is weaker, stronger, or even points the other
way; strings, hardware, and climate all vary. If you post your numbers somewhere, mention
how many sweeps you did and over how long, so others can weigh them fairly. And if you want a
second opinion on what your numbers mean, this whole write-up (and an AI assistant) can help
you read them.

Have fun, and happy tuning.
