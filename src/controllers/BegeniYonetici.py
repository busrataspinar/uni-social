
from datetime import datetime
from models.Begeni import Begeni
from data.VeriDeposu import VeriDeposu


class BegeniYonetici:
    """
    Gönderi beğeni işlemlerini yöneten Controller sınıfı.

    Tüm işlemler VeriDeposu Singleton sınıfı üzerinden ve
    saf OOP (Nesne) modelleriyle yönetilir.
    """

    def __init__(self):
        """
        Veri deposundaki ham beğeni sözlüklerini Begeni nesnelerine
        dönüştürerek belleğe bağlar.
        """
        self.depo = VeriDeposu()

        # Depodaki ham dict listesini Begeni nesne listesine çeviriyoruz
        self.begeniler: list[Begeni] = [
            Begeni(
                begeniId=b["begeniId"],
                gonderiId=b["gonderiId"],
                kullaniciId=b["kullaniciId"],
                tarih=b["tarih"]
            ) for b in self.depo.tum_begeniler
        ]

    def _depoyu_senkronize_et(self) -> None:
        """
        Bellekteki güncel Begeni nesne listesini, VeriDeposu'nun
        beklediği ham sözlük (dict) formatına çevirerek merkezi depoyu günceller.
        """
        self.depo.tum_begeniler = [
            {
                "begeniId": b.begeniId,
                "gonderiId": b.gonderiId,
                "kullaniciId": b.kullaniciId,
                "tarih": b.tarih
            } for b in self.begeniler
        ]

    # =========================================================
    # BEĞENİ EKLE
    # =========================================================

    def begeniEkle(self, gonderiId: int, kullaniciId: int) -> dict:
        """
        Kullanıcı gönderiyi daha önce beğenmemişse yeni bir beğeni nesnesi ekler.
        """
        mevcut = self._begeni_bul(gonderiId, kullaniciId)

        if mevcut:
            return {
                "basarili": False,
                "mesaj": "Bu gönderi zaten beğenildi."
            }

        # VeriDeposu'nun güvenli ve ardışık ID üretecini kullanıyoruz
        yeni_begeni = Begeni(
            begeniId=self.depo.yeni_begeni_id(),
            gonderiId=gonderiId,
            kullaniciId=kullaniciId,
            tarih=datetime.now().isoformat()
        )

        # Listeye doğrudan nesne olarak ekliyoruz
        self.begeniler.append(yeni_begeni)

        # Depoyu senkronize edip diske yazıyoruz
        self._depoyu_senkronize_et()
        self.depo.begenileri_kaydet()

        return {
            "basarili": True,
            "begeni": yeni_begeni
        }

    # =========================================================
    # BEĞENİ KALDIR
    # =========================================================

    def begeniKaldir(self, gonderiId: int, kullaniciId: int) -> dict:
        """
        Kullanıcının ilgili gönderideki beğeni nesnesini siler.
        """
        mevcut = self._begeni_bul(gonderiId, kullaniciId)

        if mevcut is None:
            return {
                "basarili": False,
                "mesaj": "Beğeni bulunamadı."
            }

        # Bulunan nesneyi listeden güvenle siliyoruz
        self.begeniler.remove(mevcut)

        # Değişiklikleri depoya bildirip diske yazıyoruz
        self._depoyu_senkronize_et()
        self.depo.begenileri_kaydet()

        return {
            "basarili": True,
            "mesaj": "Beğeni kaldırıldı."
        }

    # =========================================================
    # TOGGLE
    # =========================================================

    def begeniToggle(self, gonderiId: int, kullaniciId: int) -> dict:
        """
        Gönderi beğenilmişse beğeniyi kaldırır, beğenilmemişse beğeni ekler.
        """
        mevcut = self._begeni_bul(gonderiId, kullaniciId)

        if mevcut:
            return self.begeniKaldir(gonderiId, kullaniciId)

        return self.begeniEkle(gonderiId, kullaniciId)

    # =========================================================
    # SORGULAR (SAYI & KONTROL)
    # =========================================================

    def begeni_sayisi_getir(self, gonderiId: int) -> int:
        """
        Bir gönderinin toplam beğeni sayısını döndürür.
        """
        return len([
            b for b in self.begeniler
            if b.gonderiId == gonderiId
        ])

    def kullanici_begendi_mi(self, gonderiId: int, kullaniciId: int) -> bool:
        """
        Bir kullanıcının gönderiyi beğenip beğenmediğini boolean olarak döner.
        Arayüz buton renkleri için kullanışlıdır.
        """
        return self._begeni_bul(gonderiId, kullaniciId) is not None

    # =========================================================
    # PRIVATE YARDIMCI METOTLAR
    # =========================================================

    def _begeni_bul(self, gonderiId: int, kullaniciId: int) -> Begeni | None:
        """
        Bellekteki Begeni nesneleri arasında ID eşleşmesi arar.
        """
        for begeni in self.begeniler:
            # Nesne olduğu için nokta (.) notasyonu ile erişiyoruz
            if begeni.gonderiId == gonderiId and begeni.kullaniciId == kullaniciId:
                return begeni

        return None

    def gonderi_silinince_temizle(self, gonderiId: int) -> None:
        """
        Bir gönderi silindiğinde ona bağlı tüm beğenileri temizler.
        GonderiYonetici tarafından tetiklenir.
        """
        # İlgili gönderiye ait olmayan beğenileri tutarak listeyi temizliyoruz
        self.begeniler = [
            b for b in self.begeniler
            if b.gonderiId != gonderiId
        ]

        # Temizlik sonrası depoyu güncelleyip kaydediyoruz
        self._depoyu_senkronize_et()
        self.depo.begenileri_kaydet()