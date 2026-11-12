"""
weight_v2.py — P10 Weight hardening layer (V2)

Function:
    A layer over weight.py (v1.0.0, frozen). It does not rewrite the
    primitive; every lambda value is still computed by
    weight.leighton_weight. This layer adds stricter input validation,
    a vectorised form over a list of times, and a diagnostic that
    explains a decay. Pure math: no file I/O, no database, no crypto,
    no clock reads, no persistent state.

    Gaps in v1 closed here:
      - NaN inputs passed validation and returned NaN.
      - k = inf with t = 0 returned NaN (inf * 0).
      - lambda_zero = inf returned inf.
      - Any k > 0 was accepted, including absurd values such as 1e-300.

Public API:
    1. leighton_weight        — v1 formula with hardened validation
    2. leighton_weight_series — the formula over a list/tuple of times
    3. explain_decay          — diagnostic breakdown of one decay

Layer:    P10 — Weight
Depends:  weight.py (P10 v1.0.0)
Consumed: P11 Trust, P14 Leighton Engine, P15 HAL
Version:  1.1.0
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import math

import weight

# Sane bounds for the decay constant k (inclusive). Outside these the
# decay is effectively frozen (k too small) or instantaneous (k too
# large), which signals a mis-calibrated or mistyped k. Domain-specific
# calibration remains a P14 concern; these are only plausibility rails.
K_MIN = 1e-9
K_MAX = 1e9

NEUTRAL = 1.00


# ---------------------------------------------------------------------------
# 1. _validate (internal)
#    Checks one (lambda_zero, t, k) triple. Order matters: a missing k
#    is a ValueError (matches v1), wrong types are TypeErrors, then
#    non-finite values and out-of-bounds k are ValueErrors. Sign checks
#    are left to v1, which is called afterwards.
# ---------------------------------------------------------------------------
def _validate(lambda_zero, t, k):
    if k is None:
        raise ValueError("k (decay constant) must be provided explicitly")

    for name, value in (("lambda_zero", lambda_zero), ("t", t), ("k", k)):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(name + " must be a number")
        if not math.isfinite(value):
            raise ValueError(name + " must be finite (got " + repr(value) + ")")

    if k > 0 and not (K_MIN <= k <= K_MAX):
        raise ValueError(
            "k (decay constant) out of sane bounds ["
            + repr(K_MIN) + ", " + repr(K_MAX) + "]: got " + repr(k)
        )


# ---------------------------------------------------------------------------
# 2. leighton_weight
#    λ(t) = 1.00 + (λ₀ − 1.00) × e^(−kt), via the frozen v1 primitive,
#    after hardened validation.
# ---------------------------------------------------------------------------
def leighton_weight(lambda_zero, t, k):
    _validate(lambda_zero, t, k)
    return weight.leighton_weight(lambda_zero, t, k)


# ---------------------------------------------------------------------------
# 3. leighton_weight_series
#    Vectorised form: evaluates the formula for each t in a list or
#    tuple of times (no numpy). Returns a list of the same length.
#    Fails on the first invalid element, naming its index.
# ---------------------------------------------------------------------------
def leighton_weight_series(lambda_zero, ts, k):
    if k is None:
        raise ValueError("k (decay constant) must be provided explicitly")
    if not isinstance(ts, (list, tuple)):
        raise TypeError("ts must be a list or tuple of numbers")

    results = []
    for i, t in enumerate(ts):
        try:
            results.append(leighton_weight(lambda_zero, t, k))
        except (TypeError, ValueError) as exc:
            raise type(exc)("ts[" + str(i) + "]: " + str(exc)) from exc
    return results


# ---------------------------------------------------------------------------
# 4. explain_decay
#    Diagnostic for one decay. Returns a dict with the inputs, the
#    resulting lambda, the half-life (time for the distance to neutral
#    to halve: ln 2 / k), the fraction of the initial distance that
#    remains (e^(−kt)), the direction of drift, and a plain-English
#    summary. Pure: builds and returns data, prints nothing.
# ---------------------------------------------------------------------------
def explain_decay(lambda_zero, t, k):
    lam = leighton_weight(lambda_zero, t, k)

    remaining = math.exp(-k * t)
    half_life = math.log(2) / k
    half_lives = t / half_life
    distance_start = lambda_zero - NEUTRAL
    distance_now = lam - NEUTRAL

    if distance_start > 0:
        direction = "falling toward neutral from above"
    elif distance_start < 0:
        direction = "rising toward neutral from below"
    else:
        direction = "at neutral (no drift)"

    summary = (
        "lambda started at " + format(lambda_zero, ".6g")
        + " and is " + direction
        + ". With k=" + format(k, ".6g")
        + " the half-life is " + format(half_life, ".6g")
        + " time units; after t=" + format(t, ".6g")
        + " (" + format(half_lives, ".4g") + " half-lives) "
        + format(remaining * 100, ".4g") + "% of the initial distance"
        + " from 1.00 remains, giving lambda=" + format(lam, ".6g") + "."
    )

    return {
        "lambda_zero": lambda_zero,
        "t": t,
        "k": k,
        "lambda_t": lam,
        "neutral": NEUTRAL,
        "distance_start": distance_start,
        "distance_now": distance_now,
        "fraction_remaining": remaining,
        "half_life": half_life,
        "half_lives_elapsed": half_lives,
        "direction": direction,
        "summary": summary,
    }
