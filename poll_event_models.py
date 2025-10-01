from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Type, TypeVar, Union


# ---------- Shared submodels ----------

@dataclass
class DSKey:
    keyTag: int
    algorithm: int
    digestType: int
    digest: str


@dataclass
class PaymentInfo:
    price: str
    tokenAddress: str
    currencySymbol: str


@dataclass
class CommandTransaction:
    type: str
    status: str
    chainId: str
    hash: str
    signer: Optional[Dict[str, Any]] = None
    gasPrice: Optional[Dict[str, Any]] = None
    gasUsed: Optional[Dict[str, Any]] = None


@dataclass
class CommandFailureError:
    name: str
    args: str
    signature: str
    selector: str


@dataclass
class CommandFailureData:
    chainId: str
    address: Optional[Dict[str, Any]]
    methodName: Optional[Dict[str, Any]]
    methodArgs: Optional[Dict[str, Any]]
    error: Optional[CommandFailureError]
    rawError: str


# ---------- Token-related event data ----------

@dataclass
class NameTokenMintedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    owner: str
    name: str
    expiresAt: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameTokenBurnedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    owner: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None


@dataclass
class NameTokenTransferredData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    from_: str
    to: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None

    # JSON field is "from", but Python reserves it; support alias via factory usage.
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NameTokenTransferredData":
        return NameTokenTransferredData(
            type=d["type"],
            networkId=d["networkId"],
            finalized=d["finalized"],
            blockNumber=d["blockNumber"],
            tokenAddress=d["tokenAddress"],
            tokenId=d["tokenId"],
            from_=d.get("from"),
            to=d.get("to"),
            txHash=d.get("txHash"),
            logIndex=d.get("logIndex"),
        )


@dataclass
class NameTokenApprovedForAllData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    owner: str
    operator: str
    approved: bool
    txHash: Optional[str] = None
    logIndex: Optional[int] = None


@dataclass
class NameTokenTransferApprovedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    operator: str
    approvalId: int
    txHash: Optional[str] = None
    logIndex: Optional[int] = None


@dataclass
class NameTokenTransferApprovalRevokedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    operator: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None


@dataclass
class NameTokenLockStatusChangedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    isTransferLocked: bool
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameTokenRenewedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    tokenAddress: str
    tokenId: str
    expiresAt: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


# ---------- Name-related event data ----------

@dataclass
class NameTokenizedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    expiresAt: str
    nameservers: List[str]
    dsKeys: List[DSKey]
    claimedBy: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameUpdatedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    nameservers: List[str]
    dsKeys: List[DSKey]
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameRenewedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    expiresAt: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameClaimedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    claimedBy: str
    proofSource: int
    registrantHandle: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameDetokenizedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameTokenizationRequestedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    ownershipTokenChainId: str
    ownershipTokenOwnerAddress: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameTokenizationRejectedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameClaimRequestedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    claimedBy: str
    proofSource: int
    registrantHandle: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameClaimApprovedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    claimedBy: str
    proofSource: int
    registrantHandle: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


@dataclass
class NameClaimRejectedData:
    type: str
    networkId: str
    finalized: bool
    blockNumber: str
    domaRecordAddress: str
    name: str
    claimedBy: str
    proofSource: int
    registrantHandle: str
    txHash: Optional[str] = None
    logIndex: Optional[int] = None
    correlationId: Optional[str] = None


# ---------- Marketplace-related event data ----------

@dataclass
class NameTokenListedData:
    type: str
    tokenId: str
    tokenAddress: str
    orderbook: str
    orderId: str
    createdAt: str
    startsAt: str
    expiresAt: str
    seller: str
    payment: PaymentInfo
    buyer: Optional[str] = None


@dataclass
class NameTokenOfferReceivedData:
    type: str
    tokenId: str
    tokenAddress: str
    orderbook: str
    orderId: str
    createdAt: str
    expiresAt: str
    buyer: str
    seller: str
    payment: PaymentInfo


@dataclass
class NameTokenListingCancelledData:
    type: str
    tokenId: str
    tokenAddress: str
    orderbook: str
    orderId: str
    createdAt: str


@dataclass
class NameTokenOfferCancelledData:
    type: str
    tokenId: str
    tokenAddress: str
    orderbook: str
    orderId: str
    createdAt: str


