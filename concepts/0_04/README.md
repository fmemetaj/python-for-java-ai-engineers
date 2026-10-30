# 0.4 Built-in types   [Analog: primitives + wrappers, String, null] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_04/tests/test_skip.py` passes.

## 1. Concept

Everyday Python values are objects: unbounded `int`, IEEE-754 `float`, immutable `str`, `bool` (`True`/`False`), and `None` (the single missing-value object). There is no primitive/wrapper split and no `int` overflow to a two's-complement max.

## 2. Java version

```java
public class BuiltInTypesDemo {
    public static void main(String[] args) {
        int count = 1_000_000;
        String title = "DocsDesk";
        String missing = null;
        System.out.println(title == "DocsDesk");
        System.out.println(missing == null);
        System.out.println(count + 1);
    }
}
```

`==` on references is identity (except when cached `Integer` / interned strings confuse you). `null` is not a `String`.

## 3. Python version

```python
count = 10**100  # fine; ints do not overflow
title = "DocsDesk"
missing = None
print(title == "DocsDesk")  # value equality
print(title is "DocsDesk")  # identity; do not use this for strings
print(missing is None)  # the correct None test
```

| Java | Python |
| --- | --- |
| `int` / `long` / `BigInteger` | `int` (unbounded) |
| `String` (immutable) | `str` (immutable) |
| `null` | `None` |
| `==` vs `equals` | `is` vs `==` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `==` for primitives, `equals` for objects | `==` is value equality (`__eq__`); `is` is identity | `if status is "error":` breaks when the string is interned differently |
| `value == null` | `value is None` | `== None` works for `None` but is the wrong habit near custom `__eq__` |
| `int` overflow / wrap | `int` grows | Performance surprises, not wraparound bugs |
| `null` is not `""` | `None` is not `""` or `0` | Mixing them; see 0.5 for truthiness |
| `boolean` vs `Boolean` | `bool` is a subclass of `int` | `True + True == 2` — do not rely on it |

Official reference: [built-in types](https://docs.python.org/3/library/stdtypes.html).

## 5. Exercise

Implement `same_identity`, `same_value`, and `none_label` in `exercises/types.py`.

```bash
uv run pytest concepts/0_04
```

- Hint 1: `is` vs `==`.
- Hint 2: `None` is a singleton — compare with `is`.
- Solution: `solutions/types.py`.

## 6. Check

1. `10**100` — exception or a valid `int`?
2. `a = 256; b = 256; a is b` may be True. Why must you still use `==` for numbers?
3. `"" is None` — True or False?
4. Can you mutate `"DocsDesk"` in place like a `StringBuilder`?

**Real scenario:** an LLM JSON field is missing (`None`) vs present-but-empty (`""`). Those are different states.

**What you learned:** `==` compares values; `is` is for `None` and true identity.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
