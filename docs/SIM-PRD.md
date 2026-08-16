# Marginal Value of Speed — Simulation Spec

**Status:** Draft for review
**Version:** 0.1
**Date:** August 2026
**Relates to:** `PCS.md` §5 (Marginal Value of Speed), §6 (Safety Proposition), §19 (Initial Speed Analysis), §45 (Current Strategic Position)

---

## 1. Why This Simulation Exists

`PCS.md` §45 names one differentiating capability:

> Calculate the marginal arrival-time value of speed across the journey.

Everything else in the concept — the timeline (§12), the safety argument (§6), the positioning against Google Maps (§37) — is built on the assumption that this quantity is usually **small and surprising**. The doc's framing throughout is that speed gains evaporate downstream: "improve arrival time by only two minutes because of congestion further ahead" (§1).

That assumption has never been tested, and the worked example in §30 does not survive arithmetic. Its two motorway phases total 340 km at an implied ~110 km/h; raising the cruising cap to 120 km/h removes roughly 15 minutes of driving time, but the doc claims only ~4 minutes reach the destination. No mechanism is given for where the other 11 go.

The purpose of this simulation is to determine, before any product is specified:

1. How large the marginal value of speed actually is on realistic journeys.
2. Which route and traffic structures make it small (the product's home ground) versus large (where the message fails).
3. How common those favourable structures are among the journeys the product intends to serve.

This is a decision-support exercise, not a prototype. No API dependency, no UI, no route data required for Phase 1.

---

## 2. The Reframe This Should Settle

There are two possible product claims, and they are not the same claim.

**Claim A — "Your speed gain evaporates."** Time saved by driving faster is absorbed by downstream conditions, so the driver arrives barely earlier. This is the claim `PCS.md` currently makes. It requires a physical mechanism that destroys upstream time savings.

**Claim B — "Your speed gain is smaller than you think, and here is exactly how much it is."** Time saved is fully preserved, but it only accrues on the portion of the journey where the driver's cruising speed actually binds. On a route that is 40% constrained, raising the cap affects 60% of the distance, so the saving is real but modest relative to the driver's mental model.

Claim A is a stronger, more distinctive product. Claim B is weaker but almost certainly true, and still supports a useful journey briefing — though it substantially weakens the safety proposition in §6, since "you'd save 15 minutes" is not an argument for slowing down.

**The simulation's primary job is to determine how much of the observed effect is Claim A versus Claim B.** That determination should drive the product's positioning, not the other way round.

---

## 3. Candidate Mechanisms

Claim A needs a mechanism. Four are plausible and each behaves differently. The simulation must model them separately rather than lumping all congestion into one bucket.

**M1 — Fixed-speed slowdown.** A section traversed at a reduced but constant speed (roadworks, a permanently slow corridor, sustained heavy-but-moving traffic). Traversal time is `length / v_slow`, independent of when the driver arrives. **Upstream gains pass through untouched.** If real journeys are dominated by M1, Claim A is false and the concept must fall back to Claim B.

**M2 — Capacity-limited queue.** A bottleneck discharging at a fixed rate. Exit time depends on queue position rather than clock arrival, so the relationship between arriving earlier and leaving earlier is non-linear and depends on arrival and discharge rates. Note this can compress *or* amplify a gain depending on regime; it should be modelled explicitly rather than assumed to compress. This is the mechanism most often invoked informally, and the least understood.

**M3 — Scheduled release.** A constraint that lifts at a wall-clock time regardless of arrival: a border post or ferry with fixed operating hours, a tunnel with timed access, a roadworks closure lifted at a set time, a metered ramp on a fixed schedule. **This is the only mechanism that destroys gains completely** — arriving 15 minutes earlier at a barrier that opens at 18:00 yields exactly zero. Where M3 exists, Claim A is unambiguously true.

**M4 — Time-varying congestion.** Congestion whose severity depends on when the driver arrives. Critically, this cuts both ways: arriving earlier at a *building* peak means lighter traffic and a **larger** total gain; arriving earlier at a *dissipating* peak means heavier traffic and a smaller one. M4 cannot be assumed to work in the product's favour and may well work against it.

**Design consequence:** the simulation must report results per-mechanism, not just in aggregate. A headline "average marginal value" that mixes M1 and M3 routes is meaningless.

---

## 4. Model

### 4.1 Journey representation

A journey is an ordered list of segments. Each segment carries:

| Field | Description |
| --- | --- |
| `length_km` | Segment distance |
| `class` | motorway / primary / secondary / urban |
| `legal_limit_kmh` | Applicable speed limit |
| `free_flow_kmh` | Achievable speed absent traffic (≤ legal limit) |
| `mechanism` | `none` / `M1` / `M2` / `M3` / `M4` |
| `mechanism_params` | Per-mechanism parameters (see below) |

Mechanism parameters:

- **M1:** `v_slow_kmh`
- **M2:** `discharge_rate_veh_per_hr`, `arrival_rate_veh_per_hr`, `queue_active_window`
- **M3:** `release_time`, `service_rate` after release
- **M4:** a severity function over arrival time — minimally, a piecewise-linear profile of `v_effective` versus clock time

### 4.2 Driver strategy

A strategy is a single cruising cap `V_cap`. On each segment:

```
v_actual = min(V_cap, legal_limit, condition_implied_speed)
```

`V_cap` is capped at the legal limit throughout — consistent with `PCS.md` §6, the simulation must never model or recommend illegal speeds. Strategies to evaluate: **90, 100, 110, 120 km/h, and "legal maximum throughout."**

### 4.3 What is deliberately excluded from v1

Acceleration and deceleration dynamics, gradient, junction delay, overtaking, lane effects, driver rest stops, weather, and stochastic incident modelling. `PCS.md` §27 correctly notes these all matter for accuracy — but none of them change the sign or rough magnitude of the marginal-value effect, which is the only question v1 needs to answer. Adding them before the core question is settled is premature precision.

---

## 5. Outputs

### 5.1 Primary metrics

**Speed-elastic fraction (SEF).** The share of journey distance on which `V_cap` is the binding constraint. This is the Claim B quantity, and I expect it to explain most of the effect.

**Marginal arrival benefit (MAB).** Minutes of arrival-time improvement per +10 km/h step, reported separately for 90→100, 100→110, and 110→120.

**Pass-through ratio.** Of the raw driving time removed on speed-elastic segments, what fraction actually reaches the destination. **This is the Claim A metric.** A pass-through near 1.0 means gains are preserved and Claim A is false for that route; near 0 means gains are destroyed.

### 5.2 Secondary metrics

- MAB as a share of total journey duration
- Sensitivity of MAB to congestion severity, holding route shape fixed
- Sensitivity of MAB to the *position* of the constraint along the route (under M1 this should be exactly zero — a useful correctness check on the implementation)
- Sensitivity of MAB to departure time under M3 and M4

---

## 6. Scenario Matrix

Eight route archetypes, chosen to span the use cases in `PCS.md` §22:

| ID | Archetype | Shape |
| --- | --- | --- |
| A | Long motorway, free flowing | 400 km, 85% motorway, no significant constraint |
| B | Long motorway, one urban bottleneck | 400 km, 80% motorway, one M2 constraint near destination |
| C | The §30 reference case | Brussels→Strasbourg as described, 435 km, 78% motorway |
| D | Cross-border with timed crossing | 350 km with an M3 constraint mid-route |
| E | Mixed motorway and secondary | 300 km, 45% motorway, 40% secondary |
| F | Rush-hour city arrival | 250 km motorway into an M4 evening peak |
| G | Secondary-road dominated | 220 km, 15% motorway, low speed limits throughout |
| H | Motorway with sustained roadworks | 380 km with a 40 km M1 section |

Each archetype runs against all five speed strategies, and B/D/F additionally sweep congestion severity (light / moderate / severe) and departure time (early / peak / late).

Archetype C is the highest priority: it reproduces the doc's own worked example and will show directly whether the ~4-minute figure in §30 is defensible or needs correcting.

---

## 7. Falsification Criteria

**These are fixed before the simulation runs.** Proposed thresholds for your confirmation — move them now if you disagree, not after seeing results.

Judged on the **110→120 km/h** step, across journeys of 3 hours or longer:

| Median MAB | Verdict |
| --- | --- |
| **< 5 minutes** | **Thesis strong.** The marginal-value message stands as `PCS.md` §45's headline capability. Proceed to product PRD as written. |
| **5–10 minutes** | **Thesis conditional.** The message works only on identifiable route types. The product must be able to detect those routes and stay quiet on the others. Positioning shifts toward Claim B. |
| **> 10 minutes** | **Thesis weak.** "Speeding doesn't help" is not supportable as a headline on the product's target journeys. §6's safety proposition needs rewriting or dropping, and the product becomes a journey briefing whose speed analysis is one honest number among several. |

Two supporting criteria:

- **Mechanism prevalence.** If M1 dominates realistic long-distance routes and M3 is rare, Claim A is not generally available regardless of the median MAB.
- **Pass-through ratio.** If the median pass-through across archetypes exceeds 0.8, the "gains evaporate downstream" framing should be removed from `PCS.md` on accuracy grounds, independent of the product decision.

A result in the "weak" band is a genuinely useful outcome, not a failure. It redirects the product early and cheaply, which is the entire point of running this before the PRD.

---

## 8. Method and Deliverables

**Phase 1 — Synthetic (2–3 days).** Implement the model, run the full scenario matrix on hand-specified route definitions. No external data. This alone answers whether the effect exists in principle and which mechanisms produce it.

**Phase 2 — Real-route validation (3–4 days, conditional).** Take 10–15 real routes, derive segment structure from routing and traffic data, and check that Phase 1's archetypes resemble reality — particularly the mix of mechanisms and the typical speed-elastic fraction. This is the first point at which API cost and data quality (`PCS.md` §27) become live concerns, so it doubles as a scouting exercise for those questions.

Phase 2 runs only if Phase 1 lands in the "strong" or "conditional" band. If Phase 1 says "weak," the concept needs rethinking before more effort goes in.

**Deliverables:**

1. Simulation code, in-repo and runnable, with route definitions as data rather than hardcoded
2. Results table: every archetype × strategy × sensitivity combination
3. A written verdict against §7's criteria, including a recommended correction to `PCS.md` §30 if the arithmetic there does not hold
4. If the verdict is "conditional," a first cut at the route-detection rule the product would need

---

## 9. Open Questions

1. **Are the §7 thresholds right?** 5 and 10 minutes are my judgement of what a driver on a 4-hour trip would call negligible versus meaningful. This is the single most consequential number in the spec.
2. **Is 110→120 the right headline step?** It matches the doc's examples and European motorway limits, but if the target corridor is predominantly 130 km/h, the step should change.
3. **Should risk and fuel be quantified in v1?** `PCS.md` §3 argues additional speed costs risk, fuel and stress. Quantifying the fuel side would let the product say "4 minutes saved, €7 of fuel spent," which may be a stronger argument than arrival time alone — and would survive even a "weak" verdict on the time question. My inclination is to keep v1 focused, then add fuel in v2 if the time result is weak.
4. **Does M4 need empirical traffic profiles?** Modelling time-varying congestion credibly may require historical traffic data, which Phase 1 deliberately avoids. A crude piecewise profile may be enough to establish direction and rough magnitude.
