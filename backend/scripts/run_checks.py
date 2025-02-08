#!/usr/bin/env python

import os
import subprocess
import sys
from pathlib import Path


def run_test(command: str) -> None:
    """Testi çalıştır ve çıktıyı göster"""
    print(f"\nRunning: {command}")
    try:
        # Doğrudan pytest modülünü kullan
        subprocess.run(
            command.split(),  # Komutu parçala
            check=True,       # Hata durumunda exception fırlat
        )
    except subprocess.CalledProcessError as e:
        print(f"Test başarısız: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1)

def main():
    # Proje kök dizinini bul
    project_root = Path(__file__).parent.parent
    
    # Çalışma dizinini değiştir
    os.chdir(project_root)
    
    # Tek bir test çalıştır
    run_test("pytest tests/integration/test_woo_service.py -v")

if __name__ == "__main__":
    main() 