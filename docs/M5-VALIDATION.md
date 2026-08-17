# Validating M5 — Attainability

**Status:** Plan, ready to execute
**Date:** August 2026
**Relates to:** `SIM-PRD.md` §3 (mechanism M5), §10 (data availability); `SIM-RESULTS.md` (archetype I)

---

## 1. What Needs Validating

M5 claims that on a road where the limit exceeds what the traffic stream permits, a driver realizes only a fraction of their intended speed. Phase 1 modelled this with an invented parameter and found 51% attainment of the increment on archetype I, with overtaking manoeuvres rising from 81 to 148 between a 110 and a 130 cap.

Four separate questions sit inside that:

1. **Does the effect exist** at material magnitude on real roads?
2. **What is the attainment function** — currently `eta = 1/(1 + (rho/rho_ref) * resistance)` with `resistance` set by hand?
3. **How many overtakes** does a given speed differential actually require?
4. **How prevalent** are M5-constrained roads on target journeys?

Questions 1–3 are calibration. Question 4 decides whether M5 can carry the product, and is answerable independently.

---

## 2. The Counterfactual Problem

The product's claim is about **one driver's alternative**: if you aim for 130 instead of 110 on this road, you will realize 110 rather than 100.

No aggregate dataset contains that. Loop detectors record what drivers did, not what any individual could have done had they tried harder. This is the central methodological difficulty, and it rules out the naive approach of "download speed data and compare to the limit" — that measures the fleet, not the counterfactual.

Three ways round it, in increasing order of validity:

- **Percentile compression.** Use a high percentile (P85) as a proxy for the driver who wants to go fast, and the median as the stream. If M5 is real, the gap between them narrows as density rises — the fast driver is dragged toward the stream. This is observational and cheap.
- **Cross-sectional contrast.** Same flow, same limit, single versus dual carriageway. M5 predicts materially more compression where overtaking is constrained. This isolates the mechanism rather than merely detecting slow traffic.
- **Controlled repetition.** Drive the same segment repeatedly with deliberately different intended caps and measure realized mean speed. This observes the counterfactual directly rather than inferring it. Highest validity, smallest sample, entirely within our control.

All three should run. The first two establish magnitude and prevalence at scale; the third confirms the causal claim on a handful of roads.

---

## 3. Recovering the Speed Distribution — The Key Unlock

The percentile-compression test appears to need speed distributions, and no open portal publishes them. It does not.

The Flemish MIV feed publishes, per vehicle class per minute, **both the arithmetic and the harmonic mean speed**. At a fixed detector the arithmetic mean of spot speeds is the time-mean speed, and the harmonic mean is the space-mean speed. Wardrop's relation connects them through the variance:

```
v_time = v_space + sigma^2 / v_space
```

Rearranged, the variance is directly recoverable:

```
sigma^2 = v_harmonic * (v_arithmetic - v_harmonic)
```

So publishing both means is equivalent to publishing the spread. With `sigma` in hand, an approximate P85 follows (`v + 1.04 * sigma` under a normality assumption), and the compression test becomes possible from open data with no percentile fields and no commercial purchase.

Two caveats to carry into the analysis:

- Speed distributions are usually mildly right-skewed, so a normal approximation will bias the estimated P85 slightly. Where it matters, work with `sigma` directly rather than a derived percentile — the compression prediction can be stated as "sigma falls with density," which needs no distributional assumption at all.
- The recovered variance is the space-mean variance across all vehicles in the class, not the variance of drivers' *desired* speeds. It is a proxy, not the quantity itself.

This is the finding that makes the whole validation cheap. It should be sanity-checked against a source with genuine percentiles before the analysis is trusted.

---

## 4. Data Sources — Verified

Checked August 2026. This environment could not fetch the portals directly, so entries below rest on search results and, where noted, a schema file read in full.

### Flanders — Vlaams Verkeerscentrum "Meten in Vlaanderen" (MIV) — **primary source**

Verified against the published XSD (`tm-data/traffic`, `miv-verkeersdata.xsd`), read directly.

| Field | Content |
| --- | --- |
| `verkeersintensiteit` | vehicle count, per class |
| `voertuigsnelheid_rekenkundig` | arithmetic mean speed, per class |
| `voertuigsnelheid_harmonisch` | harmonic mean speed, per class |
| `bezettingsgraad` | occupancy — yields density |
| `onrustigheid` | turbulence measure, worth investigating |

