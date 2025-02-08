print("1. Script başladı")

try:
    print("2. Import denenecek")
    import fdb
    print("3. Import başarılı")
    
except Exception as e:
    print("HATA:", str(e))

print("4. Script bitti")
input("Bitirmek için ENTER'a basın...") 