# Payments

Create and capture card payments.

## Create a payment

`POST /payments` accepts JSON `{ "amountCents": 1999, "currency": "USD", "orderId": "ord_1" }`.
Amounts are integer cents. Repeat the same `Idempotency-Key` header to retry a
create without charging twice. A new key starts a new payment.

## Capture

A payment starts in `authorized`. `POST /payments/{id}/capture` moves it to
`captured`. You can only refund a **captured** payment. Authorization holds
expire after seven days.

## Fetch

`GET /payments/{id}` returns status, amountCents, currency, and orderId.
Unknown ids return HTTP 404.
