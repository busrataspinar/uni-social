import json
import os

class JsonIsleyicisi:
    """
    Python sözlükleri ile fiziksel JSON dosyaları arasındaki çift yönlü veri akışını yöneten köprü sınıftır.
    """
    def __init__(self, veri_dizini="data"):
        self.veri_dizini = veri_dizini
        if not os.path.exists(self.veri_dizini):
            os.makedirs(self.veri_dizini)

    def verileri_yukle(self, dosya_adi):
        """
        Belirtilen JSON dosyasından verileri okur ve Python listesine/sözlüğüne dönüştürür.
        Dosya bulunamazsa boş bir liste döndürür.
        """
        dosya_yolu = os.path.join(self.veri_dizini, f"{dosya_adi}.json")

        if not os.path.exists(dosya_yolu):
            return []

        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def verileri_kaydet(self, dosya_adi, veri):
        """
        Verileri JSON formatında kalıcı olarak dosyaya yazar.
        İşlem başarılıysa True, hata oluşursa False döndürür.
        """
        dosya_yolu = os.path.join(self.veri_dizini, f"{dosya_adi}.json")

        try:
            with open(dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(veri, f, ensure_ascii=False, indent=4)
            return True
        except IOError:
            return False