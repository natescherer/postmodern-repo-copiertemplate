"""Checks answer_matrix.py's own completeness against copier.yml's real question set.

Generic by design: parses whatever copier.yml actually defines, rather than hardcoding
this repo's specific question names -- see answer_matrix.py for the repo-specific
answer data these checks audit, including COVERAGE_EXEMPT_QUESTIONS for any question
that has a real, deliberate reason not to be fully exercised here.
"""

import warnings
from pathlib import Path

import yaml
from answer_matrix import ANSWER_MATRIX, COVERAGE_EXEMPT_QUESTIONS


def _load_questions(template_source: Path) -> dict:
    """Load the question definitions from template_source's assembled copier.yml.

    Filters out Copier's own special top-level keys (`_answers_file`, `_tasks`, ...)
    and anything else that isn't a real question mapping.

    Returns:
        The parsed question mapping, or {} if this template doesn't support being
        further templated (no self-hosting copier.yml at all).

    """
    copier_yml = template_source / "copier.yml"
    if not copier_yml.is_file():
        return {}
    data = yaml.safe_load(copier_yml.read_text(encoding="utf-8"))
    return {
        name: value
        for name, value in data.items()
        if not name.startswith("_") and isinstance(value, dict)
    }


def _question_choices(question: dict) -> set | None:
    """Extract the set of real answer values a question's `choices:` allows.

    Returns:
        The set of choice values, or None if the question has no `choices:` at all.

    """
    choices = question.get("choices")
    if choices is None:
        return None
    if isinstance(choices, list):
        return set(choices)
    return {v["value"] if isinstance(v, dict) else v for v in choices.values()}


def test_answer_matrix_covers_all_choices(template_source):
    """Verify every choice of every question is exercised somewhere in ANSWER_MATRIX.

    A question with N choices but only ever answered with one of them means the other
    N-1 code paths it gates (`when:`/Jinja `{% if %}` branches keyed on that value)
    never get rendered by this suite at all -- silently, since nothing else here would
    notice a whole branch just never ran.
    """
    questions = _load_questions(template_source)
    errors = []
    for name, question in questions.items():
        if name in COVERAGE_EXEMPT_QUESTIONS:
            continue
        choices = _question_choices(question)
        if not choices:
            continue
        answered = {combo[name] for combo in ANSWER_MATRIX if name in combo}
        missing = choices - answered
        if missing:
            errors.append(
                f"{name!r}: no answer_matrix.py combination uses {sorted(missing)!r}"
            )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101


def test_warn_on_unanswered_required_questions(template_source):
    """Warn about a no-default question that answer_matrix.py never explicitly answers.

    Copier questions without a `default:` are required -- `copier copy --defaults`
    (used throughout this suite) raises `ValueError: Question "X" is required` if such
    a question isn't supplied via `-d`. The render tests already fail hard when that
    happens; this is a faster, more specific pointer at *which* question is the gap,
    surfaced as a warning rather than a second failure, since the render tests are what
    actually enforce this.
    """
    questions = _load_questions(template_source)
    answered_keys = {key for combo in ANSWER_MATRIX for key in combo}
    for name, question in questions.items():
        if question.get("when") is False:  # a computed value, never asked or "missing"
            continue
        if "default" not in question and name not in answered_keys:
            warnings.warn(
                f"Copier question {name!r} has no default and isn't explicitly "
                "answered by any answer_matrix.py combination -- `copier copy "
                '--defaults` will fail with "Question is required" until it is.',
                stacklevel=1,
            )
