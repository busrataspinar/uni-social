

from datetime import datetime
from models.Gonderi import Gonderi
from utils.VeriDeposu import VeriDeposu


class GonderiYonetici:
    """
    Gönderi işlemlerini yöneten Controller sınıfı.

    Bu sınıf:
    - Gönderi oluşturur
    - Gönderi siler
    - Gönderi düzenler
    - Gönderileri listeler

    Tüm veriler VeriDeposu Singleton sınıfı üzerinden ve
    saf OOP (Nesne) modelleriyle yönetilir.
    """

    def __init__(self):
        """
        Veri deposundaki ham gönderi sözlüklerini Gonderi nesnelerine
        dönüştürerek belleğe bağlar.
        """
        self.depo = VeriDeposu()

        # Depodaki ham dict listesini, korumalı Gonderi nesne listesine çeviriyoruz
        self.gonderiler: list[Gonderi] = [
            Gonderi(
                gonderiId=g["gonderId"],
                yazarId=g["yazarId"],
                icerik=g["icerik"],
                tarih=g["tarih"]
            ) for g in self.depo.tum_gonderiler
        ]

    def _depoyu_senkronize_et(self) -> None:
        """
        Bellekteki güncel Gonderi nesne listesini, VeriDeposu'nun
        beklediği ham sözlük (dict) formatına çevirerek merkezi depoyu günceller.
        """
        self.depo.tum_gonderiler = [
            {
                "gonderiId": g.gonderiId,
                "yazarId": g.yazarId,
                "icerik": g.icerik,
                "tarih": g.tarih
            } for g in self.gonderiler
        ]

    # =========================================================
    # GÖNDERİ OLUŞTURMA
    # =========================================================

    def gonderi_olustur(self, yazarId: int, icerik: str) -> dict:
        """
        Yeni gönderi oluşturur, listeye ekler ve diske kaydeder.

        Args:
            yazarId (int): Gönderiyi oluşturan kullanıcı ID
            icerik (str): Gönderi içeriği

        Returns:
            dict: İşlem sonucu ve oluşturulan Gonderi nesnesi
        """
        if not icerik or not icerik.strip():
            return {
                "basarili": False,
                "mesaj": "Gönderi içeriği boş olamaz."
            }

        # VeriDeposu'nun güvenli ve ardışık ID üretecini kullanıyoruz
        yeni_gonderi = Gonderi(
            gonderiId=self.depo.yeni_gonderi_id(),
            yazarId=yazarId,
            icerik=icerik.strip(),
            tarih=datetime.now().isoformat()
        )

        # Listeye doğrudan nesne olarak ekliyoruz
        self.gonderiler.append(yeni_gonderi)

        # Değişiklikleri merkezi depoya aktar ve kaydet
        self._depoyu_senkronize_et()
        self.depo.gonderileri_kaydet()

        return {
            "basarili": True,
            "gonderi": yeni_gonderi
        }

    # =========================================================
    # GÖNDERİ SİLME
    # =========================================================

    def gonderi_sil(
            self,
            gonderiId: int,
            aktif_kullaniciId: int,
            yorum_yonetici=None,
            begeni_yonetici=None
    ) -> dict:
        """
        Gönderi siler. Sadece gönderi sahibi silebilir.
        İlişkili yorum ve beğenileri de temizler.

        Args:
            gonderiId (int): Silinecek gönderi ID
            aktif_kullaniciId (int): İşlem yapan kullanıcı ID
            yorum_yonetici (YorumYonetici, optional): Yorum temizliği için nesne
            begeni_yonetici (BegeniYonetici, optional): Beğeni temizliği için nesne
        """
        gonderi = self.gonderi_getir(gonderiId)

        if gonderi is None:
            return {
                "basarili": False,
                "mesaj": "Gönderi bulunamadı."
            }

        # Nesne yapısına geçtiğimiz için gonderi.yazarId şeklinde kontrol ediyoruz
        if gonderi.yazarId != aktif_kullaniciId:
            return {
                "basarili": False,
                "mesaj": "Bu gönderiyi silme yetkiniz yok."
            }

        # Nesneyi listeden kaldırıyoruz
        self.gonderiler.remove(gonderi)

        # Depoyu senkronize edip diske yazıyoruz
        self._depoyu_senkronize_et()
        self.depo.gonderileri_kaydet()

        # Gönderiye ait yorumları temizle
        if yorum_yonetici:
            yorum_yonetici.gonderi_silinince_temizle(gonderiId)

        # Gönderiye ait beğenileri temizle
        if begeni_yonetici:
            begeni_yonetici.gonderi_silinince_temizle(gonderiId)

        return {
            "basarili": True,
            "mesaj": "Gönderi silindi."
        }

    # =========================================================
    # GÖNDERİ DÜZENLEME
    # =========================================================

    def gonderi_duzenle(
            self,
            gonderiId: int,
            aktif_kullaniciId: int,
            yeni_icerik: str
    ) -> dict:
        """
        Gönderi içeriğini günceller ve tarihini yeniler.
        """
        if not yeni_icerik or not yeni_icerik.strip():
            return {
                "basarili": False,
                "mesaj": "Yeni içerik boş olamaz."
            }

        gonderi = self.gonderi_getir(gonderiId)

        if gonderi is None:
            return {
                "basarili": False,
                "mesaj": "Gönderi bulunamadı."
            }

        if gonderi.yazarId != aktif_kullaniciId:
            return {
                "basarili": False,
                "mesaj": "Bu gönderiyi düzenleme yetkiniz yok."
            }

        # Değerleri nesne değişkenleri üzerinden güncelliyoruz
        gonderi.icerik = yeni_icerik.strip()
        gonderi.tarih = datetime.now().isoformat()

        # Depoyu güncelleyip kaydediyoruz
        self._depoyu_senkronize_et()
        self.depo.gonderileri_kaydet()

        return {
            "basarili": True,
            "gonderi": gonderi
        }

    # =========================================================
    # GÖNDERİ GETİRME (SORGULAR)
    # =========================================================

    def tum_gonderileri_getir(self) -> list[Gonderi]:
        """
        Sistemdeki tüm gönderi nesnelerini döndürür.
        """
        return self.gonderiler

    def kullanici_gonderilerini_getir(self, yazarId: int) -> list[Gonderi]:
        """
        Belirli kullanıcıya ait gönderi nesnelerini filtreler.
        """
        return [
            g for g in self.gonderiler
            if g.yazarId == yazarId
        ]

    def gonderi_getir(self, gonderiId: int) -> Gonderi | None:
        """
        ID'ye göre tek bir Gonderi nesnesi getirir. Bulamazsa None döner.
        """
        for gonderi in self.gonderiler:
            if gonderi.gonderiId == gonderiId:
                return gonderi

        return None