import random
from datetime import datetime
from models.Gonderi import Gonderi
from utils.JsonIsleyicisi import JsonIsleyicisi


class GonderiYonetici:
    """
    Gönderi iş mantığını yöneten Controller sınıfı.
    Veriler bellekte liste olarak tutulur; her işlemde
    JsonIsleyicisi aracılığıyla gonderiler.json'a yazılır.
    """

    def __init__(self):
        self._json = JsonIsleyicisi()
        # JSON'dan gelen dict listesini Gonderi nesnelerine çevir
        self.gonderiler: list[Gonderi] = self._json_to_gonderiler(
            self._json.oku("gonderiler")
        )

    # UC6 – Gönderi Paylaş

    def gonderi_olustur(self, yazarld: int, icerik: str) -> dict:
        """
        Yeni bir gönderi oluşturur.

        Parametreler:
            yazarld : Gönderiyi paylaşan kullanıcının ID'si (int)
            icerik  : Gönderi metni (str)

        Dönüş:
            {"basarili": True,  "gonderi": Gonderi}
            {"basarili": False, "hata": str}
        """
        if not icerik or not icerik.strip():
            return {"basarili": False, "hata": "Gönderi içeriği boş olamaz."}

        yeni_id = self._yeni_id_uret()

        gonderi = Gonderi(
            gonderild=yeni_id,
            yazarld=yazarld,
            icerik=icerik.strip(),
            tarih=datetime.now()
        )

        self.gonderiler.append(gonderi)
        self._kaydet()

        return {"basarili": True, "gonderi": gonderi}

