import json
import os


class JsonIsleyicisi:
    """
    Python sözlükleri ile fiziksel JSON dosyaları arasındaki
    çift yönlü veri akışını yöneten köprü sınıftır.
    Facade tasarım deseni ile alt seviye dosya işlemlerini gizler.
    """

    def __init__(self, veri_dizini="data"):
        """
        JsonIsleyicisi nesnesini başlatır.
        Belirtilen veri dizini yoksa otomatik olarak oluşturur.

        Args:
            veri_dizini (str): JSON dosyalarının saklanacağı klasör yolu.
                               Varsayılan değer 'data' klasörüdür.
        """
        self.veri_dizini = veri_dizini
        if not os.path.exists(self.veri_dizini):
            os.makedirs(self.veri_dizini)

    def veriOku(self, dosyaYolu):
        """
        Belirtilen JSON dosyasından verileri okur ve Python listesine dönüştürür.
        Dosya bulunamazsa veya bozuksa boş liste döndürür.

        Args:
            dosyaYolu (str): Okunacak JSON dosyasının adı (uzantısız).

        Returns:
            list: Dosyadan okunan veri listesi. Hata durumunda boş liste.
        """
        tam_yol = os.path.join(self.veri_dizini, f"{dosyaYolu}.json")
        if not os.path.exists(tam_yol):
            return []
        try:
            with open(tam_yol, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def veriYaz(self, dosyaYolu, veri):
        """
        Verilen Python listesini veya sözlüğü JSON formatında dosyaya yazar.
        Mevcut dosyanın üzerine yazar.

        Args:
            dosyaYolu (str): Yazılacak JSON dosyasının adı (uzantısız).
            veri (list | dict): JSON dosyasına yazılacak veri.

        Returns:
            bool: Yazma işlemi başarılıysa True, hata oluşursa False.
        """
        tam_yol = os.path.join(self.veri_dizini, f"{dosyaYolu}.json")
        try:
            with open(tam_yol, 'w', encoding='utf-8') as f:
                json.dump(veri, f, ensure_ascii=False, indent=4)
            return True
        except IOError:
            return False