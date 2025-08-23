from typing import Dict, Any, Union
import requests

from caller_poll import DEFAULT_BASE_URL, _build_headers

__all__ = [
    "create_listing",
    "create_offer",
    "get_listing_fulfillment",
    "get_offer_fulfillment",
    "cancel_listing",
    "cancel_offer",
    "get_orderbook_fee",
    "get_supported_currencies",
]


def create_listing(
    api_key: str,
    orderbook: str,
    chain_id: str,
    parameters: Dict[str, Any],
    signature: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    POST /v1/orderbook/list
    Create a fixed priced listing on a supported orderbook (OpenSea, Doma).
    """
    if not orderbook:
        raise ValueError("orderbook must be a non-empty string")
    if not chain_id:
        raise ValueError("chain_id must be a non-empty string")
    if not isinstance(parameters, dict) or not parameters:
        raise ValueError("parameters must be a non-empty dict")
    if not signature:
        raise ValueError("signature must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/list"
    payload = {
        "orderbook": orderbook,
        "chainId": chain_id,
        "parameters": parameters,
        "signature": signature,
    }

    resp = requests.post(url, headers=_build_headers(api_key), json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def create_offer(
    api_key: str,
    orderbook: str,
    chain_id: str,
    parameters: Dict[str, Any],
    signature: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    POST /v1/orderbook/offer
    Create an offer on a supported orderbook (OpenSea, Doma).
    """
    if not orderbook:
        raise ValueError("orderbook must be a non-empty string")
    if not chain_id:
        raise ValueError("chain_id must be a non-empty string")
    if not isinstance(parameters, dict) or not parameters:
        raise ValueError("parameters must be a non-empty dict")
    if not signature:
        raise ValueError("signature must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/offer"
    payload = {
        "orderbook": orderbook,
        "chainId": chain_id,
        "parameters": parameters,
        "signature": signature,
    }

    resp = requests.post(url, headers=_build_headers(api_key), json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_listing_fulfillment(
    api_key: str,
    order_id: str,
    buyer: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    GET /v1/orderbook/listing/{orderId}/{buyer}
    Get listing fulfillment data by order id and buyer address.
    """
    if not order_id:
        raise ValueError("order_id must be a non-empty string")
    if not buyer:
        raise ValueError("buyer must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/listing/{order_id}/{buyer}"

    resp = requests.get(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_offer_fulfillment(
    api_key: str,
    order_id: str,
    fulfiller: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    GET /v1/orderbook/offer/{orderId}/{fulfiller}
    Get offer fulfillment data by order id and fulfiller (token owner) address.
    """
    if not order_id:
        raise ValueError("order_id must be a non-empty string")
    if not fulfiller:
        raise ValueError("fulfiller must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/offer/{order_id}/{fulfiller}"

    resp = requests.get(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def cancel_listing(
    api_key: str,
    order_id: str,
    signature: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    POST /v1/orderbook/listing/cancel
    Cancel a listing on a supported orderbook (OpenSea, Doma).
    """
    if not order_id:
        raise ValueError("order_id must be a non-empty string")
    if not signature:
        raise ValueError("signature must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/listing/cancel"
    payload = {"orderId": order_id, "signature": signature}

    resp = requests.post(url, headers=_build_headers(api_key), json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def cancel_offer(
    api_key: str,
    order_id: str,
    signature: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    POST /v1/orderbook/offer/cancel
    Cancel an offer on a supported orderbook (OpenSea, Doma).
    """
    if not order_id:
        raise ValueError("order_id must be a non-empty string")
    if not signature:
        raise ValueError("signature must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/offer/cancel"
    payload = {"orderId": order_id, "signature": signature}

    resp = requests.post(url, headers=_build_headers(api_key), json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_orderbook_fee(
    api_key: str,
    orderbook: str,
    chain_id: str,
    contract_address: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    GET /v1/orderbook/fee/{orderbook}/{chainId}/{contractAddress}
    Get marketplace fees for a specific orderbook and chain.
    """
    if not orderbook:
        raise ValueError("orderbook must be a non-empty string")
    if not chain_id:
        raise ValueError("chain_id must be a non-empty string")
    if not contract_address:
        raise ValueError("contract_address must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/fee/{orderbook}/{chain_id}/{contract_address}"

    resp = requests.get(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_supported_currencies(
    api_key: str,
    chain_id: str,
    contract_address: str,
    orderbook: str,
    *,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    GET /v1/orderbook/currencies/{chainId}/{contractAddress}/{orderbook}
    Get all supported currency tokens for orderbook operations on a specific chain.
    """
    if not chain_id:
        raise ValueError("chain_id must be a non-empty string")
    if not contract_address:
        raise ValueError("contract_address must be a non-empty string")
    if not orderbook:
        raise ValueError("orderbook must be a non-empty string")

    base = DEFAULT_BASE_URL.rstrip("/")
    url = f"{base}/v1/orderbook/currencies/{chain_id}/{contract_address}/{orderbook}"

    resp = requests.get(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    return resp.json()