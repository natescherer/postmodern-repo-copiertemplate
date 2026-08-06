"""Confirms copier.yml.jinja's `validator:` constraints actually reject bad answers.

Generic mechanism, repo-specific data: this module only knows how to attempt a copy and
assert it fails with a given message; which combinations should be rejected, and why,
lives in answer_matrix.py's INVALID_ANSWER_MATRIX.
"""

import pytest
from answer_matrix import INVALID_ANSWER_MATRIX
from conftest import _run

_META_KEYS = {"id", "expected_error"}


@pytest.mark.parametrize("answers", INVALID_ANSWER_MATRIX, ids=lambda a: a["id"])
def test_invalid_combination_rejected(template_source, tmp_path, answers):
    """Verify a known-invalid answer combination is rejected, not silently accepted."""
    args = ["copier", "copy", "--trust", "--defaults", "--skip-tasks"]
    for key, value in answers.items():
        if key in _META_KEYS:
            continue
        args.extend(["-d", f"{key}={value}"])
    args.extend([str(template_source), str(tmp_path / "out")])
    result = _run(args)

    expected_error = answers["expected_error"]
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode != 0, (  # noqa: S101
        f"expected copier copy to reject this combination, but it succeeded:\n{answers}"
    )
    assert expected_error in result.stderr, (  # noqa: S101
        f"expected {expected_error!r} in stderr, got:\n{result.stderr}"
    )
