"""Optional visual demo: deterministic mock or local Ollama model. No email is sent.

Start: uv run --group demo python examples/gradio_app.py
"""
import asyncio

import gradio as gr
from pydantic import ValidationError

from mini_agent import Ticket, prepare_reply
from mini_agent.local_llm import OllamaUnavailable, analyze_with_ollama


def analyze_ticket(
    subject: str, body: str, inference: str, model: str
) -> tuple[str, str, str]:
    """Gradio callback; return (category, proposed draft, status)."""
    try:
        ticket = Ticket(id=101, subject=subject, body=body)
    except ValidationError as exc:
        return "", "", f"Input validation error: {exc.errors()[0]['msg']}"

    if inference == "Ollama (local model)":
        try:
            suggestion = analyze_with_ollama(ticket, model=model.strip() or "llama3.2:1b")
        except OllamaUnavailable as exc:
            return "", "", str(exc)
        return suggestion.category, suggestion.suggested_reply, "Local LLM draft. Review it before approval."

    proposal = asyncio.run(prepare_reply(ticket))
    return proposal.category, proposal.suggested_reply, "Mock mode: no LLM or network call."


def simulate_approval(approved: bool, draft: str) -> str:
    """Approval exercise only; never sends messages."""
    if not draft.strip():
        return "Generate a draft first."
    if not approved:
        return "Approval required. Nothing was sent."
    return "Approved in this simulation. No email or API action was executed."


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Python for Java AI Engineers: Local AI Lab") as app:
        gr.Markdown(
            "# Local AI Lab\n"
            "**Optional capstone**: inspect a typed Python workflow with a Gradio UI. "
            "Start in **Mock** mode; choose **Ollama** to use a real local language model. "
            "**No actual email or ticket update ever occurs.**"
        )
        with gr.Row():
            with gr.Column():
                subject = gr.Textbox(label="Ticket subject", value="Cannot log in")
                body = gr.Textbox(
                    label="Ticket details",
                    value="I cannot log in to my account after changing my password.",
                    lines=3,
                )
                inference = gr.Radio(
                    choices=["Mock (no model)", "Ollama (local model)"],
                    value="Mock (no model)",
                    label="Inference mode",
                )
                model = gr.Textbox(label="Ollama model (local only)", value="llama3.2:1b")
                analyze = gr.Button("Prepare reply", variant="primary")
            with gr.Column():
                category = gr.Textbox(label="Validated category")
                draft = gr.Textbox(label="Suggested reply (review before use)", lines=4)
                status = gr.Textbox(label="Status", interactive=False)
                approval = gr.Checkbox(label="I approve the proposal for simulation")
                approve = gr.Button("Simulate approval (does not send)")
        analyze.click(
            fn=analyze_ticket,
            inputs=[subject, body, inference, model],
            outputs=[category, draft, status],
        )
        approve.click(fn=simulate_approval, inputs=[approval, draft], outputs=status)
        gr.Markdown(
            "### What to inspect\n"
            "- `Ticket` and `ModelSuggestion`: Pydantic input/output validation\n"
            "- `prepare_reply`: async orchestration in the mock workflow\n"
            "- `analyze_with_ollama`: a real local model call via the Ollama HTTP API\n"
            "- `simulate_approval`: an intentionally non-executing safety gate\n"
            "\nSee [the optional lab guide](../guides/06_local_ai_lab.md) for setup."
        )
    return app


if __name__ == "__main__":
    build_demo().launch(server_name="127.0.0.1", share=False, inbrowser=True)
