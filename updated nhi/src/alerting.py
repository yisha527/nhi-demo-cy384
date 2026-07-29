"""
Alerting Module
-----------------
Flags identities that need urgent attention. Prints a formatted
alert and writes to a log file.
"""

from datetime import datetime

LOG_FILE = "../data/alerts.log"


def raise_alert(identity: dict, score: int, label: str) -> None:
    message = (
        f"[ALERT] {label} RISK - '{identity['name']}' "
        f"(owner: {identity['owner']}, score: {score}/100)"
    )
    print(message)

    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().isoformat(timespec="seconds")
        f.write(f"{timestamp} | {message}\n")


def check_and_alert(identity: dict, score: int, label: str,
                     threshold: str = "HIGH") -> bool:
    """
    Trigger an alert if the identity's risk label is at or above
    the given threshold. Returns True if an alert was raised.
    """
    severity_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    if severity_order.index(label) >= severity_order.index(threshold):
        raise_alert(identity, score, label)
        return True
    return False
