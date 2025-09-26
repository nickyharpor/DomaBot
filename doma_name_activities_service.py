from __future__ import annotations
from typing import Optional, Dict, Any
from caller_graphql import DomaGraphQLClient, DEFAULT_ENDPOINT
import re

__all__ = ["DomaNameActivitiesService"]


class DomaNameActivitiesService:
    """
    High-level convenience wrapper for DomaGraphQLClient focused on Name Activities.

    Provides a helper to retrieve a paginated list of activities related to a specific name (domain).
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

    def get_name_activities(
        self,
        name: str,
        *,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        _type: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get paginated list of activities related to a specific name (domain).

        Parameters:
        - name: Name (domain) to query activities for. Required.
        - skip: Number of records to skip for pagination.
        - take: Number of records to return per page (max 100).
        - _type: Optional activity type filter (NameActivityType).
        - sort_order: Optional sort order (SortOrderType: DESC or ASC).

        Returns:
        - PaginatedNameActivitiesResponse dictionary as returned by the GraphQL API.
        """
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        return self.client.query_name_activities(
            name=name,
            skip=skip,
            take=take,
            type=_type,
            sortOrder=sort_order,
        )

    @staticmethod
    def space_before_capitals(text):
        """
        Adds a space before any capital letter in a string, except for the first letter.

        Args:
            text (str): The input string (e.g., "NameClaimedEntity").

        Returns:
            str: The string with spaces added (e.g., "Name Claimed Entity").
        """
        if not text:
            return text

        # The regex finds:
        # 1. A lowercase letter ([a-z])
        # 2. Followed by a capital letter ([A-Z])
        # It replaces this match with:
        # The lowercase letter, a space (' '), and the capital letter.
        # The ( ) creates a capture group for the letters, and \1 and \2
        # reference those groups.
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
