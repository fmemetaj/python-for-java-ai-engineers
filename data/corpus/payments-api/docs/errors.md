# Error codes

| HTTP | Meaning |
| --- | --- |
| 401 | Missing or expired Bearer token. |
| 402 | Payment Required — the card issuer declined the charge. |
| 404 | Unknown payment id. |
| 409 | Conflict — refund of a payment that is not captured, or a duplicate idempotency key with a different body. |
| 422 | Validation — amountCents must be a positive integer. |
| 429 | Rate limit. Back off and retry. |

Never echo the Authorization header or webhook secret in an error body.
