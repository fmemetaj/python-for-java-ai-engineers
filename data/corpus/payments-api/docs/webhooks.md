# Webhooks

The service posts JSON events to a merchant URL.

## Registration

`POST /webhooks` registers `{ "url": "https://merchant.example/hooks" }`.
HTTPS is required.

## Signatures

Every delivery includes `X-Signature`. Verify it with HMAC-SHA256 over the raw
body using the webhook secret. Reject the event if the hex digest does not
match. DocsDesk never logs the webhook secret.

## Events

`payment.captured`, `refund.settled`, and `payment.failed` are the events this
fixture documents. Retries use exponential backoff on HTTP 5xx.
