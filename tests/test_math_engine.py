"""Offline mathematical checks for the Grade 9 graph tutor."""
from fractions import Fraction

import pytest

from math_engine import Quadratic, check_answer, fraction_label, terms, validate_level, verified_steps


def test_vertex_calculation_exact():
    q = Quadratic(2, -6, 1)
    assert q.vertex_x == Fraction(3, 2)
    assert q.vertex_y == Fraction(-7, 2)
    assert q.opens == "Upward"


def test_downward_projectile():
    q = Quadratic(-2, 8, 1)
    assert q.vertex_x == 2
    assert q.vertex_y == 9
    assert q.opens == "Downward"
    assert "9 metres" in verified_steps(q, advanced=True)[-1]


def test_a_cannot_be_zero():
    with pytest.raises(ValueError):
        Quadratic(0, 1, 2)


@pytest.mark.parametrize(
    ("q", "level", "expected"),
    [
        (Quadratic(1, 0, -4), "Foundation", True),
        (Quadratic(2, 0, 1), "Foundation", False),
        (Quadratic(2, -5, 3), "Standard", True),
        (Quadratic(1, 0, 5), "Standard", False),
        (Quadratic(-3, 6, 2), "Advanced", True),
        (Quadratic(3, 6, 2), "Advanced", False),
    ],
)
def test_levels(q, level, expected):
    assert validate_level(q, level) is expected


def test_answer_marking_and_tolerance():
    q = Quadratic(1, -2, -3)
    assert check_answer(q, 1, -4, "Upward").all_correct
    result = check_answer(q, 1.2, -4, "Downward")
    assert result.correct_count == 1


def test_pretty_latex():
    assert terms(1, -2, 3) == "x^2 - 2x + 3"
    assert fraction_label(Fraction(3, 2)) == "3/2"
