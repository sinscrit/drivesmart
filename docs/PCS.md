# Journey Intelligence

## Product Concept & Strategy

**Status:** Working concept
**Version:** 0.1
**Date:** August 2026

---

## 1. Executive Summary

Journey Intelligence is a proposed journey-analysis product that complements existing navigation applications rather than replacing them.

Products such as Google Maps and Waze are highly effective at answering:

> What route should I take, and when will I arrive?

Journey Intelligence addresses a different set of questions:

- What will this journey actually be like?
- Where will I make or lose time?
- How much does driving faster on a particular section actually affect my arrival time?
- Which parts of the journey are predictable, congested, fast, slow, urban, motorway, rural, or otherwise significant?

The initial product would allow a user to enter a journey or share one from an existing mapping application. The system would analyze the route and convert it into a simple linear journey profile containing road characteristics, expected speeds, traffic conditions, bottlenecks, and actionable insights.

The central product hypothesis is that drivers can make better, safer and more efficient decisions when they understand the marginal value of speed across the complete journey.

For example:

> Raising your cruising speed from 110 to 120 km/h over the next motorway section would save approximately two minutes, and increase fatal-crash risk on that section by roughly 40%.

The product therefore evaluates speed as an investment rather than a preference: what is actually bought, and what is paid for it.

The initial product would therefore be a pre-trip journey intelligence tool, not another turn-by-turn navigation application.

---

## 2. The Observation

Modern navigation applications provide excellent route selection.

A typical user receives:

- a recommended route;
- alternative routes;
- distance;
- estimated arrival time;
- traffic visualization;
- incidents and closures;
- turn-by-turn navigation.

However, these systems generally present the journey as a route on a map plus a global ETA.

They provide comparatively little explanation of how that ETA is composed.

A three-hour journey could contain:

- 20 minutes of urban traffic;
- 90 minutes of free-flowing motorway;
- 25 minutes of congestion;
- 30 minutes of secondary roads;
- 15 minutes of local roads.

Those characteristics significantly affect how the journey feels and how a driver should think about progress.

The current navigation paradigm largely hides this structure.

---

## 3. The Core Problem

Drivers naturally associate increased speed with earlier arrival.

Over a simple unconstrained road:

> higher speed → lower travel time.

Real journeys are not simple unconstrained roads.

They contain downstream constraints:

- congestion;
- intersections;
- traffic lights;
- motorway bottlenecks;
- slower roads;
- urban sections;
- roadworks;
- queues;
- speed restrictions;
- difficult terrain;
- incidents.

Consequently, additional speed during one section can produce surprisingly little improvement in final arrival time.

A driver may therefore take additional risk, consume additional fuel or energy, brake more frequently and experience greater stress while obtaining almost no meaningful improvement in arrival time.

Existing navigation products rarely communicate this relationship explicitly.

---

## 4. Product Thesis

The product thesis is:

> A journey should be understood as a sequence of conditions and constraints, not merely as a line between two points.

By combining route geometry, traffic information, road characteristics and speed information, a system can construct a model of the journey and explain what is likely to happen along it.

The product can then answer a new question:

> What speed actually provides useful progress at this point in this particular journey?

This concept is referred to in this document as **useful speed**.

---

## 5. Marginal Value of Speed

The key analytical concept is the **Marginal Value of Speed**.

Instead of asking:

> How much faster can I travel?

the system asks:

> How much earlier will I actually arrive if I travel faster during this section?

Consider a motorway section where the legal limit is 120 km/h.

The system might calculate:

| Cruising speed | Predicted arrival |
| --- | --- |
| 100 km/h | 17:42 |
| 110 km/h | 17:39 |
| 120 km/h | 17:38 |

The important information is therefore not simply that 120 km/h is faster than 100 km/h.

It is:

> Increasing from 110 to 120 km/h is currently expected to improve arrival by approximately one minute.

This can become a distinctive product metric.

Possible terminology includes:

- Time Value of Speed;
- Marginal Arrival Benefit;
- Useful Speed;
- Effective Speed;
- Journey Speed Value.

Terminology should be validated with users.

---

## 6. Safety Proposition

The concept has an important safety dimension.

Traditional safety messaging tells drivers:

> Don't speed.

Journey Intelligence can provide a personalized, situational argument:

> Going faster here is unlikely to get you there meaningfully sooner.

For example:

> Heavy congestion begins approximately 35 km ahead. Increasing your cruising speed from 110 to 120 km/h before that point is expected to improve final arrival time by less than one minute.

The system must never recommend exceeding legal speed limits.

Instead, it demonstrates where additional speed within the available legal range has little practical value.

The intended outcome is smoother, calmer and more informed driving.

### Value per Unit of Risk

