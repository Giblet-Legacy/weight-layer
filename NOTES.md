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
