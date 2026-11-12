# SPEC V2 — weight-layer (P10 Weight)

SPEC_V2.md — specification for the V2 hardening layer of P10 Weight.

Function:
    This document specifies `weight_v2.py`, a layer over the frozen
    v1.0.0 primitive `weight.py`. SPEC.md remains authoritative for the
    formula and the v1 contract; this document only adds to it.

Layer:     P10 — Weight
Depends:   weight.py (P10 v1.0.0)
Version:   SPEC 1.1.0
Licence:   MSL-1.0
Author:    James Gilbert (Giblets Forge)

## 1. Relationship to v1

- `weight.py` is not modified. All lambda values are computed by
  `weight.leighton_weight`.
- On any valid input, `weight_v2.leighton_weight` returns exactly the
  same value as v1.
- Everything v1 rejects, V2 also rejects, with the same exception type.

## 2. Hardening

- Non-finite input (NaN, +inf, -inf) for lambda_zero, t or k raises
  ValueError. (v1 returned NaN or inf.)
- k must lie in [K_MIN, K_MAX] = [1e-9, 1e9], inclusive, else
  ValueError. These are plausibility rails only; domain calibration
  of k remains a P14 concern (SPEC.md §4).
- Validation order: k is None → ValueError; non-number or bool →
  TypeError; non-finite → ValueError; k out of bounds → ValueError;
  then the v1 sign checks.

## 3. Function Contracts

### 3.1 leighton_weight(lambda_zero, t, k) -> float
- As SPEC.md §3.1, plus §2 above.

### 3.2 leighton_weight_series(lambda_zero, ts, k) -> list[float]
- ts must be a list or tuple of numbers (no numpy). Empty → [].
- Returns `[leighton_weight(lambda_zero, t, k) for t in ts]`.
- k is None → ValueError, even when ts is empty.
- ts not a list/tuple → TypeError.
- An invalid element raises the same exception type as the scalar
  form, with the message prefixed `ts[i]:`.

### 3.3 explain_decay(lambda_zero, t, k) -> dict
- Same validation as 3.1.
- Returns keys: lambda_zero, t, k, lambda_t, neutral (1.00),
  distance_start (λ₀ − 1), distance_now (λ(t) − 1),
  fraction_remaining (e^(−kt)), half_life (ln 2 / k),
  half_lives_elapsed (t / half_life), direction, summary.
- direction is one of "falling toward neutral from above",
  "rising toward neutral from below", "at neutral (no drift)".
- Pure: returns data, performs no I/O.
