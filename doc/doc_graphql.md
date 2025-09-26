# Doma Multi-Chain Subgraph

Doma Subgraph could be used to get consolidated data about names tokenized on Doma Protocol. This data includes information about names, name tokens, and associated activities. Also, it includes aggregated marketplaces offers and listing information.

Endpoints:

* Testnet: [https://api-testnet.doma.xyz/graphql](https://api-testnet.doma.xyz/graphql)
* Mainnet: _Coming soon..._

## Queries

### `names`

Get paginated list of tokenized names, with optional filters and sorting.

| Argument           | Type                                                   | Description                                          |
| ------------------ | ------------------------------------------------------ | ---------------------------------------------------- |
| `skip`             | `Int`                                                  | Number of records to skip for pagination.            |
| `take`             | `Int`                                                  | Number of records to return per page (max 100).      |
| `ownedBy`          | `[AddressCAIP10!]`                                     | Filter by owner addresses (CAIP-10 format).          |
| `claimStatus`      | [`NamesQueryClaimStatus`](#type-namesqueryclaimstatus) | Filter by claim status (CLAIMED, UNCLAIMED, or ALL). |
| `name`             | `String`                                               | Filter by name (domain).                             |
| `networkIds`       | `[String!]`                                            | Filter by network IDs (CAIP-2 format).               |
| `registrarIanaIds` | `[Int!]`                                               | Filter by registrar IANA IDs.                        |
| `tlds`             | `[String!]`                                            | Filter by TLDs.                                      |
| `sortOrder`        | [`SortOrderType`](#type-sortordertype)                 | Sort order for names (DESC or ASC). Default is DESC. |

**Returns:** [`PaginatedNamesResponse!`](#type-paginatednamesresponse)

### `name`

Get information about a specific tokenized name.

| Argument | Type      | Description                |
| -------- | --------- | -------------------------- |
| `name`   | `String!` | Name to fetch information. |

**Returns:** [`NameModel!`](#type-namemodel)

### `tokens`

Get paginated list of tokens, with optional filters and sorting.

| Argument | Type      | Description                                     |
| -------- | --------- | ----------------------------------------------- |
| `skip`   | `Int`     | Number of records to skip for pagination.       |
| `take`   | `Int`     | Number of records to return per page (max 100). |
| `name`   | `String!` | Name (domain) to query tokens for.              |

**Returns:** [`PaginatedTokensResponse!`](#type-paginatedtokensresponse)

### `token`

Get information about a specific token by its ID.

| Argument  | Type      | Description                    |
| --------- | --------- | ------------------------------ |
| `tokenId` | `String!` | Token id to fetch information. |

**Returns:** [`TokenModel!`](#type-tokenmodel)

### `command`

Get information about a specific command by its correlation ID. Useful to track status of client-initiated operations (e.g. bridging a name).

| Argument        | Type      | Description                                          |
| --------------- | --------- | ---------------------------------------------------- |
| `correlationId` | `String!` | Command correlation (relay) id to fetch information. |

**Returns:** [`CommandModel!`](#type-commandmodel)

### `nameActivities`

Get paginated list of activities related to a specific name.

| Argument    | Type                                         | Description                                               |
| ----------- | -------------------------------------------- | --------------------------------------------------------- |
| `name`      | `String!`                                    | Name (domain) to query activities for.                    |
| `skip`      | `Float`                                      | Number of records to skip for pagination.                 |
| `take`      | `Float`                                      | Number of records to return per page (max 100).           |
| `type`      | [`NameActivityType`](#type-nameactivitytype) | Filter by activity type.                                  |
| `sortOrder` | [`SortOrderType`](#type-sortordertype)       | Sort order for activities (DESC or ASC). Default is DESC. |

**Returns:** [`PaginatedNameActivitiesResponse!`](#type-paginatednameactivitiesresponse)

### `tokenActivities`

Get paginated list of activities related to a specific token.

| Argument    | Type                                           | Description                                               |
| ----------- | ---------------------------------------------- | --------------------------------------------------------- |
| `tokenId`   | `String!`                                      | Token ID to query activities for.                         |
| `skip`      | `Float`                                        | Number of records to skip for pagination.                 |
| `take`      | `Float`                                        | Number of records to return per page (max 100).           |
| `type`      | [`TokenActivityType`](#type-tokenactivitytype) | Filter by activity type.                                  |
| `sortOrder` | [`SortOrderType`](#type-sortordertype)         | Sort order for activities (DESC or ASC). Default is DESC. |

**Returns:** [`PaginatedTokenActivitiesResponse!`](#type-paginatedtokenactivitiesresponse)

### `listings`

Get paginated list of "Buy Now" secondary sale listings for tokenized names, with optional filters.

| Argument           | Type        | Description                                     |
| ------------------ | ----------- | ----------------------------------------------- |
| `skip`             | `Float`     | Number of records to skip for pagination.       |
| `take`             | `Float`     | Number of records to return per page (max 100). |
| `tlds`             | `[String!]` | Filter by TLDs.                                 |
| `createdSince`     | `DateTime`  | Filter listings created since this date.        |
| `sld`              | `String`    | Second-level domain (SLD) name.                 |
| `networkIds`       | `[String!]` | Filter by network IDs (CAIP-2 format).          |
| `registrarIanaIds` | `[Int!]`    | Filter by registrar IANA IDs.                   |

**Returns:** [`PaginatedNameListingsResponse!`](#type-paginatednamelistingsresponse)

### `offers`

Get paginated list of offers for tokenized names, with optional filters.

| Argument    | Type                                   | Description                                           |
| ----------- | -------------------------------------- | ----------------------------------------------------- |
| `tokenId`   | `String`                               | Token ID to query offers for.                         |
| `offeredBy` | `[AddressCAIP10!]`                     | Filter by offerer addresses (CAIP-10 format).         |
| `skip`      | `Float`                                | Number of records to skip for pagination.             |
| `take`      | `Float`                                | Number of records to return per page (max 100).       |
| `status`    | [`OfferStatus`](#type-offerstatus)     | Filter by offer status (ACTIVE, EXPIRED, All).        |
| `sortOrder` | [`SortOrderType`](#type-sortordertype) | Sort order for offers (DESC or ASC). Default is DESC. |

**Returns:** [`PaginatedNameOffersResponse!`](#type-paginatednameoffersresponse)

### `nameStatistics`

Get statistics for a specific tokenized name.

| Argument  | Type      | Description                                                                 |
| --------- | --------- | --------------------------------------------------------------------------- |
| `tokenId` | `String!` | Name Ownership Token ID that identifies a name to retrieve statistics from. |

**Returns:** [`NameStatisticsModel!`](#type-namestatisticsmodel)

## Mutations

### `generateMetadata`

Generate metadata for a list of tokens based on their attributes. Useful to pre-create metadata before generating synthetic tokens.

| Argument | Type                                                                                   | Description                                        |
| -------- | -------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `tokens` | [`[TokenMetadataGenerationRequestInput!]!`](#type-tokenmetadatagenerationrequestinput) | List of synthetic tokens to generate metadata for. |

**Returns:** `[String!]!`

### `initiateEmailVerification`

Initiate email verification process for a given email address. Used to verify contact information before claiming a tokenized name.

| Argument | Type      | Description                                   |
| -------- | --------- | --------------------------------------------- |
| `email`  | `String!` | Email address to initiate email verification. |

**Returns:** `Boolean!`

### `completeEmailVerification`

Complete email verification process by providing the verification code sent to the email address. Returns a proof of email verification that can be used to upload registrant contacts.

| Argument | Type      | Description                                   |
| -------- | --------- | --------------------------------------------- |
| `code`   | `String!` | Email verification code.                      |
| `email`  | `String!` | Email that was used to initiate verification. |

**Returns:** `String!`

### `uploadRegistrantContacts`

Upload registrant contact information along with proof of email verification. This is used to claim a tokenized name and associate it with the provided contact details.

| Argument                 | Type                                                      | Description                                                                            |
| ------------------------ | --------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `contact`                | [`RegistrantContactInput!`](#type-registrantcontactinput) | Registrant contact information.                                                        |
| `emailVerificationProof` | `String!`                                                 | Proof of email verification, obtained after completing the email verification process. |
| `networkId`              | `String!`                                                 | Network ID (CAIP-2 format) where the name is being claimed.                            |
| `registrarIanaId`        | `Int!`                                                    | IANA ID of the registrar where the name is being claimed.                              |

**Returns:** [`ProofOfContactsVoucherResponseModel!`](#type-proofofcontactsvoucherresponsemodel)

### `uploadVerifiedRegistrantContacts`

Upload verified registrant contact information without email verification proof. This is used to claim a tokenized name with pre-verified email. Requires additional VERIFIED\_CONTACTS\_UPLOAD permission to use.

| Argument          | Type                                                      | Description                                                                |
| ----------------- | --------------------------------------------------------- | -------------------------------------------------------------------------- |
| `contact`         | [`RegistrantContactInput!`](#type-registrantcontactinput) | Registrant contact information, including name, email, address, and phone. |
| `networkId`       | `String!`                                                 | Network ID (CAIP-2 format) where the name is being claimed.                |
| `registrarIanaId` | `Int!`                                                    | IANA ID of the registrar where the name is being claimed.                  |

**Returns:** [`ProofOfContactsVoucherResponseModel!`](#type-proofofcontactsvoucherresponsemodel)

## Models

### `ChainModel` <a href="#type-chainmodel" id="type-chainmodel"></a>

Blockchain network information.

| Field       | Type      | Description                     |
| ----------- | --------- | ------------------------------- |
| `name`      | `String!` | Name of the blockchain network. |
| `networkId` | `String!` | Network ID in CAIP-2 format.    |

### `PaymentInfoModel` <a href="#type-paymentinfomodel" id="type-paymentinfomodel"></a>

Payment information for token transactions.

| Field            | Type      | Description                                   |
| ---------------- | --------- | --------------------------------------------- |
| `price`          | `BigInt!` | Price of the token in the specified currency. |
| `tokenAddress`   | `String!` | Contract address of the payment token.        |
| `currencySymbol` | `String!` | Symbol of the currency used for payment.      |

### `RegistrarModel` <a href="#type-registrarmodel" id="type-registrarmodel"></a>

| Field          | Type         | Description                      |
| -------------- | ------------ | -------------------------------- |
| `name`         | `String!`    | Registrar name.                  |
| `ianaId`       | `ID!`        | IANA ID of the registrar.        |
| `publicKeys`   | `[String!]!` | Registrar public keys.           |
| `websiteUrl`   | `String`     | Registrar website URL.           |
| `supportEmail` | `String`     | Registrar support email address. |

### `CommandModel` <a href="#type-commandmodel" id="type-commandmodel"></a>

Command information for tracking client-initiated operations.

| Field             | Type                                                 | Description                                      |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `type`            | [`CommandType!`](#type-commandtype)                  | Type of command.                                 |
| `status`          | [`CommandStatus!`](#type-commandstatus)              | Status of the command.                           |
| `source`          | [`CommandSource!`](#type-commandsource)              | Source of the command.                           |
| `serverCommandId` | `String!`                                            | Server command ID.                               |
| `clientCommandId` | `String!`                                            | Client command ID.                               |
| `failureReason`   | [`CommandFailureReason`](#type-commandfailurereason) | Reason for command failure, if any.              |
| `registrar`       | [`RegistrarModel`](#type-registrarmodel)             | Registrar associated with the command.           |
| `createdAt`       | `DateTime!`                                          | Date and time when the command was created.      |
| `updatedAt`       | `DateTime!`                                          | Date and time when the command was last updated. |

### `NameServerModel` <a href="#type-nameservermodel" id="type-nameservermodel"></a>

Nameserver information.

| Field     | Type      | Description                                       |
| --------- | --------- | ------------------------------------------------- |
| `ldhName` | `String!` | LDH (Letter-Digit-Hyphen) name of the nameserver. |

### `CurrencyModel` <a href="#type-currencymodel" id="type-currencymodel"></a>

Currency information.

| Field      | Type      | Description                          |
| ---------- | --------- | ------------------------------------ |
| `name`     | `String!` | Currency name.                       |
| `symbol`   | `String!` | Currency symbol.                     |
| `decimals` | `Int!`    | Number of decimals for the currency. |

### `ListingModel` <a href="#type-listingmodel" id="type-listingmodel"></a>

Secondary sale listing for a tokenized name.

| Field            | Type                                    | Description                                      |
| ---------------- | --------------------------------------- | ------------------------------------------------ |
| `id`             | `ID!`                                   | Listing ID.                                      |
| `externalId`     | `String!`                               | External order ID.                               |
| `price`          | `BigInt!`                               | Listing price.                                   |
| `offererAddress` | `AddressCAIP10!`                        | Offerer address in CAIP-10 format.               |
| `orderbook`      | [`OrderbookType!`](#type-orderbooktype) | Orderbook type.                                  |
| `currency`       | [`CurrencyModel!`](#type-currencymodel) | Currency used for the listing.                   |
| `expiresAt`      | `DateTime!`                             | Expiration date of the listing.                  |
| `createdAt`      | `DateTime!`                             | Date and time when the listing was created.      |
| `updatedAt`      | `DateTime!`                             | Date and time when the listing was last updated. |

### `OfferModel` <a href="#type-offermodel" id="type-offermodel"></a>

Offer for a tokenized name.

| Field            | Type                                    | Description                               |
| ---------------- | --------------------------------------- | ----------------------------------------- |
| `id`             | `ID!`                                   | Offer ID.                                 |
| `externalId`     | `String!`                               | External offer ID.                        |
| `price`          | `BigInt!`                               | Offer price.                              |
| `offererAddress` | `AddressCAIP10!`                        | Offerer address in CAIP-10 format.        |
| `orderbook`      | [`OrderbookType!`](#type-orderbooktype) | Orderbook type.                           |
| `currency`       | [`CurrencyModel!`](#type-currencymodel) | Currency used for the offer.              |
| `expiresAt`      | `DateTime!`                             | Expiration date of the offer.             |
| `createdAt`      | `DateTime!`                             | Date and time when the offer was created. |

### `TokenModel` <a href="#type-tokenmodel" id="type-tokenmodel"></a>

Tokenized name ownership information.

| Field                   | Type                                      | Description                                     |
| ----------------------- | ----------------------------------------- | ----------------------------------------------- |
| `tokenId`               | `ID!`                                     | Token ID.                                       |
| `networkId`             | `String!`                                 | Network ID in CAIP-2 format.                    |
| `ownerAddress`          | `AddressCAIP10!`                          | Owner address in CAIP-10 format.                |
| `type`                  | [`TokenType!`](#type-tokentype)           | Type of token.                                  |
| `startsAt`              | `DateTime`                                | Start date of the token validity.               |
| `expiresAt`             | `DateTime!`                               | Expiration date of the token.                   |
| `activities`            | [`[TokenActivity!]`](#type-tokenactivity) | List of activities for the token.               |
| `explorerUrl`           | `String!`                                 | Explorer URL for the token.                     |
| `tokenAddress`          | `String!`                                 | Token contract address.                         |
| `createdAt`             | `DateTime!`                               | Date and time when the token was created.       |
| `chain`                 | [`ChainModel!`](#type-chainmodel)         | Blockchain network information.                 |
| `listings`              | [`[ListingModel!]`](#type-listingmodel)   | Listings associated with the token.             |
| `openseaCollectionSlug` | `String`                                  | OpenSea collection slug for the token contract. |

### `TokenMintedActivity` <a href="#type-tokenmintedactivity" id="type-tokenmintedactivity"></a>

Activity representing a token mint.

| Field       | Type                                            | Description                                    |
| ----------- | ----------------------------------------------- | ---------------------------------------------- |
| `type`      | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                        |
| `networkId` | `String!`                                       | Network ID in CAIP-2 format.                   |
| `txHash`    | `String`                                        | Transaction hash associated with the activity. |
| `finalized` | `Boolean!`                                      | Whether the activity is finalized on-chain.    |
| `tokenId`   | `String!`                                       | Token ID.                                      |
| `createdAt` | `DateTime!`                                     | Date and time when the activity was created.   |

### `TokenTransferredActivity` <a href="#type-tokentransferredactivity" id="type-tokentransferredactivity"></a>

Activity representing a token transfer.

| Field             | Type                                            | Description                                    |
| ----------------- | ----------------------------------------------- | ---------------------------------------------- |
| `type`            | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                        |
| `networkId`       | `String!`                                       | Network ID in CAIP-2 format.                   |
| `txHash`          | `String`                                        | Transaction hash associated with the activity. |
| `finalized`       | `Boolean!`                                      | Whether the activity is finalized on-chain.    |
| `tokenId`         | `String!`                                       | Token ID.                                      |
| `createdAt`       | `DateTime!`                                     | Date and time when the activity was created.   |
| `transferredTo`   | `String!`                                       | Address the token was transferred to.          |
| `transferredFrom` | `String!`                                       | Address the token was transferred from.        |

### `TokenListedActivity` <a href="#type-tokenlistedactivity" id="type-tokenlistedactivity"></a>

Activity representing a token listing in the marketplace.

| Field       | Type                                            | Description                                    |
| ----------- | ----------------------------------------------- | ---------------------------------------------- |
| `type`      | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                        |
| `networkId` | `String!`                                       | Network ID in CAIP-2 format.                   |
| `txHash`    | `String`                                        | Transaction hash associated with the activity. |
| `finalized` | `Boolean!`                                      | Whether the activity is finalized on-chain.    |
| `tokenId`   | `String!`                                       | Token ID.                                      |
| `createdAt` | `DateTime!`                                     | Date and time when the activity was created.   |
| `orderId`   | `String!`                                       | Unique identifier for the marketplace order.   |
| `startsAt`  | `DateTime`                                      | Date and time when the listing becomes active. |
| `expiresAt` | `DateTime!`                                     | Date and time when the listing expires.        |
| `seller`    | `String!`                                       | Address of the token seller.                   |
| `buyer`     | `String`                                        | Address of the token buyer, if applicable.     |
| `payment`   | [`PaymentInfoModel!`](#type-paymentinfomodel)   | Payment details for the listing.               |
| `orderbook` | [`OrderbookType!`](#type-orderbooktype)         | Type of orderbook where the token is listed.   |

### `TokenOfferReceivedActivity` <a href="#type-tokenofferreceivedactivity" id="type-tokenofferreceivedactivity"></a>

Activity representing an offer received for a token.

| Field       | Type                                            | Description                                      |
| ----------- | ----------------------------------------------- | ------------------------------------------------ |
| `type`      | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                          |
| `networkId` | `String!`                                       | Network ID in CAIP-2 format.                     |
| `txHash`    | `String`                                        | Transaction hash associated with the activity.   |
| `finalized` | `Boolean!`                                      | Whether the activity is finalized on-chain.      |
| `tokenId`   | `String!`                                       | Token ID.                                        |
| `createdAt` | `DateTime!`                                     | Date and time when the activity was created.     |
| `orderId`   | `String!`                                       | Unique identifier for the marketplace order.     |
| `expiresAt` | `DateTime!`                                     | Date and time when the offer expires.            |
| `buyer`     | `String!`                                       | Address of the potential buyer making the offer. |
| `seller`    | `String!`                                       | Address of the token seller receiving the offer. |
| `payment`   | [`PaymentInfoModel!`](#type-paymentinfomodel)   | Payment details for the offer.                   |
| `orderbook` | [`OrderbookType!`](#type-orderbooktype)         | Type of orderbook where the offer was made.      |

### `TokenListingCancelledActivity` <a href="#type-tokenlistingcancelledactivity" id="type-tokenlistingcancelledactivity"></a>

Activity representing a cancelled token listing.

| Field       | Type                                            | Description                                            |
| ----------- | ----------------------------------------------- | ------------------------------------------------------ |
| `type`      | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                                |
| `networkId` | `String!`                                       | Network ID in CAIP-2 format.                           |
| `txHash`    | `String`                                        | Transaction hash associated with the activity.         |
| `finalized` | `Boolean!`                                      | Whether the activity is finalized on-chain.            |
| `tokenId`   | `String!`                                       | Token ID.                                              |
| `createdAt` | `DateTime!`                                     | Date and time when the activity was created.           |
| `orderId`   | `String!`                                       | Unique identifier for the cancelled marketplace order. |
| `reason`    | `String`                                        | Reason for cancelling the listing, if provided.        |
| `orderbook` | [`OrderbookType!`](#type-orderbooktype)         | Type of orderbook where the listing was cancelled.     |

### `TokenOfferCancelledActivity` <a href="#type-tokenoffercancelledactivity" id="type-tokenoffercancelledactivity"></a>

Activity representing a cancelled offer for a token.

| Field       | Type                                            | Description                                            |
| ----------- | ----------------------------------------------- | ------------------------------------------------------ |
| `type`      | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                                |
| `networkId` | `String!`                                       | Network ID in CAIP-2 format.                           |
| `txHash`    | `String`                                        | Transaction hash associated with the activity.         |
| `finalized` | `Boolean!`                                      | Whether the activity is finalized on-chain.            |
| `tokenId`   | `String!`                                       | Token ID.                                              |
| `createdAt` | `DateTime!`                                     | Date and time when the activity was created.           |
| `orderId`   | `String!`                                       | Unique identifier for the cancelled marketplace order. |
| `reason`    | `String`                                        | Reason for cancelling the offer, if provided.          |
| `orderbook` | [`OrderbookType!`](#type-orderbooktype)         | Type of orderbook where the offer was cancelled.       |

### `TokenPurchasedActivity` <a href="#type-tokenpurchasedactivity" id="type-tokenpurchasedactivity"></a>

Activity representing a token purchase in the marketplace.

| Field         | Type                                            | Description                                      |
| ------------- | ----------------------------------------------- | ------------------------------------------------ |
| `type`        | [`TokenActivityType!`](#type-tokenactivitytype) | Type of token activity.                          |
| `networkId`   | `String!`                                       | Network ID in CAIP-2 format.                     |
| `txHash`      | `String`                                        | Transaction hash associated with the activity.   |
| `finalized`   | `Boolean!`                                      | Whether the activity is finalized on-chain.      |
| `tokenId`     | `String!`                                       | Token ID.                                        |
| `createdAt`   | `DateTime!`                                     | Date and time when the activity was created.     |
| `orderId`     | `String!`                                       | Unique identifier for the marketplace order.     |
| `purchasedAt` | `DateTime!`                                     | Date and time when the token was purchased.      |
| `seller`      | `String!`                                       | Address of the token seller.                     |
| `buyer`       | `String!`                                       | Address of the token buyer.                      |
| `payment`     | [`PaymentInfoModel!`](#type-paymentinfomodel)   | Payment details for the purchase.                |
| `orderbook`   | [`OrderbookType!`](#type-orderbooktype)         | Type of orderbook where the token was purchased. |

### `DSKeyModel` <a href="#type-dskeymodel" id="type-dskeymodel"></a>

DNSSEC DS Key information.

| Field        | Type      | Description         |
| ------------ | --------- | ------------------- |
| `keyTag`     | `Int!`    | DS Key Tag.         |
| `algorithm`  | `Int!`    | DS Key Algorithm.   |
| `digest`     | `String!` | DS Key Digest.      |
| `digestType` | `Int!`    | DS Key Digest Type. |

### `NameModel` <a href="#type-namemodel" id="type-namemodel"></a>

Tokenized name information.

| Field          | Type                                           | Description                                                    |
| -------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| `name`         | `ID!`                                          | Name (domain).                                                 |
| `expiresAt`    | `DateTime!`                                    | Expiration date of the name.                                   |
| `tokenizedAt`  | `DateTime!`                                    | Date and time when the name was tokenized.                     |
| `eoi`          | `Boolean!`                                     | Whether the name is an expression of interest (EOI).           |
| `registrar`    | [`RegistrarModel!`](#type-registrarmodel)      | Registrar associated with the name.                            |
| `nameservers`  | [`[NameServerModel!]!`](#type-nameservermodel) | List of nameservers for the name.                              |
| `dsKeys`       | [`[DSKeyModel!]`](#type-dskeymodel)            | DNSSEC DS Keys for the name.                                   |
| `transferLock` | `Boolean`                                      | Whether transfer lock is enabled for the name ownership token. |
| `claimedBy`    | `AddressCAIP10`                                | Wallet address that claimed the name.                          |
| `tokens`       | [`[TokenModel!]`](#type-tokenmodel)            | Tokens associated with the name.                               |
| `activities`   | [`[NameActivity!]`](#type-nameactivity)        | Activities associated with the name.                           |

### `NameClaimedActivity` <a href="#type-nameclaimedactivity" id="type-nameclaimedactivity"></a>

Activity representing a name claim.

| Field       | Type                                          | Description                                    |
| ----------- | --------------------------------------------- | ---------------------------------------------- |
| `type`      | [`NameActivityType!`](#type-nameactivitytype) | Type of name activity.                         |
| `txHash`    | `String`                                      | Transaction hash associated with the activity. |
| `sld`       | `String!`                                     | Second-level domain (SLD) name.                |
| `tld`       | `String!`                                     | Top-level domain (TLD) name.                   |
| `createdAt` | `DateTime!`                                   | Date and time when the activity was created.   |
| `claimedBy` | `String!`                                     | Wallet address that claimed the name.          |

### `NameRenewedActivity` <a href="#type-namerenewedactivity" id="type-namerenewedactivity"></a>

Activity representing a name renewal.

| Field       | Type                                          | Description                                    |
| ----------- | --------------------------------------------- | ---------------------------------------------- |
| `type`      | [`NameActivityType!`](#type-nameactivitytype) | Type of name activity.                         |
| `txHash`    | `String`                                      | Transaction hash associated with the activity. |
| `sld`       | `String!`                                     | Second-level domain (SLD) name.                |
| `tld`       | `String!`                                     | Top-level domain (TLD) name.                   |
| `createdAt` | `DateTime!`                                   | Date and time when the activity was created.   |
| `expiresAt` | `DateTime!`                                   | Expiration date of the renewed name.           |

### `NameDetokenizedActivity` <a href="#type-namedetokenizedactivity" id="type-namedetokenizedactivity"></a>

Activity representing a name detokenization.

| Field       | Type                                          | Description                                    |
| ----------- | --------------------------------------------- | ---------------------------------------------- |
| `type`      | [`NameActivityType!`](#type-nameactivitytype) | Type of name activity.                         |
| `txHash`    | `String`                                      | Transaction hash associated with the activity. |
| `sld`       | `String!`                                     | Second-level domain (SLD) name.                |
| `tld`       | `String!`                                     | Top-level domain (TLD) name.                   |
| `createdAt` | `DateTime!`                                   | Date and time when the activity was created.   |
| `networkId` | `String!`                                     | Network ID in CAIP-2 format.                   |

### `NameTokenizedActivity` <a href="#type-nametokenizedactivity" id="type-nametokenizedactivity"></a>

Activity representing a name tokenization.

| Field       | Type                                          | Description                                    |
| ----------- | --------------------------------------------- | ---------------------------------------------- |
| `type`      | [`NameActivityType!`](#type-nameactivitytype) | Type of name activity.                         |
| `txHash`    | `String`                                      | Transaction hash associated with the activity. |
| `sld`       | `String!`                                     | Second-level domain (SLD) name.                |
| `tld`       | `String!`                                     | Top-level domain (TLD) name.                   |
| `createdAt` | `DateTime!`                                   | Date and time when the activity was created.   |
| `networkId` | `String!`                                     | Network ID in CAIP-2 format.                   |

### `NameListingModel` <a href="#type-namelistingmodel" id="type-namelistingmodel"></a>

Secondary sale listing for a tokenized name, including name and registrar info.

| Field            | Type                                      | Description                                      |
| ---------------- | ----------------------------------------- | ------------------------------------------------ |
| `id`             | `ID!`                                     | Listing ID.                                      |
| `externalId`     | `String!`                                 | External order ID.                               |
| `price`          | `BigInt!`                                 | Listing price.                                   |
| `offererAddress` | `AddressCAIP10!`                          | Offerer address in CAIP-10 format.               |
| `orderbook`      | [`OrderbookType!`](#type-orderbooktype)   | Orderbook type.                                  |
| `currency`       | [`CurrencyModel!`](#type-currencymodel)   | Currency used for the listing.                   |
| `expiresAt`      | `DateTime!`                               | Expiration date of the listing.                  |
| `createdAt`      | `DateTime!`                               | Date and time when the listing was created.      |
| `updatedAt`      | `DateTime!`                               | Date and time when the listing was last updated. |
| `name`           | `String!`                                 | Name (domain) associated with the listing.       |
| `nameExpiresAt`  | `DateTime!`                               | Expiration date of the name.                     |
| `registrar`      | [`RegistrarModel!`](#type-registrarmodel) | Registrar associated with the name.              |
| `tokenId`        | `String!`                                 | Token ID associated with the listing.            |
| `tokenAddress`   | `String!`                                 | Token contract address.                          |
| `chain`          | [`ChainModel!`](#type-chainmodel)         | Blockchain network information.                  |

### `NameOfferModel` <a href="#type-nameoffermodel" id="type-nameoffermodel"></a>

Offer for a tokenized name, including name and registrar info.

| Field            | Type                                      | Description                               |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| `id`             | `ID!`                                     | Offer ID.                                 |
| `externalId`     | `String!`                                 | External offer ID.                        |
| `price`          | `BigInt!`                                 | Offer price.                              |
| `offererAddress` | `AddressCAIP10!`                          | Offerer address in CAIP-10 format.        |
| `orderbook`      | [`OrderbookType!`](#type-orderbooktype)   | Orderbook type.                           |
| `currency`       | [`CurrencyModel!`](#type-currencymodel)   | Currency used for the offer.              |
| `expiresAt`      | `DateTime!`                               | Expiration date of the offer.             |
| `createdAt`      | `DateTime!`                               | Date and time when the offer was created. |
| `name`           | `String!`                                 | Name (domain) associated with the offer.  |
| `nameExpiresAt`  | `DateTime!`                               | Expiration date of the name.              |
| `registrar`      | [`RegistrarModel!`](#type-registrarmodel) | Registrar associated with the name.       |
| `tokenId`        | `String!`                                 | Token ID associated with the offer.       |
| `tokenAddress`   | `String!`                                 | Token contract address.                   |
| `chain`          | [`ChainModel!`](#type-chainmodel)         | Blockchain network information.           |

### `NameStatisticsModel` <a href="#type-namestatisticsmodel" id="type-namestatisticsmodel"></a>

Statistics for a specific tokenized name.

| Field             | Type                             | Description                                   |
| ----------------- | -------------------------------- | --------------------------------------------- |
| `name`            | `String!`                        | Name (domain).                                |
| `highestOffer`    | [`OfferModel`](#type-offermodel) | Highest offer for the name.                   |
| `activeOffers`    | `Int!`                           | Number of active offers for the name.         |
| `offersLast3Days` | `Int!`                           | Number of offers received in the last 3 days. |

### `ProofOfContactsVoucherModel` <a href="#type-proofofcontactsvouchermodel" id="type-proofofcontactsvouchermodel"></a>

Proof of contacts voucher for registrant contact verification.

| Field              | Type      | Description                                                            |
| ------------------ | --------- | ---------------------------------------------------------------------- |
| `registrantHandle` | `String!` | Registrant handle.                                                     |
| `nonce`            | `String!` | Nonce for the voucher.                                                 |
| `publicKey`        | `String!` | Registrar Public key that was used for contact information encryption. |
| `proofSource`      | `Int!`    | Proof source type.                                                     |
| `expiresAt`        | `Float!`  | Expiration timestamp for the voucher.                                  |

### `ProofOfContactsVoucherResponseModel` <a href="#type-proofofcontactsvoucherresponsemodel" id="type-proofofcontactsvoucherresponsemodel"></a>

Response containing proof of contacts voucher and its signature.

| Field                    | Type                                                                | Description                |
| ------------------------ | ------------------------------------------------------------------- | -------------------------- |
| `proofOfContactsVoucher` | [`ProofOfContactsVoucherModel!`](#type-proofofcontactsvouchermodel) | Proof of contacts voucher. |
| `signature`              | `String!`                                                           | Signature for the voucher. |

### `PaginatedNamesResponse` <a href="#type-paginatednamesresponse" id="type-paginatednamesresponse"></a>

Paginated response for querying tokenized names. Contains a list of NameModel items and pagination metadata.

| Field             | Type                               | Description                               |
| ----------------- | ---------------------------------- | ----------------------------------------- |
| `items`           | [`[NameModel!]!`](#type-namemodel) | List of items for the current page.       |
| `totalCount`      | `Int!`                             | Total number of items matching the query. |
| `pageSize`        | `Int!`                             | Number of items per page.                 |
| `currentPage`     | `Int!`                             | Current page number (1-based).            |
| `totalPages`      | `Int!`                             | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                         | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                         | Indicates if there is a next page.        |

### `PaginatedTokensResponse` <a href="#type-paginatedtokensresponse" id="type-paginatedtokensresponse"></a>

Paginated response for querying tokenized name ownership tokens. Contains a list of TokenModel items and pagination metadata.

| Field             | Type                                 | Description                               |
| ----------------- | ------------------------------------ | ----------------------------------------- |
| `items`           | [`[TokenModel!]!`](#type-tokenmodel) | List of items for the current page.       |
| `totalCount`      | `Int!`                               | Total number of items matching the query. |
| `pageSize`        | `Int!`                               | Number of items per page.                 |
| `currentPage`     | `Int!`                               | Current page number (1-based).            |
| `totalPages`      | `Int!`                               | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                           | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                           | Indicates if there is a next page.        |

### `PaginatedTokenActivitiesResponse` <a href="#type-paginatedtokenactivitiesresponse" id="type-paginatedtokenactivitiesresponse"></a>

Paginated response for querying token activities. Contains a list of TokenActivity items and pagination metadata.

| Field             | Type                                       | Description                               |
| ----------------- | ------------------------------------------ | ----------------------------------------- |
| `items`           | [`[TokenActivity!]!`](#type-tokenactivity) | List of items for the current page.       |
| `totalCount`      | `Int!`                                     | Total number of items matching the query. |
| `pageSize`        | `Int!`                                     | Number of items per page.                 |
| `currentPage`     | `Int!`                                     | Current page number (1-based).            |
| `totalPages`      | `Int!`                                     | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                                 | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                                 | Indicates if there is a next page.        |

### `PaginatedNameActivitiesResponse` <a href="#type-paginatednameactivitiesresponse" id="type-paginatednameactivitiesresponse"></a>

Paginated response for querying name activities. Contains a list of NameActivity items and pagination metadata.

| Field             | Type                                     | Description                               |
| ----------------- | ---------------------------------------- | ----------------------------------------- |
| `items`           | [`[NameActivity!]!`](#type-nameactivity) | List of items for the current page.       |
| `totalCount`      | `Int!`                                   | Total number of items matching the query. |
| `pageSize`        | `Int!`                                   | Number of items per page.                 |
| `currentPage`     | `Int!`                                   | Current page number (1-based).            |
| `totalPages`      | `Int!`                                   | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                               | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                               | Indicates if there is a next page.        |

### `PaginatedNameOffersResponse` <a href="#type-paginatednameoffersresponse" id="type-paginatednameoffersresponse"></a>

Paginated response for querying offers for tokenized names. Contains a list of NameOfferModel items and pagination metadata.

| Field             | Type                                         | Description                               |
| ----------------- | -------------------------------------------- | ----------------------------------------- |
| `items`           | [`[NameOfferModel!]!`](#type-nameoffermodel) | List of items for the current page.       |
| `totalCount`      | `Int!`                                       | Total number of items matching the query. |
| `pageSize`        | `Int!`                                       | Number of items per page.                 |
| `currentPage`     | `Int!`                                       | Current page number (1-based).            |
| `totalPages`      | `Int!`                                       | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                                   | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                                   | Indicates if there is a next page.        |

### `PaginatedNameListingsResponse` <a href="#type-paginatednamelistingsresponse" id="type-paginatednamelistingsresponse"></a>

Paginated response for querying listings for tokenized names. Contains a list of NameListingModel items and pagination metadata.

| Field             | Type                                             | Description                               |
| ----------------- | ------------------------------------------------ | ----------------------------------------- |
| `items`           | [`[NameListingModel!]!`](#type-namelistingmodel) | List of items for the current page.       |
| `totalCount`      | `Int!`                                           | Total number of items matching the query. |
| `pageSize`        | `Int!`                                           | Number of items per page.                 |
| `currentPage`     | `Int!`                                           | Current page number (1-based).            |
| `totalPages`      | `Int!`                                           | Total number of pages available.          |
| `hasPreviousPage` | `Boolean!`                                       | Indicates if there is a previous page.    |
| `hasNextPage`     | `Boolean!`                                       | Indicates if there is a next page.        |

## Unions

### `TokenActivity` <a href="#type-tokenactivity" id="type-tokenactivity"></a>

**Possible types:** [`TokenMintedActivity`](#type-tokenmintedactivity), [`TokenTransferredActivity`](#type-tokentransferredactivity), [`TokenListedActivity`](#type-tokenlistedactivity), [`TokenOfferReceivedActivity`](#type-tokenofferreceivedactivity), [`TokenListingCancelledActivity`](#type-tokenlistingcancelledactivity), [`TokenOfferCancelledActivity`](#type-tokenoffercancelledactivity), [`TokenPurchasedActivity`](#type-tokenpurchasedactivity)

### `NameActivity` <a href="#type-nameactivity" id="type-nameactivity"></a>

Union type for different name activities.

**Possible types:** [`NameClaimedActivity`](#type-nameclaimedactivity), [`NameRenewedActivity`](#type-namerenewedactivity), [`NameDetokenizedActivity`](#type-namedetokenizedactivity), [`NameTokenizedActivity`](#type-nametokenizedactivity)

## Input Types

### `TokenMetadataGenerationRequestInput` <a href="#type-tokenmetadatagenerationrequestinput" id="type-tokenmetadatagenerationrequestinput"></a>

Input for generating token metadata, including name, network, type, and validity period.

| Field       | Type                            | Description                                        |
| ----------- | ------------------------------- | -------------------------------------------------- |
| `name`      | `String!`                       | Name (domain) for which to generate metadata.      |
| `networkId` | `String!`                       | Network ID in CAIP-2 format.                       |
| `type`      | [`TokenType!`](#type-tokentype) | Type of token to generate metadata for.            |
| `startsAt`  | `DateTime`                      | Optional start date for the token validity period. |
| `expiresAt` | `DateTime!`                     | Expiration date for the token.                     |

### `RegistrantContactInput` <a href="#type-registrantcontactinput" id="type-registrantcontactinput"></a>

Registrant contact information for domain registration.

| Field          | Type      | Description                                          |
| -------------- | --------- | ---------------------------------------------------- |
| `name`         | `String!` | Full name of the registrant.                         |
| `organization` | `String`  | Organization name of the registrant (optional).      |
| `email`        | `String!` | Email address of the registrant.                     |
| `phone`        | `String!` | Phone number of the registrant.                      |
| `fax`          | `String`  | Fax number of the registrant (optional).             |
| `street`       | `String!` | Street address of the registrant.                    |
| `city`         | `String!` | City of the registrant.                              |
| `state`        | `String!` | State or province of the registrant.                 |
| `postalCode`   | `String!` | Postal code of the registrant.                       |
| `countryCode`  | `String!` | Country code of the registrant (ISO 3166-1 alpha-2). |

## Enums

### `CommandType` <a href="#type-commandtype" id="type-commandtype"></a>

Command Type

| Value                           | Description                                                             |
| ------------------------------- | ----------------------------------------------------------------------- |
| `TOKENIZE`                      | Tokenize a domain name.                                                 |
| `EOI_CLAIM`                     | (Deprecated) Transfer EOI name from an escrow.                          |
| `APPROVE_TOKENIZATION`          | Approve a tokenization request.                                         |
| `REJECT_TOKENIZATION`           | Reject a tokenization request.                                          |
| `APPROVE_CLAIM_REQUEST`         | Approve a claim request for a domain.                                   |
| `REJECT_CLAIM_REQUEST`          | Reject a claim request for a domain.                                    |
| `RENEW`                         | Renew a domain name.                                                    |
| `UPDATE`                        | Update domain (both nameservers and DNSSEC DS keys).                    |
| `UPDATE_NAMESERVERS`            | Update nameservers for a domain.                                        |
| `UPDATE_DS_KEYS`                | Update DNSSEC DS keys for a domain.                                     |
| `DETOKENIZE`                    | Detokenize a domain name. Checks if current owner has claimed a domain. |
| `DELETE`                        | Delete a domain or token (only for expired domains).                    |
| `COMPLIANCE_LOCK_STATUS_CHANGE` | Change compliance lock status for an ownership token.                   |
| `COMPLIANCE_DETOKENIZE`         | Detokenize a domain due to compliance reasons.                          |
| `UPDATE_METADATA`               | Update metadata for a token.                                            |
| `SET_REVERSE_MAPPING`           | Set reverse mapping for an address.                                     |
| `VOUCHER_PAYMENT`               | Process a voucher payment.                                              |
| `REQUEST_TOKENIZATION`          | User-initiated request to tokenize a domain.                            |
| `TRANSFER_HOOK`                 | Transfer hook event.                                                    |
| `REQUEST_CLAIM`                 | User-initiated request to claim a domain.                               |
| `REQUEST_DETOKENIZATION`        | User-initiated request to detokenize a domain.                          |
| `REQUEST_BRIDGE`                | User-initiated request to bridge a token.                               |
| `UNKNOWN`                       | Unknown or unsupported command type.                                    |

### `CommandStatus` <a href="#type-commandstatus" id="type-commandstatus"></a>

Command Status

| Value                 | Description                                          |
| --------------------- | ---------------------------------------------------- |
| `PENDING`             | Command is pending.                                  |
| `FINALIZING`          | Command is finalizing                                |
| `SUCCEEDED`           | Command has been cancelled.                          |
| `FAILED`              | Command has failed.                                  |
| `PARTIALLY_SUCCEEDED` | Command partially succeeded. Used for bulk commands. |

### `CommandSource` <a href="#type-commandsource" id="type-commandsource"></a>

Command Source

| Value   | Description                                           |
| ------- | ----------------------------------------------------- |
| `RELAY` | Command initiated by the registrar (using Relay API). |
| `USER`  | Command initiated by the user (e.g. Bridge or Claim). |

### `CommandFailureReason` <a href="#type-commandfailurereason" id="type-commandfailurereason"></a>

Command Failure Reason

| Value                | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `INTERNAL_ERROR`     | Internal error occurred during command execution. Please contact support. |
| `TRANSACTION_FAILED` | Transaction failed during command execution.                              |

### `OrderbookType` <a href="#type-orderbooktype" id="type-orderbooktype"></a>

Orderbook Type

| Value     | Description               |
| --------- | ------------------------- |
| `DOMA`    | Doma orderbook (primary). |
| `OPENSEA` | OpenSea orderbook.        |

### `TokenType` <a href="#type-tokentype" id="type-tokentype"></a>

Token Type

| Value       | Description                         |
| ----------- | ----------------------------------- |
| `OWNERSHIP` | Ownership token.                    |
| `SYNTHETIC` | Synthetic token. Not supported yet. |

### `TokenActivityType` <a href="#type-tokenactivitytype" id="type-tokenactivitytype"></a>

Token Activity Type

| Value               | Description                                  |
| ------------------- | -------------------------------------------- |
| `MINTED`            | Token was minted.                            |
| `TRANSFERRED`       | Token was transferred.                       |
| `LISTED`            | Token was listed for sale in the marketplace |
| `OFFER_RECEIVED`    | An offer was received for the token          |
| `LISTING_CANCELLED` | A listing for the token was cancelled        |
| `OFFER_CANCELLED`   | An offer for the token was cancelled         |
| `PURCHASED`         | Token was purchased in the marketplace       |

### `NameActivityType` <a href="#type-nameactivitytype" id="type-nameactivitytype"></a>

Name Activity Type

| Value         | Description                           |
| ------------- | ------------------------------------- |
| `TOKENIZED`   | Name was tokenized.                   |
| `CLAIMED`     | Name was claimed by a wallet address. |
| `RENEWED`     | Name was renewed.                     |
| `DETOKENIZED` | Name was detokenized.                 |

### `NamesQueryClaimStatus` <a href="#type-namesqueryclaimstatus" id="type-namesqueryclaimstatus"></a>

Names Claim Status

| Value       | Description                            |
| ----------- | -------------------------------------- |
| `CLAIMED`   | Name has been claimed.                 |
| `UNCLAIMED` | Name has not been claimed.             |
| `ALL`       | All names, regardless of claim status. |

### `SortOrderType` <a href="#type-sortordertype" id="type-sortordertype"></a>

Sort Order Type

| Value  | Description       |
| ------ | ----------------- |
| `DESC` | Descending order. |
| `ASC`  | Ascending order.  |

### `OfferStatus` <a href="#type-offerstatus" id="type-offerstatus"></a>

Offer Status Filter

| Value     | Description                       |
| --------- | --------------------------------- |
| `ACTIVE`  | Offer is currently active.        |
| `EXPIRED` | Offer has expired.                |
| `All`     | All offers, regardless of status. |
