import unittest
import tempfile
import shutil
from pathlib import Path
from src.utils.files import (
    ensure_directory,
    get_file_size,
    get_unique_filename,
    format_bytes
)


class TestFilesUtils(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_ensure_directory_creates_dir(self):
        test_path = Path(self.temp_dir) / "nova_pasta"
        result = ensure_directory(str(test_path))
        self.assertTrue(result.exists())
        self.assertTrue(result.is_dir())
    
    def test_ensure_directory_existing_dir(self):
        existing_dir = Path(self.temp_dir)
        result = ensure_directory(str(existing_dir))
        self.assertEqual(result, existing_dir)
    
    def test_get_file_size(self):
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Hello World")
        size = get_file_size(str(test_file))
        self.assertGreater(size, 0)
        self.assertEqual(size, 11)
    
    def test_get_unique_filename_no_collision(self):
        directory = Path(self.temp_dir)
        filename = get_unique_filename(directory, "arquivo", "txt")
        self.assertEqual(filename, "arquivo.txt")
    
    def test_get_unique_filename_with_collision(self):
        directory = Path(self.temp_dir)
        (directory / "arquivo.txt").touch()
        (directory / "arquivo_1.txt").touch()
        
        filename = get_unique_filename(directory, "arquivo", "txt")
        self.assertEqual(filename, "arquivo_2.txt")
    
    def test_format_bytes_kb(self):
        self.assertEqual(format_bytes(1024), "1.00 KB")
    
    def test_format_bytes_mb(self):
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")
    
    def test_format_bytes_gb(self):
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.00 GB")
    
    def test_format_bytes_small(self):
        self.assertEqual(format_bytes(500), "500 bytes")
    
    def test_format_bytes_zero(self):
        self.assertEqual(format_bytes(0), "0 bytes")


if __name__ == '__main__':
    unittest.main()
