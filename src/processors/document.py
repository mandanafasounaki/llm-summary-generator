from ..config.settings import settings
from ..models.schemas import DocumentClass
import logging
from pathlib import Path
import pypdf 
from docx import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Process and extract text from documents.
    """
    SUPPORTED_FORMATS = {'.txt', '.pdf', '.docx'}

    def extract_text(self, file_path: Path):
        """
        Extract text from a document

        Args: 
            file_path: path to the document
        
        Returns:
            Extracted text from the document
        """
        input_doc = DocumentClass(file_path = Path(file_path))
        doc_path = input_doc.file_path
        doc_suffix = input_doc.file_path.suffix

        if doc_suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {doc_suffix}")
        
        try:
            if doc_suffix == '.pdf':
                return self._extract_from_pdf(doc_path)
            elif doc_suffix == '.docx':
                return self._extract_from_docx(doc_path)
            else:
                return self._extract_from_txt(doc_path)
        except Exception as e:
            logger.error(f"Error processing {doc_path}: {e}")
            raise


    def _extract_from_pdf(self, path: Path):
        """
        Extract text from PDF file.
        """
        with open(path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text.strip()


    def _extract_from_docx(self, path: Path):
        """
        Extract text from docx file.
        """
        doc = Document(path)
        return '\n'.join([par.text for par in doc.paragraphs])
    

    def _extract_from_txt(self, path: Path):
        """
        Extract text from txt file.
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()