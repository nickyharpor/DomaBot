import pytest
from unittest.mock import MagicMock
from dotenv import load_dotenv
import os
from pprint import pprint

# Environment detection
load_dotenv()
env = os.getenv("ENV")
if env == 'live':
    import config_live
    config = config_live
elif env == 'dev':
    import config_dev
    config = config_dev
else:
    import config_test
    config = config_test

from caller_poll import (
    DEFAULT_BASE_URL,
    _build_headers,
    _bool_to_str,
    poll_events,
    acknowledge_events,
    reset_last_acknowledged_event,
)


def test_build_headers_returns_expected_dict():
    headers = _build_headers(config.doma_api_key)
    assert headers == {
        "Api-Key": config.doma_api_key,
        "Accept": "application/json",
    }


def test_bool_to_str_true_false():
    assert _bool_to_str(True) == "true"
    assert _bool_to_str(False) == "false"


def test_poll_events_print_result_only():
    result = poll_events(
        api_key=config.doma_api_key
    )
    pprint(result)


def test_poll_events_builds_params_and_returns_json(monkeypatch):
    expected = {
        "events": [
            {
                "id": 1,
                "type": "COMMAND_CREATED",
                "eventData": {
                    "relayId": "relay-1",
                    "transactions": [],
                    "failureData": None,
                    "type": "COMMAND_CREATED",
                },
            }
        ],
        "lastId": 1,
        "hasMoreEvents": False,
    }
    captured = {}

    def fake_get(url, headers, params, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        captured["timeout"] = timeout
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        resp.json.return_value = expected
        return resp

    monkeypatch.setattr("caller_poll.requests.get", fake_get)

    result = poll_events(
        api_key=config.doma_api_key,
        event_types=["NAME_UPDATED", "COMMAND_CREATED"],
        limit=10,
        finalized_only=False,
        timeout=7,
    )

    assert result == expected
    assert captured["url"] == f"{DEFAULT_BASE_URL}/v1/poll"
    assert captured["headers"] == _build_headers(config.doma_api_key)
    assert captured["timeout"] == 7
    # Params should include repeated eventTypes and proper string conversions
    assert captured["params"] == [
        ("eventTypes", "NAME_UPDATED"),
        ("eventTypes", "COMMAND_CREATED"),
        ("limit", "10"),
        ("finalizedOnly", "false"),
    ]


def test_poll_events_no_finalized_only_when_none(monkeypatch):
    captured = {}

    def fake_get(url, headers, params, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        captured["timeout"] = timeout
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        # Minimal valid response per schema: only 'events' is required
        resp.json.return_value = {"events": []}
        return resp

    monkeypatch.setattr("caller_poll.requests.get", fake_get)

    result = poll_events(
        api_key=config.doma_api_key,
        event_types=None,
        limit=None,
        finalized_only=None,
    )

    assert result == {"events": []}
    assert captured["url"] == f"{DEFAULT_BASE_URL}/v1/poll"
    assert captured["headers"] == _build_headers(config.doma_api_key)
    assert captured["params"] == []  # finalizedOnly omitted when None


def test_poll_events_limit_validation_error():
    with pytest.raises(ValueError):
        poll_events(api_key=config.doma_api_key, limit=0)


def test_acknowledge_events_success(monkeypatch):
    last_event_id = 123
    captured = {}

    def fake_post(url, headers, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["timeout"] = timeout
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        return resp

    monkeypatch.setattr("caller_poll.requests.post", fake_post)

    # Should not raise
    acknowledge_events(api_key=config.doma_api_key, last_event_id=last_event_id, timeout=5)

    assert captured["url"] == f"{DEFAULT_BASE_URL}/v1/poll/ack/{last_event_id}"
    assert captured["headers"] == _build_headers(config.doma_api_key)
    assert captured["timeout"] == 5


def test_acknowledge_events_invalid_id_raises():
    with pytest.raises(ValueError):
        acknowledge_events(api_key=config.doma_api_key, last_event_id=-1)
    # Despite type hints, passing None at runtime should hit our validation
    with pytest.raises(ValueError):
        acknowledge_events(api_key=config.doma_api_key, last_event_id=None)  # type: ignore[arg-type]


def test_reset_last_acknowledged_event_success(monkeypatch):
    event_id = 42
    captured = {}

    def fake_post(url, headers, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["timeout"] = timeout
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        return resp

    monkeypatch.setattr("caller_poll.requests.post", fake_post)

    # Should not raise
    reset_last_acknowledged_event(api_key=config.doma_api_key, event_id=event_id, timeout=3)

    assert captured["url"] == f"{DEFAULT_BASE_URL}/v1/poll/reset/{event_id}"
    assert captured["headers"] == _build_headers(config.doma_api_key)
    assert captured["timeout"] == 3


def test_reset_last_acknowledged_event_invalid_event_id_raises():
    with pytest.raises(ValueError):
        reset_last_acknowledged_event(api_key=config.doma_api_key, event_id=-10)
    with pytest.raises(ValueError):
        reset_last_acknowledged_event(api_key=config.doma_api_key, event_id=None)  # type: ignore[arg-type]