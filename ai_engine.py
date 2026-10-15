"""OpenAI Responses API adapter for differentiated graph exercises.

Credentials are supplied by the host application; never store a key here.
"""
from dataclasses import dataclass
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from math_engine import Marking, Quadratic, validate_level, fraction_label


DEFAULT_MODEL = "gpt-5-mini"


class ExerciseSchema(BaseModel):
    a: int = Field(description="Quadratic leading coefficient")
    b: int = Field(description="Linear coefficient")
    c: int = Field(description="Constant coefficient")
    title: str = Field(description="Short, student-friendly exercise title")
    context: str = Field(description="One or two sentences of level-appropriate problem context")
    hint_1: str = Field(description="First hint, without numerical vertex coordinates")
    hint_2: str = Field(description="More specific hint, without giving the numerical vertex coordinates")
    learning_tip: str = Field(description="General concept explanation; avoid specific numerical answers")


@dataclass(frozen=True)
class Exercise:
    quadratic: Quadratic
    level: str
    title: str
    context: str
    hints: tuple[str, str]
    learning_tip: str


SYSTEM_PROMPT = """You are an expert Grade 9 mathematics teacher creating DIFFERENTIATED
practice on a SINGLE CORE SKILL: use the GRAPH of a quadratic to identify the
vertex and the opening direction. Only write for a student in straightforward
English (A2-B1). Return a valid structured output according to the schema.

Rules for difficulty differentiation:
- Foundation: a = 1 or -1; b = 0; integer c in [-6, 6]. Very direct
  graph translation f(x) = +/-x² + c. Scaffold with plain-language hints.
- Standard: a belongs to {-2,-1,1,2}; b nonzero between -8 and 8;
  c between -8 and 8. Grade-level practice using -b/(2a).
- Advanced: a = -2,-3,-4; b between +4 and +12; c between 0 and 8.
  Use a realistic ball/projectile height h(t) in METRES after t SECONDS,
  domain t >= 0; explore the maximum/vertex in a real-world interpretation.

Hints must be gradual: hint_1 gives conceptual direction, hint_2 describes a
method or formula but NEVER states the actual vertex or full final answer.
In context: clearly ask students to identify the vertex coordinates AND
whether the parabola opens up/down. Advanced: interpret the peak height and
time. Do not include any numerical answers in context, hints or learning tip.
Use short accurate English; avoid markdown tables, arbitrary trigonometry,
extra subproblems or solving roots.
"""


def client_for(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, timeout=30.0, max_retries=1)


def generate_exercise(
    client: OpenAI,
    model: str,
    level: Literal["Foundation", "Standard", "Advanced"],
    last_coefficients: tuple[int, int, int] | None = None,
) -> Exercise:
    """Generate via actual API; retry if schema-compliant values break constraints."""
    user_msg = f"Create a NEW {level} level activity on the graph vertex."
    if last_coefficients:
        user_msg += f" Previous coefficients {last_coefficients}; use a different triple."
    for attempt in range(3):
        answer = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg + f" Generation attempt {attempt + 1}."},
            ],
            text_format=ExerciseSchema,
            store=False,
        )
        result = answer.output_parsed
        if result is None:
            raise RuntimeError("The model did not return a usable exercise.")
        q = Quadratic(result.a, result.b, result.c)
        if not validate_level(q, level):
            continue
        if last_coefficients == (q.a, q.b, q.c):
            continue
        if not all(
            isinstance(text, str) and 5 <= len(text.strip()) <= 750
            for text in (result.title, result.context, result.hint_1, result.hint_2, result.learning_tip)
        ):
            continue
        return Exercise(
            quadratic=q,
            level=level,
            title=result.title.strip(),
            context=result.context.strip(),
            hints=(result.hint_1.strip(), result.hint_2.strip()),
            learning_tip=result.learning_tip.strip(),
        )
    raise RuntimeError("AI returned unsuitable coefficients three times. Please try Generate again.")


def feedback_for_answer(
    client: OpenAI,
    model: str,
    exercise: Exercise,
    marking: Marking,
) -> str:
    """Student-centered AI guidance grounded in independently checked facts."""
    q = exercise.quadratic
    verdict = (
        f"x-coordinate: {'correct' if marking.x_correct else 'incorrect'}; "
        f"y-coordinate: {'correct' if marking.y_correct else 'incorrect'}; "
        f"opening direction: {'correct' if marking.direction_correct else 'incorrect'}."
    )
    instructions = (
        "You are a kind and concise math teacher. Use simple A2-B1 English, "
        "1-3 sentences. Teach, do not shame. You MUST use the grading facts given "
        "by the app as authoritative, not recompute. For an incorrect response, "
        "offer ONE useful level-appropriate next step. Do not reveal the numeric "
        "vertex until the learner clicks Show solution. For correct work, provide "
        "specific praise about the method. No markdown tables."
    )
    prompt = (
        f"Difficulty: {exercise.level}. Function coefficients a={q.a}, b={q.b}, c={q.c}. "
        f"True vertex (x,y)=({fraction_label(q.vertex_x)}, {fraction_label(q.vertex_y)}). "
        f"True opening={q.opens}. The student's results: {verdict}"
    )
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt,
        store=False,
        max_output_tokens=200,
    )
    return (response.output_text or "").strip()
