import random
from datetime import datetime
from models.Gonderi import Gonderi
from utils.JsonIsleyicisi import JsonIsleyicisi


class GonderiYonetici:
    """
    Gönderi iş mantığını yöneten Controller sınıfı.
    Veriler bellekte liste olarak tutulur; her işlemde
    JsonIsleyicisi aracılığıyla veritabanına yazılır.
    """

    def __init__(self):
        self._json = JsonIsleyicisi()
        # Güncelleme: .oku yerine .veriOku metodu kullanıldı
        self.gonderiler: list[Gonderi] = self._json_to_gonderiler(
            self._json.veriOku("gonderiler")
        )

    def gonderi_olustur(self, yazarld: int, icerik: str) -> dict:
        """Yeni bir gönderi oluşturur."""
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

    def gonderi_sil(
        self,
        gonderild: int,
        yazarld: int,
        yorum_yonetici=None,
        begeni_yonetici=None
    ) -> dict:
        """
        Bir gönderiyi siler. Yalnızca gönderinin sahibi silebilir.
        Silinince bağlı yorumlar ve beğeniler de temizlenir.
        """
        gonderi = self._gonderi_bul(gonderild)
        if gonderi is None:
            return {"basarili": False, "hata": "Gönderi bulunamadı."}

        if gonderi.yazarld != yazarld:
            return {"basarili": False, "hata": "Bu gönderiyi silme yetkiniz yok."}

        self.gonderiler.remove(gonderi)
        self._kaydet()

        # Güncelleme: Diğer sınıfların temizleme metot isimleri (gonderi_silinince_temizle) ile eşitlendi
        if yorum_yonetici is not None:
            yorum_yonetici.gonderi_silinince_temizle(gonderild)

        if begeni_yonetici is not None:
            begeni_yonetici.gonderi_silinince_temizle(gonderild)

        return {"basarili": True}

    def gonderi_duzenle(self, gonderild: int, yazarld: int, yeni_icerik: str) -> dict:
        """Mevcut bir gönderinin içeriğini günceller."""
        if not yeni_icerik or not yeni_icerik.strip():
            return {"basarili": False, "hata": "Güncellenmiş içerik boş olamaz."}

        gonderi = self._gonderi_bul(gonderild)
        if gonderi is None:
            return {"basarili": False, "hata": "Gönderi bulunamadı."}

        if gonderi.yazarld != yazarld:
            return {"basarili": False, "hata": "Bu gönderiyi düzenleme yetkiniz yok."}

        gonderi.icerik = yeni_icerik.strip()
        gonderi.tarih = datetime.now()

        self._kaydet()

        return {"basarili": True, "gonderi": gonderi}

    def tum_gonderileri_getir(self) -> list:
        """Tüm gönderileri döndürür."""
        return list(self.gonderiler)

    def kullanici_gonderilerini_getir(self, yazarld: int) -> list:
        """Belirli bir kullanıcının gönderilerini döndürür (profil sayfası)."""
        return [g for g in self.gonderiler if g.yazarld == yazarld]

    def gonderi_getir(self, gonderild: int):
        """ID'ye göre tekil gönderi döndürür; bulunamazsa None."""
        return self._gonderi_bul(gonderild)

    def _gonderi_bul(self, gonderild: int):
        for g in self.gonderiler:
            if g.gonderild == gonderild:
                return g
        return None

    def _yeni_id_uret(self) -> int:
        """8 haneli benzersiz rastgele ID üretir."""
        mevcut_idler = {g.gonderild for g in self.gonderiler}
        while True:
            yeni = random.randint(10000000, 99999999)
            if yeni not in mevcut_idler:
                return yeni

    def _json_to_gonderiler(self, veri: list) -> list:
        """JSON'dan okunan dict listesini Gonderi nesnelerine çevirir."""
        gonderiler = []
        if not veri:
            return gonderiler
        for d in veri:
            g = Gonderi(
                gonderild=d["gonderild"],
                yazarld=d["yazarld"],
                icerik=d["icerik"],
                tarih=datetime.fromisoformat(d["tarih"])
                if isinstance(d["tarih"], str) else d["tarih"]
            )
            gonderiler.append(g)
        return gonderiler

    def _kaydet(self):
        """Bellekteki gönderi listesini JSON'a yazar."""
        veri = [
            {
                "gonderild": g.gonderild,
                "yazarld": g.yazarld,
                "icerik": g.icerik,
                "tarih": g.tarih.isoformat()
                if isinstance(g.tarih, datetime) else g.tarih
            }
            for g in self.gonderiler
        ]
        # Güncelleme: .yaz yerine .veriYaz metodu kullanıldı
        self._json.veriYaz("gonderiler", veri)