"""
Risk Classification Module
----------------------------
Converts a numeric risk score into a human-readable label.
Adjust thresholds based on your own risk appetite - document your
reasoning in the report (this maps to "setting risk thresholds").
"""


def classify_risk(score: int) -> str:
    if score >= 75:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    else:
        return "LOW"
