import gzip
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from src.core.settings import get_settings

settings = get_settings()

class LogManager:
    def __init__(self):
        self.log_dir = Path("logs")
        self.archive_dir = self.log_dir / "archive"
        self.max_log_size_mb = 100
        self.retention_days = 30
        
        # Dizinleri oluştur
        self.log_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)

    def rotate_logs(self):
        """Log dosyalarını döndürür ve arşivler"""
        current_time = datetime.now()
        
        for log_file in self.log_dir.glob("*.log"):
            # Dosya boyutunu kontrol et
            size_mb = log_file.stat().st_size / (1024 * 1024)
            if size_mb > self.max_log_size_mb:
                self._archive_log(log_file, current_time)
                
            # Dosya yaşını kontrol et
            file_age = current_time - datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_age.days > self.retention_days:
                self._archive_log(log_file, current_time)

    def _archive_log(self, log_file: Path, timestamp: datetime):
        """Log dosyasını sıkıştırıp arşivler"""
        archive_name = f"{log_file.stem}_{timestamp.strftime('%Y%m%d_%H%M%S')}.log.gz"
        archive_path = self.archive_dir / archive_name
        
        # Dosyayı sıkıştır
        with log_file.open('rb') as f_in:
            with gzip.open(archive_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Orijinal dosyayı temizle
        log_file.write_text('')

    def cleanup_archives(self):
        """Eski arşiv dosyalarını temizler"""
        current_time = datetime.now()
        for archive in self.archive_dir.glob("*.gz"):
            archive_age = current_time - datetime.fromtimestamp(archive.stat().st_mtime)
            if archive_age.days > self.retention_days * 2:  # Arşivler için 2 kat süre
                archive.unlink()

def main():
    """Ana log yönetim rutini"""
    try:
        manager = LogManager()
        manager.rotate_logs()
        manager.cleanup_archives()
    except Exception as e:
        from src.utils.error_handler import ErrorHandler
        ErrorHandler.handle_error(e, "log_management")

if __name__ == "__main__":
    main() 