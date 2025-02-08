"""Import düzeltme scripti"""

import os
import re
from pathlib import Path


def fix_imports(file_path: str) -> None:
    """Bir Python dosyasındaki importları düzeltir"""
    
    # Farklı encoding'leri dene
    encodings = ['utf-8', 'latin1', 'cp1254', 'iso-8859-9']
    content = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print(f"HATA: {file_path} dosyası okunamadı!")
        return
    
    # Relative importları absolute importlara çevir
    patterns = [
        (r'from core\.', 'from src.core.'),
        (r'from utils\.', 'from src.utils.'),
        (r'from api\.', 'from src.api.'),
        (r'from wolvox\.', 'from src.wolvox.'),
        (r'from database\.', 'from src.database.'),
        (r'from models\.', 'from src.models.'),
        (r'from services\.', 'from src.services.'),
        (r'from logging import', 'from src.utils.logger import'),
        (r'from core\.logging import', 'from src.utils.logger import'),
        (r'import core\.', 'import src.core.'),
        (r'import utils\.', 'import src.utils.'),
        (r'import api\.', 'import src.api.'),
        (r'import wolvox\.', 'import src.wolvox.'),
        (r'import database\.', 'import src.database.'),
        (r'import models\.', 'import src.models.'),
        (r'import services\.', 'import src.services.'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    if modified:
        print(f"Fixing imports in: {file_path}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"HATA: {file_path} dosyası yazılamadı! Hata: {str(e)}")

def process_directory(directory: str) -> None:
    """Bir dizindeki tüm Python dosyalarını işler"""
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_imports(file_path)

if __name__ == '__main__':
    # src dizinindeki tüm Python dosyalarını düzelt
    src_dir = Path(__file__).parent / 'src'
    process_directory(str(src_dir))
    print("Import düzeltme işlemi tamamlandı!")
