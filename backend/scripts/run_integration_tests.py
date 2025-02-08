import os
import sys

import pytest


def run_tests():
    """Tüm integration testlerini çalıştırır"""
    test_dir = "tests/integration"
    args = [
        "-v",
        "--tb=short",
        "-m", "integration",
        test_dir
    ]
    
    print("\n🔍 WooCommerce Integration Testleri Başlatılıyor...")
    result = pytest.main(args)
    
    if result == 0:
        print("\n✨ Tüm testler başarılı!")
    else:
        print("\n❌ Bazı testler başarısız!")
        sys.exit(1)

if __name__ == "__main__":
    # Python path'i ayarla
    sys.path.insert(0, os.path.abspath("."))
    run_tests() 