"""
Unit tests for the Risk Scoring Module.

Run with:  pytest test_risk_scoring.py -v
(from inside the tests/ folder, with src/ one level up)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from risk_scoring import (
    score_permissions,
    score_age,
    score_inactivity,
    calculate_risk_score,
)


# ---------- score_permissions ----------

def test_no_permissions_scores_zero():
    assert score_permissions([]) == 0


def test_few_low_risk_permissions_scores_by_volume():
    # 2 permissions * 5 pts = 10, no high-risk perm present
    assert score_permissions(["repo:read", "chat:read"]) == 10


def test_many_low_risk_permissions_caps_volume_at_20():
    # 10 low-risk permissions would be 50 pts uncapped; volume caps at 20
    perms = [f"scope:{i}" for i in range(10)]
    assert score_permissions(perms) == 20


def test_single_high_risk_permission_adds_flat_20():
    # 1 perm (5 pts) + high-risk flag (20 pts) = 25
    assert score_permissions(["deploy:prod"]) == 25


def test_total_permission_score_caps_at_40():
    perms = [f"scope:{i}" for i in range(10)] + ["admin:all"]
    assert score_permissions(perms) == 40


# ---------- score_age ----------

def test_new_identity_scores_zero_age():
    assert score_age(10) == 0


def test_age_boundary_180_days_scores_zero():
    assert score_age(180) == 0


def test_age_just_over_180_days_scores_10():
    assert score_age(181) == 10


def test_age_just_over_365_days_scores_20():
    assert score_age(366) == 20


def test_age_over_two_years_scores_30():
    assert score_age(731) == 30


# ---------- score_inactivity ----------

def test_recently_used_identity_scores_zero_inactivity():
    assert score_inactivity(5) == 0


def test_idle_just_over_30_days_scores_10():
    assert score_inactivity(31) == 10


def test_idle_just_over_90_days_scores_20():
    assert score_inactivity(91) == 20


def test_idle_over_a_year_scores_30():
    assert score_inactivity(400) == 30


# ---------- calculate_risk_score (integration of all three) ----------

def test_low_risk_identity_scores_low_total():
    identity = {"permissions": ["repo:read"], "age_days": 10, "idle_days": 2}
    # perms: 5, age: 0, idle: 0 => 5
    assert calculate_risk_score(identity) == 5


def test_high_risk_identity_scores_high_total():
    identity = {
        "permissions": ["admin:all", "storage:admin"],
        "age_days": 800,
        "idle_days": 400,
    }
    # perms: min(10,20)+20=30, age: 30, idle: 30 => 90
    assert calculate_risk_score(identity) == 90


def test_score_never_exceeds_100():
    identity = {
        "permissions": ["admin:all"] * 10,
        "age_days": 5000,
        "idle_days": 5000,
    }
    assert calculate_risk_score(identity) <= 100
