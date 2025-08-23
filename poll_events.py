from typing import Optional, Dict, Any


__all__ = ["describe_event_type"]


def _get_event_data(event: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Accept either:
      - full poll event with 'eventData' and top-level fields like 'name', 'tokenId', 'relayId'
      - or the eventData payload itself
    and return a merged view that the describer can use.
    """
    if not event:
        return {}
    if "eventData" in event and isinstance(event["eventData"], dict):
        # Merge top-level convenience fields (name, tokenId, relayId) so they can be used in descriptions
        merged = dict(event["eventData"])
        for k in ("name", "tokenId", "relayId"):
            if k in event and k not in merged:
                merged[k] = event[k]
        return merged
    return dict(event)


def _fmt_price(data: Dict[str, Any]) -> Optional[str]:
    price = data.get("payment", {}).get("price") if isinstance(data.get("payment"), dict) else data.get("amount")
    symbol = data.get("payment", {}).get("currencySymbol") if isinstance(data.get("payment"), dict) else data.get("currencySymbol")
    if price is None and symbol is None:
        return None
    if symbol:
        return f"{price} {symbol}"
    return str(price) if price is not None else None


def describe_event_type(event_type: str, event: Optional[Dict[str, Any]] = None) -> str:
    """
    Return a human-friendly description string for the given Poll API event type.

    Parameters:
    - event_type: One of the Poll API event types (e.g. 'NAME_TOKENIZED', 'COMMAND_FAILED', etc.).
    - event: Optional event object. Can be either the full poll event (with 'eventData')
             or the 'eventData' object itself. When provided, the description includes more context.

    Returns:
    - A user-friendly description string.
    """
    data = _get_event_data(event)

    # Common fields we might use
    name = data.get("name")
    token_id = data.get("tokenId")
    token_addr = data.get("tokenAddress")
    network_id = data.get("networkId")
    expires_at = data.get("expiresAt")
    tx_hash = data.get("txHash")
    orderbook = data.get("orderbook")
    order_id = data.get("orderId")
    buyer = data.get("buyer")
    seller = data.get("seller")
    owner = data.get("owner")
    claimed_by = data.get("claimedBy")
    from_addr = data.get("from")
    to_addr = data.get("to")
    operator = data.get("operator")
    approved = data.get("approved")
    is_locked = data.get("isTransferLocked")
    price_s = _fmt_price(data)
    relay_id = data.get("relayId")

    et = event_type or ""
    # Name lifecycle and management
    if et == "NAME_TOKENIZATION_REQUESTED":
        return f"Tokenization requested for {name or 'a name'} on {data.get('ownershipTokenChainId') or network_id} by {data.get('ownershipTokenOwnerAddress') or 'an address'}."
    if et == "NAME_TOKENIZATION_REJECTED":
        return f"Tokenization request rejected for {name or 'a name'}."
    if et == "NAME_TOKENIZED":
        suffix = f", expires at {expires_at}" if expires_at else ""
        net = f" on {network_id}" if network_id else ""
        return f"Name {name or 'N/A'} tokenized{net}{suffix}."
    if et == "NAME_UPDATED":
        return f"Name {name or 'N/A'} records updated (nameservers and/or DNSSEC DS keys)."
    if et == "NAME_RENEWED":
        suffix = f" until {expires_at}" if expires_at else ""
        return f"Name {name or 'N/A'} renewed{suffix}."
    if et == "NAME_CLAIMED":
        return f"Name {name or 'N/A'} claimed by {claimed_by or 'a wallet'}."
    if et == "NAME_CLAIM_REQUESTED":
        return f"Claim requested for {name or 'N/A'} by {claimed_by or 'a wallet'}."
    if et == "NAME_CLAIM_REJECTED":
        return f"Claim rejected for {name or 'N/A'}."
    if et == "NAME_CLAIM_APPROVED":
        return f"Claim approved for {name or 'N/A'}."
    if et == "NAME_DETOKENIZED":
        return f"Name {name or 'N/A'} detokenized."

    # Token lifecycle and approvals
    if et == "NAME_TOKEN_MINTED":
        parts = []
        if token_id:
            parts.append(f"token {token_id}")
        else:
            parts.append("a token")
        if owner:
            parts.append(f"minted to {owner}")
        else:
            parts.append("minted")
        if name:
            parts.append(f"for {name}")
        if network_id:
            parts.append(f"on {network_id}")
        return " ".join(parts) + "."
    if et == "NAME_TOKEN_TRANSFERRED":
        return f"Token {token_id or ''} transferred from {from_addr or 'N/A'} to {to_addr or 'N/A'}."
    if et == "NAME_TOKEN_RENEWED":
        suffix = f" until {expires_at}" if expires_at else ""
        return f"Token {token_id or ''} renewed{suffix}."
    if et == "NAME_TOKEN_BURNED":
        return f"Token {token_id or ''} burned by {owner or 'owner'}."
    if et == "NAME_TOKEN_APPROVED_FOR_ALL":
        status = "granted" if approved else "revoked"
        return f"Operator {operator or 'N/A'} {status} approval for all tokens by {owner or 'owner'}."
    if et == "NAME_TOKEN_TRANSFER_APPROVED":
        return f"Transfer approved to {operator or 'N/A'} for token {token_id or ''} (approvalId={data.get('approvalId')})."
    if et == "NAME_TOKEN_TRANSFER_APPROVAL_REVOKED":
        return f"Transfer approval revoked for {operator or 'N/A'} on token {token_id or ''}."
    if et == "NAME_TOKEN_LOCK_STATUS_CHANGED":
        return f"Transfer lock for token {token_id or ''} set to {is_locked!r}."

    # Payments and marketplace
    if et == "PAYMENT_FULFILLED":
        amount = price_s or "a payment"
        return f"Payment fulfilled by {buyer or 'a buyer'} for {amount}."
    if et == "NAME_TOKEN_LISTED":
        price = price_s or "a price"
        ob = f" on {orderbook}" if orderbook else ""
        exp = f" (expires {expires_at})" if expires_at else ""
        return f"Token {token_id or ''} listed by {seller or 'seller'} for {price}{ob}{exp} (order {order_id or 'N/A'})."
    if et == "NAME_TOKEN_OFFER_RECEIVED":
        price = price_s or "an offer"
        ob = f" on {orderbook}" if orderbook else ""
        exp = f" (expires {expires_at})" if expires_at else ""
        return f"Offer received by {seller or 'seller'} from {buyer or 'buyer'} for {price}{ob}{exp} (order {order_id or 'N/A'})."
    if et == "NAME_TOKEN_LISTING_CANCELLED":
        ob = f" on {orderbook}" if orderbook else ""
        return f"Listing {order_id or 'N/A'} for token {token_id or ''} cancelled{ob}."
    if et == "NAME_TOKEN_OFFER_CANCELLED":
        ob = f" on {orderbook}" if orderbook else ""
        return f"Offer {order_id or 'N/A'} for token {token_id or ''} cancelled{ob}."
    if et == "NAME_TOKEN_PURCHASED":
        price = price_s or "a price"
        ob = f" on {orderbook}" if orderbook else ""
        return f"Token {token_id or ''} purchased by {buyer or 'buyer'} from {seller or 'seller'} for {price}{ob}."

    # Command lifecycle
    if et == "COMMAND_CREATED":
        rid = relay_id or data.get("clientCommandId") or data.get("serverCommandId")
        return f"Command created (relayId={rid or 'N/A'})."
    if et == "COMMAND_SUCCEEDED":
        rid = relay_id or data.get("clientCommandId") or data.get("serverCommandId")
        return f"Command succeeded (relayId={rid or 'N/A'})."
    if et == "COMMAND_FAILED":
        rid = relay_id or data.get("clientCommandId") or data.get("serverCommandId")
        return f"Command failed (relayId={rid or 'N/A'})."
    if et == "COMMAND_UPDATED":
        rid = relay_id or data.get("clientCommandId") or data.get("serverCommandId")
        return f"Command updated (relayId={rid or 'N/A'})."

    # Fallback
    suffix = f" (tx {tx_hash})" if tx_hash else ""
    target = name or token_id or token_addr or network_id or "event"
    return f"{et.replace('_', ' ').title()} occurred for {target}{suffix}."