The arrival-time argument above depends on journey structure: it is strong where downstream constraints absorb progress and weak where they do not. A second argument does not depend on journey structure at all, and is therefore more robust.

Time saved over a fixed distance scales as `1/v` — each additional 10 km/h buys progressively fewer minutes. Crash risk scales in the opposite direction: the established power model (Nilsson, sustained by Elvik's later meta-analyses) puts fatal-crash risk at approximately the fourth power of mean speed, serious injury at the third, and slight injury at the second.

Dividing one by the other, **the time bought per unit of additional risk falls with roughly the fifth power of speed.**

Per 100 km of speed-elastic driving:

| Speed step | Time saved | Approximate fatal-risk multiplier |
| --- | --- | --- |
| 100 → 110 km/h | 5.5 min | ×1.46 |
| 110 → 120 km/h | 4.5 min | ×1.42 |
| 120 → 130 km/h | 3.8 min | ×1.38 |

Across the full range, 100 → 130 km/h buys under 14 minutes per 100 km while nearly tripling fatal-crash risk.

This relationship holds on empty motorway in perfect conditions. It requires no bottleneck, no queue and no congestion, which makes it available on every journey the product analyzes rather than only on favourably-structured ones.

The product objective can therefore be stated as: **maximize value per unit of risk taken.** Where additional speed increases exposure without materially advancing arrival, it is a poor investment — and the product's role is to make that visible with the driver's own journey and numbers rather than as a general exhortation.

---

## 7. Existing Market

Research indicates substantial technical precedent for this concept, although implementations are fragmented across different industries.

### Rail

Railway Driver Advisory Systems (DAS) calculate speed profiles that allow trains to meet timetable requirements while reducing unnecessary acceleration, braking and energy consumption.

Examples include systems such as:

- Knorr-Bremse LEADER;
- Cubris GreenSpeed;
- Energymiser;
- HaslerRail DAS.

Rail provides perhaps the strongest conceptual precedent.

The fundamental question is:

> Given the route, constraints and required arrival time, what speed profile should the train follow?

### Heavy Trucks

Truck manufacturers use predictive cruise and powertrain systems that look ahead along the route.

Examples include:

- Volvo I-See;
- Mercedes-Benz Predictive Powertrain Control;
- Scania Active Prediction / predictive cruise systems.

These systems use information such as:

- gradients;
- road geometry;
- speed limits;
- topography;
- upcoming road conditions.

They adjust acceleration, coasting, gearing and speed to reduce fuel consumption without materially compromising journey time.

### Passenger Vehicles

Passenger vehicles increasingly contain local predictive-driving features.

Examples include:

- Audi Predictive Efficiency Assist;
- Porsche InnoDrive;
- Mercedes-Benz ECO Assist and predictive assistance systems.

These systems can anticipate:

- bends;
- junctions;
- roundabouts;
- speed-limit changes;
- traffic;
- terrain.

However, these capabilities are primarily embedded within the vehicle rather than presented as a general journey-intelligence product.

### GLOSA

Green Light Optimal Speed Advisory provides another important precedent.

A GLOSA system might advise a driver to approach a traffic light more slowly because travelling faster would merely result in reaching a red light sooner.

This demonstrates the underlying behavioral principle:

> Higher instantaneous speed does not necessarily mean greater useful progress.

Journey Intelligence extends that concept from the next traffic light to potentially the entire journey.

---

## 8. Current Navigation Market

Major consumer navigation products include:

- Google Maps;
- Waze;
- Apple Maps;
- TomTom;
- Sygic;
- HERE-based products;
- specialist applications such as A Better Routeplanner.

These products already possess enormous advantages in:

- mapping;
- routing;
- traffic data;
- navigation;
- installed user base;
- CarPlay integration;
- Android Auto integration.

Competing directly with them as a general-purpose navigator would therefore create a substantial and unnecessary product challenge.

Journey Intelligence should initially complement rather than replace navigation.

---

## 9. Market Gap Hypothesis

The market contains:

- Navigation systems that optimize routes.
- Eco-routing systems that optimize route selection for energy.
- Fleet systems that analyze driver behavior.
- Vehicle systems that optimize acceleration and speed.
- Rail systems that optimize complete speed profiles.

What appears less common in mainstream consumer applications is:

> A whole-journey analytical layer explaining the relationship between road conditions, traffic, speed and final arrival time.

The potential whitespace therefore lies at the intersection of:

> navigation + predictive traffic + road intelligence + speed optimization + driver explanation.

---

## 10. Product Positioning

Journey Intelligence should not initially position itself as:

> "A better Google Maps."

Instead:

> Understand your drive before you start.

Google Maps/Waze can continue answering:

> How do I get there?

Journey Intelligence answers:

> What should I expect along the way?

and:

> What will actually affect when I arrive?

---

## 11. Initial User Experience

The MVP should have two principal entry mechanisms.

### A. Plan a Journey

The user enters:

- origin;
- destination;
- departure time.

The application calculates and analyzes the journey.

### B. Share a Journey

The user plans a journey using an existing application such as Google Maps or Waze.

They select:

> Share → Journey Intelligence

The application extracts whatever journey information is available from the shared link, such as:

- destination;
- origin where available;
- waypoints where available.

It then reconstructs and analyzes an equivalent route.

The MVP should not depend on perfectly recovering the exact road-by-road route selected in the originating application.

---

## 12. The Journey Timeline

The principal interface should probably not be another map.

Instead, the route can be transformed into a linear representation of the journey.

For example:

```
HOME
  ↓
  18 km — Urban
  Expected 35–50 km/h
  Moderate traffic
  ↓
  142 km — Motorway
  Expected 105–115 km/h
  Free flowing
  ↓
  23 km — Congestion
  Expected 35–55 km/h
  ~25 minutes
  ↓
  96 km — Motorway
  Expected 105–120 km/h
  Free flowing
  ↓
  12 km — Urban
  Expected 25–40 km/h
  ↓
DESTINATION
```

This creates a mental model of the journey that conventional maps do not readily provide.

---

## 13. Journey Summary

The timeline can be accompanied by a high-level summary.

For example:

- **Expected journey:** 4h 23m
- **Motorway:** 78%
- **Urban:** 12%
- **Secondary roads:** 10%
- **Expected congestion:** 37 minutes
- **Main bottleneck:** Luxembourg approach
- **Journey uncertainty:** ±18 minutes

Useful-speed insight:

> Travelling at 120 rather than 110 km/h during the main motorway sections is currently expected to improve arrival time by approximately four minutes, at roughly 40% higher fatal-crash risk over those sections.

*Note: the four-minute figure is illustrative and unverified. Pending the simulation in `SIM-PRD.md`, no specific arrival-benefit number in this document should be treated as established.*

The objective is not to overwhelm the user with road data.

It is to convert complex geographic and traffic information into a small number of understandable insights.

---

## 14. Route Comparison

The product can eventually compare routes using dimensions beyond ETA.

For example:

**Route A**

- 3h 52m
- Mostly motorway
- Higher congestion exposure
- Arrival uncertainty ±24m

**Route B**

- 3h 57m
- More secondary roads
- Lower congestion exposure
- Arrival uncertainty ±11m

Conventional navigation might emphasize Route A because it is nominally five minutes faster.

Journey Intelligence might explain:

> Route A is approximately five minutes faster under expected conditions, but Route B is substantially more predictable.

This introduces the concept of **route quality** rather than simply route speed.

---

## 15. Route Resilience

A longer-term product capability is route resilience.

Two routes with identical ETAs may respond very differently to disruption.

A motorway corridor with few exits or alternatives could suffer a major delay following an accident.

A parallel route through a denser road network might allow numerous rerouting options.

A future resilience score could consider:

- availability of alternative roads;
- historical congestion volatility;
- incident frequency;
- dependence on bridges/tunnels;
- motorway bottlenecks;
- rerouting possibilities;
- variability of historical journey times.

This would help distinguish:

> fastest expected route

from:

> most reliable route.

---

## 16. Technical Concept

The initial system would combine multiple data sources.

### Routing Layer

Potential providers include:

- Google Routes;
- HERE;
- TomTom;
- OpenStreetMap-based routing engines.

This layer provides:

- route geometry;
- distance;
- ETA;
- traffic-aware ETA;
- alternatives;
- route steps.

### Traffic Layer

Provides:

- expected congestion;
- traffic speed;
- traffic severity;
- traffic-aware journey duration.

Google Routes, HERE and TomTom are potential sources.

### Road Intelligence Layer

OpenStreetMap is particularly useful for:

- motorway/primary/secondary/residential classification;
- speed limits;
- road surfaces;
- lane counts where available;
- access restrictions;
- road characteristics.

Commercial datasets from HERE or TomTom may later supplement this information.

---

## 17. Processing Pipeline

The conceptual pipeline is:

```
Journey input/share
  ↓
Origin + destination + waypoints
  ↓
Routing engine
  ↓
Detailed route geometry
  ↓
Map matching
  ↓
Road classification
  ↓
Traffic enrichment
  ↓
Raw route segments
  ↓
Segment aggregation
  ↓
Expected-speed model
  ↓
Journey timeline
  ↓
Speed-value analysis
  ↓
User insights
```

A critical technical capability will be converting potentially hundreds or thousands of raw road segments into perhaps 5–15 meaningful journey phases.

That segmentation and interpretation engine could become an important proprietary component of the product.

---

## 18. Speed Model

The system should distinguish several concepts.

**Legal Speed** — the applicable speed limit.

**Road Capability** — the speed implied by the road type and geometry under suitable conditions.

**Attainable Speed** — the mean speed the traffic stream actually permits, which is frequently well below both the legal limit and the vehicle's capability.

**Expected Speed** — the speed realistically achievable given traffic and road conditions.

**Useful Speed** — the speed beyond which additional speed provides progressively less meaningful improvement in final arrival time.

The relationship between these values becomes part of the journey model.

### Why Attainable Speed Matters

A road may permit 130 km/h and a vehicle may be capable of 180, but if the traffic stream is moving at 90 with heavy goods vehicles at 85, no driver sustains their intended cruising speed. The realistic pattern is a sawtooth: accelerate into a gap, close on a slower vehicle, wait for an overtaking opportunity, pass, accelerate again.

The consequence is that raising an intended cruising speed may produce very little change in realized mean speed. Peak speed and mean speed diverge sharply, and it is mean speed that determines arrival time.

This effect is well established in traffic engineering as percent time spent following, and it is strongest on single-carriageway roads where overtaking opportunities are limited. It is distinct from congestion: the road is not jammed, it is simply occupied by vehicles travelling more slowly than the driver intends.

It also compounds the risk argument in §6. Chasing a high cruising speed through a mixed stream does not merely fail to save much time — it requires repeated overtaking manoeuvres, which are among the higher-risk actions available to a driver. The product can therefore express a segment insight of the form:

> Your realistic mean speed here is approximately 108 km/h whether you aim for 110 or 140. Pursuing the higher speed is expected to save around two minutes and require roughly fourteen additional overtaking manoeuvres.

Establishing how reliably attainable speed can be estimated from available data is a priority research question (§42).

---

## 19. Initial Speed Analysis

The first implementation does not need a sophisticated machine-learning model.

The system could initially simulate several legal speed strategies.

For example:

- maximum 90 km/h;
- maximum 100 km/h;
- maximum 110 km/h;
- applicable legal/traffic speed.

For each scenario, the system calculates expected arrival.

This produces something like:

| Strategy | Expected arrival |
| --- | --- |
| Max 90 | 18:53 |
| Max 100 | 18:47 |
| Max 110 | 18:43 |
| Normal legal-speed profile | 18:41 |

The product can then communicate diminishing returns.

More sophisticated traffic distributions and probabilistic models can follow later.

---

## 20. MVP Definition

The MVP should be deliberately narrow.

It should not attempt to provide turn-by-turn navigation.

It should provide a pre-trip journey briefing.

### MVP Input

- origin;
- destination;
- departure time;

or:

- shared mapping/navigation link.

### MVP Output

- expected journey duration;
- route distance;
- linear journey timeline;
- road-type breakdown;
- congestion breakdown;
- expected speeds;
- major bottlenecks;
- alternative-route comparison where useful;
- initial useful-speed analysis.

The user can subsequently continue navigation using Google Maps, Waze or another preferred application.

---

## 21. Why Start Pre-Trip?

A pre-trip product avoids several difficult problems:

- replacing established navigation applications;
- building complete navigation UI;
- Android Auto navigation requirements;
- CarPlay navigation requirements;
- continuous GPS navigation;
- voice guidance;
- rerouting;
- background navigation complexity.

It also provides a clear usage moment:

> Before a significant journey, understand what you're about to encounter.

The concept is likely to have greater initial value for longer or unfamiliar journeys than short everyday trips.

---

## 22. Initial Target Use Cases

Potentially strong early use cases include:

- long-distance journeys;
- holiday driving;
- unfamiliar routes;
- cross-border travel;
- business travel;
- airport journeys;
- professional drivers;
- EV drivers;
- motorhome/caravan users;
- motorcycle touring;
- journeys during heavy traffic periods.

The product should initially be validated against these higher-value journeys rather than attempting to optimize everyday five-minute trips.

---

## 23. Potential Future Evolution

If the pre-trip concept proves valuable, the product could progressively become more real-time.

Possible future capabilities include:

**Live Journey Companion** — continue updating journey intelligence while another navigation application handles navigation.

**Dynamic Useful-Speed Advice** — recalculate the value of speed as congestion changes.

**Incident Sensitivity** — explain how an accident or closure changes route risk.

**Route Reliability** — predict arrival-time distributions rather than a single ETA.

**Vehicle Awareness** — incorporate:

- EV range;
- fuel consumption;
- vehicle efficiency;
- towing;
- vehicle speed limitations.

**Driver Preferences** — optimize journeys according to preferences such as:

- predictability;
- comfort;
- motorway preference;
- fuel economy;
- scenic driving;
- reduced congestion;
- fewer difficult junctions.

---

## 24. Potential Business Models

Business-model assumptions remain unvalidated.

Possible models include:

**Consumer Subscription** — premium journey analysis for frequent long-distance drivers.

**Freemium** — basic journey breakdown free, with advanced reliability, speed-value and historical analysis paid.

**Fleet / Professional Driver Product** — journey intelligence for fleets, delivery operators or professional drivers.

**OEM Licensing** — provide the analysis engine to vehicle manufacturers.

**Navigation/Data Partnerships** — provide journey-intelligence APIs to existing navigation products.

**Insurance / Safety Applications** — potentially use journey intelligence to support safer driving programs, subject to significant privacy and regulatory considerations.

---

## 25. Strategic Advantage

The product should avoid competing in areas where incumbents have overwhelming advantages.

It does not need to own:

- maps;
- basic routing;
- traffic collection;
- turn-by-turn navigation.

Instead, it should build intelligence on top of those capabilities.

Potential proprietary value lies in:

1. journey segmentation;
2. expected-speed modelling;
3. marginal speed-value calculations;
4. route reliability analysis;
5. route resilience analysis;
6. explanation and presentation of journey conditions.

The objective is therefore not to build another mapping database.

It is to build a **journey reasoning engine**.

---

## 26. Key Product Hypotheses

The project currently depends on several hypotheses.

**H1 — Users want journey understanding.** Drivers care about more than ETA when undertaking substantial journeys.

**H2 — Linear representation adds value.** A journey timeline communicates useful information that is difficult to perceive from a conventional map.

**H3 — Speed-value information changes behavior.** Showing that additional speed produces negligible arrival benefit can influence driving decisions.

**H4 — Existing data is sufficient.** Routing, traffic and road datasets contain enough information to construct sufficiently accurate journey profiles.

**H5 — Sharing provides viable distribution.** Users will share or submit routes from existing navigation tools rather than requiring Journey Intelligence to replace them.

**H6 — Analysis can be sufficiently simple.** The system can turn complex route data into useful conclusions without overwhelming users.

These should be treated as hypotheses requiring validation rather than assumptions.

---

## 27. Principal Risks and Open Questions

### User Demand

Will drivers actually consult another application before travelling?

### Frequency

Are sufficiently long or complex journeys frequent enough to support a standalone consumer product?

### Route Sharing

How reliably can routes shared from Google Maps, Waze and Apple Maps be interpreted?

In particular:

- Does the shared object contain only a destination?
- Does it preserve origin?
- Are waypoints preserved?
- Can the specifically selected alternative route be identified?
- If not, how closely can the system reconstruct it?

The MVP should tolerate imperfect route transfer by clearly describing the analyzed route rather than claiming that it is necessarily identical to the route shown by the originating navigation application.

### Data Quality

OpenStreetMap coverage varies geographically.

Attributes such as:

- road classification;
- speed limit;
- number of lanes;
- road surface;
- access restrictions

may be incomplete or inconsistent.

The product must determine which attributes are sufficiently reliable for consumer-facing recommendations.

### Traffic Accuracy

Current traffic is inherently dynamic.

A prediction made before departure may change substantially during a long journey.

The product therefore needs to distinguish between:

- known road characteristics;
- current traffic conditions;
- predicted conditions;
- uncertain conditions.

### Speed-Modelling Accuracy

The relationship between speed and final arrival time is more complicated than simply dividing distance by speed.

Real journeys involve:

- acceleration and deceleration;
- junctions;
- traffic lights;
- variable traffic;
- queues;
- road geometry;
- overtaking;
- speed-limit changes;
- incidents.

The initial model can be approximate, but the product must avoid presenting false precision.

### Data Licensing

Combining Google, OpenStreetMap, HERE, TomTom or other datasets may introduce restrictions concerning:

- caching;
- derived data;
- displaying data from competing mapping providers;
- attribution;
- long-term storage;
- commercial usage.

Licensing should be investigated before the architecture becomes dependent on a particular combination of providers.

### API Economics

Traffic-aware routing and commercial road data can become expensive at scale.

The cost per analyzed journey therefore needs to be understood early.

### Driver Distraction

If the product evolves into an in-drive companion, recommendations must be extremely simple and appropriately timed.

The pre-trip MVP largely avoids this problem.

---

## 28. Important Product Boundary

The system should distinguish between analysis and instruction.

The objective is not to tell a driver:

> Drive at exactly 107 km/h.

Such precision would be inappropriate given changing real-world conditions.

Instead, the product should communicate conclusions such as:

> There is little journey-time benefit from maintaining the maximum permitted speed over the next motorway section.

or:

> Traffic conditions ahead currently determine most of your arrival time.

or:

> This is the section where differences in cruising speed have the greatest effect on arrival time.

The system provides decision intelligence, while the driver remains responsible for appropriate speed and driving behavior.

---

## 29. Information Hierarchy

The product should resist the temptation to expose every available piece of data.

A useful hierarchy could be:

### Level 1 — Journey at a Glance

Immediately visible:

- ETA;
- distance;
- major journey phases;
- congestion exposure;
- principal bottleneck;
- one or two important insights.

### Level 2 — Journey Timeline

A linear representation showing:

- road types;
- expected speeds;
- traffic;
- major transitions;
- significant constraints.

### Level 3 — Detailed Analysis

For users who want more information:

- individual segments;
- speed limits;
- traffic assumptions;
- route alternatives;
- time-at-speed scenarios;
- reliability;
- road surfaces;
- detailed bottlenecks.

This keeps the primary experience simple while allowing the underlying analytical richness to remain accessible.

---

## 30. Example User Journey

A user intends to drive from Brussels to Strasbourg.

They normally use Google Maps.

**Step 1.** They search for the journey in Google Maps.

**Step 2.** They use the operating system's Share function and select Journey Intelligence.

Alternatively, they enter Brussels and Strasbourg directly into Journey Intelligence.

**Step 3.** Journey Intelligence resolves the origin, destination and any available waypoints.

**Step 4.** The system calculates an equivalent traffic-aware route and enriches it with road information.

**Step 5.** The user receives:

> Brussels → Strasbourg
> 435 km
> Expected: 4h 31m
> Typical uncertainty: ±20m

The journey timeline shows:

```
Brussels urban        18 km · ~31 min
  ↓
Motorway             167 km · ~1h31
  ↓
Luxembourg congestion 31 km · ~39 min
  ↓
Motorway             173 km · ~1h36
  ↓
Strasbourg approach   46 km · ~54 min
```

The system highlights:

**Main constraint**

> Congestion approaching Luxembourg currently accounts for approximately 22 minutes of additional journey time.

And:

**Speed insight**

> This journey contains 340 km of motorway currently flowing at around 110 km/h. Raising your cruising speed to 120 km/h would remove approximately 15 minutes of driving time and increase fatal-crash risk over those sections by roughly 40%.

> How much of those 15 minutes reaches your destination depends on the constraints ahead. The Luxembourg congestion is a sustained slow section rather than a timed or capacity-limited one, so most of the saving is expected to pass through.

*Note: an earlier draft of this document claimed a destination benefit of approximately four minutes here, without specifying any mechanism that would absorb the remaining eleven. That figure was not defensible and has been replaced. The pass-through fraction is the subject of the simulation specified in `SIM-PRD.md`, and the wording above should be revised once that produces a measured value.*

**Step 6.** The user closes Journey Intelligence and navigates normally using their preferred navigation application.

This is the complete MVP experience.

---

## 31. The Linear Journey Model

The linear timeline could become the visual identity of the product.

Maps are excellent for answering:

> Where am I going?

A timeline may be better for answering:

> What happens next?

Distance along the horizontal axis represents progress through the journey.

Different sections represent different journey environments.

For example:

```
START
Urban ━━━ Motorway ━━━━━━━━━━━ Traffic ━━━ Motorway ━━━━━━━━━ Secondary ━━━ Destination
```

Important events can be attached to positions along the line:

- congestion;
- tolls;
- border crossings;
- difficult junctions;
- charging/fuel stops;
- roadworks;
- major speed changes;
- weather changes;
- rest opportunities.

The timeline therefore has the potential to evolve beyond speed analysis into a general journey briefing interface.

---

## 32. Broader Product Opportunity

The initial insight concerns speed.

However, the underlying product may ultimately be broader.

Once a journey has been transformed into a structured timeline, many other questions become possible:

- Where will the difficult parts be?
- When should I take a break?
- Where is traffic most uncertain?
- Where will fuel consumption increase?
- Where will an EV consume significantly more energy?
- Which route is less stressful?
- Which route has fewer bottlenecks?
- Which route is easier when towing?
- Which route provides more opportunities to stop?
- Where does weather become significant?

This suggests that the deeper product may not ultimately be a speed advisory system.

It may be a **journey intelligence platform**, with useful-speed analysis as its first distinctive capability.

---

## 33. Data Architecture Direction

The architecture should deliberately separate raw data providers from the product's analytical model.

A simplified architecture is:

```
Input
  ↓
Route Provider Adapter
  ↓
Canonical Route Model
  ↓
Road Enrichment
  ↓
Traffic Enrichment
  ↓
Journey Segmentation
  ↓
Journey Intelligence Engine
  ↓
Presentation API
  ↓
Web / Mobile UI
```

This allows Google, HERE, TomTom or other providers to be substituted without rewriting the product logic.

The proprietary model should operate on a normalized internal representation rather than directly on a particular provider's response format.

---

## 34. Canonical Segment Model

Internally, each route segment could eventually contain attributes such as:

- segment ID;
- start/end coordinates;
- length;
- road classification;
- road name;
- legal speed limit;
- expected speed;
- free-flow speed;
- traffic speed;
- congestion classification;
- surface;
- lanes;
- gradient;
- urban/rural classification;
- historical variability;
- predicted traversal time;
- confidence score.

Not every source will provide every attribute.

The canonical model should therefore support missing data and record the source/confidence of each value.

---

## 35. Journey Segmentation Engine

Raw map data may divide a journey into hundreds or thousands of road segments.

That is unsuitable for a human-facing journey briefing.

The segmentation engine should merge adjacent segments when their characteristics are sufficiently similar.

A new meaningful journey phase might be created when there is a significant change in:

- road class;
- expected speed;
- legal speed;
- traffic;
- urban/rural environment;
- surface;
- road conditions;
- route complexity.

For example, forty consecutive motorway segments might become:

> Motorway — 84 km — approximately 46 minutes

while a significant congestion event creates a separate phase:

> Heavy congestion — 11 km — approximately 22 minutes

The quality of this abstraction is likely to be one of the product's most important technical differentiators.

---

## 36. Journey Intelligence Engine

The intelligence engine sits above segmentation.

Its role is not merely to calculate statistics but to determine:

> What is worth telling the user?

Potential insight types include:

**Bottleneck Insight**

> Most expected delay occurs during a 17 km section approaching Antwerp.

**Speed-Value Insight**

> Increasing cruising speed during the next motorway phase produces little expected destination-time benefit.

**Risk-Value Insight**

> The time gained on this section costs disproportionate risk: 40% higher fatal-crash exposure for four minutes.

**Attainability Insight**

> Traffic flow on this section limits your realistic mean speed to approximately 105 km/h regardless of your intended cruising speed.

**Reliability Insight**

> This journey has unusually high arrival-time uncertainty because of traffic around Brussels.

**Alternative-Route Insight**

> The alternative route is seven minutes slower on average but considerably less exposed to congestion.

**Road-Character Insight**

> The final 45 minutes contain predominantly slower secondary roads.

This insight-selection layer may eventually become as important as the underlying calculations.

---

## 37. Competitive Strategy

The product should avoid competing with navigation incumbents on their strongest dimensions.

Do not initially compete on:

- map quality;
- POI search;
- turn-by-turn directions;
- voice navigation;
- live rerouting;
- traffic collection;
- street imagery.

Instead, leverage existing infrastructure and compete on:

- interpretation;
- explanation;
- journey understanding;
- predictive insights;
- route quality;
- useful-speed analysis.

This creates a complementary position rather than a replacement proposition.

---

## 38. Distribution Hypothesis

A major strategic question remains:

> Why will somebody open this product if Google Maps is already open?

Several possible answers should be tested.

**Share From Maps** — the lowest-friction hypothesis:

> Google Maps/Waze → Share → Journey Intelligence

**Long-Trip Planning** — users deliberately consult Journey Intelligence before substantial journeys.

**Web Analysis** — a lightweight website allows users to paste a Maps link without installing an application. This may be particularly attractive for early validation.

**Browser / Platform Integration** — later integrations could reduce friction further.

**Professional Use** — professional drivers or fleet operators may have sufficient recurring value to integrate the product directly into their workflow.

The MVP should test distribution behavior just as seriously as technical feasibility.

---

## 39. MVP Delivery Form

A native mobile application may not be necessary initially.

A particularly lean validation product could simply be:

> journeyintelligence.example

with:

> Paste a Google Maps/Waze link

or:

> From: \_\_\_\_\_\_
> To: \_\_\_\_\_\_
> Departure: \_\_\_\_\_\_

followed by:

> Analyze Journey

This produces the journey briefing.

Such an implementation could validate the central value proposition before investing heavily in native applications, sharing extensions or vehicle integrations.

---

## 40. MVP Success Criteria

The first prototype should answer four questions.

**1. Can we build the journey model?** Can available data reliably produce meaningful route segments?

**2. Can we calculate useful speed?** Can we produce defensible estimates of how different legal cruising-speed strategies affect final arrival time?

**3. Do users understand the timeline?** Does the linear journey representation communicate something that a conventional map does not?

**4. Do users care?** After seeing the analysis, do drivers say:

> "I would want this before a long journey."

The fourth question is ultimately more important than the first three.

---

## 41. Initial Validation Plan

Before building a complete product, create a prototype capable of analyzing perhaps 20–50 representative journeys.

Include:

- short motorway journeys;
- long motorway journeys;
- urban-to-urban journeys;
- cross-border journeys;
- heavily congested routes;
- routes with meaningful alternatives;
- rural routes;
- journeys with mixed road types.

For each journey, evaluate:

- segmentation quality;
- traffic representation;
- road classification;
- speed-value calculations;
- timeline usefulness.

Then place the results in front of real drivers.

Do not initially ask:

> "Would you buy this?"

Instead, give them a journey they understand and observe what information attracts their attention and what changes their interpretation of the trip.

---

## 42. Research Priorities

The next research phase should investigate five areas in parallel.

### Technical

- shared-link parsing;
- routing APIs;
- traffic APIs;
- OSM map matching;
- speed-limit coverage;
- historical traffic availability.

### Mathematical

Develop the first model for:

> marginal arrival-time benefit of speed.

### UX

Prototype several representations of the linear journey timeline.

### Market

Conduct deeper competitive analysis of:

- rail Driver Advisory Systems;
- truck predictive-driving systems;
- passenger-car predictive assistance;
- eco-routing;
- fleet driver coaching;
- specialist journey planners.

### Commercial

Determine:

- API cost per journey;
- likely infrastructure cost;
- licensing constraints;
- plausible consumer pricing;
- fleet/OEM alternatives.

---

## 43. Near-Term Product Roadmap

**Phase 0 — Feasibility.** Build scripts capable of analyzing individual journeys. No polished application required.

**Phase 1 — Journey Briefing Prototype.** User enters origin/destination. Return:

- route;
- timeline;
- road breakdown;
- congestion;
- useful-speed analysis.

**Phase 2 — Shared Route.** Accept shared/pasted Google Maps and Waze journeys.

**Phase 3 — Route Comparison.** Compare alternatives by:

- ETA;
- congestion;
- reliability;
- journey character;
- useful-speed profile.

**Phase 4 — Real-Time Companion.** Explore updating the journey model while the user navigates with an existing navigation product.

**Phase 5 — Platform.** Expose Journey Intelligence through an API for:

- fleets;
- OEMs;
- navigation products;
- mobility platforms.

Progression beyond Phase 2 should depend upon evidence from earlier stages.

---

## 44. Strategic Questions to Preserve

Several questions should deliberately remain open rather than being prematurely decided.

- Is this primarily a consumer application or an underlying B2B technology?
- Is useful-speed analysis the product, or merely the feature that introduces a broader journey-intelligence product?
- Does the strongest value occur before the journey or during it?
- Are consumers willing to perform an additional action before navigating?
- Is the linear journey timeline itself sufficiently valuable to create a recurring habit?
- Does the product primarily improve safety, efficiency, predictability, comfort — or some combination?
- Which user segment experiences the problem strongly enough to pay for a solution?

These questions should guide experimentation rather than being resolved through assumption.

---

## 45. Current Strategic Position

At this stage, the strongest working proposition is:

> Journey Intelligence is a pre-trip analysis layer that complements existing navigation applications by explaining how a journey is expected to unfold and which factors will actually determine arrival time.

The initial differentiating capability is:

> Calculate the marginal arrival-time value of speed across the journey.

The initial interaction is:

> Enter or share a journey → receive a linear journey briefing → continue navigating with the user's existing navigation application.

The initial technical strategy is:

> Use existing routing, traffic and road datasets while developing proprietary journey segmentation and interpretation.

The initial competitive strategy is:

> Do not replace Google Maps or Waze. Build the intelligence layer they currently do not provide.

---

## 46. North-Star Product Experience

Ultimately, the product should be able to take a complex journey and reduce it to something a driver understands in seconds:

> **Paris → Brussels**
> 3h 18m · 312 km
>
> The first hour should flow normally.
>
> The main uncertainty is a 28 km section approaching Brussels, where approximately 20 minutes of congestion is currently expected.
>
> Most of the journey is motorway.
>
> Under current conditions, increasing motorway cruising speed from 110 to 120 km/h is expected to improve arrival by only approximately three minutes, for roughly 40% more fatal-crash risk over those sections.
>
> The alternative route is eight minutes slower but currently more predictable.

That is the experience the project should initially attempt to prove.

It is not another set of directions.

It is an explanation of the journey.

---

## 47. Working Definition

Journey Intelligence is the process of transforming route, road, traffic and contextual data into an understandable model of how a journey is expected to unfold, what will constrain progress, how predictable the journey is, and which driving decisions materially affect the outcome.

That definition should remain broad enough to accommodate future capabilities while keeping the initial product focused on a clear and testable problem.
