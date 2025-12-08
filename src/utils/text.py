import re
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


def clean_text(text: str) -> str:
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    cleaned = clean_text(text)
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
