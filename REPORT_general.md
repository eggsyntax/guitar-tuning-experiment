# Should you always tune a guitar string *up* to pitch? A small experiment.

*Experiment and data by **Egg Syntax**. Data analysis and writing by **Claude Opus 4.8**.*

There's a piece of advice that circulates among guitarists: when you tune a string,
finish by bringing it **up** to the right pitch, not **down**. The idea is that easing up
into pitch leaves the string seated and settled, while coming down from above leaves a
little slack that later slips — so the string drifts out of tune sooner. It's plausible,
it's widely repeated, and it may well have been true for older strings and hardware. But is
it still true today? I decided to actually measure it — on a 2023 PRS SE McCarty 594 Singlecut, a hardtail electric (no tremolo, so nothing there to add its own tuning drift).

## How the test worked

The trick to a fair test is separating the thing you care about (tuning *direction*) from
two things that muddy it:

- **The weather.** Temperature and humidity constantly nudge every string at once, so you
  can't just tune up one day, down the next, and compare.
- **The strings themselves.** A thick wound low-E behaves differently from a thin plain
  high-E no matter how you tune it, so you can't just compare "up strings" to "down
  strings" if they happen to be different kinds of string.

So I did two things. First, on every check I had **half the strings finished up and half
finished down**, alternating across the neck. Because all six are checked at the same
moment, whatever the weather is doing hits both groups equally and cancels out when I
compare them. Second, I ran the whole thing **again with the roles swapped** — the strings
that were "tuned up" in the first run were "tuned down" in the second, and vice versa. If
tuning up wins in *both* runs, it's really about direction. If instead the same physical
strings win both times, it's just those strings being stubborn. Running it both ways lets
me tell those apart.

Over about five days I repeatedly checked all six strings and noted any that had drifted
more than 3 cents off pitch (a cent is 1/100th of a semitone — 3 cents is roughly the
smallest error a good ear starts to notice). That gave 23 full check-ins across the two
runs, a total of 138 data points.

## What I found

Two questions, two answers.

**1. How *often* does a string go out of tune?**

| finished... | chance it's out of tune on a given check |
|---|---|
| **up** to pitch | about **49%** |
| **down** to pitch | about **65%** |

Strings finished by tuning up went out of tune noticeably less often — a gap of about 16
percentage points.

**2. How *far* out does it drift?**

On average, strings finished up sat about **3.2 cents** off pitch; strings finished down,
about **5.0 cents** — roughly **1.8 cents** more drift for the "down" strings. When strings
**were** out of tune, the ones tuned down weren't much further out than the ones tuned up. So
tuning up doesn't shrink the misses — it makes them happen less often, and that's where the
overall gap comes from.

## How sure am I?

Fairly, for this guitar. The advantage showed up in **both** runs and for **five of the
six strings** (and the two mild exceptions disagreed with each other, so no single string
was quietly working against the pattern). Putting numbers on the confidence: the analysis
puts the probability that tuning up genuinely helps at roughly **96–99%**, both for
frequency and for amount of drift.

I also stress-tested the statistical analysis. Because a guitar's strings all share one neck and react to
the same room together, the individual measurements aren't fully independent, and naive
statistics can be fooled by that. When I redid the analysis in a way that accounts for it
(treating each full check-in, rather than each string, as the basic unit), the conclusion
didn't weaken — if anything it held up slightly better. The shared movement actually helps
here, because it affects the "up" and "down" strings together and cancels out of the
comparison.

## Caveats

The big one: **this is one guitar over five days.** That's enough to see a clear pattern on
*this* instrument, but not enough to declare a universal law. A different guitar, different
strings, older or newer hardware, or a different climate could all shift the result. Think
of this as a well-controlled case study, not the final word.

A couple of smaller points: I only re-tuned strings to within 3 cents rather than always
dead-on, which could blur things slightly; and I couldn't record the exact size of a handful of the
earliest readings, so those count toward "how often" but not "how far." Neither changes the
overall picture.

## Bottom line

On my guitar, the old advice held up: **finishing a string by tuning up to pitch really did
keep it in tune better** — it went out of tune about 16 percentage points less often and
drifted a bit less far. The effect is modest, not dramatic, and it's one instrument's worth
of evidence. But if you've ever wondered whether "always tune up" is worth the small extra
fuss of overshooting and coming back, this little experiment says: yes, probably.

*(A [full technical write-up](REPORT_full.md), with the data and analysis code, is available
for anyone who wants to check the work — see the
[GitHub repo](https://github.com/eggsyntax/guitar-tuning-experiment).)*
