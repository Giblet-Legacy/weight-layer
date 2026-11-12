# NOTES — weight-layer (P10 Weight)

NOTES.md — open questions, divergences and decisions for P10 Weight.

## Open questions
- (none)

## Divergences from v1.2.1 specification
- (none)

## Decisions
- Uses Python's `math.exp` for the exponential. No external
  mathematical dependencies.
- k is strictly required. There is no default. This matches the
  v1.2.1 architecture: "tooling refuses to run without an explicit
  value".
- No persistent state. Lambda is recomputed on demand from lambda_0,
  t, and k. This matches the architecture: "λ is computed from an
  observation stream — never stored as authoritative state".
- V2 (`weight_v2.py`) is a layer, not a rewrite. It validates, then
  delegates to `weight.leighton_weight`, so the formula lives in one
  place only.
- Non-finite inputs are a ValueError (a bad value), not a TypeError
  (they are still floats).
- k sane bounds are [1e-9, 1e9], inclusive. At k=1e-9 the half-life is
  ~22 years in seconds; at k=1e9 it is under a nanosecond. Anything
  outside is treated as a mistyped k. Exposed as `K_MIN` / `K_MAX`.
- The series form accepts only list or tuple, so a string is never
  silently iterated as characters. It fails on the first bad element
  and names its index.
- `explain_decay` returns a dict rather than printing, keeping the
  layer free of I/O.
- v1 is left as-is despite the NaN/inf gap; consumers should call V2.
