"""
Unit tests for the Discovery Engine.

Run with:  pytest test_discovery.py -v

Uses pytest's built-in tmp_path fixture to create throwaway CSV
files for each test, so nothing here touches your real data/ folder.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from discovery import discover_identities


VALID_CSV = """id,name,type,owner,age_days,idle_days,active,permissions,risk_score,risk_level
nhi-0001,api_key-001,API Key,platform-team,35,15,True,payments:write|users:read,25,MEDIUM
nhi-0002,cicd_token-002,CI/CD Token,payments-eng,99,4,True,repo:write|deploy:prod,39,MEDIUM
"""

MISSING_COLUMN_CSV = """id,name,type,owner,age_days,idle_days,permissions
nhi-0003,broken-003,API Key,dev-team,10,2,repo:read
"""


def test_discovers_all_valid_rows(tmp_path):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(VALID_CSV)

    identities = discover_identities(str(csv_file))

    assert len(identities) == 2
    assert identities[0]["name"] == "api_key-001"


def test_permissions_are_split_into_a_list(tmp_path):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(VALID_CSV)

    identities = discover_identities(str(csv_file))

    assert identities[0]["permissions"] == ["payments:write", "users:read"]


def test_numeric_fields_are_converted_to_int(tmp_path):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(VALID_CSV)

    identities = discover_identities(str(csv_file))

    assert identities[0]["age_days"] == 35
    assert isinstance(identities[0]["age_days"], int)


def test_active_field_is_converted_to_bool(tmp_path):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(VALID_CSV)

    identities = discover_identities(str(csv_file))

    assert identities[0]["active"] is True


def test_reference_score_is_captured(tmp_path):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(VALID_CSV)

    identities = discover_identities(str(csv_file))

    assert identities[0]["reference_risk_score"] == 25
    assert identities[0]["reference_risk_level"] == "MEDIUM"


def test_row_missing_required_column_is_skipped(tmp_path, capsys):
    csv_file = tmp_path / "identities.csv"
    csv_file.write_text(MISSING_COLUMN_CSV)

    identities = discover_identities(str(csv_file))

    assert len(identities) == 0
    captured = capsys.readouterr()
    assert "WARN" in captured.out


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        discover_identities("this/path/does/not/exist.csv")
