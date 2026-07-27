"""
Risk Scoring Module
--------------------
Calculates a risk score (0-100) for each identity based on:
  - Permission scope   (0-40 points)
  - Age                (0-30 points)
  - Inactivity          (0-30 points)

Higher score = higher risk.
Tune the weights/thresholds below to fit your own reasoning -
document WHY you chose them in your report, that's part of the
"fair risk-scoring algorithm" challenge you listed.
"""

from datetime import datetime

TODAY = datetime.today()

# Permissions considered high-risk if present
HIGH_RISK_PERMS = {"admin:all", "admin:database", "delete:all",
                    "write:all", "read:all"}


def score_permissions(permissions: list[str]) -> int:
    """More permissions, and riskier permissions, = higher score."""
    score = 0
    score += min(len(permissions) * 5, 20)  # up to 20 pts for volume
    if any(p in HIGH_RISK_PERMS for p in permissions):
        score += 20  # flat penalty for any high-risk permission
    return min(score, 40)


def score_age(created_date: str) -> int:
    """Older identities are riskier (more likely forgotten)."""
    created = datetime.strptime(created_date, "%Y-%m-%d")
    age_days = (TODAY - created).days

    if age_days > 730:      # older than 2 years
        return 30
    elif age_days > 365:    # 1-2 years
        return 20
    elif age_days > 180:    # 6-12 months
        return 10
    else:
        return 0


def score_inactivity(last_used: str) -> int:
    """Identities not used recently are riskier (likely stale/orphaned)."""
    last_used_date = datetime.strptime(last_used, "%Y-%m-%d")
    idle_days = (TODAY - last_used_date).days

    if idle_days > 365:
        return 30
    elif idle_days > 90:
        return 20
    elif idle_days > 30:
        return 10
    else:
        return 0


def calculate_risk_score(identity: dict) -> int:
    """Combine sub-scores into a final 0-100 risk score."""
    perm_score = score_permissions(identity["permissions"])
    age_score = score_age(identity["created_date"])
    inactivity_score = score_inactivity(identity["last_used"])

    total = perm_score + age_score + inactivity_score
    return min(total, 100)
