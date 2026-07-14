from app.core.math_engine import StadiumSeverityEngine

def test_baseline_score():
    engine = StadiumSeverityEngine()
    # An empty log should return the baseline score of 10.00
    assert engine.calculate_channel_severity("") == 10.00

def test_critical_escalation():
    engine = StadiumSeverityEngine()
    # A log containing severe keywords like 'fire' and 'injury' should escalate highly
    high_threat_score = engine.calculate_channel_severity("Report of a fire and an injury in the stands.")
    assert high_threat_score > 10.00