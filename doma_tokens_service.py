from __future__ import annotations

from typing import Optional, Dict, Any

from caller_graphql import DomaGraphQLClient, DEFAULT_ENDPOINT


__all__ = ["DomaTokensService"]


class DomaTokensService:
    """
    High-level convenience wrapper for DomaGraphQLClient focused on Tokens.

    Provides a helper to retrieve a paginated list of tokens for a specific name (domain).
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

    def get_tokens(
        self,
        name: str,
        *,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get paginated list of tokens for a specific name (domain).

        Parameters:
        - name: Name (domain) to query tokens for. Required.
        - skip: Number of records to skip for pagination.
        - take: Number of records to return per page (max 100).

        Returns:
        - PaginatedTokensResponse dictionary as returned by the GraphQL API.
        """
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        return self.client.query_tokens(name=name, skip=skip, take=take)

    def get_token(self, token_id: str) -> Dict[str, Any]:
        """
        Get information about a specific token by its ID.

        Parameters:
        - token_id: Token id to fetch information for.

        Returns:
        - TokenModel dictionary as returned by the GraphQL API.
        """
        if not token_id or not isinstance(token_id, str):
            raise ValueError("token_id must be a non-empty string")
        return self.client.query_token(token_id)