@dataclass
class NameTokenPurchasedData:
    type: str
    tokenId: str
    tokenAddress: str
    orderbook: str
    orderId: str
    createdAt: str
    purchasedAt: str
    seller: str
    buyer: str
    payment: PaymentInfo
    txHash: Optional[str] = None


# ---------- Command-related event data ----------

@dataclass
class CommandCreatedData:
    type: str
    relayId: str
    transactions: List[CommandTransaction]
    failureData: Optional[CommandFailureData]


@dataclass
class CommandSucceededData:
    type: str
    relayId: str
    transactions: List[CommandTransaction]
    failureData: Optional[CommandFailureData]


@dataclass
class CommandFailedData:
    type: str
    relayId: str
    transactions: List[CommandTransaction]
    failureData: Optional[CommandFailureData]


@dataclass
class CommandUpdatedData:
    type: str
    relayId: str
    transactions: List[CommandTransaction]
    failureData: Optional[CommandFailureData]


# ---------- Union and parser ----------

EventData = Union[
    # Token-related
    NameTokenMintedData,
    NameTokenBurnedData,
    NameTokenTransferredData,
    NameTokenApprovedForAllData,
    NameTokenTransferApprovedData,
    NameTokenTransferApprovalRevokedData,
    NameTokenLockStatusChangedData,
    NameTokenRenewedData,
    # Name-related
    NameTokenizedData,
    NameUpdatedData,
    NameRenewedData,
    NameClaimedData,
    NameDetokenizedData,
    NameTokenizationRequestedData,
    NameTokenizationRejectedData,
    NameClaimRequestedData,
    NameClaimApprovedData,
    NameClaimRejectedData,
    # Marketplace
    NameTokenListedData,
    NameTokenOfferReceivedData,
    NameTokenListingCancelledData,
    NameTokenOfferCancelledData,
    NameTokenPurchasedData,
    # Command
    CommandCreatedData,
    CommandSucceededData,
    CommandFailedData,
    CommandUpdatedData,
]


_T = TypeVar("_T")


def _coerce(cls: Type[_T], d: Dict[str, Any]) -> _T:
    # Special handling for nested models
    if cls is NameTokenTransferredData:
        return NameTokenTransferredData.from_dict(d)  # type: ignore[return-value]
    if cls in (NameTokenizedData, NameUpdatedData):
        # Map dsKeys dicts to DSKey objects
        ds = [DSKey(**x) for x in d.get("dsKeys", [])]
        return cls(dsKeys=ds, **{k: v for k, v in d.items() if k != "dsKeys"})  # type: ignore[call-arg]
    if cls in (NameTokenListedData, NameTokenOfferReceivedData, NameTokenPurchasedData):
        pay = d.get("payment")
        payment = PaymentInfo(**pay) if isinstance(pay, dict) else None
        return cls(payment=payment, **{k: v for k, v in d.items() if k != "payment"})  # type: ignore[call-arg]
    if cls in (CommandCreatedData, CommandSucceededData, CommandFailedData, CommandUpdatedData):
        txs = [CommandTransaction(**t) for t in d.get("transactions", [])]
        fd = d.get("failureData")
        failure = None
        if isinstance(fd, dict):
            err_d = fd.get("error")
            err = CommandFailureError(**err_d) if isinstance(err_d, dict) else None
            failure = CommandFailureData(
                chainId=fd.get("chainId"),
                address=fd.get("address"),
                methodName=fd.get("methodName"),
                methodArgs=fd.get("methodArgs"),
                error=err,
                rawError=fd.get("rawError"),
            )
        return cls(transactions=txs, failureData=failure, **{k: v for k, v in d.items() if k not in ("transactions", "failureData")})  # type: ignore[call-arg]
    # Default simple construction
    return cls(**d)  # type: ignore[call-arg]


