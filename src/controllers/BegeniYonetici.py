import random
from datetime import datetime

from models.Begeni import Begeni
from utils.JsonIsleyicisi import JsonIsleyicisi


def _yeni_id() -> int:
    """
    1. kişinin kullandığı yöntemle aynı:
    8 haneli rastgele tam sayı.  Örnek: 18090992
    """
    return random.randint(10_000_000, 99_999_999)


class BegeniYonetici:
    """
    Gönderilere yapılan beğenilerin eklenmesi ve kaldırılmasını
    yöneten Controller sınıfı.

    Bellek Yapısı
    -------------
    self.begeniler : list[Begeni]  – Tüm beğeni nesneleri

    Uygulama açılışında JSON'dan yüklenir;
    her değişiklik sonrası JSON'a geri yazılır.
    """

    BEGENI_DOSYA = "data/begeniler.json"

    def __init__(self) -> None:
        self.json = JsonIsleyicisi()
        self.begeniler: list[Begeni] = []
        self._verileri_yukle()

    # ==================================================================
    # PRIVATE – Yükleme / Kaydetme
    # ==================================================================

    def _verileri_yukle(self) -> None:
        """Uygulama başında JSON'dan tüm beğenileri belleğe yükler."""
        ham = self.json.oku(self.BEGENI_DOSYA)
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
        self.json.yaz(self.BEGENI_DOSYA, veri)

    def begeniEkle(self, gonderild: int, kullanicild: int) -> dict:
        """
        Bir gönderiye beğeni ekler.
        Kullanıcı aynı gönderiyi zaten beğenmişse işlem yapılmaz.

        Parametreler
        ------------
        gonderild   : Beğenilecek gönderinin ID'si
        kullanicild : Beğeniyi yapan kullanıcının ID'si

        Dönüş
        -----
        {"basarili": True,  "begeni": Begeni, "begeni_sayisi": int}
        {"basarili": False, "mesaj": str}
        """
        # Çift beğeni engeli
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

