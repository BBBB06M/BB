"""Gemini API integration for GraphMind AI's differentiated quadratic exercises.

Keys are loaded by Streamlit from its private Secrets store, never from the repo.
Free-tier availability and quotas depend on your Google AI Studio project.
"""
from __future__ import annotations

from google import genai
from google.genai import types

from ai_engine import Exercise, ExerciseSchema, SYSTEM_PROMPT
from math_engine import Marking, Quadratic, fraction_label, validate_level

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"


def gemini_client(api_key: str):
    if not api_key or not api_key.strip():
        raise ValueError("Gemini API key is missing.")
    return genai.Client(api_key=api_key.strip())


def generate_gemini_exercise(client, model: str, level: str, last_coefficients=None) -> Exercise:
    """Ask Gemini for an original task, then independently verify the coefficients."""
    if level not in ("Foundation", "Standard", "Advanced"):
        raise ValueError("Unknown difficulty level")
    prompt = f"Create a NEW {level} exercise about the vertex of a quadratic graph."
    if last_coefficients:
        prompt += f" Use coefficients different from {last_coefficients}."
    for attempt in range(3):
        response = client.models.generate_content(
            model=model,
            contents=prompt + f" Attempt {attempt + 1}.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ExerciseSchema,
                temperature=0.8,
            ),
        )
        if response.parsed is not None:
            result = (
                response.parsed
                if isinstance(response.parsed, ExerciseSchema)
                else ExerciseSchema.model_validate(response.parsed)
            )
        elif response.text:
            result = ExerciseSchema.model_validate_json(response.text)
        else:
            raise RuntimeError("Gemini did not return usable exercise data.")

        q = Quadratic(result.a, result.b, result.c)
        if not validate_level(q, level):
            continue
        if last_coefficients == (q.a, q.b, q.c):
            continue
        pieces = (result.title, result.context, result.hint_1, result.hint_2, result.learning_tip)
        if not all(isinstance(t, str) and 5 <= len(t.strip()) <= 750 for t in pieces):
            continue
        return Exercise(
            quadratic=q,
            level=level,
            title=result.title.strip(),
            context=result.context.strip(),
            hints=(result.hint_1.strip(), result.hint_2.strip()),
            learning_tip=result.learning_tip.strip(),
        )
    raise RuntimeError("Gemini generated invalid question parameters repeatedly. Try again.")


def gemini_feedback(client, model: str, exercise: Exercise, marking: Marking) -> str:
    """Feedback based only on math_engine's checked results, without revealing answers."""
    q = exercise.quadratic
    verdict = (
        f"vertex-x {'correct' if marking.x_correct else 'incorrect'}; "
        f"vertex-y {'correct' if marking.y_correct else 'incorrect'}; "
        f"opening {'correct' if marking.direction_correct else 'incorrect'}"
    )
    prompt = (
        "You are a supportive Grade 9 mathematics tutor. Write 1-3 short sentences "
        "in simple A2-B1 English. Treat the following correctness flags as the truth; "
        "do not recompute them. For a wrong answer suggest one next step suitable "
        "for the learner's level. Do not reveal the numerical vertex. "
        "Do not request personal data.\n"
        f"Level: {exercise.level}. Coefficients: a={q.a}, b={q.b}, c={q.c}. "
        f"Verified vertex: ({fraction_label(q.vertex_x)}, {fraction_label(q.vertex_y)}). "
        f"Direction: {q.opens}. Student result: {verdict}."
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=250,
        ),
    )
    return (response.text or "").strip() or "Check your graph and try one more time."
