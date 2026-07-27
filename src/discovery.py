"""
Discovery Engine
----------------
Scans a data source and returns a list of machine identities.
Right now it reads from a local JSON file (simulating a scan).
Later you can extend this to read from cloud provider APIs,
.env files, GitHub repos, or Kubernetes secrets.
"""

import json
from pathlib import Path


def discover_identities(source_path: str) -> list[dict]:
    """
    Load and validate identities from the given JSON file.
    Returns a list of dicts, each representing one identity.
    """
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"No such data source: {source_path}")

    with open(path, "r") as f:
        raw_identities = json.load(f)

    required_fields = {"name", "owner", "type", "permissions",
                        "created_date", "last_used"}

    valid_identities = []
    for identity in raw_identities:
        missing = required_fields - identity.keys()
        if missing:
            print(f"[WARN] Skipping '{identity.get('name', '?')}' "
                  f"- missing fields: {missing}")
            continue
        valid_identities.append(identity)

    print(f"[INFO] Discovered {len(valid_identities)} identities.")
    return valid_identities


if __name__ == "__main__":
    # Quick manual test
    identities = discover_identities("../data/identities.json")
    for i in identities:
        print(i["name"], "-", i["owner"])
