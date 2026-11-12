# CHANGELOG — weight-layer (P10 Weight)

CHANGELOG.md — build history for P10 Weight, latest entry at top.

## [v1.1.0] — 2026-11-12

### Good
- Laptop audit per PROMPT_P10.md: v1 confirmed 11/11 green.
- `weight_v2.py` added as a layer over v1 (v1 untouched), specified in
  `SPEC_V2.md`, tested by `test_weight_v2.py`. 25/25 tests pass.
- V2 rejects NaN/inf inputs and k outside [1e-9, 1e9].
- `leighton_weight_series` evaluates a list/tuple of times (no numpy).
- `explain_decay` returns a diagnostic breakdown (half-life, fraction
  remaining, direction of drift, plain-English summary).

### Bad
- Audit found v1 accepts non-finite input: NaN in any argument returns
  NaN, `k=inf, t=0` returns NaN, `lambda_zero=inf` returns inf. Fixed
  in V2, not in v1 (Immutable Rule). Consumers should move to V2.
- README status still read "0.0.0-dev (in build, pre-freeze)" after
  the v1.0.0 freeze. Corrected.

### Ugly
- k bounds [1e-9, 1e9] are a judgement call, not derived from any
  domain. Revisit when P14 calibrates k per domain.

## [v1.0.0] — 2026-11-12

### Good
- `weight.py` implemented to SPEC v1.0.0.
- 11/11 pytest tests pass.
- Leighton neutral-attractor decay formula: λ(t) = 1.00 + (λ₀ − 1.00) × e^(−kt).
- Refuses to run without explicit k.

### Bad
- Initial type check ordering raised TypeError instead of ValueError when k=None. Caught by test_k_required, fixed by moving the None check before the isinstance check.

### Ugly
- (none)

## [v0.0.0] — scaffold

### Good
- Repository scaffolded: `Giblet-Legacy/weight-layer` created for P10.
- Pure math layer, no dependencies on other Forge Stack layers.

### Bad
- (none)

### Ugly
- (none)
