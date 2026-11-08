from modules.detector import to_seconds, stamp, extract_events, evaluate

def test_timestamp_conversion():
    assert to_seconds("00:01:05.50") == 65.5
    assert stamp(65) == "01:05"

def test_extracts_timed_beats():
    raw = """**LADY JULIANA (Shocked):**
Start: (00:01.00) | End: (00:03.00)
"Why did you do this?"
"""
    events = extract_events(raw)
    assert len(events) == 1
    assert events[0]["kind"] == "dialogue"
    assert "Why" in events[0]["dialogue"]

def test_window_duration_and_evidence():
    events=[{"start":0,"end":5,"kind":"dialogue","dialogue":"Stop!","text":"Stop!"},
            {"start":30,"end":35,"kind":"dialogue","dialogue":"The truth is coming.","text":"The truth is coming."}]
    result=evaluate(events,0,35,"A family secret changes everything.")
    assert result["duration"] == 35
    assert result["hook_type"] == "dialogue"
    assert result["ending_type"] == "dialogue"
