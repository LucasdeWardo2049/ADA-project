import logging
from typing import List
from .model import LLMModel
from ..utils.text import split_into_chunks

logger = logging.getLogger(__name__)


class Summarizer:
    
    def __init__(self, model_name: str = "unicamp-dl/ptt5-base-portuguese-vocab"):
        self.model = LLMModel(model_name)
        self.model.load()
    
    def summarize(self, text: str, max_summary_length: int = 500) -> str:
        logger.info("Gerando resumo do texto...")
        
        if len(text) > 3000:
            logger.info("Texto longo detectado, dividindo em chunks...")
            chunks = split_into_chunks(text, max_length=1000)
            
            chunk_summaries = []
            for i, chunk in enumerate(chunks[:5]):
                logger.info(f"Resumindo chunk {i+1}/{min(len(chunks), 5)}")
                prompt = f"resume o seguinte texto em português: {chunk}"
                summary = self.model.generate_text(prompt, max_length=200, min_length=30)
                chunk_summaries.append(summary)
            
            combined = " ".join(chunk_summaries)
            prompt = f"faça um resumo consolidado em português: {combined}"
            final_summary = self.model.generate_text(prompt, max_length=max_summary_length, min_length=100)
        else:
            prompt = f"resume o seguinte texto em português: {text[:2000]}"
            final_summary = self.model.generate_text(prompt, max_length=max_summary_length, min_length=50)
        
        logger.info("Resumo gerado com sucesso")
        return final_summary
    
    def cleanup(self) -> None:
        self.model.unload()
