import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from pptx import Presentation

CONVERT_SCRIPT = str(Path(__file__).resolve().parent.parent / "scripts" / "convert.py")
DEMO_MD = str(Path(__file__).resolve().parent.parent / "examples" / "demo.md")


class TestEndToEnd:
    def test_demo_produces_pptx(self, tmp_output_dir):
        out = str(tmp_output_dir / "output.pptx")
        result = subprocess.run(
            [sys.executable, CONVERT_SCRIPT, DEMO_MD, out],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert Path(out).exists()

    def test_output_is_valid_zip(self, tmp_output_dir):
        out = str(tmp_output_dir / "output.pptx")
        subprocess.run(
            [sys.executable, CONVERT_SCRIPT, DEMO_MD, out],
            capture_output=True, text=True,
        )
        assert zipfile.is_zipfile(out)

    def test_slide_count(self, tmp_output_dir):
        out = str(tmp_output_dir / "output.pptx")
        subprocess.run(
            [sys.executable, CONVERT_SCRIPT, DEMO_MD, out],
            capture_output=True, text=True,
        )
        prs = Presentation(out)
        assert len(prs.slides) >= 8

    def test_first_slide_title(self, tmp_output_dir):
        out = str(tmp_output_dir / "output.pptx")
        subprocess.run(
            [sys.executable, CONVERT_SCRIPT, DEMO_MD, out],
            capture_output=True, text=True,
        )
        prs = Presentation(out)
        first_slide = prs.slides[0]
        title_text = first_slide.placeholders[0].text_frame.text
        assert "My Awesome Presentation" in title_text

    def test_missing_input_exits_1(self, tmp_output_dir):
        result = subprocess.run(
            [sys.executable, CONVERT_SCRIPT, "/nonexistent/file.md"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1

    def test_custom_config(self, tmp_output_dir):
        md_file = tmp_output_dir / "test.md"
        md_file.write_text("# Custom Title\n\n- item one\n")
        config = tmp_output_dir / "config.json"
        config.write_text(json.dumps({"colors": {"primary": "FF0000"}}))
        out = str(tmp_output_dir / "out.pptx")

        result = subprocess.run(
            [sys.executable, CONVERT_SCRIPT, str(md_file), out],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert Path(out).exists()
