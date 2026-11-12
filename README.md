# weight-layer — P10 Weight

README.md — repository purpose and layer contract for P10 Weight.

Function:
    This repository implements primitive layer P10 of the Forge Stack:
    the Leighton Weight neutral-attractor decay formula. It is a pure
    math layer, with no file I/O, no database, no crypto.

Layer:    P10 — Weight
Depends:  (none — pure math)
Consumed: P11 Trust, P14 Leighton Engine, P15 HAL
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
Status:   1.1.0 (v1.0.0 frozen in weight.py; V2 hardening layer in weight_v2.py)

Use `weight_v2` for new code. It returns the same values as v1 and
additionally rejects NaN/inf and implausible k. See SPEC.md and
SPEC_V2.md.
