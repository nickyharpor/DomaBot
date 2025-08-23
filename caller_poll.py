from typing import List, Optional, Sequence, Tuple, Union, Dict, Any
import requests

__all__ = [
    "poll_events",
    "acknowledge_events",
    "reset_last_acknowledged_event",
]

DEFAULT_BASE_URL = "https://api-testnet.doma.xyz"

def _build_headers(api_key: str) -> Dict[str, str]:
    return {
        "Api-Key": api_key,
        "Accept": "application/json",
    }


def _bool_to_str(value: bool) -> str:
    return "true" if value else "false"


def poll_events(
    api_key: str,
    event_types: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
    finalized_only: Optional[bool] = True,
    timeout: Union[int, float] = 15,
) -> Dict[str, Any]:
    """
    GET /v1/poll
    Poll for new Doma Protocol events since the last acknowledged event.

    Args:
        event_types: Optional list of event type filters. Each value is sent as a separate 'eventTypes' query param.
        limit: Optional max number of events to return.
        finalized_only: If True, return only finalized events. If None, do not send the parameter.
        api_key: API key to authenticate the request.
        timeout: Requests timeout in seconds.

    Returns:
        Parsed JSON dict as returned by the API, e.g. {'events': [...], 'lastId': ..., 'hasMoreEvents': ...}

    Raises:
        requests.HTTPError for non-2xx responses.
        ValueError if inputs are invalid.
    """
    url = f"{DEFAULT_BASE_URL}/v1/poll"

    # Build query params; use list of tuples to allow repeated keys for eventTypes
    params: List[Tuple[str, str]] = []
    if event_types:
        for et in event_types:
            params.append(("eventTypes", et))
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        params.append(("limit", str(limit)))
    if finalized_only is not None:
        params.append(("finalizedOnly", _bool_to_str(bool(finalized_only))))

    resp = requests.get(url, headers=_build_headers(api_key), params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def acknowledge_events(
    api_key: str,
    last_event_id: int,
    timeout: Union[int, float] = 15,
) -> None:
    """
    POST /v1/poll/ack/{lastEventId}
    Acknowledge received events up to and including last_event_id.

    Args:
        last_event_id: The last processed event id.
        api_key: API key to authenticate the request.
        timeout: Requests timeout in seconds.

    Returns:
        None. Raises if not successful.

    Raises:
        requests.HTTPError for non-2xx responses.
        ValueError if inputs invalid.
    """
    if last_event_id is None or last_event_id < 0:
        raise ValueError("last_event_id must be a non-negative integer")

    url = f"{DEFAULT_BASE_URL}/v1/poll/ack/{last_event_id}"

    resp = requests.post(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()


def reset_last_acknowledged_event(
    api_key: str,
    event_id: int,
    timeout: Union[int, float] = 15,
) -> None:
    """
    POST /v1/poll/reset/{eventId}
    Reset the last acknowledged event id to event_id to re-consume events.

    Args:
        event_id: Event id to reset the polling cursor to (use 0 to reset to the beginning).
        api_key: API key to authenticate the request.
        timeout: Requests timeout in seconds.

    Returns:
        None. Raises if not successful.

    Raises:
        requests.HTTPError for non-2xx responses.
        ValueError if inputs invalid.
    """
    if event_id is None or event_id < 0:
        raise ValueError("event_id must be a non-negative integer")

    url = f"{DEFAULT_BASE_URL}/v1/poll/reset/{event_id}"

    resp = requests.post(url, headers=_build_headers(api_key), timeout=timeout)
    resp.raise_for_status()