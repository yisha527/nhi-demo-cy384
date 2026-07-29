"""
Discovery Engine
----------------
Scans a data source and returns a list of machine identities.
Reads from a CSV file (simulating a scan of an environment).

Expected CSV columns:
    id, name, type, owner, age_days, idle_days, active, permissions,
    risk_score, risk_level

Note: risk_score and risk_level in the CSV are treated as reference/
ground-truth values only (useful for testing your own scoring logic
against). Your own risk_scoring.py module recalculates these fresh
from age_days, idle_days, and permissions.
"""

import csv
from pathlib import Path


def discover_identities(source_path: str) -> list[dict]:
    """
    Load and normalize identities from the given CSV file.
    Returns a list of dicts, each representing one identity.
    """
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"No such data source: {source_path}")

    required_fields = {"id", "name", "type", "owner", "age_days",
                        "idle_days", "active", "permissions"}

    identities = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            missing = required_fields - row.keys()
            if missing:
                print(f"[WARN] Skipping row - missing fields: {missing}")
                continue

            identity = {
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "owner": row["owner"],
                "age_days": int(row["age_days"]),
                "idle_days": int(row["idle_days"]),
                "active": row["active"].strip().lower() == "true",
                "permissions": [p.strip() for p in row["permissions"].split("|") if p.strip()],
                # keep the CSV's own score/label as reference values, if present
                "reference_risk_score": int(row["risk_score"]) if row.get("risk_score") else None,
                "reference_risk_level": row.get("risk_level"),
            }
            identities.append(identity)

    print(f"[INFO] Discovered {len(identities)} identities.")
    return identities


if __name__ == "__main__":
    identities = discover_identities("../data/nhi_inventory.csv")
    for i in identities:
        print(i["id"], "-", i["name"], "-", i["permissions"])
