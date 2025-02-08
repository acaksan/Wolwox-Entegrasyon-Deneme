print("Script başladı")

try:
    print("1. Import öncesi")
    import fdb  # firebird.driver yerine fdb kullanalım
    print("2. fdb import edildi")
    
    # DLL yolunu ayarla
    fdb.load_api(r"C:\Program Files (x86)\Firebird\Firebird_2_5\bin\fbclient.dll")
    print("3. DLL yüklendi")
    
    # Bağlantıyı dene
    conn = fdb.connect(
        dsn=r'D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB',
        user='SYSDBA',
        password='masterkey'
    )
    print("4. Bağlantı başarılı!")
    
    conn.close()
    print("5. Bağlantı kapatıldı")

except ImportError as e:
    print(f"\n❌ Import Hatası:")
    print(f"Hata mesajı: {str(e)}")
    
except Exception as e:
    print(f"\n❌ Genel Hata:")
    print(f"Hata tipi: {type(e).__name__}")
    print(f"Hata mesajı: {str(e)}")

print("\nScript bitti")
input("Devam etmek için ENTER'a basın...") 