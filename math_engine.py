"""Mathematically verified quadratic-graph calculations and answer checking.

AI generates coefficients and learner-facing language. This module, rather than
an AI text prediction, computes and validates the mathematical answer.
"""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Quadratic:
    a: int
    b: int
    c: int

    def __post_init__(self) -> None:
        for value in (self.a, self.b, self.c):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError("Quadratic coefficients must be integers.")
        if self.a == 0:
            raise ValueError("The leading coefficient a must not be zero.")

    def evaluate(self, x: Fraction | float | int) -> Fraction | float:
        return self.a * x * x + self.b * x + self.c

    @property
    def vertex_x(self) -> Fraction:
        return Fraction(-self.b, 2 * self.a)

    @property
    def vertex_y(self) -> Fraction:
        return self.evaluate(self.vertex_x)

    @property
    def opens(self) -> str:
        return "Upward" if self.a > 0 else "Downward"

    @property
    def axis(self) -> Fraction:
        return self.vertex_x


def fraction_label(value: Fraction | int) -> str:
    fraction = Fraction(value)
    if fraction.denominator == 1:
        return str(fraction.numerator)
    return f"{fraction.numerator}/{fraction.denominator}"


def terms(a: int, b: int, c: int, symbol: str = "x") -> str:
    """A readable LaTeX quadratic expression, without adjacent '+ -' signs."""
    chunks = []
    for coefficient, power in [(a, 2), (b, 1), (c, 0)]:
        if coefficient == 0:
            continue
        magnitude = abs(coefficient)
        if power == 2:
            term = f"{'' if magnitude == 1 else magnitude}{symbol}^2"
        elif power == 1:
            term = f"{'' if magnitude == 1 else magnitude}{symbol}"
        else:
            term = str(magnitude)
        if not chunks:
            chunks.append(("-" if coefficient < 0 else "") + term)
        else:
            chunks.append((" - " if coefficient < 0 else " + ") + term)
    return "".join(chunks) or "0"


def validate_level(q: Quadratic, level: str) -> bool:
    """Reject unexpected AI-generated values; difficulty has hard bounds."""
    if level == "Foundation":
        return abs(q.a) == 1 and q.b == 0 and -6 <= q.c <= 6
    if level == "Standard":
        return 1 <= abs(q.a) <= 2 and 1 <= abs(q.b) <= 8 and -8 <= q.c <= 8
    if level == "Advanced":
        # A projectile-height model: h(t) = at² + bt + c, t >= 0.
        return -4 <= q.a <= -2 and 4 <= q.b <= 12 and 0 <= q.c <= 8
    raise ValueError(f"Unknown level: {level}")


@dataclass(frozen=True)
class Marking:
    x_correct: bool
    y_correct: bool
    direction_correct: bool

    @property
    def all_correct(self) -> bool:
        return self.x_correct and self.y_correct and self.direction_correct

    @property
    def correct_count(self) -> int:
        return sum((self.x_correct, self.y_correct, self.direction_correct))


def check_answer(
    q: Quadratic,
    x_value: float,
    y_value: float,
    direction: str,
    tolerance: float = 0.051,
) -> Marking:
    return Marking(
        x_correct=abs(float(q.vertex_x) - x_value) <= tolerance,
        y_correct=abs(float(q.vertex_y) - y_value) <= tolerance,
        direction_correct=direction == q.opens,
    )


def verified_steps(q: Quadratic, advanced: bool = False) -> list[str]:
    """Steps computed from exact Fraction arithmetic, not from model text."""
    symbol = "t" if advanced else "x"
    heading = "maximum height" if advanced else "turning point (vertex)"
    steps = [
        f"The coefficient a is **{q.a}**. Since a is {'positive' if q.a > 0 else 'negative'}, the parabola opens **{q.opens.lower()}**.",
        f"Use the vertex formula: ${symbol}_v = -b/(2a) = -({q.b})/[2({q.a})] = {fraction_label(q.vertex_x)}$.",
        f"Substitute into the function: ${symbol}={fraction_label(q.vertex_x)}$, so $y_v = {fraction_label(q.vertex_y)}$.",
        f"The {heading} is at **({fraction_label(q.vertex_x)}, {fraction_label(q.vertex_y)})**.",
    ]
    if advanced:
        steps.append(
            f"Interpretation: the object's highest point is **{fraction_label(q.vertex_y)} metres** at **{fraction_label(q.vertex_x)} seconds**."
        )
    return steps
