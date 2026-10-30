"""Write down the hosted-vs-own choice. Offline."""

from __future__ import annotations

from course_kit.hosted import choose_stack, decision_record, lock_in_flags

decision = choose_stack(
    own_recall=0.8,
    hosted_available=True,
    can_export=True,
    can_eval=True,
    overlap=0.1,
)
flags = lock_in_flags(vendor_chunking=True, exportable=False, billed_separately=True)

# Example 1 — hosted retrieval is billed separately and not exportable.
assert flags["billed_separately"] is True
assert flags["ci_honest"] is False

# Example 2 — we still pick own because we can eval.
assert decision.choice == "own"

# Example 3 — the record is pasteable into a portfolio README.
payload = decision_record(decision, flags=flags)
assert payload["assistants"] is False
assert payload["api"] == "responses"

# Example 4 — flags travel with the record.
nested = payload["flags"]
assert isinstance(nested, dict)
assert nested["vendor_chunking"] is True

# Example 5 — this is not a legal opinion; it is an engineering ADR.
print(payload["reason"])
print("A.6 examples ok")
