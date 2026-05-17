from datetime import datetime
from models.Yorum import Yorum
from data.VeriDeposu import VeriDeposu


class YorumYonetici:
    """
    Gönderilere yapılan yorum işlemlerini yöneten Controller sınıfı.

    Tüm işlemler VeriDeposu Singleton sınıfı üzerinden ve
    saf OOP (Nesne) modelleriyle yönetilir.
    """

    def __init__(self):
        """
        Veri deposundaki ham yorum sözlüklerini Yorum nesnelerine
        dönüştürerek belleğe bağlar.
        """
        self.depo = VeriDeposu()

        # Depodaki ham dict listesini Yorum nesne listesine çeviriyoruz
        self.yorumlar: list[Yorum] = [
            Yorum(
                yorumId=y["yorumId"],
                gonderiId=y["gonderiId"],
                yazarId=y["yazarId"],
                icerik=y["icerik"],
                tarih=y["tarih"]
            ) for y in self.depo.tum_yorumlar
        ]

    def _depoyu_senkronize_et(self) -> None:
        """
        Bellekteki güncel Yorum nesne listesini, VeriDeposu'nun
        beklediği ham sözlük (dict) formatına çevirerek merkezi depoyu günceller.
        """
        self.depo.tum_yorumlar = [
            {
                "yorumId": y.yorumId,
                "gonderiId": y.gonderiId,
                "yazarId": y.yazarId,
                "icerik": y.icerik,
                "tarih": y.tarih
            } for y in self.yorumlar
        ]

    # =========================================================
    # YORUM EKLEME
    # =========================================================

    def yorumEkle(self, gonderiId: int, yazarId: int, icerik: str) -> dict:
        """
        Bir gönderinin altına yeni bir yorum nesnesi ekler ve kaydeder.
        """
        if not icerik or not icerik.strip():
            return {
                "basarili": False,
                "mesaj": "Yorum boş olamaz."
            }

        # VeriDeposu'nun güvenli ve ardışık ID üretecini kullanıyoruz
        yeni_yorum = Yorum(
            yorumId=self.depo.yeni_yorum_id(),
            gonderiId=gonderiId,
            yazarId=yazarId,
            icerik=icerik.strip(),
            tarih=datetime.now().isoformat()
        )

        # Listeye doğrudan nesne olarak ekliyoruz
        self.yorumlar.append(yeni_yorum)

        # Depoyu senkronize edip diske yazıyoruz
        self._depoyu_senkronize_et()
        self.depo.yorumlari_kaydet()

        return {
            "basarili": True,
            "yorum": yeni_yorum
        }

    # =========================================================
    # YORUM SİLME
    # =========================================================

    def yorumSil(self, yorumId: int, aktif_kullaniciId: int) -> dict:
        """
        Belirtilen yorumu sistemden siler. Sadece yorum sahibi silebilir.
        """
        yorum = self._yorum_bul(yorumId)

        if yorum is None:
            return {
                "basarili": False,
                "mesaj": "Yorum bulunamadı."
            }

        # Nesne yapısına geçtiğimiz için nokta (.) notasyonuyla erişiyoruz
        if yorum.yazarId != aktif_kullaniciId:
            return {
                "basarili": False,
                "mesaj": "Bu yorumu silme yetkiniz yok."
            }

        # Nesneyi listeden kaldırıyoruz
        self.yorumlar.remove(yorum)

        # Değişiklikleri depoya bildirip diske yazıyoruz
        self._depoyu_senkronize_et()
        self.depo.yorumlari_kaydet()

        return {
            "basarili": True,
            "mesaj": "Yorum silindi."
        }

    # =========================================================
    # YORUM GETİRME (SORGULAR)
    # =========================================================

    def gonderi_yorumlari_getir(self, gonderiId: int) -> list[Yorum]:
        """
        Belirli bir gönderiye ait tüm yorum nesnelerini getirir.
        """
        return [
            y for y in self.yorumlar
            if y.gonderiId == gonderiId
        ]

    def kullanici_yorumlari_getir(self, yazarId: int) -> list[Yorum]:
        """
        Belirli bir kullanıcının yazdığı tüm yorum nesnelerini filtreler.
        """
        return [
            y for y in self.yorumlar
            if y.yazarId == yazarId
        ]

    def gonderi_yorum_sayisi(self, gonderiId: int) -> int:
        """
        Bir gönderiye ait toplam yorum sayısını döndürür.
        """
        return len([
            y for y in self.yorumlar
            if y.gonderiId == gonderiId
        ])

    # =========================================================
    # PRIVATE YARDIMCI METOTLAR
    # =========================================================

    def _yorum_bul(self, yorumId: int) -> Yorum | None:
        """
        Bellekteki Yorum nesneleri arasında ID eşleşmesi arar.
        """
        for yorum in self.yorumlar:
            if yorum.yorumId == yorumId:
                return yorum

        return None

    def gonderi_silinince_temizle(self, gonderiId: int) -> None:
        """
        Gönderi silindiğinde ona bağlı tüm yorum nesnelerini toplu temizler.
        GonderiYonetici tarafından tetiklenir.
        """
        # İlgili gönderiye ait olmayan yorumları tutarak listeyi güncelliyoruz
        self.yorumlar = [
            y for y in self.yorumlar
            if y.gonderiId != gonderiId
        ]

        # Temizlik sonrası depoyu senkronize edip kaydediyoruz
        self._depoyu_senkronize_et()
        self.depo.yorumlari_kaydet()