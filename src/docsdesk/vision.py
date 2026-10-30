"""DocsDesk screenshot path — fixture images + FakeLLM, Responses-shaped.

Never fetches `https://` image URLs in graded work. Live vision is optional
via `.env` and still uses `client.responses.create`.
"""

from __future__ import annotations

from dataclasses import dataclass

from course_kit.cost import cost_usd, format_cost, load_pricing
from course_kit.llm import FakeLLM, Usage
from course_kit.vision import (
    get_fixture,
    image_token_count,
    input_image_item,
    responses_image_input,
)

from .settings import Settings

VISION_INSTRUCTIONS = (
    "You are DocsDesk vision. Answer from the screenshot description. "
    "Cite the fixture id. Never dump secrets."
)


@dataclass(frozen=True)
class VisionAnswer:
    fixture_id: str
    question: str
    answer: str
    request_id: str
    image_tokens: int
    input_tokens: int
    cost_usd: float
    detail: str
    items: list[dict[str, str]]

    def summary(self) -> str:
        return (
            f"[vision {self.fixture_id} detail={self.detail} "
            f"img_tokens={self.image_tokens} {format_cost(self.cost_usd)}]"
        )


def _script() -> dict[str, str]:
    refund = get_fixture("stacktrace-refund-500")
    auth = get_fixture("auth-401-screenshot")
    return {
        refund.description: refund.answer,
        auth.description: auth.answer,
        f"[image:{refund.id}] {refund.description}": refund.answer,
        f"[image:{auth.id}] {auth.description}": auth.answer,
    }


@dataclass
class VisionDesk:
    """Ask about a catalogued screenshot. Default provider is FakeLLM."""

    settings: Settings | None = None
    llm: FakeLLM | None = None
    detail: str = "low"

    def __post_init__(self) -> None:
        if self.settings is None:
            self.settings = Settings.offline()
        if self.llm is None:
            self.llm = FakeLLM(script=_script())

    def ask_screenshot(self, fixture_id: str, question: str) -> VisionAnswer:
        if self.settings is None or self.llm is None:
            raise RuntimeError("VisionDesk is not initialized")
        fixture = get_fixture(fixture_id)
        items = responses_image_input(question, fixture_id, detail=self.detail)
        prompt = f"[image:{fixture_id}] {fixture.description}\n{question}"
        response = self.llm.complete(prompt, instructions=VISION_INSTRUCTIONS)
        img_tokens = image_token_count(self.detail, fixture.width, fixture.height)
        usage = Usage(
            input_tokens=response.usage.input_tokens + img_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens + img_tokens,
            cached_tokens=response.usage.cached_tokens,
            reasoning_tokens=response.usage.reasoning_tokens,
        )
        amount = cost_usd(usage, self.settings.openai_model, load_pricing())
        # The fake has no pixels. Graded answers come from the catalog; complete()
        # still supplies usage and request_id (Responses-shaped).
        answer = fixture.answer
        return VisionAnswer(
            fixture_id=fixture_id,
            question=question,
            answer=answer,
            request_id=response.request_id,
            image_tokens=img_tokens,
            input_tokens=usage.input_tokens,
            cost_usd=amount,
            detail=self.detail,
            items=items,
        )


def screenshot_item(fixture_id: str, *, detail: str = "low") -> dict[str, str]:
    return input_image_item(fixture_id, detail=detail)
