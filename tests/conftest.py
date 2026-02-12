import sys
from pathlib import Path

import pytest

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from convert import DEFAULT_COLORS, DEFAULT_FONTS


@pytest.fixture
def colors():
    return dict(DEFAULT_COLORS)


@pytest.fixture
def fonts():
    return dict(DEFAULT_FONTS)


@pytest.fixture
def sample_section_md():
    return "# Section Title\n\n### Subtitle here"


@pytest.fixture
def sample_content_md():
    return (
        "## Slide Title\n\n"
        "- Bullet one\n"
        "- Bullet **bold** two\n"
        "1. Numbered item\n"
        "\n"
        "```python\nprint('hi')\n```\n"
        "\n"
        "note:\nSpeaker notes here"
    )


@pytest.fixture
def tmp_output_dir(tmp_path):
    return tmp_path
