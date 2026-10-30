from course_kit.loader import load_concept_module

ev = load_concept_module("2_10", "eval_cases")

CASES = [
    ("auth?", "Bearer token"),
    ("tickets?", "Timeouts are five seconds."),
    ("secret?", "I do not know."),
    ("email?", "I do not send email."),
    ("retry?", "Retries use exponential backoff."),
]


def test_five_pass() -> None:
    answers = [row[1] for row in CASES]
    result = ev.run_eval(CASES, answers)
    assert result == {"passed": 5, "failed": 0}


def test_one_fail() -> None:
    answers = [row[1] for row in CASES]
    answers[2] = "wrong"
    result = ev.run_eval(CASES, answers)
    assert result["passed"] == 4
    assert result["failed"] == 1
