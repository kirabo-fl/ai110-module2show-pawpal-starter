"""
PawPal+ AI Advisor — RAG pipeline with input and output guardrails.

Flow:
  User query
    → input guardrail (is this pet-related?)
    → retriever   (keyword match against knowledge_base.FACTS, top-3)
    → prompt builder (system prompt + retrieved facts + pet context)
    → Gemini API  (gemini-1.5-flash, minimal tokens)
    → output guardrail (dangerous-term scan)
    → structured result dict
"""

import os
from dotenv import load_dotenv
from knowledge_base import FACTS

load_dotenv()

# ── Constants ──────────────────────────────────────────────────────────────

_PET_KEYWORDS = {
    "dog", "cat", "pet", "animal", "puppy", "kitten", "feed", "food",
    "walk", "vet", "medication", "medicine", "groom", "grooming", "breed",
    "paw", "fur", "coat", "litter", "vaccination", "vaccine", "exercise",
    "treat", "collar", "leash", "bath", "claw", "nail", "flea", "tick",
    "buddy", "mochi", "golden", "retriever", "ragdoll", "persian",
    "schedule", "task", "care", "brush", "water", "health", "senior",
    "play", "scratch", "dental", "teeth", "heartworm", "parasite",
}

_DANGEROUS_TERMS = {
    "ibuprofen", "acetaminophen", "tylenol", "aspirin", "xylitol",
    "bleach", "antifreeze", "naproxen", "advil",
}

_SYSTEM_PROMPT = (
    "You are PawPal+, a concise and caring pet care assistant. "
    "Use only the retrieved facts below to answer the question. "
    "If the answer is not covered by the facts, say so and recommend consulting a vet. "
    "Never suggest giving pets human medications."
)


# ── Retrieval ──────────────────────────────────────────────────────────────

def retrieve(query: str, top_k: int = 3) -> list[str]:
    """Return the top_k most relevant fact strings for the query."""
    words = set(query.lower().replace("?", "").replace(".", "").split())
    scored = sorted(
        FACTS,
        key=lambda f: len(words & set(f["tags"])),
        reverse=True,
    )
    # Keep facts that share at least one tag with the query
    relevant = [f["text"] for f in scored if len(words & set(f["tags"])) > 0]
    if not relevant:
        # Fallback: return the first two generic facts
        return [scored[0]["text"], scored[1]["text"]]
    return relevant[:top_k]


# ── Guardrails ─────────────────────────────────────────────────────────────

def is_pet_related(query: str) -> bool:
    """Return True if the query contains at least one pet-related keyword."""
    words = set(query.lower().replace("?", "").replace(".", "").replace(",", "").split())
    return bool(words & _PET_KEYWORDS)


def check_output_safety(text: str) -> tuple[bool, str]:
    """
    Scan the model response for dangerous terms.
    Returns (is_safe, message).
    """
    lower = text.lower()
    for term in _DANGEROUS_TERMS:
        if term in lower:
            flagged_msg = (
                f"⚠️ This response was flagged because it mentions '{term}', "
                "which can be harmful to pets. Please consult your vet before "
                "acting on any medication advice.\n\n"
                f"Original response: {text}"
            )
            return False, flagged_msg
    return True, text


# ── Main pipeline ──────────────────────────────────────────────────────────

def ask_advisor(query: str, pet_context: str = "") -> dict:
    """
    Full RAG pipeline.

    Args:
        query:       The user's pet care question.
        pet_context: Optional string like "Buddy, Dog, Golden Retriever, age 3".

    Returns a dict with keys:
        status         — "ok" | "rejected" | "flagged" | "error"
        answer         — AI answer (present when status is "ok" or "flagged")
        reason         — Explanation (present when status is "rejected" or "error")
        retrieved_facts — List of fact strings used as context
    """
    # ── 1. Input guardrail ─────────────────────────────────────────────────
    if not is_pet_related(query):
        return {
            "status": "rejected",
            "reason": (
                "This question doesn't appear to be pet-related. "
                "PawPal+ only answers pet care questions."
            ),
            "retrieved_facts": [],
        }

    # ── 2. Retrieve relevant facts ─────────────────────────────────────────
    facts = retrieve(query)
    facts_block = "\n".join(f"- {f}" for f in facts)
    pet_block = f"\nPet context: {pet_context}" if pet_context else ""

    # ── 3. Build prompt (minimal tokens: system + 3 facts + question) ──────
    full_prompt = (
        f"{_SYSTEM_PROMPT}\n\n"
        f"Retrieved facts:\n{facts_block}"
        f"{pet_block}\n\n"
        f"Question: {query}\n\n"
        "Answer in 2-3 sentences."
    )

    # ── 4. Call Gemini ─────────────────────────────────────────────────────
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "reason": "GEMINI_API_KEY is not set. Add it to your .env file.",
            "retrieved_facts": facts,
        }

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemma-3-4b-it",
            contents=full_prompt,
        )
        text = response.text.strip()
    except Exception as exc:
        return {
            "status": "error",
            "reason": f"Gemini API error: {exc}",
            "retrieved_facts": facts,
        }

    # ── 5. Output guardrail ────────────────────────────────────────────────
    safe, result = check_output_safety(text)
    return {
        "status": "flagged" if not safe else "ok",
        "answer": result,
        "retrieved_facts": facts,
    }
