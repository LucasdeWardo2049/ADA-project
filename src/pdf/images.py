import logging
from pathlib import Path
from typing import List, Optional, Any, Tuple
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
    
    def extract_images(self, output_dir: Optional[str] = None, min_size: int = 100) -> List[str]:
        """Extrai imagens do PDF com filtros de qualidade.
        
        Args:
            output_dir: Diretório de saída (None para padrão imagens/<pdf_name>)
            min_size: Tamanho mínimo em pixels (largura ou altura) para extrair imagem
        
        Returns:
            Lista de caminhos das imagens extraídas
        """
        if output_dir is None:
            pdf_name = self.pdf_path.stem
            output_dir = f"imagens/{pdf_name}"
        
        output_path = ensure_directory(output_dir)
        extracted_images = []
        
        logger.info(f"Extraindo imagens para: {output_path} (min_size: {min_size}px)")
        
        image_counter = 0
        skipped_small = 0
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
                        image_width = base_image.get("width", 0)
                        image_height = base_image.get("height", 0)
                        
                        if image_width < min_size and image_height < min_size:
                            skipped_small += 1
                            logger.debug(f"Imagem muito pequena ignorada: {image_width}x{image_height}px")
                            continue
                        
                        base_name = f"page{page_num + 1}_img{img_index + 1}"
                        filename = get_unique_filename(output_path, base_name, image_ext)
                        image_path = output_path / filename
                        
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        
                        extracted_images.append(str(image_path))
                        image_counter += 1
                        logger.debug(f"Imagem extraída: {filename} ({image_width}x{image_height}px, {image_ext})")
                        
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
        
        logger.info(f"Total de imagens extraídas: {image_counter} (ignoradas {skipped_small} muito pequenas)")
        return extracted_images
    
    def count_images(self) -> int:
        total = 0
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            total += len(page.get_images())
        return total
    
    def close(self) -> None:
        if self.doc:
            self.doc.close()
            logger.info("PDF fechado (extração de imagens)")
    
    def __enter__(self) -> 'ImageExtractor':
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
