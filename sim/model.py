"""Core journey model for the marginal-value-of-speed simulation.

Implements the segment model and the five constraint mechanisms defined in
docs/SIM-PRD.md section 3, plus the risk model from section 4.

Stdlib only, by design: this must run without an install step.
"""

from dataclasses import dataclass, field
from typing import Optional

# Mechanism identifiers, per SIM-PRD section 3.
NONE = "none"
M1_FIXED_SLOW = "M1"  # fixed-speed slowdown; arrival-time independent
M2_QUEUE = "M2"  # capacity-limited queue
M3_SCHEDULED = "M3"  # scheduled release (barrier opens at a wall-clock time)
M4_TIMEVARYING = "M4"  # congestion whose severity depends on arrival time
M5_ATTAINABILITY = "M5"  # following constraint; stream limits realized speed

# --- M5 calibration -------------------------------------------------------
# These are engineering estimates, NOT empirical fits. They set how much of a
# driver's intended excess over the traffic stream is actually realized.
# Phase 1 exists to establish direction and magnitude; Phase 2 must replace
# these with values derived from real speed data. run.py sweeps them.
OVERTAKE_RESISTANCE = {"dual": 0.15, "single": 1.20}
REFERENCE_DENSITY_VEH_PER_KM = 5.0


@dataclass
class Segment:
    """One stretch of road with homogeneous character."""

    name: str
    length_km: float
    road_class: str  # motorway / primary / secondary / urban
    legal_limit_kmh: float
    free_flow_kmh: float
    mechanism: str = NONE
    carriageway: str = "dual"
    params: dict = field(default_factory=dict)


@dataclass
class SegmentResult:
    name: str
    length_km: float
    time_hr: float
    realized_kmh: float
    desired_kmh: float
    overtakes: float
    delay_hr: float  # time beyond unconstrained traversal at desired speed
    binding: bool  # was V_cap the constraint that mattered here?


def _interp(profile, t_hr):
    """Linear interpolation over a list of (clock_hr, value) breakpoints."""
    if t_hr <= profile[0][0]:
        return profile[0][1]
    if t_hr >= profile[-1][0]:
        return profile[-1][1]
    for (t0, v0), (t1, v1) in zip(profile, profile[1:]):
        if t0 <= t_hr <= t1:
            if t1 == t0:
                return v1
            return v0 + (v1 - v0) * (t_hr - t0) / (t1 - t0)
    return profile[-1][1]


def _m5_realized_speed(v_desired, stream_mean, density, carriageway):
    """Speed actually achievable in a mixed traffic stream.

    The driver realizes only a fraction of their intended excess over the
    stream. That fraction (the attainment efficiency) falls as density rises
    and as overtaking gets harder:

        realized = stream_mean + (v_desired - stream_mean) * eta
        eta      = 1 / (1 + (density / rho_ref) * resistance)

    Below stream speed the driver is never held up, so eta does not apply.
    """
    if v_desired <= stream_mean:
        return v_desired, 1.0
    resistance = OVERTAKE_RESISTANCE.get(carriageway, 1.0)
    eta = 1.0 / (1.0 + (density / REFERENCE_DENSITY_VEH_PER_KM) * resistance)
    return stream_mean + (v_desired - stream_mean) * eta, eta


def _overtakes(length_km, v_realized, stream_mean, density):
    """Vehicles passed over a stretch.

    Travelling distance d at speed v while the stream moves at u, the driver
    covers d * (1 - u/v) more ground than the stream, and passes every vehicle
    in it. Exact for a uniform stream.
    """
    if v_realized <= stream_mean:
        return 0.0
    return density * length_km * (1.0 - stream_mean / v_realized)


def _m2_queue_delay(seg, arrival_clock_hr):
    """Deterministic fluid-queue delay at a capacity-limited bottleneck.

    Standard cumulative-count treatment. During the peak, cumulative arrivals
    outrun the discharge rate, so delay grows linearly with how late into the
    peak the driver arrives. During the drain, it falls back linearly.

    Note the marginal behaviour this produces: arriving earlier within the
    peak moves the driver ahead of (lambda * delta) vehicles which the
    bottleneck discharges at mu, so the departure improves by
    (lambda / mu) * delta -- MORE than the time saved upstream, since
    lambda > mu during congestion. This model AMPLIFIES upstream gains rather
    than absorbing them. See docs/SIM-RESULTS.md.
    """
    t0 = seg.params["queue_start_hr"]
    t1 = seg.params["queue_peak_end_hr"]
    lam = seg.params["arrival_rate_vph"]
    mu = seg.params["capacity_vph"]
    lam_drain = seg.params.get("drain_arrival_rate_vph", mu * 0.7)

    if arrival_clock_hr <= t0:
        return 0.0

    queue_at_peak_end = (lam - mu) * (t1 - t0)  # vehicles

    if arrival_clock_hr <= t1:
        return (arrival_clock_hr - t0) * (lam / mu - 1.0)

    if mu <= lam_drain:  # never clears within the modelled window
        return queue_at_peak_end / mu

    clear_hr = t1 + queue_at_peak_end / (mu - lam_drain)
    if arrival_clock_hr >= clear_hr:
        return 0.0
    queue_now = queue_at_peak_end - (mu - lam_drain) * (arrival_clock_hr - t1)
    return max(0.0, queue_now / mu)


