"""Route archetypes for the simulation, per docs/SIM-PRD.md section 7.

Nine archetypes spanning the use cases in PCS.md section 22. Each is a
hand-specified segment list; no external data is required for Phase 1.
"""

from model import (
    Journey,
    Segment,
    M1_FIXED_SLOW,
    M2_QUEUE,
    M3_SCHEDULED,
    M4_TIMEVARYING,
    M5_ATTAINABILITY,
    NONE,
)


def _motorway(name, km, limit=130.0, free_flow=130.0):
    return Segment(name, km, "motorway", limit, free_flow)


def _urban(name, km, limit=50.0, free_flow=35.0):
    return Segment(name, km, "urban", limit, free_flow)


def _secondary(name, km, limit=90.0, free_flow=80.0):
    return Segment(name, km, "secondary", limit, free_flow)


# A -- Long motorway, free flowing. The case where the time thesis should be
# at its weakest: nothing constrains the driver at all.
ROUTE_A = Journey(
    "A: long motorway, free flowing",
    [
        _urban("origin urban", 20),
        _motorway("motorway", 340),
        _urban("destination urban", 40, free_flow=40),
    ],
)

# B -- Long motorway with one capacity-limited bottleneck near the destination.
ROUTE_B = Journey(
    "B: motorway + urban bottleneck",
    [
        _urban("origin urban", 18),
        _motorway("motorway", 320),
        Segment(
            "approach bottleneck",
            22,
            "motorway",
            110.0,
            110.0,
            mechanism=M2_QUEUE,
            params={
                "queue_start_hr": 15.5,
                "queue_peak_end_hr": 18.0,
                "arrival_rate_vph": 4200,
                "capacity_vph": 3400,
                "drain_arrival_rate_vph": 2600,
            },
        ),
        _urban("destination urban", 40, free_flow=40),
    ],
    departure_hr=13.0,
)

# C -- The PCS section 30 reference case, Brussels to Strasbourg.
# Segment speeds are back-derived from the distances and durations stated
# in the document, so this reproduces its own worked example exactly.
ROUTE_C = Journey(
    "C: Brussels-Strasbourg (PCS 30)",
    [
        _urban("Brussels urban", 18, free_flow=35),
        _motorway("motorway 1", 167, limit=120.0, free_flow=120.0),
        Segment(
            "Luxembourg congestion",
            31,
            "motorway",
            120.0,
            120.0,
            mechanism=M1_FIXED_SLOW,
            params={"v_slow_kmh": 47.7},
        ),
        _motorway("motorway 2", 173, limit=120.0, free_flow=120.0),
        _secondary("Strasbourg approach", 46, limit=90.0, free_flow=51),
    ],
    departure_hr=13.0,
)

# C2 -- Same route, Luxembourg constraint modelled as a queue rather than a
# fixed slowdown. Isolates how much the verdict depends on that choice.
ROUTE_C2 = Journey(
    "C2: Brussels-Strasbourg, queue variant",
    [
        _urban("Brussels urban", 18, free_flow=35),
        _motorway("motorway 1", 167, limit=120.0, free_flow=120.0),
        Segment(
            "Luxembourg congestion",
            31,
            "motorway",
            120.0,
            120.0,
            mechanism=M2_QUEUE,
            params={
                "queue_start_hr": 14.0,
                "queue_peak_end_hr": 17.5,
                "arrival_rate_vph": 4000,
                "capacity_vph": 3200,
                "drain_arrival_rate_vph": 2400,
            },
        ),
        _motorway("motorway 2", 173, limit=120.0, free_flow=120.0),
        _secondary("Strasbourg approach", 46, limit=90.0, free_flow=51),
    ],
    departure_hr=13.0,
)

# D -- Cross-border journey with a timed crossing mid-route. The only
# mechanism that destroys upstream gains outright.
ROUTE_D = Journey(
    "D: cross-border, timed crossing",
    [
        _motorway("motorway to border", 180),
        Segment(
            "border crossing",
            4,
            "primary",
            70.0,
            70.0,
            mechanism=M3_SCHEDULED,
            params={"release_hr": 11.0, "service_time_hr": 0.15},
        ),
        _motorway("motorway from border", 166),
    ],
    departure_hr=8.0,
)

# E -- Mixed motorway and secondary.
ROUTE_E = Journey(
    "E: mixed motorway and secondary",
    [
        _urban("origin urban", 15),
        _motorway("motorway", 135),
        _secondary("secondary", 120),
        _urban("destination urban", 30, free_flow=38),
    ],
)

# F -- Motorway into an evening peak. Severity depends on arrival time, and
# arriving earlier means arriving before the peak builds.
ROUTE_F = Journey(
    "F: rush-hour city arrival",
    [
        _motorway("motorway", 200),
        Segment(
            "city approach",
            50,
            "motorway",
            110.0,
            110.0,
            mechanism=M4_TIMEVARYING,
            params={
                "speed_profile": [
                    (14.0, 105.0),
                    (16.0, 95.0),
                    (17.0, 55.0),
                    (18.5, 45.0),
                    (19.5, 75.0),
                    (21.0, 100.0),
                ]
            },
        ),
    ],
    departure_hr=14.5,
)

# G -- Secondary-road dominated, low limits throughout.
ROUTE_G = Journey(
    "G: secondary-road dominated",
    [
        _urban("origin", 12),
        _secondary("secondary 1", 95, limit=80.0, free_flow=72),
        _motorway("short motorway", 33, limit=120.0, free_flow=120.0),
        _secondary("secondary 2", 68, limit=80.0, free_flow=70),
        _urban("destination", 12, free_flow=32),
    ],
)

# H -- Motorway with a long sustained roadworks section (fixed-speed).
ROUTE_H = Journey(
    "H: motorway with roadworks",
    [
        _urban("origin urban", 15),
        _motorway("motorway 1", 160),
        Segment(
            "roadworks",
            40,
            "motorway",
            80.0,
            80.0,
            mechanism=M1_FIXED_SLOW,
            params={"v_slow_kmh": 78.0},
        ),
        _motorway("motorway 2", 145),
        _urban("destination urban", 20, free_flow=38),
    ],
)

# I -- Pure attainability case. Generous limit, but the stream runs at 90 with
# heavy goods vehicles slower still, on single carriageway where overtaking is
# constrained. This is the mechanism that suppresses time gain and raises risk
# at the same time.
ROUTE_I = Journey(
    "I: single-carriageway mixed stream",
    [
        Segment(
            "single carriageway",
            200,
            "primary",
            130.0,
            130.0,
            mechanism=M5_ATTAINABILITY,
            carriageway="single",
            params={"stream_mean_kmh": 90.0, "density_veh_per_km": 4.0},
        ),
    ],
)

ALL_ROUTES = [
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_C2,
    ROUTE_D,
    ROUTE_E,
    ROUTE_F,
    ROUTE_G,
    ROUTE_H,
    ROUTE_I,
]

# Journeys of three hours or more at a 110 cap, per the SIM-PRD section 8.1
# falsification criteria. Confirmed by the runner rather than assumed.
LONG_JOURNEY_MIN_HR = 3.0
