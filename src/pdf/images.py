import logging
from pathlib import Path
from typing import List
import fitz

from ..utils.files import ensure_directory, get_unique_filename

logger = logging.getLogger(__name__)


class ImageExtractor:
    
    def __init__(self, pdf_path: str):
        """Inicializa o extrator de imagens com tratamento de erros."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
        
        try:
            self.doc = fitz.open(pdf_path)
            logger.info(f"PDF carregado para extração de imagens: {pdf_path}")
        except fitz.FileDataError as error:
            logger.error(f"PDF inválido ou corrompido: {error}")
            raise ValueError("Não foi possível abrir o PDF para extração de imagens") from error
        except Exception as error:
            logger.error(f"Erro ao abrir PDF: {error}")
            raise
    
    def extract_images(self, output_dir: str = None) -> List[str]:
        if output_dir is None:
            pdf_name = self.pdf_path.stem
            output_dir = f"imagens/{pdf_name}"
        
        output_path = ensure_directory(output_dir)
        extracted_images = []
        
        logger.info(f"Extraindo imagens para: {output_path}")
        
        image_counter = 0
        total_pages = len(self.doc)
        
        for page_num in range(total_pages):
            try:
                page = self.doc[page_num]
                image_list = page.get_images()
                
                if (page_num + 1) % 20 == 0:
                    logger.debug(f"Processando imagens: página {page_num + 1}/{total_pages}")
                
                for img_index, img_info in enumerate(image_list):
                    try:
                        xref = img_info[0]
                        base_image = self.doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        base_name = f"page{page_num + 1}_img{img_index + 1}"
                        filename = get_unique_filename(output_path, base_name, image_ext)
                        image_path = output_path / filename
                        
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        
                        extracted_images.append(str(image_path))
                        image_counter += 1
                        logger.debug(f"Imagem extraída: {filename}")
                        
                    except MemoryError:
                        logger.error(f"Memória insuficiente ao extrair imagem {img_index + 1} da página {page_num + 1}")
                        continue
                    except (IOError, OSError) as error:
                        logger.warning(f"Erro de I/O ao salvar imagem {img_index + 1}: {error}")
                        continue
                    except Exception as error:
                        logger.warning(f"Erro ao extrair imagem {img_index + 1} da página {page_num + 1}: {error}")
                        continue
                        
            except Exception as error:
                logger.warning(f"Erro ao processar página {page_num + 1} para imagens: {error}")
                continue
        
        logger.info(f"Total de imagens extraídas: {image_counter}")
        return extracted_images
    
    def count_images(self) -> int:
        total = 0
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            total += len(page.get_images())
        return total
    
    def close(self):
        if self.doc:
            self.doc.close()
            logger.info("PDF fechado (extração de imagens)")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
