import re
import unicodedata
from collections import Counter
from typing import List, Tuple, Set
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def get_portuguese_stopwords() -> Set[str]:
    return set(stopwords.words('portuguese'))


def normalize_unicode(text: str) -> str:
    """Normaliza caracteres Unicode para forma NFKD."""
    return unicodedata.normalize('NFKD', text)


def remove_line_breaks_hyphens(text: str) -> str:
    """Remove hífens de quebra de linha (ex: 'desenvolvi-\nmento' -> 'desenvolvimento')."""
    return re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)


def clean_text(text: str, advanced: bool = True) -> str:
    """Limpa e normaliza texto com opções avançadas.
    
    Args:
        text: Texto a ser limpo
        advanced: Se True, aplica normalizações avançadas
    
    Returns:
        Texto limpo e normalizado
    """
    if advanced:
        text = normalize_unicode(text)
        text = remove_line_breaks_hyphens(text)
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;:!?\-]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def remove_accents(text: str) -> str:
    """Remove acentos do texto mantendo caracteres base."""
    nfkd_form = unicodedata.normalize('NFD', text)
    return ''.join([char for char in nfkd_form if not unicodedata.combining(char)])


def tokenize(text: str, advanced_clean: bool = True) -> List[str]:
    """Tokeniza texto em palavras individuais.
    
    Args:
        text: Texto a ser tokenizado
        advanced_clean: Se True, usa limpeza avançada
    
    Returns:
        Lista de tokens em minúsculas
    """
    cleaned = clean_text(text, advanced=advanced_clean)
    return [word.lower() for word in cleaned.split() if word]


def count_words(text: str) -> int:
    return len(tokenize(text))


def get_vocabulary_size(text: str) -> int:
    tokens = tokenize(text)
    return len(set(tokens))


def get_most_common_words(text: str, n: int = 10, remove_stopwords: bool = True) -> List[Tuple[str, int]]:
    tokens = tokenize(text)
    
    if remove_stopwords:
        stop_words = get_portuguese_stopwords()
        tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    counter = Counter(tokens)
    return counter.most_common(n)


def split_into_chunks(text: str, max_length: int = 1024) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
