# Northwind Payments API

Original course fixture: a tiny Spring Boot service that DocsDesk indexes in
Module 4. Not a real bank. No secrets. Public domain sample written for this
repository.

Package: `com.northwind.payments`

Run (in a real Spring project this would be `./mvnw spring-boot:run`):

```
GET  /payments/{id}
POST /payments
POST /payments/{id}/refunds
POST /webhooks
```

See `docs/` for operator-facing Markdown and `docs/PaymentController.md` for a
Javadoc-style excerpt of the controller.