Five vehicle classes by estimated length: class 2 cars (1.00–4.90 m), class 3 vans (4.90–6.90 m), class 4 rigid lorries (6.90–12.00 m), class 5 articulated and buses (>12.00 m). Class 1 is documented as unreliable and unused.

Minute resolution, double inductive loops, open licence (Model Licence for Free Reuse). Aggregations to quarter-hour, hour and day are also offered.

This source supplies **every input M5 calibration needs**: flow, density via occupancy, mean speed, variance via Wardrop, and — through the class split — the slow-vehicle population that creates the following constraint in the first place. It also covers the Brussels corridor that the PCS examples use.

**Its one limitation is decisive for the cross-sectional test:** the loops are mainly on motorways, i.e. dual carriageway. The single-versus-dual contrast, which is where M5 bites hardest, cannot be run from this source alone.

### Netherlands — NDW

Publishes flow (vehicles/hour) and average speed (km/h) per minute, from roadside systems and floating car data, covering motorways and provincial roads. Historical archive and a "Dexter" open-data module exist.

Only a single average speed is confirmed, so the Wardrop trick is **not** available here unless both mean types turn out to be published. Still valuable for the speed-flow relationship itself and for corridor coverage. Worth checking whether provincial (non-motorway) detectors exist, since those could supply the single-carriageway contrast.

### Germany — BASt — **weaker than expected**

The sensors measure, per vehicle, the vehicle type, speed, **distance to the preceding vehicle**, axle spacing and weights, across 2,000+ stations. Headway per vehicle is exactly what HCM 7 follower density needs.

However, the published open data is described as **hourly** raw data, and repeated searching did **not** confirm that speed appears in the published files at all — the documentation that surfaced describes counts by vehicle group and class. The gap between what the sensors measure and what BASt publishes is the open question.

**Action:** obtain `DZ-Beschreibung.pdf` and the hourly dataset description from bast.de and confirm the column list before planning any German analysis. Do not assume speed is present.

### OpenStreetMap GPS traces — **downgraded**

The bulk `planet.gpx` dump has not been refreshed since 2013. Per-area retrieval via the API still works, and public traces are still being uploaded.

Not recommended as a primary source: travel mode is unknown (cyclists and pedestrians are mixed in), sampling rates vary, and there is no traffic context to pair a trace against. Useful at most as a sanity check.

### Commercial probe data (TomTom, HERE, INRIX)

Not investigated in detail. Given that Flanders supplies variance for free, the case for purchasing has weakened considerably. Revisit only if the cross-sectional contrast cannot be sourced otherwise.

---

## 5. The Traffic-Engineering Baseline

Before calibrating anything, replace the invented `eta` with an established relationship.

**HCM 7th edition** uses **follower density** — vehicles in a follower state per mile per lane, a follower being a vehicle with a headway of 2.5 seconds or less — as the service measure for all two-lane highway configurations. It replaced percent-time-spent-following specifically because PTSF could not be measured in the field, and the older Class I/II/III highway classification was dropped at the same time.

Two consequences for us:

1. The profession has already converged on a **field-measurable** following metric. We should adopt it rather than invent one, and it is directly derivable from any data source carrying per-vehicle headway.
2. HCM is US-calibrated. Germany's **HBS** is the appropriate European counterpart and should be consulted before HCM values are applied to a Benelux/French corridor.

Swapping `eta` for a published speed-flow relationship is a few days of work, costs nothing, and converts M5 from a fabricated parameter into standard traffic engineering. **Do this first** — it may render much of the calibration below unnecessary.

---

## 6. Method

**Step 1 — Literature substitution (days, free).** Replace `eta` in `sim/model.py` with an HCM/HBS speed-flow relationship. Re-run the scenario matrix and compare against the Phase 1 numbers. If archetype I's attainment holds near 51%, the invented parameter was adequate and the remaining steps are confirmation rather than correction.

**Step 2 — Flanders calibration (1–2 weeks).** Ingest MIV minute data across a range of Flemish motorway sites. For each site-minute: compute density from occupancy, `sigma` from the two means, and the class mix. Fit realized car speed (class 2) against density and heavy-vehicle share. Test the core prediction: **`sigma` falls as density rises.** This is the mechanism's signature and needs no distributional assumption.

