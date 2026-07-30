"""
Risk Scoring Module
--------------------
Calculates a risk score (0-100) for each identity based on:
  - Permission scope   (0-40 points)
  - Age                (0-30 points)
  - Inactivity          (0-30 points)
"""

HIGH_RISK_PERMS = {"admin:all", "storage:admin", "delete:all",
                    "deploy:prod", "channel:admin"}


def score_permissions(permissions: list[str]) -> int:
    score = 0
    score += min(len(permissions) * 5, 20)
    if any(p in HIGH_RISK_PERMS for p in permissions):
        score += 20
    return min(score, 40)


def score_age(age_days: int) -> int:
    if age_days > 730:
        return 30
    elif age_days > 365:
        return 20
    elif age_days > 180:
        return 10
    else:
        return 0


def score_inactivity(idle_days: int) -> int:
    if idle_days > 365:
        return 30
    elif idle_days > 90:
        return 20
    elif idle_days > 30:
        return 10
    else:
        return 0


def calculate_risk_score(identity: dict) -> int:
    perm_score = score_permissions(identity["permissions"])
    age_score = score_age(identity["age_days"])
    inactivity_score = score_inactivity(identity["idle_days"])

    total = perm_score + age_score + inactivity_score
    return min(total, 100)
