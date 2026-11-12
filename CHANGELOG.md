# CHANGELOG — weight-layer (P10 Weight)

CHANGELOG.md — build history for P10 Weight, latest entry at top.

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

### Good
- Repository scaffolded: `Giblet-Legacy/weight-layer` created for P10.
- Pure math layer, no dependencies on other Forge Stack layers.

### Bad
- (none)

### Ugly
- (none)
