import io
import json
import types
import pytest
from urllib import error as urlerror

import caller_graphql
from caller_graphql import DomaGraphQLClient, GraphQLClientError

# Use config.doma_api_key as required; provide a fallback if module is absent.
try:
    import config  # type: ignore
except Exception:  # pragma: no cover - fallback only for local runs without config module
    config = types.SimpleNamespace(doma_api_key="test_api_key")


class FakeResponse:
    def __init__(self, obj):
        self._payload = json.dumps(obj).encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


@pytest.mark.parametrize(
    "operation_name, field_key, invoker, expected_vars",
    [
        ("Names", "names", lambda c: c.query_names(skip=0, take=1), {"skip": 0, "take": 1}),
        ("Name", "name", lambda c: c.query_name("example.com"), {"name": "example.com"}),
        (
            "Tokens",
            "tokens",
            lambda c: c.query_tokens("example.com", skip=0, take=1),
            {"name": "example.com", "skip": 0, "take": 1},
        ),
        ("Token", "token", lambda c: c.query_token("t1"), {"tokenId": "t1"}),
        ("Command", "command", lambda c: c.query_command("corr1"), {"correlationId": "corr1"}),
        (
            "NameActivities",
            "nameActivities",
            lambda c: c.query_name_activities("example.com", skip=0.0, take=10.0),
            {"name": "example.com", "skip": 0.0, "take": 10.0},
        ),
        (
            "TokenActivities",
            "tokenActivities",
            lambda c: c.query_token_activities("t1", skip=0.0, take=10.0),
            {"tokenId": "t1", "skip": 0.0, "take": 10.0},
        ),
        ("Listings", "listings", lambda c: c.query_listings(tlds=["com"], take=5.0), {"tlds": ["com"], "take": 5.0}),
        ("Offers", "offers", lambda c: c.query_offers(tokenId="t1", take=5.0), {"tokenId": "t1", "take": 5.0}),
        ("NameStatistics", "nameStatistics", lambda c: c.query_name_statistics("t1"), {"tokenId": "t1"}),
    ],
)
def test_all_operations_send_correct_payload_and_headers(monkeypatch, operation_name, field_key, invoker, expected_vars):
    seen = {}

    def fake_urlopen(req, timeout):
        payload = json.loads(req.data.decode("utf-8"))
        seen["payload"] = payload
        seen["headers"] = dict(req.headers)
        # Respond with a minimal valid data envelope for the requested field
        return FakeResponse({"data": {field_key: {"marker": operation_name}}})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    result = invoker(client)

    assert result == {"marker": operation_name}
    assert "payload" in seen and "headers" in seen
    assert seen["payload"]["operationName"] == operation_name
    # Verify expected non-None variables are present and correct
    for k, v in expected_vars.items():
        assert seen["payload"]["variables"][k] == v
    # API key and common headers present
    assert seen["headers"].get("X-API-Key") == config.doma_api_key
    assert seen["headers"].get("Content-Type") == "application/json"
    assert seen["headers"].get("Accept") == "application/json"


def test_api_key_header_added_and_used(monkeypatch):
    captured = {}

    def fake_urlopen(req, timeout):
        captured["headers"] = dict(req.headers)
        # Return minimal valid response for any query
        return FakeResponse({"data": {"name": {"ok": True}}})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    client.query_name("example.com")

    assert captured["headers"].get("X-API-Key") == config.doma_api_key


def test_does_not_override_existing_authorization(monkeypatch):
    captured = {}

    def fake_urlopen(req, timeout):
        captured["headers"] = dict(req.headers)
        return FakeResponse({"data": {"name": {"ok": True}}})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(headers={"Authorization": "Bearer abc123"}, api_key=config.doma_api_key)
    client.query_name("example.com")

    assert "Authorization" in captured["headers"]
    assert "X-API-Key" not in captured["headers"]


def test_filter_none_removes_unset_variables(monkeypatch):
    def fake_urlopen(req, timeout):
        payload = json.loads(req.data.decode("utf-8"))
        # Ensure None values were removed
        assert "status" not in payload["variables"]
        assert "sortOrder" not in payload["variables"]
        return FakeResponse({"data": {"offers": {"ok": True}}})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    # All optional args None should be stripped from variables
    client.query_offers(tokenId=None, offeredBy=None, skip=None, take=None, status=None, sortOrder=None)


def test_http_error_raises_graphql_client_error(monkeypatch):
    def fake_urlopen(req, timeout):
        body = b'{"errors":[{"message":"boom"}]}'
        raise urlerror.HTTPError(
            url="http://example.invalid/graphql",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=io.BytesIO(body),
        )

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    with pytest.raises(GraphQLClientError) as ei:
        client.query_name("example.com")
    err = ei.value
    assert "HTTP 400" in str(err)
    assert err.status == 400
    assert err.errors and err.errors[0].get("message") == "boom"


def test_top_level_graphql_errors_raise(monkeypatch):
    def fake_urlopen(req, timeout):
        return FakeResponse({"errors": [{"message": "GraphQL bad"}]})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    with pytest.raises(GraphQLClientError) as ei:
        client.query_name("example.com")
    assert "GraphQL responded with errors" in str(ei.value)


def test_invalid_json_response_raises(monkeypatch):
    class BadJSONResponse:
        def read(self):
            return b"not-json"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(req, timeout):
        return BadJSONResponse()

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    with pytest.raises(GraphQLClientError) as ei:
        client.query_name("example.com")
    assert "Failed to decode GraphQL response as JSON" in str(ei.value)


def test_missing_data_field_raises(monkeypatch):
    def fake_urlopen(req, timeout):
        return FakeResponse({"no_data_here": True})

    monkeypatch.setattr(caller_graphql.request, "urlopen", fake_urlopen)

    client = DomaGraphQLClient(api_key=config.doma_api_key)
    with pytest.raises(GraphQLClientError) as ei:
        client.query_name("example.com")
    assert "missing 'data' field" in str(ei.value).lower()