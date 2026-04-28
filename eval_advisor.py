#!/usr/bin/env python3
"""
eval_advisor.py — Evaluation and guardrail demonstration for PawPal+ AI Advisor.

Tests four cases:
  1. Valid dog exercise query       → expects AI answer (live API call)
  2. Valid cat grooming query       → expects AI answer (live API call)
  3. Off-topic query                → expects REJECTED by input guardrail (no API needed)
  4. Dangerous-term response        → expects FLAGGED by output guardrail (mocked, no API needed)

Run:
    python eval_advisor.py

Requires GEMINI_API_KEY in .env for tests 1-2; tests 3-4 run without any API key.
"""

from ai_advisor import is_pet_related, retrieve, check_output_safety, ask_advisor

LINE = "─" * 62


def _header(label: str) -> None:
    print(f"\n{LINE}")
    print(f"  {label}")
    print(LINE)


def _result_line(status: str, passed: bool) -> None:
    icon = "PASS ✓" if passed else "FAIL ✗"
    print(f"  [{icon}]  status={status}")


# ── Test cases ─────────────────────────────────────────────────────────────

def test_dog_exercise_query() -> bool:
    """Valid dog query — expects a live AI answer."""
    _header("Test 1: Valid dog exercise query (live API)")
    query = "How often should I walk my Golden Retriever?"
    ctx   = "Buddy, Dog, Golden Retriever, age 3"
    print(f"  Query  : {query}")
    print(f"  Context: {ctx}")

    result = ask_advisor(query, ctx)

    if result["status"] == "error":
        print(f"  ⚠ Skipped — API unavailable: {result['reason']}")
        return None  # don't count against score

    print("\n  Retrieved facts:")
    for f in result["retrieved_facts"]:
        print(f"    · {f[:90]}...")
    print(f"\n  Answer : {result.get('answer', result.get('reason'))}")

    passed = result["status"] == "ok"
    _result_line(result["status"], passed)
    return passed


def test_cat_grooming_query() -> bool:
    """Valid cat query — expects a live AI answer."""
    _header("Test 2: Valid cat grooming query (live API)")
    query = "How often should I brush my Ragdoll cat?"
    ctx   = "Mochi, Cat, Ragdoll, age 2"
    print(f"  Query  : {query}")
    print(f"  Context: {ctx}")

    result = ask_advisor(query, ctx)

    if result["status"] == "error":
        print(f"  ⚠ Skipped — API unavailable: {result['reason']}")
        return None

    print("\n  Retrieved facts:")
    for f in result["retrieved_facts"]:
        print(f"    · {f[:90]}...")
    print(f"\n  Answer : {result.get('answer', result.get('reason'))}")

    passed = result["status"] == "ok"
    _result_line(result["status"], passed)
    return passed


def test_off_topic_guardrail() -> bool:
    """Off-topic query — must be rejected by input guardrail without any API call."""
    _header("Test 3: Off-topic input guardrail (no API needed)")
    query = "What is the best restaurant in Chicago?"
    print(f"  Query  : {query}")

    pet_related = is_pet_related(query)
    fired       = not pet_related
    print(f"  is_pet_related() returned : {pet_related}")
    print(f"  Guardrail fired           : {fired}")
    if fired:
        print("  → Query rejected before reaching Gemini API")

    passed = fired
    _result_line("rejected" if fired else "passed-through", passed)
    return passed


def test_output_safety_guardrail() -> bool:
    """Dangerous term in model response — must be flagged by output guardrail."""
    _header("Test 4: Output safety guardrail (mocked response, no API needed)")
    mock_response = "You can give your dog ibuprofen for pain relief."
    print(f"  Mock response : {mock_response}")

    safe, message = check_output_safety(mock_response)
    print(f"  is_safe       : {safe}")
    print(f"  Guardrail msg : {message[:100]}...")

    passed = not safe
    _result_line("flagged" if not safe else "passed-through", passed)
    return passed


# ── Runner ─────────────────────────────────────────────────────────────────

def run_evaluation() -> None:
    print(LINE)
    print("  PawPal+ AI Advisor — Evaluation Report")
    print(LINE)

    results = [
        test_dog_exercise_query(),
        test_cat_grooming_query(),
        test_off_topic_guardrail(),
        test_output_safety_guardrail(),
    ]

    counted = [(r, i + 1) for i, r in enumerate(results) if r is not None]
    passed  = sum(1 for r, _ in counted if r)
    total   = len(counted)
    skipped = len(results) - total

    print(f"\n{LINE}")
    print(f"  Results : {passed}/{total} passed", end="")
    if skipped:
        print(f"  ({skipped} skipped — add GEMINI_API_KEY to .env to run live tests)", end="")
    print(f"\n{LINE}\n")


if __name__ == "__main__":
    run_evaluation()
