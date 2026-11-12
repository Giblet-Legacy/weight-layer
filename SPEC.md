# SPEC — weight-layer (P10 Weight)

SPEC.md — the complete layer specification for P10 Weight.

Function:
    This document is the authoritative specification for primitive
    layer P10 of the Forge Stack. It defines the Leighton Weight
    neutral-attractor decay formula.

Layer:     P10 — Weight
Depends:   (none — pure math)
Consumed:  P11 Trust, P14 Leighton Engine, P15 HAL
Version:   SPEC 1.0.0
Licence:   MSL-1.0
Author:    James Gilbert (Giblets Forge)

## 1. The Leighton Weight Formula

Lambda (λ) is the Leighton Weight, a trust score. It decays over
time toward a neutral attractor, never toward zero. A quiet claim
drifts toward "unknown", not "distrusted".

The exact formula:

    λ(t) = 1.00 + (λ₀ − 1.00) × e^(−kt)

Where:
- λ₀ (lambda_zero) is the initial trust value. Must be > 0.
- k is the decay constant. Must be > 0.
- t is elapsed time in the same units as 1/k. Must be >= 0.
- e is the mathematical constant, e ≈ 2.71828.

## 2. Critical Rules

- k is never called lambda. It is the decay constant. Tooling
  refuses to run without an explicit value.
- The formula pulls toward 1.00, never toward 0.00. This is
  invariant: as t → ∞, λ(t) → 1.00.
- The formula is purely mathematical. No file I/O, no database,
  no crypto, no clock reads. Time t is provided by the caller.
- No persistent state. Lambda is never stored. It is always
  recomputed from the observation stream and parameters.

## 3. Function Contracts

### 3.1 leighton_weight(lambda_zero: float, t: float, k: float) -> float
- Input: initial lambda, elapsed time, decay constant.
- Output: current lambda, a float.
- Failure:
  - ValueError if k is None or k <= 0.
  - ValueError if lambda_zero <= 0.
  - ValueError if t < 0.
  - TypeError if any input is not a number.

## 4. Known Limitations (P10 v1.0.0)

- No domain-specific k calibration. The tooling accepts any k > 0.
  Validation that k is properly calibrated per domain is a P14
  concern, not P10.
- No observation ingestion. P10 computes lambda given parameters.
  Extracting observations from a ledger is P14's job.
