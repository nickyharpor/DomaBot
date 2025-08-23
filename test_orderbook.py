import types
import pytest
import requests

import caller_orderbook

# Use config.doma_api_key as required; provide a fallback if module is absent.
try:
    import config  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without config module
    config = types.SimpleNamespace(doma_api_key="test_api_key")


class FakeResp:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


@pytest.fixture
def api_key():
    return config.doma_api_key


@pytest.fixture
def base_url(monkeypatch):
    base = "https://api.example.test"
    monkeypatch.setattr(caller_orderbook, "DEFAULT_BASE_URL", base, raising=True)
    return base


@pytest.fixture
def expected_headers(monkeypatch, api_key):
    headers = {"X-API-Key": api_key}
    # Ensure the module under test uses our deterministic header builder
    def fake_build_headers(key: str):
        assert key == api_key
        return headers

    monkeypatch.setattr(caller_orderbook, "_build_headers", fake_build_headers, raising=True)
    return headers


def test_create_listing_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_post(url, *, headers=None, json=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["json"] = json
        seen["timeout"] = timeout
        return FakeResp({"result": "ok", "id": "L1"})

    monkeypatch.setattr(caller_orderbook.requests, "post", fake_post, raising=True)

    payload_params = {"tokenAddress": "0xabc", "tokenId": "1", "price": "100"}
    out = caller_orderbook.create_listing(
        api_key=api_key,
        orderbook="OPENSEA",
        chain_id="eip155:1",
        parameters=payload_params,
        signature="0xsig",
        timeout=11,
    )

    assert out == {"result": "ok", "id": "L1"}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/list"
    assert seen["headers"] == expected_headers
    assert seen["json"] == {
        "orderbook": "OPENSEA",
        "chainId": "eip155:1",
        "parameters": payload_params,
        "signature": "0xsig",
    }
    assert seen["timeout"] == 11


@pytest.mark.parametrize(
    "kwargs, err_msg",
    [
        (dict(orderbook="", chain_id="1", parameters={"a": 1}, signature="s"), "orderbook"),
        (dict(orderbook="DOMA", chain_id="", parameters={"a": 1}, signature="s"), "chain_id"),
        (dict(orderbook="DOMA", chain_id="1", parameters={}, signature="s"), "parameters"),
        (dict(orderbook="DOMA", chain_id="1", parameters="bad", signature="s"), "parameters"),
        (dict(orderbook="DOMA", chain_id="1", parameters={"a": 1}, signature=""), "signature"),
    ],
)
def test_create_listing_validation(kwargs, err_msg, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.create_listing(api_key=api_key, **kwargs)
    assert err_msg in str(ei.value)


def test_create_offer_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_post(url, *, headers=None, json=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["json"] = json
        seen["timeout"] = timeout
        return FakeResp({"result": "ok", "id": "O1"})

    monkeypatch.setattr(caller_orderbook.requests, "post", fake_post, raising=True)

    params = {"tokenAddress": "0xabc", "tokenId": "1", "price": "50"}
    out = caller_orderbook.create_offer(
        api_key=api_key,
        orderbook="DOMA",
        chain_id="eip155:8453",
        parameters=params,
        signature="0xsig",
        timeout=7,
    )

    assert out == {"result": "ok", "id": "O1"}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/offer"
    assert seen["headers"] == expected_headers
    assert seen["json"] == {
        "orderbook": "DOMA",
        "chainId": "eip155:8453",
        "parameters": params,
        "signature": "0xsig",
    }
    assert seen["timeout"] == 7


@pytest.mark.parametrize(
    "kwargs, err_msg",
    [
        (dict(orderbook="", chain_id="1", parameters={"a": 1}, signature="s"), "orderbook"),
        (dict(orderbook="DOMA", chain_id="", parameters={"a": 1}, signature="s"), "chain_id"),
        (dict(orderbook="DOMA", chain_id="1", parameters={}, signature="s"), "parameters"),
        (dict(orderbook="DOMA", chain_id="1", parameters="bad", signature="s"), "parameters"),
        (dict(orderbook="DOMA", chain_id="1", parameters={"a": 1}, signature=""), "signature"),
    ],
)
def test_create_offer_validation(kwargs, err_msg, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.create_offer(api_key=api_key, **kwargs)
    assert err_msg in str(ei.value)


def test_get_listing_fulfillment_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_get(url, *, headers=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["timeout"] = timeout
        return FakeResp({"fulfillment": {"ok": True}})

    monkeypatch.setattr(caller_orderbook.requests, "get", fake_get, raising=True)

    out = caller_orderbook.get_listing_fulfillment(api_key=api_key, order_id="ORD123", buyer="0xBuyer", timeout=4)
    assert out == {"fulfillment": {"ok": True}}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/listing/ORD123/0xBuyer"
    assert seen["headers"] == expected_headers
    assert seen["timeout"] == 4


@pytest.mark.parametrize(
    "order_id,buyer,err_contains",
    [
        ("", "0xBuyer", "order_id"),
        ("ORD", "", "buyer"),
    ],
)
def test_get_listing_fulfillment_validation(order_id, buyer, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.get_listing_fulfillment(api_key=api_key, order_id=order_id, buyer=buyer)
    assert err_contains in str(ei.value)


def test_get_offer_fulfillment_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_get(url, *, headers=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["timeout"] = timeout
        return FakeResp({"fulfillment": {"ok": True}})

    monkeypatch.setattr(caller_orderbook.requests, "get", fake_get, raising=True)

    out = caller_orderbook.get_offer_fulfillment(api_key=api_key, order_id="ORD456", fulfiller="0xOwner", timeout=9)
    assert out == {"fulfillment": {"ok": True}}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/offer/ORD456/0xOwner"
    assert seen["headers"] == expected_headers
    assert seen["timeout"] == 9


@pytest.mark.parametrize(
    "order_id,fulfiller,err_contains",
    [
        ("", "0xOwner", "order_id"),
        ("ORD", "", "fulfiller"),
    ],
)
def test_get_offer_fulfillment_validation(order_id, fulfiller, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.get_offer_fulfillment(api_key=api_key, order_id=order_id, fulfiller=fulfiller)
    assert err_contains in str(ei.value)


def test_cancel_listing_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_post(url, *, headers=None, json=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["json"] = json
        seen["timeout"] = timeout
        return FakeResp({"cancelled": True})

    monkeypatch.setattr(caller_orderbook.requests, "post", fake_post, raising=True)

    out = caller_orderbook.cancel_listing(api_key=api_key, order_id="ORD789", signature="0xsig", timeout=12)
    assert out == {"cancelled": True}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/listing/cancel"
    assert seen["headers"] == expected_headers
    assert seen["json"] == {"orderId": "ORD789", "signature": "0xsig"}
    assert seen["timeout"] == 12


@pytest.mark.parametrize(
    "order_id,signature,err_contains",
    [
        ("", "0xsig", "order_id"),
        ("ORD", "", "signature"),
    ],
)
def test_cancel_listing_validation(order_id, signature, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.cancel_listing(api_key=api_key, order_id=order_id, signature=signature)
    assert err_contains in str(ei.value)


def test_cancel_offer_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_post(url, *, headers=None, json=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["json"] = json
        seen["timeout"] = timeout
        return FakeResp({"cancelled": True})

    monkeypatch.setattr(caller_orderbook.requests, "post", fake_post, raising=True)

    out = caller_orderbook.cancel_offer(api_key=api_key, order_id="ORD321", signature="0xsig", timeout=13)
    assert out == {"cancelled": True}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/offer/cancel"
    assert seen["headers"] == expected_headers
    assert seen["json"] == {"orderId": "ORD321", "signature": "0xsig"}
    assert seen["timeout"] == 13


@pytest.mark.parametrize(
    "order_id,signature,err_contains",
    [
        ("", "0xsig", "order_id"),
        ("ORD", "", "signature"),
    ],
)
def test_cancel_offer_validation(order_id, signature, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.cancel_offer(api_key=api_key, order_id=order_id, signature=signature)
    assert err_contains in str(ei.value)


def test_get_orderbook_fee_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_get(url, *, headers=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["timeout"] = timeout
        return FakeResp({"feeBps": 250})

    monkeypatch.setattr(caller_orderbook.requests, "get", fake_get, raising=True)

    out = caller_orderbook.get_orderbook_fee(
        api_key=api_key,
        orderbook="OPENSEA",
        chain_id="eip155:1",
        contract_address="0xcontract",
        timeout=5,
    )
    assert out == {"feeBps": 250}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/fee/OPENSEA/eip155:1/0xcontract"
    assert seen["headers"] == expected_headers
    assert seen["timeout"] == 5


@pytest.mark.parametrize(
    "orderbook,chain_id,contract_address,err_contains",
    [
        ("", "1", "0xC", "orderbook"),
        ("OPENSEA", "", "0xC", "chain_id"),
        ("OPENSEA", "1", "", "contract_address"),
    ],
)
def test_get_orderbook_fee_validation(orderbook, chain_id, contract_address, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.get_orderbook_fee(
            api_key=api_key,
            orderbook=orderbook,
            chain_id=chain_id,
            contract_address=contract_address,
        )
    assert err_contains in str(ei.value)


def test_get_supported_currencies_success(monkeypatch, api_key, base_url, expected_headers):
    seen = {}

    def fake_get(url, *, headers=None, timeout=None):
        seen["url"] = url
        seen["headers"] = headers
        seen["timeout"] = timeout
        return FakeResp({"items": [{"symbol": "ETH"}]})

    monkeypatch.setattr(caller_orderbook.requests, "get", fake_get, raising=True)

    out = caller_orderbook.get_supported_currencies(
        api_key=api_key,
        chain_id="eip155:1",
        contract_address="0xcontract",
        orderbook="DOMA",
        timeout=8,
    )
    assert out == {"items": [{"symbol": "ETH"}]}
    assert seen["url"] == f"{base_url.rstrip('/')}/v1/orderbook/currencies/eip155:1/0xcontract/DOMA"
    assert seen["headers"] == expected_headers
    assert seen["timeout"] == 8


@pytest.mark.parametrize(
    "chain_id,contract_address,orderbook,err_contains",
    [
        ("", "0xC", "DOMA", "chain_id"),
        ("1", "", "DOMA", "contract_address"),
        ("1", "0xC", "", "orderbook"),
    ],
)
def test_get_supported_currencies_validation(chain_id, contract_address, orderbook, err_contains, api_key):
    with pytest.raises(ValueError) as ei:
        caller_orderbook.get_supported_currencies(
            api_key=api_key,
            chain_id=chain_id,
            contract_address=contract_address,
            orderbook=orderbook,
        )
    assert err_contains in str(ei.value)


def test_http_error_propagates(monkeypatch, api_key):
    def fake_post(url, *, headers=None, json=None, timeout=None):
        return FakeResp({"error": "bad"}, status_code=400)

    monkeypatch.setattr(caller_orderbook.requests, "post", fake_post, raising=True)

    with pytest.raises(requests.HTTPError):
        caller_orderbook.create_listing(
            api_key=api_key,
            orderbook="DOMA",
            chain_id="eip155:1",
            parameters={"a": 1},
            signature="0xsig",
        )