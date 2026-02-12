import json

import pytest

from convert import load_config


class TestLoadConfig:
    def test_json_config(self, tmp_path):
        md = tmp_path / "slides.md"
        md.write_text("# test")
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"colors": {"primary": "FF0000"}}))
        result = load_config(str(md))
        assert result["colors"]["primary"] == "FF0000"

    def test_yaml_config(self, tmp_path):
        yaml = pytest.importorskip("yaml")
        md = tmp_path / "slides.md"
        md.write_text("# test")
        cfg = tmp_path / "config.yaml"
        cfg.write_text("colors:\n  primary: '00FF00'\n")
        result = load_config(str(md))
        assert result["colors"]["primary"] == "00FF00"

    def test_no_config_returns_empty(self, tmp_path):
        md = tmp_path / "slides.md"
        md.write_text("# test")
        result = load_config(str(md))
        assert result == {}

    def test_malformed_json_returns_empty(self, tmp_path):
        md = tmp_path / "slides.md"
        md.write_text("# test")
        cfg = tmp_path / "config.json"
        cfg.write_text("{invalid json!!")
        result = load_config(str(md))
        assert result == {}
