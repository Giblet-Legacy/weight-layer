"""
test_weight_v2.py — P10 Weight V2 test suite

Function:
    Executable expression of SPEC_V2.md. Confirms weight_v2.py agrees
    with the frozen v1 primitive on valid input, and covers the
    hardening it adds: non-finite rejection, k bounds, the vectorised
    series form, and the explain_decay diagnostic.

Layer:    P10 — Weight
Spec:     SPEC_V2.md (P10 v1.1.0)
Licence:  MSL-1.0
"""

import math
import pytest

import weight
import weight_v2

NAN = float("nan")
INF = float("inf")


# 1. V2 matches v1 exactly on valid inputs
def test_matches_v1_on_valid_input():
    for args in [(0.8, 0.0, 0.1), (2.0, 100.0, 0.1), (0.2, 7.5, 0.3), (1.0, 50.0, 2.0)]:
        assert weight_v2.leighton_weight(*args) == weight.leighton_weight(*args)


# 2. v1 contract still holds: k required, sign rules, type rules
def test_v1_contract_preserved():
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(1.0, 10.0, None)
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(1.0, 10.0, 0.0)
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(1.0, 10.0, -0.1)
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(0.0, 10.0, 0.1)
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(1.0, -5.0, 0.1)
    with pytest.raises(TypeError):
        weight_v2.leighton_weight("1.0", 10.0, 0.1)
    with pytest.raises(TypeError):
        weight_v2.leighton_weight(1.0, 10.0, True)


# 3. NaN rejected for every input (v1 returned NaN)
@pytest.mark.parametrize("args", [(NAN, 1.0, 0.1), (1.0, NAN, 0.1), (1.0, 1.0, NAN)])
def test_nan_rejected(args):
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(*args)


# 4. Infinity rejected for every input (v1 returned inf / NaN)
@pytest.mark.parametrize("args", [(INF, 1.0, 0.1), (1.0, INF, 0.1), (2.0, 0.0, INF)])
def test_inf_rejected(args):
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(*args)


# 5. k outside sane bounds rejected; bounds themselves accepted
def test_k_bounds():
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(2.0, 1.0, 1e-300)
    with pytest.raises(ValueError):
        weight_v2.leighton_weight(2.0, 1.0, 1e300)
    weight_v2.leighton_weight(2.0, 1.0, weight_v2.K_MIN)
    weight_v2.leighton_weight(2.0, 1.0, weight_v2.K_MAX)


# 6. Series matches scalar evaluation element by element
def test_series_matches_scalar():
    ts = [0.0, 1.0, 5.0, 10.0, 100.0]
    out = weight_v2.leighton_weight_series(0.5, ts, 0.2)
    assert out == [weight_v2.leighton_weight(0.5, t, 0.2) for t in ts]
    assert weight_v2.leighton_weight_series(0.5, (1.0, 2.0), 0.2) == out[1:2] + [
        weight_v2.leighton_weight(0.5, 2.0, 0.2)
    ]
    assert weight_v2.leighton_weight_series(0.5, [], 0.2) == []


# 7. Series validation: k required, container type, bad element index
def test_series_validation():
    with pytest.raises(ValueError):
        weight_v2.leighton_weight_series(0.5, [], None)
    with pytest.raises(TypeError):
        weight_v2.leighton_weight_series(0.5, "123", 0.2)
    with pytest.raises(TypeError):
        weight_v2.leighton_weight_series(0.5, 1.0, 0.2)
    with pytest.raises(ValueError, match=r"ts\[2\]"):
        weight_v2.leighton_weight_series(0.5, [0.0, 1.0, -1.0], 0.2)
    with pytest.raises(TypeError, match=r"ts\[1\]"):
        weight_v2.leighton_weight_series(0.5, [0.0, "1"], 0.2)


# 8. Diagnostic values are consistent with the formula
def test_explain_decay_values():
    d = weight_v2.explain_decay(2.0, 10.0, 0.1)
    assert d["lambda_t"] == weight.leighton_weight(2.0, 10.0, 0.1)
    assert d["half_life"] == pytest.approx(math.log(2) / 0.1)
    assert d["fraction_remaining"] == pytest.approx(math.exp(-1.0))
    assert d["distance_now"] == pytest.approx(d["distance_start"] * d["fraction_remaining"])
    assert d["half_lives_elapsed"] == pytest.approx(1.0 / math.log(2))
    assert d["neutral"] == 1.00
    assert isinstance(d["summary"], str) and "half-life" in d["summary"]


# 9. Diagnostic reports direction of drift
def test_explain_decay_direction():
    assert "above" in weight_v2.explain_decay(2.0, 1.0, 0.1)["direction"]
    assert "below" in weight_v2.explain_decay(0.5, 1.0, 0.1)["direction"]
    assert "neutral" in weight_v2.explain_decay(1.0, 1.0, 0.1)["direction"]


# 10. Diagnostic refuses to run without an explicit k
def test_explain_decay_requires_k():
    with pytest.raises(ValueError):
        weight_v2.explain_decay(2.0, 1.0, None)
