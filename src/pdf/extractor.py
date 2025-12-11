import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
import fitz
import re

from ..utils.text import count_words, get_vocabulary_size, get_most_common_words
from ..utils.files import get_file_size

logger = logging.getLogger(__name__)


class PDFExtractor:
    
    def __init__(self, pdf_path: str):
        """Inicializa o extrator de PDF com tratamento robusto de erros."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
        
        try:
            self.doc = fitz.open(pdf_path)
            logger.info(f"PDF carregado: {pdf_path} ({len(self.doc)} páginas)")
        except fitz.FileDataError as error:
            logger.error(f"PDF corrompido ou inválido: {error}")
            raise ValueError(f"Não foi possível abrir o PDF: arquivo corrompido ou inválido") from error
        except Exception as error:
            logger.error(f"Erro ao abrir PDF: {error}")
            raise
    
    def extract_text(self) -> str:
        """Extrai todo o texto do PDF com tratamento de erros por página."""
        text_parts = []
        total_pages = len(self.doc)
        
        for page_num in range(total_pages):
            try:
                page = self.doc[page_num]
                text = page.get_text()
                text_parts.append(text)
                
                if (page_num + 1) % 50 == 0:
                    logger.debug(f"Processadas {page_num + 1}/{total_pages} páginas")
                    
            except MemoryError:
                logger.error(f"Memória insuficiente ao processar página {page_num + 1}")
                raise MemoryError(f"Memória insuficiente para processar PDF grande. Tente dividir o arquivo.") from None
            except Exception as error:
                logger.warning(f"Erro ao extrair texto da página {page_num + 1}: {error}")
                text_parts.append(f"[Erro na página {page_num + 1}]")
        
        full_text = '\n'.join(text_parts)
        logger.info(f"Texto extraído: {len(full_text)} caracteres de {total_pages} páginas")
        return full_text
    
    def count_words_from_pdf(self) -> int:
        """Conta palavras usando estrutura interna do PDF (mais preciso).
        
        Usa page.get_text('words') do PyMuPDF que retorna palavras
        como o visualizador de PDF as vê, geralmente mais preciso
        que tokenização de texto.
        
        Returns:
            Número total de palavras detectadas no PDF
        """
        total_words = 0
        total_pages = len(self.doc)
        
        try:
            for page_num in range(total_pages):
                try:
                    page = self.doc[page_num]
                    words = page.get_text("words")
                    total_words += len(words)
                except Exception as error:
                    logger.warning(f"Erro ao contar palavras da página {page_num + 1}: {error}")
                    
            logger.info(f"Contagem de palavras (modo PDF): {total_words} palavras")
            return total_words
        except Exception as error:
            logger.error(f"Erro na contagem de palavras do PDF: {error}")
            return 0
    
    def detect_titles(self) -> List[str]:
        """Detecta possíveis títulos baseado no tamanho da fonte e formatação."""
        titles = []
        
        try:
            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if "lines" not in block:
                        continue
                    
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            font_size = span["size"]
                            font_flags = span["flags"]
                            
                            is_bold = font_flags & 2**4
                            is_large = font_size > 12
                            is_short = len(text.split()) <= 15
                            
                            if text and (is_bold or is_large) and is_short:
                                titles.append(text)
            
            logger.info(f"Detectados {len(titles)} possíveis títulos")
        except Exception as error:
            logger.warning(f"Erro ao detectar títulos: {error}")
        
        return titles
    
    def detect_sections(self) -> List[Dict[str, Any]]:
        """Detecta seções baseado em padrões numéricos e de texto."""
        sections = []
        section_pattern = re.compile(r'^(\d+\.?\s+|[IVX]+\.?\s+|[A-Z]\.?\s+)(.+)$', re.MULTILINE)
        
        try:
            text = self.extract_text()
            matches = section_pattern.finditer(text)
            
            for match in matches:
                section_number = match.group(1).strip()
                section_title = match.group(2).strip()
                
                if len(section_title) > 5 and len(section_title) < 200:
                    sections.append({
                        'number': section_number,
                        'title': section_title
                    })
            
            logger.info(f"Detectadas {len(sections)} seções")
        except Exception as error:
            logger.warning(f"Erro ao detectar seções: {error}")
        
        return sections
    
    def extract_keywords(self, n: int = 15) -> List[Tuple[str, int]]:
        """Extrai palavras-chave mais relevantes do documento."""
        try:
            text = self.extract_text()
            keywords = get_most_common_words(text, n=n, remove_stopwords=True)
            logger.info(f"Extraídas {len(keywords)} palavras-chave")
            return keywords
        except Exception as error:
            logger.warning(f"Erro ao extrair palavras-chave: {error}")
            return []
    
    def get_page_count(self) -> int:
        return len(self.doc)
    
    def get_file_size(self) -> int:
        return get_file_size(str(self.pdf_path))
    
    def analyze(self, word_mode: str = 'text', keep_numbers: bool = False, top_n_words: int = 10, analyze_structure: bool = True) -> Dict[str, Any]:
        """Realiza análise completa do PDF incluindo estrutura e metadados.
        
        Args:
            word_mode: 'text' para tokenização de texto ou 'pdf' para contagem nativa do PDF
            keep_numbers: Se True, números são contados como palavras (apenas modo 'text')
            top_n_words: Número de palavras mais comuns a extrair
            analyze_structure: Se True, detecta títulos, seções e palavras-chave
        
        Returns:
            Dicionário com todas as métricas e análises
        """
        logger.info("Iniciando análise do PDF...")
        
        try:
            text = self.extract_text()
            page_count = self.get_page_count()
            file_size = self.get_file_size()
            
            logger.debug(f"Analisando métricas de texto (modo: {word_mode})...")
            
            if word_mode == 'pdf':
                word_count = self.count_words_from_pdf()
                vocabulary_size = get_vocabulary_size(text, keep_numbers=keep_numbers)
                most_common = get_most_common_words(text, n=top_n_words, keep_numbers=keep_numbers)
            else:
                word_count = count_words(text, keep_numbers=keep_numbers)
                vocabulary_size = get_vocabulary_size(text, keep_numbers=keep_numbers)
                most_common = get_most_common_words(text, n=top_n_words, keep_numbers=keep_numbers)
            
            avg_words_per_page = word_count / max(page_count, 1)
            lexical_diversity = (vocabulary_size / max(word_count, 1)) * 100
            
            analysis = {
                'file_path': str(self.pdf_path),
                'file_name': self.pdf_path.name,
                'page_count': page_count,
                'file_size_bytes': file_size,
                'word_count': word_count,
                'vocabulary_size': vocabulary_size,
                'avg_words_per_page': round(avg_words_per_page, 2),
                'lexical_diversity': round(lexical_diversity, 2),
                'most_common_words': most_common,
                'full_text': text
            }
            
            if analyze_structure:
                logger.debug("Detectando estrutura do documento...")
                titles = self.detect_titles()
                sections = self.detect_sections()
                keywords = self.extract_keywords(n=15)
                
                analysis['titles'] = titles[:10]
                analysis['sections'] = sections[:20]
                analysis['keywords'] = keywords
            
            logger.info("Análise completa com sucesso")
            return analysis
            
        except MemoryError:
            logger.error("Memória insuficiente para analisar PDF")
            raise
        except Exception as error:
            logger.error(f"Erro durante análise: {error}")
            raise RuntimeError(f"Falha ao analisar PDF: {error}") from error
    
    def close(self) -> None:
        if self.doc:
            self.doc.close()
            logger.info("PDF fechado")
    
    def __enter__(self) -> 'PDFExtractor':
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
