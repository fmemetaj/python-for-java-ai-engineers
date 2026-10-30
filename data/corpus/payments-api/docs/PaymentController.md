# PaymentController (Javadoc excerpt)

The controller is a Spring `@RestController`. Naive character chunking splits the
fenced Java below; structure-aware chunking keeps the fence as one chunk.

## Mappings

```java
@RestController
@RequestMapping("/payments")
public class PaymentController {
    private final PaymentService payments;

    public PaymentController(PaymentService payments) {
        this.payments = payments;
    }

    @PostMapping
    public PaymentResponse create(@RequestBody CreatePaymentRequest body,
                                  @RequestHeader("Idempotency-Key") String key) {
        return payments.create(body, key);
    }

    @GetMapping("/{id}")
    public PaymentResponse get(@PathVariable String id) {
        return payments.get(id);
    }

    @PostMapping("/{id}/refunds")
    public RefundResponse refund(@PathVariable String id,
                                 @RequestBody RefundRequest body) {
        return payments.refund(id, body);
    }
}
```

`@PostMapping` on `create` is `POST /payments`. `@PostMapping("/{id}/refunds")`
is the refund route. The `Idempotency-Key` header is required on create.
