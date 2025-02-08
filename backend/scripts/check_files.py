import sys
from pathlib import Path


def check_test_files():
    """Test dosyalarının varlığını ve yapısını kontrol et"""
    
    # Kontrol edilecek dosyalar
    files_to_check = [
        "tests/integration/test_woo_service.py",
        "tests/integration/test_woocommerce_integration.py",
        "tests/e2e/test_order_flow.py",
        "src/services/woocommerce_product_service.py",
        ".env",
        "requirements-dev.txt"
    ]
    
    # Proje kök dizinini bul
    project_root = Path(__file__).parent.parent
    
    print("\n📁 Dosya Kontrolleri:")
    print("="*50)
    
    all_exist = True
    for file_path in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ Mevcut: {file_path}")
            
            # Test dosyaları için içerik kontrolü
            if file_path.endswith("test_woo_service.py"):
                content = full_path.read_text()
                print("\n📝 test_woo_service.py içeriği:")
                print("-"*50)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-"*50)
        else:
            print(f"❌ Eksik: {file_path}")
            all_exist = False
    
    # Pytest kontrolü
    try:
        import pytest
        print(f"\n✅ pytest versiyonu: {pytest.__version__}")
    except ImportError:
        print("\n❌ pytest yüklü değil!")
        all_exist = False
    
    # Python path kontrolü
    print("\n🔍 Python Path:")
    for path in sys.path:
        print(f"  - {path}")
    
    return all_exist

if __name__ == "__main__":
    if check_test_files():
        print("\n✅ Tüm dosya kontrolleri başarılı!")
        sys.exit(0)
    else:
        print("\n❌ Bazı dosyalar eksik veya hatalı!")
        sys.exit(1) 