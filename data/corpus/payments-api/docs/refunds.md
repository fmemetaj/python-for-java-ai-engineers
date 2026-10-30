# Refunds

Refund a captured payment, in full or in part.

## Full refund

`POST /payments/{id}/refunds` with `{ "amountCents": <original> }` refunds the
entire captured amount. The payment status becomes `refunded`.

## Partial refunds

Partial refunds are allowed while remaining captured cents are greater than
zero. Each refund needs its own `Idempotency-Key`. You cannot refund an
`authorized` (not yet captured) payment — that returns HTTP 409.

## Settlement

Refunds settle on the next batch. Webhook event `refund.settled` fires when the
card network confirms.
