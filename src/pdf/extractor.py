import logging
from pathlib import Path
from typing import Dict, Any
import fitz

from ..utils.text import count_words, get_vocabulary_size, get_most_common_words
from ..utils.files import get_file_size

logger = logging.getLogger(__name__)


class PDFExtractor:
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
        
        self.doc = fitz.open(pdf_path)
        logger.info(f"PDF carregado: {pdf_path}")
    
    def extract_text(self) -> str:
        text_parts = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text_parts.append(page.get_text())
        
        full_text = '\n'.join(text_parts)
        logger.info(f"Texto extraído: {len(full_text)} caracteres")
        return full_text
    
    def get_page_count(self) -> int:
        return len(self.doc)
    
    def get_file_size(self) -> int:
        return get_file_size(str(self.pdf_path))
    
    def analyze(self) -> Dict[str, Any]:
        logger.info("Iniciando análise do PDF...")
        
        text = self.extract_text()
        page_count = self.get_page_count()
        file_size = self.get_file_size()
        word_count = count_words(text)
        vocabulary_size = get_vocabulary_size(text)
        most_common = get_most_common_words(text, n=10)
        
        analysis = {
            'file_path': str(self.pdf_path),
            'file_name': self.pdf_path.name,
            'page_count': page_count,
            'file_size_bytes': file_size,
            'word_count': word_count,
            'vocabulary_size': vocabulary_size,
            'most_common_words': most_common,
            'full_text': text
        }
        
        logger.info("Análise completa")
        return analysis
    
    def close(self):
        if self.doc:
            self.doc.close()
            logger.info("PDF fechado")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
