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

