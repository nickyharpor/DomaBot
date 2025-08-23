import json
import typing as t
from urllib import request, error

DEFAULT_ENDPOINT = "https://api-testnet.doma.xyz/graphql"


class GraphQLClientError(Exception):
    """Raised when the GraphQL API responds with errors."""

    def __init__(self, message: str, errors: t.Optional[t.List[dict]] = None, status: t.Optional[int] = None):
        super().__init__(message)
        self.errors = errors or []
        self.status = status

    def __str__(self) -> str:
        base = super().__str__()
        if self.status:
            base = f"[HTTP {self.status}] {base}"
        if self.errors:
            return f"{base} | GraphQL errors: {self.errors}"
        return base


def _filter_none(d: t.Mapping[str, t.Any]) -> dict:
    """Return a new dict without None values."""
    return {k: v for k, v in d.items() if v is not None}


class DomaGraphQLClient:
    """
    Minimal GraphQL client for Doma Multi-Chain Subgraph.

    Usage example:
        client = DomaGraphQLClient()  # uses testnet endpoint by default
        resp = client.query_names(tlds=["com"], take=10)
    """

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        headers: t.Optional[dict] = None,
        timeout: float = 30.0,
        api_key: t.Optional[str] = None,
    ):
        self.endpoint = endpoint
        self.headers = headers or {}
        if api_key and "Authorization" not in self.headers and "X-API-Key" not in self.headers and "x-api-key" not in self.headers:
            # Add API key header if caller didn't already provide auth headers
            self.headers["X-API-Key"] = api_key
        self.timeout = timeout

    def _execute(self, query: str, variables: t.Optional[dict] = None, operation_name: t.Optional[str] = None) -> dict:
        payload: dict = {"query": query, "variables": variables or {}}
        if operation_name:
            payload["operationName"] = operation_name

        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        headers.update(self.headers or {})

        req = request.Request(self.endpoint, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
        except error.HTTPError as e:
            detail = e.read().decode("utf-8") if e.fp else ""
            try:
                parsed = json.loads(detail)
            except Exception:
                parsed = None
            raise GraphQLClientError(
                f"HTTP error from GraphQL endpoint: {e.reason}",
                errors=(parsed.get("errors") if isinstance(parsed, dict) else None),
                status=e.code,
            ) from None
        except error.URLError as e:
            raise GraphQLClientError(f"Network error calling GraphQL endpoint: {e.reason}") from None
        except json.JSONDecodeError as e:
            raise GraphQLClientError(f"Failed to decode GraphQL response as JSON: {e}") from None

        if not isinstance(data, dict):
            raise GraphQLClientError("Unexpected GraphQL response format (not a JSON object).")

        if "errors" in data and data["errors"]:
            raise GraphQLClientError("GraphQL responded with errors.", errors=data["errors"])

        if "data" not in data:
            raise GraphQLClientError("GraphQL response missing 'data' field.")

        return data["data"]

    # 1) names
    def query_names(
        self,
        skip: t.Optional[int] = None,
        take: t.Optional[int] = None,
        ownedBy: t.Optional[t.List[str]] = None,
        claimStatus: t.Optional[str] = None,
        name: t.Optional[str] = None,
        networkIds: t.Optional[t.List[str]] = None,
        registrarIanaIds: t.Optional[t.List[int]] = None,
        tlds: t.Optional[t.List[str]] = None,
        sortOrder: t.Optional[str] = None,
    ) -> dict:
        query = """
        query Names(
          $skip: Int
          $take: Int
          $ownedBy: [AddressCAIP10!]
          $claimStatus: NamesQueryClaimStatus
          $name: String
          $networkIds: [String!]
          $registrarIanaIds: [Int!]
          $tlds: [String!]
          $sortOrder: SortOrderType
        ) {
          names(
            skip: $skip
            take: $take
            ownedBy: $ownedBy
            claimStatus: $claimStatus
            name: $name
            networkIds: $networkIds
            registrarIanaIds: $registrarIanaIds
            tlds: $tlds
            sortOrder: $sortOrder
          ) {
            items {
              name
              expiresAt
              tokenizedAt
              eoi
              registrar {
                name
                ianaId
                publicKeys
                websiteUrl
                supportEmail
              }
              nameservers {
                ldhName
              }
              dsKeys {
                keyTag
                algorithm
                digest
                digestType
              }
              transferLock
              claimedBy
              tokens {
                tokenId
                networkId
                ownerAddress
                type
                startsAt
                expiresAt
                explorerUrl
                tokenAddress
                createdAt
                chain {
                  name
                  networkId
                }
                listings {
                  id
                  externalId
                  price
                  offererAddress
                  orderbook
                  currency {
                    name
                    symbol
                    decimals
                  }
                  expiresAt
                  createdAt
                  updatedAt
                }
                openseaCollectionSlug
              }
              activities {
                __typename
                ... on NameClaimedActivity {
                  type
                  txHash
                  sld
                  tld
                  createdAt
                  claimedBy
                }
                ... on NameRenewedActivity {
                  type
                  txHash
                  sld
                  tld
                  createdAt
                  expiresAt
                }
                ... on NameDetokenizedActivity {
                  type
                  txHash
                  sld
                  tld
                  createdAt
                  networkId
                }
                ... on NameTokenizedActivity {
                  type
                  txHash
                  sld
                  tld
                  createdAt
                  networkId
                }
              }
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(
            dict(
                skip=skip,
                take=take,
                ownedBy=ownedBy,
                claimStatus=claimStatus,
                name=name,
                networkIds=networkIds,
                registrarIanaIds=registrarIanaIds,
                tlds=tlds,
                sortOrder=sortOrder,
            )
        )
        data = self._execute(query, variables, operation_name="Names")
        return data["names"]

    # 2) name
    def query_name(self, name: str) -> dict:
        query = """
        query Name($name: String!) {
          name(name: $name) {
            name
            expiresAt
            tokenizedAt
            eoi
            registrar {
              name
              ianaId
              publicKeys
              websiteUrl
              supportEmail
            }
            nameservers {
              ldhName
            }
            dsKeys {
              keyTag
              algorithm
              digest
              digestType
            }
            transferLock
            claimedBy
            tokens {
              tokenId
              networkId
              ownerAddress
              type
              startsAt
              expiresAt
              explorerUrl
              tokenAddress
              createdAt
              chain {
                name
                networkId
              }
              listings {
                id
                externalId
                price
                offererAddress
                orderbook
                currency {
                  name
                  symbol
                  decimals
                }
                expiresAt
                createdAt
                updatedAt
              }
              openseaCollectionSlug
            }
            activities {
              __typename
              ... on NameClaimedActivity {
                type
                txHash
                sld
                tld
                createdAt
                claimedBy
              }
              ... on NameRenewedActivity {
                type
                txHash
                sld
                tld
                createdAt
                expiresAt
              }
              ... on NameDetokenizedActivity {
                type
                txHash
                sld
                tld
                createdAt
                networkId
              }
              ... on NameTokenizedActivity {
                type
                txHash
                sld
                tld
                createdAt
                networkId
              }
            }
          }
        }
        """
        data = self._execute(query, {"name": name}, operation_name="Name")
        return data["name"]

    # 3) tokens
    def query_tokens(self, name: str, skip: t.Optional[int] = None, take: t.Optional[int] = None) -> dict:
        query = """
        query Tokens($name: String!, $skip: Int, $take: Int) {
          tokens(name: $name, skip: $skip, take: $take) {
            items {
              tokenId
              networkId
              ownerAddress
              type
              startsAt
              expiresAt
              activities {
                __typename
                ... on TokenMintedActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                }
                ... on TokenTransferredActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  transferredTo
                  transferredFrom
                }
                ... on TokenListedActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  orderId
                  startsAt
                  expiresAt
                  seller
                  buyer
                  payment {
                    price
                    tokenAddress
                    currencySymbol
                  }
                  orderbook
                }
                ... on TokenOfferReceivedActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  orderId
                  expiresAt
                  buyer
                  seller
                  payment {
                    price
                    tokenAddress
                    currencySymbol
                  }
                  orderbook
                }
                ... on TokenListingCancelledActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  orderId
                  reason
                  orderbook
                }
                ... on TokenOfferCancelledActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  orderId
                  reason
                  orderbook
                }
                ... on TokenPurchasedActivity {
                  type
                  networkId
                  txHash
                  finalized
                  tokenId
                  createdAt
                  orderId
                  purchasedAt
                  seller
                  buyer
                  payment {
                    price
                    tokenAddress
                    currencySymbol
                  }
                  orderbook
                }
              }
              explorerUrl
              tokenAddress
              createdAt
              chain {
                name
                networkId
              }
              listings {
                id
                externalId
                price
                offererAddress
                orderbook
                currency {
                  name
                  symbol
                  decimals
                }
                expiresAt
                createdAt
                updatedAt
              }
              openseaCollectionSlug
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(dict(name=name, skip=skip, take=take))
        data = self._execute(query, variables, operation_name="Tokens")
        return data["tokens"]

    # 4) token
    def query_token(self, tokenId: str) -> dict:
        query = """
        query Token($tokenId: String!) {
          token(tokenId: $tokenId) {
            tokenId
            networkId
            ownerAddress
            type
            startsAt
            expiresAt
            activities {
              __typename
              ... on TokenMintedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
              }
              ... on TokenTransferredActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                transferredTo
                transferredFrom
              }
              ... on TokenListedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                startsAt
                expiresAt
                seller
                buyer
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
              ... on TokenOfferReceivedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                expiresAt
                buyer
                seller
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
              ... on TokenListingCancelledActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                reason
                orderbook
              }
              ... on TokenOfferCancelledActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                reason
                orderbook
              }
              ... on TokenPurchasedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                purchasedAt
                seller
                buyer
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
            }
            explorerUrl
            tokenAddress
            createdAt
            chain {
              name
              networkId
            }
            listings {
              id
              externalId
              price
              offererAddress
              orderbook
              currency {
                name
                symbol
                decimals
              }
              expiresAt
              createdAt
              updatedAt
            }
            openseaCollectionSlug
          }
        }
        """
        data = self._execute(query, {"tokenId": tokenId}, operation_name="Token")
        return data["token"]

    # 5) command
    def query_command(self, correlationId: str) -> dict:
        query = """
        query Command($correlationId: String!) {
          command(correlationId: $correlationId) {
            type
            status
            source
            serverCommandId
            clientCommandId
            failureReason
            registrar {
              name
              ianaId
              publicKeys
              websiteUrl
              supportEmail
            }
            createdAt
            updatedAt
          }
        }
        """
        data = self._execute(query, {"correlationId": correlationId}, operation_name="Command")
        return data["command"]

    # 6) nameActivities
    def query_name_activities(
        self,
        name: str,
        skip: t.Optional[float] = None,
        take: t.Optional[float] = None,
        type: t.Optional[str] = None,
        sortOrder: t.Optional[str] = None,
    ) -> dict:
        query = """
        query NameActivities(
          $name: String!
          $skip: Float
          $take: Float
          $type: NameActivityType
          $sortOrder: SortOrderType
        ) {
          nameActivities(
            name: $name
            skip: $skip
            take: $take
            type: $type
            sortOrder: $sortOrder
          ) {
            items {
              __typename
              ... on NameClaimedActivity {
                type
                txHash
                sld
                tld
                createdAt
                claimedBy
              }
              ... on NameRenewedActivity {
                type
                txHash
                sld
                tld
                createdAt
                expiresAt
              }
              ... on NameDetokenizedActivity {
                type
                txHash
                sld
                tld
                createdAt
                networkId
              }
              ... on NameTokenizedActivity {
                type
                txHash
                sld
                tld
                createdAt
                networkId
              }
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(dict(name=name, skip=skip, take=take, type=type, sortOrder=sortOrder))
        data = self._execute(query, variables, operation_name="NameActivities")
        return data["nameActivities"]

    # 7) tokenActivities
    def query_token_activities(
        self,
        tokenId: str,
        skip: t.Optional[float] = None,
        take: t.Optional[float] = None,
        type: t.Optional[str] = None,
        sortOrder: t.Optional[str] = None,
    ) -> dict:
        query = """
        query TokenActivities(
          $tokenId: String!
          $skip: Float
          $take: Float
          $type: TokenActivityType
          $sortOrder: SortOrderType
        ) {
          tokenActivities(
            tokenId: $tokenId
            skip: $skip
            take: $take
            type: $type
            sortOrder: $sortOrder
          ) {
            items {
              __typename
              ... on TokenMintedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
              }
              ... on TokenTransferredActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                transferredTo
                transferredFrom
              }
              ... on TokenListedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                startsAt
                expiresAt
                seller
                buyer
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
              ... on TokenOfferReceivedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                expiresAt
                buyer
                seller
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
              ... on TokenListingCancelledActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                reason
                orderbook
              }
              ... on TokenOfferCancelledActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                reason
                orderbook
              }
              ... on TokenPurchasedActivity {
                type
                networkId
                txHash
                finalized
                tokenId
                createdAt
                orderId
                purchasedAt
                seller
                buyer
                payment {
                  price
                  tokenAddress
                  currencySymbol
                }
                orderbook
              }
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(dict(tokenId=tokenId, skip=skip, take=take, type=type, sortOrder=sortOrder))
        data = self._execute(query, variables, operation_name="TokenActivities")
        return data["tokenActivities"]

    # 8) listings
    def query_listings(
        self,
        skip: t.Optional[float] = None,
        take: t.Optional[float] = None,
        tlds: t.Optional[t.List[str]] = None,
        createdSince: t.Optional[str] = None,
        sld: t.Optional[str] = None,
        networkIds: t.Optional[t.List[str]] = None,
        registrarIanaIds: t.Optional[t.List[int]] = None,
    ) -> dict:
        query = """
        query Listings(
          $skip: Float
          $take: Float
          $tlds: [String!]
          $createdSince: DateTime
          $sld: String
          $networkIds: [String!]
          $registrarIanaIds: [Int!]
        ) {
          listings(
            skip: $skip
            take: $take
            tlds: $tlds
            createdSince: $createdSince
            sld: $sld
            networkIds: $networkIds
            registrarIanaIds: $registrarIanaIds
          ) {
            items {
              id
              externalId
              price
              offererAddress
              orderbook
              currency {
                name
                symbol
                decimals
              }
              expiresAt
              createdAt
              updatedAt
              name
              nameExpiresAt
              registrar {
                name
                ianaId
                publicKeys
                websiteUrl
                supportEmail
              }
              tokenId
              tokenAddress
              chain {
                name
                networkId
              }
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(
            dict(
                skip=skip,
                take=take,
                tlds=tlds,
                createdSince=createdSince,
                sld=sld,
                networkIds=networkIds,
                registrarIanaIds=registrarIanaIds,
            )
        )
        data = self._execute(query, variables, operation_name="Listings")
        return data["listings"]

    # 9) offers
    def query_offers(
        self,
        tokenId: t.Optional[str] = None,
        offeredBy: t.Optional[t.List[str]] = None,
        skip: t.Optional[float] = None,
        take: t.Optional[float] = None,
        status: t.Optional[str] = None,
        sortOrder: t.Optional[str] = None,
    ) -> dict:
        query = """
        query Offers(
          $tokenId: String
          $offeredBy: [AddressCAIP10!]
          $skip: Float
          $take: Float
          $status: OfferStatus
          $sortOrder: SortOrderType
        ) {
          offers(
            tokenId: $tokenId
            offeredBy: $offeredBy
            skip: $skip
            take: $take
            status: $status
            sortOrder: $sortOrder
          ) {
            items {
              id
              externalId
              price
              offererAddress
              orderbook
              currency {
                name
                symbol
                decimals
              }
              expiresAt
              createdAt
              name
              nameExpiresAt
              registrar {
                name
                ianaId
                publicKeys
                websiteUrl
                supportEmail
              }
              tokenId
              tokenAddress
              chain {
                name
                networkId
              }
            }
            totalCount
            pageSize
            currentPage
            totalPages
            hasPreviousPage
            hasNextPage
          }
        }
        """
        variables = _filter_none(
            dict(
                tokenId=tokenId,
                offeredBy=offeredBy,
                skip=skip,
                take=take,
                status=status,
                sortOrder=sortOrder,
            )
        )
        data = self._execute(query, variables, operation_name="Offers")
        return data["offers"]

    # 10) nameStatistics
    def query_name_statistics(self, tokenId: str) -> dict:
        query = """
        query NameStatistics($tokenId: String!) {
          nameStatistics(tokenId: $tokenId) {
            name
            highestOffer {
              id
              externalId
              price
              offererAddress
              orderbook
              currency {
                name
                symbol
                decimals
              }
              expiresAt
              createdAt
            }
            activeOffers
            offersLast3Days
          }
        }
        """
        data = self._execute(query, {"tokenId": tokenId}, operation_name="NameStatistics")
        return data["nameStatistics"]


__all__ = [
    "DomaGraphQLClient",
    "GraphQLClientError",
    "DEFAULT_ENDPOINT",
]