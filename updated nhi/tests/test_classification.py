"""
Unit tests for the Risk Classification Module.

Run with:  pytest test_classification.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from classification import classify_risk


def test_score_zero_is_low():
    assert classify_risk(0) == "LOW"


def test_score_just_below_medium_boundary_is_low():
    assert classify_risk(24) == "LOW"


def test_score_at_medium_boundary_is_medium():
    assert classify_risk(25) == "MEDIUM"


def test_score_just_below_high_boundary_is_medium():
    assert classify_risk(49) == "MEDIUM"


def test_score_at_high_boundary_is_high():
    assert classify_risk(50) == "HIGH"


def test_score_just_below_critical_boundary_is_high():
    assert classify_risk(74) == "HIGH"


def test_score_at_critical_boundary_is_critical():
    assert classify_risk(75) == "CRITICAL"


def test_score_max_is_critical():
    assert classify_risk(100) == "CRITICAL"