**Step 3 — Single-carriageway contrast (blocked, needs a source).** The Flemish loops are motorway-only. Options, to be resolved during Step 2: provincial detectors within NDW; a Walloon or French regional counting programme; or falling back on HBS values for single-carriageway roads. **This step is the one at risk and should be scoped early rather than late.**

**Step 4 — Controlled drives (1 week, parallel).** Ten to twenty runs over two or three representative single-carriageway segments, alternating intended cap between runs, phone GPS at 1 Hz. Measure realized mean speed per run, and extract the sawtooth signature and overtaking count from the speed trace. Small sample, but it observes the counterfactual directly, and it produces demonstration material no purchased dataset would.

**Step 5 — Prevalence (days).** Pure OSM geometry over the launch corridor: single carriageway, lane count, limit. No traffic data needed. Produces the share of typical target-journey distance that is structurally exposed to M5.

Steps 1, 4 and 5 are independent of the blocked Step 3 and should proceed regardless.

---

## 7. Falsification Criteria

Fixed in advance, consistent with `SIM-PRD.md` §8.

**Magnitude** — attainment of the intended increment on M5-exposed segments:

| Attainment | Reading |
| --- | --- |
| **< 70%** | Effect is strong; a driver loses most of what they intend |
| **70–85%** | Effect is real but modest |
| **> 85%** | Effect is not material; M5 does not support a product claim |

**Prevalence** — share of typical target-journey distance that is M5-exposed:

| Share | Verdict |
| --- | --- |
| **≥ 25% at < 70% attainment** | **M5 carries the product.** It becomes the headline insight, ahead of both speed-elasticity and the congestion story. |
| **10–25%** | **Supporting insight.** Reported where present, not the product's spine. |
| **< 10%, or attainment > 85% generally** | **Curiosity.** Drop it from the product narrative. |

Both must clear together. A strong effect on 5% of distance is not a feature.

**Mechanism confirmation** — `sigma` must fall measurably with density in Step 2. If speed variance is flat or rising with density, the following-constraint story is wrong regardless of what the mean speeds do, and the result should be treated as disconfirming.

---

## 8. Open Items

1. **Confirm the BASt column list** before relying on German data. The sensors measure speed and headway; whether the published files carry either is unconfirmed and the searches leaned negative.
2. **Find a single-carriageway detector source.** Step 3 is the plan's weak point.
3. **Sanity-check the Wardrop-derived variance** against any source with genuine percentiles, before building conclusions on it.
4. **Check whether NDW publishes both mean types.** If it does, the Wardrop method extends to the Dutch network and the usable corridor roughly doubles.
5. **Investigate `onrustigheid`** in the MIV feed. If it is a turbulence or variance measure, it may give the following signal directly without the Wardrop step.

---

## Sources

- [Vlaams Verkeerscentrum — Data](https://www.verkeerscentrum.be/data)
- [MIV traffic data XSD (tm-data/traffic)](https://github.com/tm-data/traffic/blob/master/miv-verkeersdata.xsd)
- [Meten-in-Vlaanderen: minuutwaarden verkeersmetingen](https://data.gov.be/nl/datasets/7a4c24dc-d3db-460a-b73b-cf748ecb25dc)
- [Nationaal Dataportaal Wegverkeer](https://www.ndw.nu/)
- [NDW open data](https://opendata.ndw.nu/)
- [BASt — Automatische Dauerzählstellen: Rohdaten](https://www.bast.de/DE/Publikationen/Daten/Verkehrstechnik/DZ.html)
- [BASt — Automatische Straßenverkehrszählung](https://www.bast.de/DE/Themen/Digitales/HF_1/Massnahmen/verkehrszaehlung/verkehrszaehlung.html)
- [HCM 7th Edition — two-lane highway methods overview](https://mctrans.ce.ufl.edu/two-lane-highways-analysis-a-look-ahead-at-the-upcoming-release-of-the-hcm-from-a-practitioners-perspective/)
- [Highway Capacity Manual 7th Edition](https://www.nationalacademies.org/publications/26432)
- [Planet.gpx — OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Planet.gpx)
