import os
import shutil
from pathlib import Path


def setup_environment():
    """Uygulama çalışma ortamını hazırlar"""
    # Src dizinini bul
    src_dir = Path(__file__).parent.parent
    
    # Gerekli dizinleri oluştur
    os.makedirs(src_dir / "logs", exist_ok=True)
    
    # .env dosyasını kontrol et
    env_file = src_dir / ".env"
    env_example = src_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f".env dosyası oluşturuldu: {env_file}")
        print("Lütfen .env dosyasındaki değerleri güncelleyin!")
    
    return True

if __name__ == "__main__":
    setup_environment() 