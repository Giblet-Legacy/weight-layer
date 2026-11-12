"""
weight.py — P10 Weight primitive layer

Function:
    Pure math implementation of the Leighton Weight neutral-attractor
    decay formula. No file I/O, no crypto, no persistent state.

Public API:
    1. leighton_weight — Compute λ(t) = 1.00 + (λ₀ − 1.00) × e^(−kt)

Layer:    P10 — Weight
Depends:  (none — pure math)
Consumed: P11 Trust, P14 Leighton Engine, P15 HAL
Version:  1.0.0 (on freeze; 0.0.0-dev until then)
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import math

# ---------------------------------------------------------------------------
# 1. leighton_weight
#    Computes the current lambda given initial value, elapsed time,
#    and decay constant k. Neutral attractor: lambda drifts to 1.00.
# ---------------------------------------------------------------------------
def leighton_weight(lambda_zero, t, k):
    if k is None:
        raise ValueError("k (decay constant) must be provided and positive")

    if not isinstance(lambda_zero, (int, float)) or isinstance(lambda_zero, bool):
        raise TypeError("lambda_zero must be a number")
    if not isinstance(t, (int, float)) or isinstance(t, bool):
        raise TypeError("t must be a number")
    if not isinstance(k, (int, float)) or isinstance(k, bool):
        raise TypeError("k must be a number")

    if k <= 0:
        raise ValueError("k (decay constant) must be provided and positive")
    if lambda_zero <= 0:
        raise ValueError("lambda_zero must be positive")
    if t < 0:
        raise ValueError("t must be non-negative")

    return 1.00 + (lambda_zero - 1.00) * math.exp(-k * t)
