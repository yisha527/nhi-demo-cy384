"""
Main Pipeline
--------------
Runs the full Non-Human Identity Management workflow:
  1. Discover identities
  2. Score each one
  3. Classify risk level
  4. Alert on anything High/Critical
  5. Print a summary table
"""

from discovery import discover_identities
from risk_scoring import calculate_risk_score
from classification import classify_risk
from alerting import check_and_alert


def run_pipeline(data_source: str = "../data/identities.json"):
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
        })

    print_summary(results)
    return results


def print_summary(results: list[dict]) -> None:
    print("\n" + "=" * 60)
    print(f"{'Identity':<22}{'Owner':<18}{'Score':<8}{'Risk'}")
    print("-" * 60)
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"{r['name']:<22}{r['owner']:<18}{r['score']:<8}{r['label']}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
