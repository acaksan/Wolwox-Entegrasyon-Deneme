import datetime
import os
import shutil
from pathlib import Path

import boto3
from src.core.config import get_settings

settings = get_settings()

def create_backup():
    """Veritabanı ve uygulama verilerinin yedeğini alır"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(settings.BACKUP_PATH) / timestamp
    
    try:
        # Dizini oluştur
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Firebird veritabanı yedeği
        os.system(f'gbak -b {settings.FIREBIRD_DATABASE} {backup_dir}/database.fbk')
        
        # Redis verilerini yedekle
        os.system(f'redis-cli save && cp /var/lib/redis/dump.rdb {backup_dir}/redis.rdb')
        
        # Dosyaları sıkıştır
        shutil.make_archive(str(backup_dir), 'zip', backup_dir)
        
        # S3'e yükle
        if settings.AWS_BACKUP_ENABLED:
            s3 = boto3.client('s3')
            s3.upload_file(
                f'{backup_dir}.zip',
                settings.AWS_BUCKET_NAME,
                f'backups/{timestamp}.zip'
            )
            
        # Eski yedekleri temizle
        cleanup_old_backups()
        
        return True
    except Exception as e:
        print(f"Backup error: {str(e)}")
        return False

def cleanup_old_backups():
    """30 günden eski yedekleri siler"""
    retention_days = settings.BACKUP_RETENTION_DAYS
    backup_dir = Path(settings.BACKUP_PATH)
    
    for backup in backup_dir.glob('*'):
        if backup.is_dir():
            age = datetime.datetime.now() - datetime.datetime.fromtimestamp(backup.stat().st_mtime)
            if age.days > retention_days:
                shutil.rmtree(backup)

if __name__ == "__main__":
    create_backup() 