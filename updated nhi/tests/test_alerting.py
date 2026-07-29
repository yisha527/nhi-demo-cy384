"""
Unit tests for the Alerting Module.

Run with:  pytest test_alerting.py -v

We monkeypatch LOG_FILE to a temp path so tests never write to your
real data/alerts.log.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import alerting


SAMPLE_IDENTITY = {"name": "test-identity", "owner": "test-owner"}


def test_raise_alert_prints_message(capsys, tmp_path, monkeypatch):
    monkeypatch.setattr(alerting, "LOG_FILE", str(tmp_path / "alerts.log"))
    alerting.raise_alert(SAMPLE_IDENTITY, 90, "CRITICAL")
    captured = capsys.readouterr()
    assert "CRITICAL" in captured.out
    assert "test-identity" in captured.out
    assert "90/100" in captured.out


def test_raise_alert_writes_to_log_file(tmp_path, monkeypatch):
    log_file = tmp_path / "alerts.log"
    monkeypatch.setattr(alerting, "LOG_FILE", str(log_file))

    alerting.raise_alert(SAMPLE_IDENTITY, 80, "CRITICAL")

    contents = log_file.read_text()
    assert "test-identity" in contents
    assert "CRITICAL" in contents


def test_check_and_alert_triggers_at_or_above_threshold(tmp_path, monkeypatch):
    log_file = tmp_path / "alerts.log"
    monkeypatch.setattr(alerting, "LOG_FILE", str(log_file))

    triggered = alerting.check_and_alert(SAMPLE_IDENTITY, 60, "HIGH", threshold="HIGH")

    assert triggered is True


def test_check_and_alert_does_not_trigger_below_threshold(tmp_path, monkeypatch):
    log_file = tmp_path / "alerts.log"
    monkeypatch.setattr(alerting, "LOG_FILE", str(log_file))

    triggered = alerting.check_and_alert(SAMPLE_IDENTITY, 30, "MEDIUM", threshold="HIGH")

    assert triggered is False


def test_check_and_alert_critical_always_triggers_high_threshold(tmp_path, monkeypatch):
    log_file = tmp_path / "alerts.log"
    monkeypatch.setattr(alerting, "LOG_FILE", str(log_file))

    triggered = alerting.check_and_alert(SAMPLE_IDENTITY, 95, "CRITICAL", threshold="HIGH")

    assert triggered is True
