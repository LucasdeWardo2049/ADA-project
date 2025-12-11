import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.pdf.extractor import PDFExtractor


class TestPDFExtractor(unittest.TestCase):
    
    def test_init_with_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            PDFExtractor("arquivo_inexistente.pdf")
    
    @patch('src.pdf.extractor.fitz')
    def test_get_page_count(self, mock_fitz):
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 10
        mock_fitz.open.return_value = mock_doc
        
        with patch.object(Path, 'exists', return_value=True):
            extractor = PDFExtractor("teste.pdf")
            self.assertEqual(extractor.get_page_count(), 10)
    
    @patch('src.pdf.extractor.fitz')
    def test_extract_text_basic(self, mock_fitz):
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Texto da página"
        
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        
        mock_fitz.open.return_value = mock_doc
        
        with patch.object(Path, 'exists', return_value=True):
            extractor = PDFExtractor("teste.pdf")
            text = extractor.extract_text()
            self.assertIn("Texto da página", text)
    
    @patch('src.pdf.extractor.fitz')
    def test_detect_titles(self, mock_fitz):
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 0
        mock_fitz.open.return_value = mock_doc
        
        with patch.object(Path, 'exists', return_value=True):
            extractor = PDFExtractor("teste.pdf")
            titles = extractor.detect_titles()
            self.assertIsInstance(titles, list)
    
    @patch('src.pdf.extractor.fitz')
    def test_detect_sections(self, mock_fitz):
        mock_page = MagicMock()
        mock_page.get_text.return_value = "1. Introdução\n2. Desenvolvimento"
        
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        
        mock_fitz.open.return_value = mock_doc
        
        with patch.object(Path, 'exists', return_value=True):
            extractor = PDFExtractor("teste.pdf")
            sections = extractor.detect_sections()
            self.assertIsInstance(sections, list)
    
    @patch('src.pdf.extractor.fitz')
    def test_context_manager(self, mock_fitz):
        mock_doc = MagicMock()
        mock_fitz.open.return_value = mock_doc
        
        with patch.object(Path, 'exists', return_value=True):
            with PDFExtractor("teste.pdf") as extractor:
                self.assertIsNotNone(extractor)
            
            mock_doc.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
