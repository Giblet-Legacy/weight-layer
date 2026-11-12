"""
test_weight.py — P10 Weight test suite

Function:
    Executable expression of SPEC.md. Written before weight.py per
    build discipline.

Layer:    P10 — Weight
Spec:     SPEC.md v1.0.0
Licence:  MSL-1.0
"""

import math
import pytest

import weight

def test_lambda_at_zero_time_equals_lambda_zero():
    # At t=0, e^(−k*0) = 1, so λ = 1 + (λ₀−1) = λ₀
    assert weight.leighton_weight(0.8, 0.0, 0.1) == pytest.approx(0.8)
    assert weight.leighton_weight(1.5, 0.0, 0.1) == pytest.approx(1.5)

def test_lambda_decays_toward_neutral():
    # Starting above 1.00, drifts down toward 1.00
    lam = weight.leighton_weight(2.0, 100.0, 0.1)
    assert 1.0 < lam < 2.0

def test_lambda_rises_toward_neutral():
    # Starting below 1.00, drifts up toward 1.00
    lam = weight.leighton_weight(0.2, 100.0, 0.1)
    assert 0.2 < lam < 1.0

def test_lambda_approaches_neutral_asymptotically():
    # For very large t, λ → 1.00
    lam = weight.leighton_weight(5.0, 10000.0, 0.1)
    assert abs(lam - 1.0) < 1e-6

def test_lambda_at_neutral_stays_neutral():
    # If λ₀ = 1.00, lambda stays 1.00 forever
    assert weight.leighton_weight(1.0, 100.0, 0.1) == pytest.approx(1.0)

def test_formula_matches_manual_computation():
    # Hand-calculate: λ = 1 + (0.5 − 1) * e^(-0.2 * 10)
    expected = 1.0 + (0.5 - 1.0) * math.exp(-0.2 * 10)
    assert weight.leighton_weight(0.5, 10.0, 0.2) == pytest.approx(expected)

def test_k_required():
    with pytest.raises(ValueError):
        weight.leighton_weight(1.0, 10.0, None)

def test_k_must_be_positive():
    with pytest.raises(ValueError):
        weight.leighton_weight(1.0, 10.0, 0.0)
    with pytest.raises(ValueError):
        weight.leighton_weight(1.0, 10.0, -0.1)

def test_lambda_zero_must_be_positive():
    with pytest.raises(ValueError):
        weight.leighton_weight(0.0, 10.0, 0.1)
    with pytest.raises(ValueError):
        weight.leighton_weight(-0.5, 10.0, 0.1)

def test_time_must_be_non_negative():
    with pytest.raises(ValueError):
        weight.leighton_weight(1.0, -5.0, 0.1)

def test_types_rejected():
    with pytest.raises(TypeError):
        weight.leighton_weight("1.0", 10.0, 0.1)
    with pytest.raises(TypeError):
        weight.leighton_weight(1.0, "10", 0.1)
    with pytest.raises(TypeError):
        weight.leighton_weight(1.0, 10.0, "0.1")
