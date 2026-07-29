"""
Main Pipeline
--------------
Runs the full Non-Human Identity Management workflow:
  1. Discover identities (from CSV)
  2. Score each one with our own algorithm
  3. Classify risk level
  4. Alert on anything High/Critical
  5. Print a summary table, including a comparison against the
     CSV's reference risk_score/risk_level (useful for your
     Testing & Reporting phase)
"""

from discovery import discover_identities
from risk_scoring import calculate_risk_score
from classification import classify_risk
from alerting import check_and_alert


def run_pipeline(data_source: str = "../data/nhi_inventory.csv"):
    identities = discover_identities(data_source)

    results = []
    for identity in identities:
        score = calculate_risk_score(identity)
        label = classify_risk(score)
        check_and_alert(identity, score, label, threshold="HIGH")

        results.append({
            "name": identity["name"],
            "owner": identity["owner"],
            "score": score,
            "label": label,
            "ref_score": identity.get("reference_risk_score"),
            "ref_label": identity.get("reference_risk_level"),
        })

    print_summary(results)
    return results


def print_summary(results: list[dict]) -> None:
    print("\n" + "=" * 78)
    print(f"{'Identity':<20}{'Score':<8}{'Risk':<10}{'Ref Score':<12}{'Ref Risk':<10}")
    print("-" * 78)
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"{r['name']:<20}{r['score']:<8}{r['label']:<10}"
              f"{str(r['ref_score']):<12}{str(r['ref_label']):<10}")
    print("=" * 78)


if __name__ == "__main__":
    run_pipeline()
