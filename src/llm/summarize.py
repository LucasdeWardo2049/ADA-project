import logging
from typing import List
from .model import LLMModel
from ..utils.text import split_into_chunks

logger = logging.getLogger(__name__)


class Summarizer:
    
    def __init__(self, model_name: str = "unicamp-dl/ptt5-base-portuguese-vocab"):
        self.model = LLMModel(model_name)
        self.model.load()
    
    def summarize(self, text: str, max_summary_length: int = 500, deterministic: bool = False) -> str:
        """Gera resumo do texto usando LLM.
        
        Args:
            text: Texto a ser resumido
            max_summary_length: Tamanho máximo do resumo
            deterministic: Se True, gera resumos reproduzíveis
        
        Returns:
            Texto do resumo gerado
        """
        import time
        start_time = time.time()
        
        logger.info("Gerando resumo do texto...")
        logger.info(f"Modelo: {self.model.model_name} | Dispositivo: {self.model.device}")
        
        if len(text) > 3000:
            logger.info("Texto longo detectado, dividindo em chunks...")
            chunks = split_into_chunks(text, max_length=1000)
            
            chunk_summaries = []
            for i, chunk in enumerate(chunks[:5]):
                logger.info(f"Resumindo chunk {i+1}/{min(len(chunks), 5)}")
                prompt = (
                    f"Resuma o seguinte texto em português de forma clara e objetiva, "
                    f"focando nos pontos principais e conclusões:\n\n{chunk}"
                )
                summary = self.model.generate_text(
                    prompt, 
                    max_length=200, 
                    min_length=30,
                    deterministic=deterministic
                )
                chunk_summaries.append(summary)
            
            combined = " ".join(chunk_summaries)
            prompt = (
                f"Faça um resumo consolidado em até 3 parágrafos do seguinte conteúdo, "
                f"mantendo as informações mais relevantes:\n\n{combined}"
            )
            final_summary = self.model.generate_text(
                prompt, 
                max_length=max_summary_length, 
                min_length=100,
                deterministic=deterministic
            )
        else:
            prompt = (
                f"Resuma o seguinte texto em português de forma clara para um público geral, "
                f"enfatizando objetivos, metodologia e conclusões principais:\n\n{text[:2000]}"
            )
            final_summary = self.model.generate_text(
                prompt, 
                max_length=max_summary_length, 
                min_length=50,
                deterministic=deterministic
            )
        
        elapsed_time = time.time() - start_time
        logger.info(f"Resumo gerado com sucesso em {elapsed_time:.2f}s")
        return final_summary
    
    def cleanup(self) -> None:
        self.model.unload()