EVENT_DATA_CLASS_BY_TYPE: Dict[str, Type[EventData]] = {
    # Token-related
    "NAME_TOKEN_MINTED": NameTokenMintedData,
    "NAME_TOKEN_BURNED": NameTokenBurnedData,
    "NAME_TOKEN_TRANSFERRED": NameTokenTransferredData,
    "NAME_TOKEN_APPROVED_FOR_ALL": NameTokenApprovedForAllData,
    "NAME_TOKEN_TRANSFER_APPROVED": NameTokenTransferApprovedData,
    "NAME_TOKEN_TRANSFER_APPROVAL_REVOKED": NameTokenTransferApprovalRevokedData,
    "NAME_TOKEN_LOCK_STATUS_CHANGED": NameTokenLockStatusChangedData,
    "NAME_TOKEN_RENEWED": NameTokenRenewedData,
    # Name-related
    "NAME_TOKENIZED": NameTokenizedData,
    "NAME_UPDATED": NameUpdatedData,
    "NAME_RENEWED": NameRenewedData,
    "NAME_CLAIMED": NameClaimedData,
    "NAME_DETOKENIZED": NameDetokenizedData,
    "NAME_TOKENIZATION_REQUESTED": NameTokenizationRequestedData,
    "NAME_TOKENIZATION_REJECTED": NameTokenizationRejectedData,
    "NAME_CLAIM_REQUESTED": NameClaimRequestedData,
    "NAME_CLAIM_APPROVED": NameClaimApprovedData,
    "NAME_CLAIM_REJECTED": NameClaimRejectedData,
    # Marketplace
    "NAME_TOKEN_LISTED": NameTokenListedData,
    "NAME_TOKEN_OFFER_RECEIVED": NameTokenOfferReceivedData,
    "NAME_TOKEN_LISTING_CANCELLED": NameTokenListingCancelledData,
    "NAME_TOKEN_OFFER_CANCELLED": NameTokenOfferCancelledData,
    "NAME_TOKEN_PURCHASED": NameTokenPurchasedData,
    # Command-related
    "COMMAND_CREATED": CommandCreatedData,
    "COMMAND_SUCCEEDED": CommandSucceededData,
    "COMMAND_FAILED": CommandFailedData,
    "COMMAND_UPDATED": CommandUpdatedData,
}


def parse_event_data(event_type: str, payload: Dict[str, Any]):
    """
    Parse an eventData payload into a strongly-typed dataclass instance.

    Parameters:
      - event_type: Poll API event type string (e.g., 'NAME_TOKENIZED', 'COMMAND_FAILED', etc.)
      - payload: eventData object from the Poll API response

    Returns:
      - An instance of the corresponding dataclass model.
    """
    try:
        cls = EVENT_DATA_CLASS_BY_TYPE[event_type]
        return _coerce(cls, payload)
    except:
        return None


def dataclass_to_string(data_instance) -> str:
    data_dict = asdict(data_instance)
    output_lines = []
    for field_name, value in data_dict.items():
        if isinstance(value, list):
            display_value = f"{value}"
        elif isinstance(value, dict) and 'message' in value:
            display_value = f"{value.get('message')}"
        else:
            display_value = value

        output_lines.append(f"{field_name}: `{display_value}`")

    # 3. Join the lines with a newline character.
    return "\n".join(output_lines)


__all__ = [
    # Shared
    "DSKey",
    "PaymentInfo",
    "CommandTransaction",
    "CommandFailureError",
    "CommandFailureData",
    # Token-related
    "NameTokenMintedData",
    "NameTokenBurnedData",
    "NameTokenTransferredData",
    "NameTokenApprovedForAllData",
    "NameTokenTransferApprovedData",
    "NameTokenTransferApprovalRevokedData",
    "NameTokenLockStatusChangedData",
    "NameTokenRenewedData",
    # Name-related
    "NameTokenizedData",
    "NameUpdatedData",
    "NameRenewedData",
    "NameClaimedData",
    "NameDetokenizedData",
    "NameTokenizationRequestedData",
    "NameTokenizationRejectedData",
    "NameClaimRequestedData",
    "NameClaimApprovedData",
    "NameClaimRejectedData",
    # Marketplace
    "NameTokenListedData",
    "NameTokenOfferReceivedData",
    "NameTokenListingCancelledData",
    "NameTokenOfferCancelledData",
    "NameTokenPurchasedData",
    # Command-related
    "CommandCreatedData",
    "CommandSucceededData",
    "CommandFailedData",
    "CommandUpdatedData",
    # Union and helpers
    "EventData",
    "EVENT_DATA_CLASS_BY_TYPE",
    "parse_event_data",
    "dataclass_to_string",
]
