import os
from pathlib import Path

from PIL import Image


def setup_test_environment():
    """Test ortamını hazırlar"""
    print("\n🔧 Test ortamı hazırlanıyor...")
    
    # Test veri dizinini oluştur
    test_data_dir = Path("tests/data")
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Test görseli oluştur
    test_image_path = test_data_dir / "test_image.jpg"
    if not test_image_path.exists():
        print("📸 Test görseli oluşturuluyor...")
        img = Image.new('RGB', (100, 100), color='red')
        img.save(test_image_path)
        print(f"✅ Test görseli oluşturuldu: {test_image_path}")
    
    print("✨ Test ortamı hazır!")

if __name__ == "__main__":
    setup_test_environment() 