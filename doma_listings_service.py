from __future__ import annotations

from typing import Optional, List, Dict, Any

from caller_graphql import DomaGraphQLClient, DEFAULT_ENDPOINT

__all__ = ["DomaListingsService"]


class DomaListingsService:
    """
    High-level convenience wrapper for DomaGraphQLClient focused on Name Listings.

    Provides a helper to retrieve a paginated list of "Buy Now" secondary sale listings for tokenized names,
    with optional filters.
    """

    def __init__(
        self,
        client: Optional[DomaGraphQLClient] = None,
        *,
        endpoint: str = DEFAULT_ENDPOINT,
        api_key: Optional[str] = None,
        headers: Optional[dict] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the service.

        You can provide an existing DomaGraphQLClient via 'client', or allow the service
        to construct one by passing endpoint/api_key/headers/timeout.
        """
        if client is not None:
            self.client = client
        else:
            self.client = DomaGraphQLClient(endpoint=endpoint, headers=headers, timeout=timeout, api_key=api_key)

    def get_listings(
        self,
        *,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        tlds: Optional[List[str]] = None,
        created_since: Optional[str] = None,
        sld: Optional[str] = None,
        network_ids: Optional[List[str]] = None,
        registrar_iana_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Get paginated list of "Buy Now" secondary sale listings for tokenized names, with optional filters.

        Parameters:
        - skip: Number of records to skip for pagination.
        - take: Number of records to return per page (max 100).
        - tlds: Filter by TLDs.
        - created_since: Filter listings created since this date (ISO8601 string).
        - sld: Second-level domain (SLD) name filter.
        - network_ids: Filter by network IDs (CAIP-2 format).
        - registrar_iana_ids: Filter by registrar IANA IDs.

        Returns:
        - PaginatedNameListingsResponse dictionary as returned by the GraphQL API.
        """
        return self.client.query_listings(
            skip=skip,
            take=take,
            tlds=tlds,
            createdSince=created_since,
            sld=sld,
            networkIds=network_ids,
            registrarIanaIds=registrar_iana_ids,
        )
