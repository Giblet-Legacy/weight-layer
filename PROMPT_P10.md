# P10 Weight — Laptop Audit Prompt

P10 weight-layer is frozen at v1.0.0 on the phone with 11/11 tests passing.

## Your Task

1. Pull `Giblet-Legacy/weight-layer`.
2. Audit against SPEC.md and CHANGELOG.md.
3. Run `pytest -q` — expect 11 passed.
4. If you find gaps, create `weight_v2.py` (do NOT edit v1).
5. Suggested V2 hardening: validate k has sane bounds (not absurdly small/large), add explicit support for vectorised t (numpy not allowed — use list comprehension), add a diagnostic function that explains the decay given λ₀, k, t.
6. Push when green so the phone can verify.
