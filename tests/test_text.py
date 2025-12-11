import unittest
from src.utils.text import (
    clean_text,
    tokenize,
    count_words,
    get_vocabulary_size,
    get_most_common_words,
    remove_accents,
    normalize_unicode,
    split_into_chunks
)


class TestTextUtils(unittest.TestCase):
    
    def test_clean_text_basic(self):
        text = "Olá,  mundo!  123  ##"
        result = clean_text(text, advanced=False)
        self.assertIsInstance(result, str)
        self.assertNotIn("##", result)
    
    def test_clean_text_advanced(self):
        text = "desenvolvi-\nmento de software"
        result = clean_text(text, advanced=True)
        self.assertIn("desenvolvimento", result)
    
    def test_tokenize_simple(self):
        text = "Python é uma linguagem"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 4)
        self.assertIn("python", tokens)
        self.assertIn("linguagem", tokens)
    
    def test_count_words(self):
        text = "um dois três quatro cinco"
        count = count_words(text)
        self.assertEqual(count, 5)
    
    def test_count_words_empty(self):
        count = count_words("")
        self.assertEqual(count, 0)
    
    def test_get_vocabulary_size(self):
        text = "python python java java c"
        vocab = get_vocabulary_size(text)
        self.assertEqual(vocab, 3)
    
    def test_get_most_common_words(self):
        text = "python python java java java c"
        common = get_most_common_words(text, n=2, remove_stopwords=False)
        self.assertEqual(len(common), 2)
        self.assertEqual(common[0][0], "java")
        self.assertEqual(common[0][1], 3)
    
    def test_remove_accents(self):
        text = "São Paulo, José, Ação"
        result = remove_accents(text)
        self.assertEqual(result, "Sao Paulo, Jose, Acao")
    
    def test_normalize_unicode(self):
        text = "café"
        result = normalize_unicode(text)
        self.assertIsInstance(result, str)
    
    def test_split_into_chunks(self):
        text = " ".join(["palavra"] * 100)
        chunks = split_into_chunks(text, max_length=50)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 60)


if __name__ == '__main__':
    unittest.main()
