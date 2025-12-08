import logging
from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

logger = logging.getLogger(__name__)


class LLMModel:
    
    def __init__(self, model_name: str = "unicamp-dl/ptt5-base-portuguese-vocab"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Usando dispositivo: {self.device}")
        
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForSeq2SeqLM] = None
    
    def load(self):
        logger.info(f"Carregando modelo: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            logger.info("Modelo carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            logger.info("Tentando modelo alternativo: google/flan-t5-small")
            self.model_name = "google/flan-t5-small"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.model.to(self.device)
    
    def generate_text(self, prompt: str, max_length: int = 512, min_length: int = 50) -> str:
        if not self.model or not self.tokenizer:
            raise RuntimeError("Modelo não carregado. Chame load() primeiro.")
        
        logger.debug(f"Gerando texto para prompt de {len(prompt)} caracteres")
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.debug(f"Texto gerado: {len(generated_text)} caracteres")
        
        return generated_text
    
    def unload(self):
        if self.model:
            del self.model
            self.model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info("Modelo descarregado")
