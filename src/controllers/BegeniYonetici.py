import random
from datetime import datetime

from models.Begeni import Begeni
from utils.JsonIsleyicisi import JsonIsleyicisi


def _yeni_id() -> int:
    """8 haneli rastgele tam sayı üretir."""
    return random.randint(10_000_000, 99_999_999)


class BegeniYonetici:
    """
    Gönderilere yapılan beğenilerin eklenmesi ve kaldırılmasını
    yöneten Controller sınıfı.
    """

    # Güncelleme: Dosya yolu ve uzantı JsonIsleyicisi tarafından yönetildiği için sadece ad bırakıldı.
    BEGENI_DOSYA = "begeniler"

    def __init__(self) -> None:
        self.json = JsonIsleyicisi()
        self.begeniler: list[Begeni] = []
        self._verileri_yukle()

    # ==================================================================
    # PRIVATE – Yükleme / Kaydetme
    # ==================================================================

    def _verileri_yukle(self) -> None:
        """Uygulama başında JSON'dan tüm beğenileri belleğe yükler."""
        # Güncelleme: .oku yerine .veriOku kullanıldı
        ham = self.json.veriOku(self.BEGENI_DOSYA)
        for d in ham:
            self.begeniler.append(Begeni(
                begenild    = d["begenild"],
                gonderild   = d["gonderild"],
                kullanicild = d["kullanicild"],
                tarih       = d["tarih"],
            ))

    def _begenileri_kaydet(self) -> None:
        """Bellekteki beğeni listesini JSON dosyasına yazar."""
        veri = []
        for b in self.begeniler:
            veri.append({
                "begenild"    : b.begenild,
                "gonderild"   : b.gonderild,
                "kullanicild" : b.kullanicild,
                "tarih"       : b.tarih,
            })
        # Güncelleme: .yaz yerine .veriYaz kullanıldı
        self.json.veriYaz(self.BEGENI_DOSYA, veri)

    def _begeni_bul(self, gonderild: int, kullanicild: int) -> Begeni | None:
        """Kullanıcının belirli bir gönderiyi beğenip beğenmediğini kontrol eder."""
        for b in self.begeniler:
            if b.gonderild == gonderild and b.kullanicild == kullanicild:
                return b
        return None

    def begeniEkle(self, gonderild: int, kullanicild: int) -> dict:
        """Bir gönderiye beğeni ekler."""
        mevcut = self._begeni_bul(gonderild, kullanicild)
        if mevcut:
            sayi = self.begeni_sayisi_getir(gonderild)
            return {
                "basarili": False,
                "mesaj": "Bu gönderiyi zaten beğendiniz.",
                "begeni_sayisi": sayi,
            }

        yeni_begeni = Begeni(
            begenild    = _yeni_id(),
            gonderild   = gonderild,
            kullanicild = kullanicild,
            tarih       = datetime.now().isoformat(),
        )

        self.begeniler.append(yeni_begeni)
        self._begenileri_kaydet()

        sayi = self.begeni_sayisi_getir(gonderild)
        return {"basarili": True, "begeni": yeni_begeni, "begeni_sayisi": sayi}

    def begeniKaldir(self, gonderild: int, kullanicild: int) -> dict:
        """Kullanıcının bir gönderiye yaptığı beğeniyi kaldırır."""
        mevcut = self._begeni_bul(gonderild, kullanicild)

        if not mevcut:
            return {"basarili": False, "mesaj": "Bu gönderiyi beğenmediniz."}

        self.begeniler.remove(mevcut)
        self._begenileri_kaydet()

        sayi = self.begeni_sayisi_getir(gonderild)
        return {"basarili": True, "mesaj": "Beğeni kaldırıldı.", "begeni_sayisi": sayi}

    def begeniToggle(self, gonderild: int, kullanicild: int) -> dict:
        """Kullanıcı beğendiyse kaldırır, beğenmediyse ekler."""
        mevcut = self._begeni_bul(gonderild, kullanicild)
        if mevcut:
            return self.begeniKaldir(gonderild, kullanicild) | {"islem": "kaldirildi"}
        else:
            sonuc = self.begeniEkle(gonderild, kullanicild)
            sonuc["islem"] = "eklendi"
            return sonuc

    def begeni_sayisi_getir(self, gonderild: int) -> int:
        """Bir gönderinin toplam beğeni sayısını döndürür."""
        return len([b for b in self.begeniler if b.gonderild == gonderild])

    def kullanici_begendi_mi(self, gonderild: int, kullanicild: int) -> bool:
        """Kullanıcının ilgili gönderiyi beğenip beğenmediğini döndürür."""
        return self._begeni_bul(gonderild, kullanicild) is not None

    def kullanici_begeni_gecmisi(self, kullanicild: int) -> list[Begeni]:
        """Bir kullanıcının beğendiği tüm gönderilerin beğeni kayıtlarını döndürür."""
        return [b for b in self.begeniler if b.kullanicild == kullanicild]

    def gonderi_silinince_temizle(self, gonderild: int) -> None:
        """Bir gönderi silindiğinde ona ait tüm beğenileri temizler."""
        self.begeniler = [b for b in self.begeniler if b.gonderild != gonderild]
        self._begenileri_kaydet()