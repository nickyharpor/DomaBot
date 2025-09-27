from __future__ import annotations

from typing import Iterable, List, Optional, Set, Dict, Any

from caller_graphql import DomaGraphQLClient, DEFAULT_ENDPOINT


__all__ = ["DomaNamesService"]


class DomaNamesService:
    """
    High-level convenience wrapper for DomaGraphQLClient focused on Names.

    Provides helper methods to retrieve domain names by owner address or by name filter,
    with optional claimStatus filtering. Internally handles pagination to return all results.
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

    def _iterate_all_names(self, *, take: int = 100, **filters: Any) -> Iterable[Dict[str, Any]]:
        """
        Internal generator to iterate all names using skip/take pagination with given filters.
        """
        if take <= 0 or take > 100:
            take = 100
        skip = 0
        while True:
            resp = self.client.query_names(skip=skip, take=take, **filters)
            items = resp.get("items", []) or []
            for it in items:
                yield it
            # Proceed to next page if any; guard against infinite loops
            has_next = bool(resp.get("hasNextPage")) and len(items) > 0
            if not has_next:
                break
            skip += take

    @staticmethod
    def _names_list(items: Iterable[Dict[str, Any]]) -> List[str]:
        """
        Extract and deduplicate name strings preserving insertion order.
        """
        seen: Set[str] = set()
        out: List[str] = []
        for it in items:
            nm = it.get("name")
            if isinstance(nm, str) and nm and nm not in seen:
                seen.add(nm)
                out.append(nm)
        return out

    def get_names_by_owner(
        self,
        owner_address_caip10: str,
        *,
        claim_status: Optional[str] = None,
        take: int = 100,
    ) -> List[str]:
        """
        Get all domain names owned by a specific CAIP-10 formatted address.

        Parameters:
        - owner_address_caip10: Wallet address in CAIP-10 format to filter by.
        - claim_status: Optional claim status filter (CLAIMED, UNCLAIMED, or ALL).
        - take: Page size (max 100). The method paginates to return all results.

        Returns:
        - List of domain name strings.
        """
        if not owner_address_caip10:
            raise ValueError("owner_address_caip10 must be a non-empty CAIP-10 address")

        filters: Dict[str, Any] = {"ownedBy": [owner_address_caip10]}
        if claim_status:
            filters["claimStatus"] = claim_status

        items_iter = self._iterate_all_names(take=take, **filters)
        return self._names_list(items_iter)

    def get_names_by_name(
        self,
        name_filter: str,
        *,
        claim_status: Optional[str] = None,
        take: int = 100,
    ) -> List[str]:
        """
        Get all domain names filtered by the provided name string.

        Parameters:
        - name_filter: Name (domain) filter string.
        - claim_status: Optional claim status filter (CLAIMED, UNCLAIMED, or ALL).
        - take: Page size (max 100). The method paginates to return all results.

        Returns:
        - List of domain name strings that match the filter.
        """
        if not name_filter:
            raise ValueError("name_filter must be a non-empty string")

        filters: Dict[str, Any] = {"name": name_filter}
        if claim_status:
            filters["claimStatus"] = claim_status

        items_iter = self._iterate_all_names(take=take, **filters)
        return self._names_list(items_iter)

    def get_name(self, name: str) -> Dict[str, Any]:
        """
        Get information about a specific tokenized (domain) name.

        Parameters:
        - name: Name (domain) to fetch information for.

        Returns:
        - NameModel dictionary as returned by the GraphQL API.
        """
        if not name:
            raise ValueError("name must be a non-empty string")
        return self.client.query_name(name)
