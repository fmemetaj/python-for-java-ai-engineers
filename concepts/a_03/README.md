# A.3 Image token economics   [Analog: metered object storage / CDN egress] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_03/tests/test_skip.py` passes.

Official docs: [Images and vision](https://platform.openai.com/docs/guides/images-vision) (token counts), [Pricing](https://platform.openai.com/docs/pricing). Helpers: `course_kit.vision.image_token_count`, `image_cost_usd`. Prices: `data/pricing.yaml` (retrieved 2026-10-30).

## 1. Concept

**Image tokens** are input tokens. `detail=low` is a flat **85** tokens. `detail=high` scales the image, tiles it into 512px squares, and bills `85 + 170 * tiles`. USD uses the model's **input** rate from `data/pricing.yaml`. Never hard-code rates in prose.

## 2. Java version

```java
public class ImageCostDemo {
    public static int lowDetailTokens() {
        return 85;
    }
    public static void main(String[] args) {
        int tokens = lowDetailTokens();
        double inputPerMillion = 0.40;
        double usd = tokens * inputPerMillion / 1_000_000.0;
        System.out.println(tokens);
        System.out.println(usd);
    }
}
```

S3/CloudFront bills **bytes transferred**. Vision bills **tokens**, which do not equal file size.

## 3. Python version

```python
from course_kit.vision import image_token_count, image_cost_usd

image_token_count("low", 1024, 768)  # 85
image_token_count("high", 1024, 768)  # 765
```

| Java / cloud | Python (this course) |
| --- | --- |
| S3 GET / CDN egress (bytes) | image tokens (low=85, high=tiles) |
| Storage class | `detail=low` vs `high` |
| Invoice line "data transfer" | `image_tokens * input_per_million / 1e6` |
| Object metadata size | width/height used only for high-detail tiles |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Bill the JPEG file size | Tokens ignore bytes; a tiny 4K PNG can still tile | "It's only 20 KB" and a large bill |
| Output tokens are the expensive ones | Images are **input** | Using `output_per_million` for the screenshot |
| Hard-code `$0.40` | Read `data/pricing.yaml` | Stale prices in a README |
| `detail=high` always | Low is enough for a stacktrace | 4×–10× cost for no extra recall |

## 5. Exercise

Implement `image_tokens` and `vision_cost_usd`. Pass rates in as arguments.

```bash
uv run pytest concepts/a_03
```

- Hint 1: low is always 85; high uses the helper in `course_kit.vision`.
- Hint 2: `(image + text) * input_rate + output * output_rate` per million.
- Solution: `solutions/tokens.py`.

## 6. Check

1. How many tokens is `detail=low` on a 64×64 image?
2. Are image tokens input or output?
3. Why is CDN egress a partial analog?
4. Predict: 1024×768 high-detail token count.
5. Where do USD rates live in this repo?

## Setup / troubleshooting

- Prices: `data/pricing.yaml`, source URL + date in the file. Do not copy rates into code you will forget to update.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `VisionDesk` adds `image_tokens` to `usage.input_tokens` before `cost_usd`.

**What you learned:** low=85; high=tiles; images bill as input; rates stay in YAML.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
