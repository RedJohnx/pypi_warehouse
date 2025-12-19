import json
from datetime import datetime

def _read_json_line(capsys):
    captured = capsys.readouterr()
    line = captured.err.strip()
    assert line, "Expected a log line on stderr, got empty output"
    return json.loads(line)

def test_json_has_timestamp(capsys):
    from logfmt import Logger
    log = Logger("myapp", output="json", timestamp=True)

    log.info("hello")
    obj = _read_json_line(capsys)

    assert "ts" in obj
    # very lightweight sanity check: ISO-like string
    assert "T" in obj["ts"]

def test_json_no_timestamp_when_disabled(capsys):
    from logfmt import Logger
    log = Logger("myapp", output="json", timestamp=False)

    log.info("hello")
    obj = _read_json_line(capsys)

    assert "ts" not in obj

def test_json_non_serializable_field_is_stringified(capsys):
    from logfmt import Logger
    log = Logger("myapp", output="json")

    log.info("payload", payload={1, 2, 3})  # set is not JSON serializable
    obj = _read_json_line(capsys)

    # because json.dumps(..., default=str)
    assert "payload" in obj["fields"]
    assert isinstance(obj["fields"]["payload"], str)

def test_json_exception_helper_adds_exception_field(capsys):
    from logfmt import Logger
    log = Logger("myapp", output="json")

    try:
        1 / 0
    except Exception as e:
        log.exception("boom", exc=e)

    obj = _read_json_line(capsys)

    assert obj["level"] == "error"
    assert obj["msg"] == "boom"
    assert "exception" in obj["fields"]
    assert "ZeroDivisionError" in obj["fields"]["exception"]

def test_level_filtering_still_works_in_json_mode(capsys):
    from logfmt import Logger, LogLevel
    log = Logger("myapp", output="json", level=LogLevel.ERROR)

    log.info("should_not_print")
    captured = capsys.readouterr()
    assert captured.err.strip() == ""

    log.error("should_print", code=500)
    obj = _read_json_line(capsys)

    assert obj["level"] == "error"
    assert obj["fields"]["code"] == 500
