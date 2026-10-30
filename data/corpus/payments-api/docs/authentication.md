# Authentication

Clients authenticate with a JWT Bearer token.

## Authorization header

Send `Authorization: Bearer <jwt>` on every mutating request. DocsDesk and this
service never log the raw token. The JWT is signed with HS256. The `sub` claim
is the merchant id.

## Public vs private routes

`GET /health` is public. `POST /payments`, `GET /payments/{id}`, and refunds
require a valid Bearer token. A missing header returns HTTP 401. An expired JWT
returns HTTP 401 with `error=token_expired`.

## Rotation

Keys rotate every 90 days. Old tokens fail after the `exp` claim. Do not put
tokens in query strings.
