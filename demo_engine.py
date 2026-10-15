"""Rule-based practice mode: works without an external AI API or payments.

Demo mode intentionally does NOT claim to be AI integration. It creates
level-appropriate randomized questions; math_engine verifies all answers.
"""
import secrets

from ai_engine import Exercise
from math_engine import Marking, Quadratic, validate_level


def generate_demo_exercise(level: str, last_coefficients=None) -> Exercise:
    """Make a fresh exercise in one of three curriculum differentiation levels."""
    if level not in ("Foundation", "Standard", "Advanced"):
        raise ValueError("Unknown level")
    q = None
    for _ in range(80):
        if level == "Foundation":
            q = Quadratic(secrets.choice((-1, 1)), 0, secrets.randbelow(13) - 6)
        elif level == "Standard":
            q = Quadratic(
                secrets.choice((-2, -1, 1, 2)),
                secrets.choice(tuple(range(-8, 0)) + tuple(range(1, 9))),
                secrets.randbelow(17) - 8,
            )
        else:
            q = Quadratic(
                secrets.choice((-4, -3, -2)),
                secrets.randbelow(9) + 4,
                secrets.randbelow(9),
            )
        if validate_level(q, level) and (q.a, q.b, q.c) != last_coefficients:
            break
    else:
        raise RuntimeError("Could not create a different demo question")

    if level == "Foundation":
        return Exercise(
            quadratic=q,
            level=level,
            title="Explore a shifted parabola",
            context="Look at the graph of this quadratic. Find the vertex (x, y) and choose whether the curve opens upward or downward.",
            hints=(
                "First look where the curve turns. That turning point is the vertex.",
                "There is no x term. The vertex is on the y-axis; check the constant term for its height.",
            ),
            learning_tip="When the function has the form f(x) = ax² + c, the vertex lies on the y-axis. A positive a opens up; a negative a opens down.",
        )
    if level == "Standard":
        return Exercise(
            quadratic=q,
            level=level,
            title="Find the turning point",
            context="Study this function and its graph. Determine the vertex coordinates and opening direction.",
            hints=(
                "The vertex lies on the axis of symmetry. Start by identifying a, b and c.",
                "Calculate x = -b/(2a), then substitute that x value into the function to find y.",
            ),
            learning_tip="For f(x) = ax² + bx + c, the axis of symmetry is x = -b/(2a). The sign of a tells you the opening direction.",
        )
    return Exercise(
        quadratic=q,
        level=level,
        title="A ball's flight",
        context="The ball's height h(t), in metres after t seconds, follows this function for t ≥ 0. Find the time and height of its highest point, and state whether the parabola opens upward or downward.",
        hints=(
            "The maximum height occurs at the vertex because the coefficient of t² is negative.",
            "Find the peak time with t = -b/(2a), then calculate the height h(t) using that time.",
        ),
        learning_tip="For downward-opening projectile graphs, the vertex gives the highest point. Interpret its horizontal coordinate as time and its vertical coordinate as height.",
    )


def demo_feedback(marking: Marking, level: str) -> str:
    """Short verified non-AI guidance, without leaking the correct vertex."""
    if marking.all_correct:
        if level == "Advanced":
            return "All three are correct! You found the time, height and direction of the maximum."
        return "All three are correct! You identified the vertex and the opening correctly."
    steps = []
    if not marking.x_correct:
        steps.append("Recheck the vertex's horizontal coordinate using -b/(2a).")
    if not marking.y_correct:
        steps.append("Substitute your vertex x-value into the function to calculate its height.")
    if not marking.direction_correct:
        steps.append("Check the sign of a: positive opens upward, negative opens downward.")
    return " ".join(steps)
