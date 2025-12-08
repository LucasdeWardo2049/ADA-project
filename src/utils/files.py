import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_directory(path: str) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    logger.info(f"Diretório garantido: {directory}")
    return directory


def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def get_unique_filename(directory: Path, base_name: str, extension: str) -> str:
    if not extension.startswith('.'):
        extension = f'.{extension}'
    
    filename = f"{base_name}{extension}"
    counter = 1
    
    while (directory / filename).exists():
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return filename


def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"
