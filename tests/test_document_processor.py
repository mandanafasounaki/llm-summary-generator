from io import BytesIO
from pathlib import Path

import pytest
from docx import Document
from reportlab.pdfgen import canvas


def create_test_pdf(tmp_path: Path, content: str) -> Path:
    """Create a real PDF file with the given content"""
    file_path = tmp_path / "test.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, content)
    c.save()
    file_path.write_bytes(buffer.getvalue())
    return file_path


def create_test_txt(tmp_path: Path, content: str) -> Path:
    """Create a text file with the given content"""
    file_path = tmp_path / "test.txt"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def create_test_docx(tmp_path: Path, content: str) -> Path:
    """Create a Word document with the given content"""
    file_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph(content)
    doc.save(str(file_path))
    return file_path


def create_test_file(tmp_path: Path, content: str, suffix: str) -> Path:
    file_path = tmp_path / f"test{suffix}"
    file_path.write_text(content)
    return file_path


class TestDocumentProcessor:
    TEXT = """AI-powered agents are an emerging field with no established theoretical frameworks fordefining, developing, 
        and evaluating them. This section is a best-effort attempt to build aframework from the existing literature, but it will evolve as the field does. 
        Compared to therest of the book, this section is more experimental. I received helpful feedback from earlyreviewers, and I hope to get feedback from readers of 
        this blog post, too.
        2. before this book came out, Anthropic published a blog post on Building effective agents(Dec 2024). 
        I’m glad to see that Anthropic’s blog post and my agent section are conceptually aligned, 
        though with slightly different terminologies. However, Anthropic’spost focuses on isolated patterns,
        whereas my post covers why and how things work. I alsofocus more on planning, tool selection, and failure modes.
        3.The post contains a lot of background information. Feel free to skip ahead if it feels a littletoo in the weeds!
        """

    def test_pdf_processing(self, tmp_path, document_processor, settings):
        file_path = create_test_pdf(tmp_path, self.TEXT)

        # Initialize processor with settings
        processor = document_processor

        # Process the PDF
        result = processor.extract_text(str(file_path))

        # Verify results
        assert isinstance(result, str)
        assert len(result) > 0

    def test_txt_processing(self, tmp_path, document_processor, settings):
        # Create text file
        file_path = create_test_txt(tmp_path, self.TEXT)

        # Initialize processor with settings
        processor = document_processor

        # Process the text file
        result = processor.extract_text(str(file_path))

        # Verify results
        assert isinstance(result, str)
        assert len(result) > 0

    def test_docx_processing(self, tmp_path, document_processor, settings):
        # Create Word document
        file_path = create_test_docx(tmp_path, self.TEXT)

        # Initialize processor with settings
        processor = document_processor

        # Process the Word document
        result = processor.extract_text(str(file_path))

        # Verify results
        assert isinstance(result, str)
        assert len(result) > 0

    def test_unsupported_format(self, tmp_path, document_processor):
        file_path = create_test_file(tmp_path, "Test content", ".xyz")
        with pytest.raises(ValueError, match="Unsupported format"):
            document_processor.extract_text(str(file_path))

    def test_file_not_found(self, document_processor):
        with pytest.raises(FileNotFoundError):
            document_processor.extract_text("nonexistent.txt")

    def test_empty_file(self, tmp_path, document_processor):
        file_path = create_test_file(tmp_path, "", ".txt")
        result = document_processor.extract_text(str(file_path))
        assert result == ""

    def test_large_file(self, tmp_path, document_processor, settings):
        # Create a file larger than the limit
        large_content = "x" * (settings.MAX_FILE_SIZE + 1)
        file_path = create_test_file(tmp_path, large_content, ".txt")
        with pytest.raises(ValueError, match="File size exceeds limit"):
            document_processor.extract_text(str(file_path))
