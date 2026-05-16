"""Regression test: PEP 723 inline-script metadata must parse as valid TOML.

Why this exists: convert.py once shipped with narrative prose lines inside its
`# /// script` fence. `uv run` parses that fence as strict TOML, so the script
failed at first invocation with `key with no value, expected '='`. The fix
moved the prose above the fence. This test locks the contract so a future edit
can't silently reintroduce the same shape.

Scope is intentionally narrow: we don't validate dependency syntax or version
specifiers — just that the block round-trips through a TOML parser.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# tomllib landed in the stdlib in 3.11. Below that we'd need an external dep
# (tomli); skip rather than adding one for a regression-only smoke test.
tomllib = pytest.importorskip("tomllib")

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = [
    REPO_ROOT / "skill" / "scripts" / "convert.py",
    REPO_ROOT / "skill" / "scripts" / "merge.py",
]

PEP723_BLOCK = re.compile(
    r"^# /// script\s*\n(?P<body>(?:#(?: .*)?\n)*?)# ///\s*$",
    re.MULTILINE,
)


def _strip_pep723_comments(block_body: str) -> str:
    """Convert PEP 723 comment-fenced TOML back to raw TOML.

    Each metadata line is prefixed with `# ` (or `#` for blank lines). The
    PEP-723 reading recipe strips that prefix to recover the embedded TOML.
    """
    lines = []
    for line in block_body.splitlines():
        if line.startswith("# "):
            lines.append(line[2:])
        elif line.startswith("#"):
            lines.append(line[1:])
        else:
            # PEP 723 mandates every block line begin with `#`; bail loudly
            # so a malformed comment-prefix shape doesn't pass silently.
            raise AssertionError(f"non-comment line inside PEP 723 block: {line!r}")
    return "\n".join(lines)


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_pep723_block_parses_as_toml(script: Path) -> None:
    src = script.read_text(encoding="utf-8")
    match = PEP723_BLOCK.search(src)
    assert match is not None, f"no PEP 723 block found in {script}"
    toml_body = _strip_pep723_comments(match.group("body"))
    # tomllib.loads raises tomllib.TOMLDecodeError on any structural problem;
    # letting that propagate is the test's whole point.
    parsed = tomllib.loads(toml_body)
    # Sanity: every supported script declares its runtime + deps.
    assert "requires-python" in parsed, f"{script} missing requires-python"
    assert "dependencies" in parsed, f"{script} missing dependencies"
