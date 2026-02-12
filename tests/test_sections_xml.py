import zipfile

from pptx import Presentation

from convert import add_content_slide, add_sections_to_pptx_file


class TestAddSectionsToPptxFile:
    def test_section_xml_injected(self, tmp_path, colors, fonts):
        prs = Presentation()
        # Add 2 slides
        for title in ["## Slide 1", "## Slide 2"]:
            data = {
                "title": title,
                "subtitle": None,
                "content": [{"type": "bullet", "text": "item", "indent": 0}],
                "notes": None,
                "is_section": False,
            }
            add_content_slide(prs, data, colors, fonts)

        out = tmp_path / "test.pptx"
        prs.save(str(out))

        sections_info = {
            1: {"name": "Section A", "count": 1},
            2: {"name": "Section B", "count": 1},
        }
        add_sections_to_pptx_file(str(out), sections_info)

        # Verify the modified pptx contains section XML
        with zipfile.ZipFile(str(out), "r") as z:
            pres_xml = z.read("ppt/presentation.xml").decode()
            assert "sectionLst" in pres_xml
            assert "Section A" in pres_xml
            assert "Section B" in pres_xml

    def test_empty_sections_noop(self, tmp_path, colors, fonts):
        prs = Presentation()
        data = {
            "title": "## T",
            "subtitle": None,
            "content": [{"type": "bullet", "text": "x", "indent": 0}],
            "notes": None,
            "is_section": False,
        }
        add_content_slide(prs, data, colors, fonts)

        out = tmp_path / "test.pptx"
        prs.save(str(out))

        # No sections with names → should not modify file
        add_sections_to_pptx_file(str(out), {1: {"name": None, "count": 1}})
        with zipfile.ZipFile(str(out), "r") as z:
            pres_xml = z.read("ppt/presentation.xml").decode()
            assert "sectionLst" not in pres_xml
