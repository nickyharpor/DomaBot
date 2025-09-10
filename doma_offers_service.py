from __future__ import annotations

from typing import Optional, List, Dict, Any

from caller_graphql import DomaGraphQLClient, DEFAULT_ENDPOINT

__all__ = ["DomaOffersService"]


class DomaOffersService:
    """
    High-level convenience wrapper for DomaGraphQLClient focused on Name Offers.

    Provides a helper to retrieve a paginated list of offers for tokenized names, with optional filters.
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

    def get_offers(
        self,
        *,
        token_id: Optional[str] = None,
        offered_by: Optional[List[str]] = None,
        skip: Optional[float] = None,
        take: Optional[float] = None,
        status: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get paginated list of offers for tokenized names, with optional filters.

        Parameters:
        - token_id: Token ID to query offers for.
        - offered_by: Filter by offerer addresses (CAIP-10 format).
        - skip: Number of records to skip for pagination.
        - take: Number of records to return per page (max 100).
        - status: Offer status filter (OfferStatus: ACTIVE, EXPIRED, All).
        - sort_order: Sort order (SortOrderType: DESC or ASC).

        Returns:
        - PaginatedNameOffersResponse dictionary as returned by the GraphQL API.
        """
        return self.client.query_offers(
            tokenId=token_id,
            offeredBy=offered_by,
            skip=skip,
            take=take,
            status=status,
            sortOrder=sort_order,
        )