def traverse_segment(seg, v_cap, clock_hr):
    """Traverse one segment. Returns a SegmentResult."""
    v_desired = min(v_cap, seg.legal_limit_kmh, seg.free_flow_kmh)
    unconstrained_hr = seg.length_km / v_desired
    binding = v_cap < min(seg.legal_limit_kmh, seg.free_flow_kmh)
    overtakes = 0.0

    if seg.mechanism == NONE:
        time_hr = unconstrained_hr
        realized = v_desired

    elif seg.mechanism == M1_FIXED_SLOW:
        realized = min(v_desired, seg.params["v_slow_kmh"])
        time_hr = seg.length_km / realized
        binding = binding and v_desired < seg.params["v_slow_kmh"]

    elif seg.mechanism == M2_QUEUE:
        delay = _m2_queue_delay(seg, clock_hr)
        time_hr = unconstrained_hr + delay
        realized = seg.length_km / time_hr

    elif seg.mechanism == M3_SCHEDULED:
        release = seg.params["release_hr"]
        service = seg.params.get("service_time_hr", 0.0)
        wait = max(0.0, release - clock_hr)
        time_hr = unconstrained_hr + wait + service
        realized = seg.length_km / time_hr

    elif seg.mechanism == M4_TIMEVARYING:
        profile = seg.params["speed_profile"]
        remaining = seg.length_km
        step = 0.5
        elapsed = 0.0
        while remaining > 1e-9:
            d = min(step, remaining)
            v = min(v_desired, _interp(profile, clock_hr + elapsed))
            elapsed += d / v
            remaining -= d
        time_hr = elapsed
        realized = seg.length_km / time_hr

    elif seg.mechanism == M5_ATTAINABILITY:
        stream = seg.params["stream_mean_kmh"]
        density = seg.params["density_veh_per_km"]
        realized, _eta = _m5_realized_speed(
            v_desired, stream, density, seg.carriageway
        )
        time_hr = seg.length_km / realized
        overtakes = _overtakes(seg.length_km, realized, stream, density)

    else:
        raise ValueError(f"unknown mechanism: {seg.mechanism}")

    return SegmentResult(
        name=seg.name,
        length_km=seg.length_km,
        time_hr=time_hr,
        realized_kmh=realized,
        desired_kmh=v_desired,
        overtakes=overtakes,
        delay_hr=time_hr - unconstrained_hr,
        binding=binding,
    )


@dataclass
class Journey:
    name: str
    segments: list
    departure_hr: float = 9.0  # clock time, 24h decimal


@dataclass
class JourneyResult:
    journey: str
    v_cap: float
    total_hr: float
    distance_km: float
    segments: list

    @property
    def arrival_hr(self):
        return self.segments[0].__dict__.get("_departure", 0.0) + self.total_hr

    @property
    def total_overtakes(self):
        return sum(s.overtakes for s in self.segments)

    @property
    def speed_elastic_fraction(self):
        """Share of distance where V_cap was the binding constraint."""
        elastic = sum(s.length_km for s in self.segments if s.binding)
        return elastic / self.distance_km if self.distance_km else 0.0

    def risk_index(self, exponent):
        """Exposure-weighted risk, relative units.

        Crash rate per unit distance scales as v^exponent (Nilsson power
        model), so journey risk is the distance-weighted sum of v^exponent.
        Only meaningful as a ratio between two strategies.
        """
        return sum(s.length_km * (s.realized_kmh ** exponent) for s in self.segments)


def run_journey(journey, v_cap):
    clock = journey.departure_hr
    results = []
    for seg in journey.segments:
        r = traverse_segment(seg, v_cap, clock)
        clock += r.time_hr
        results.append(r)
    return JourneyResult(
        journey=journey.name,
        v_cap=v_cap,
        total_hr=sum(r.time_hr for r in results),
        distance_km=sum(r.length_km for r in results),
        segments=results,
    )
