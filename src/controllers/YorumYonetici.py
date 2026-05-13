
import random
from datetime import datetime

from models.Yorum import Yorum
from utils.JsonIsleyicisi import JsonIsleyicisi


def _yeni_id() -> int:
    """
    1. kişinin kullandığı yöntemle aynı:
    8 haneli rastgele tam sayı.  Örnek: 30155879
    """
    return random.randint(10_000_000, 99_999_999)


class YorumYonetici:
    """
    Gönderilere yapılan yorumların oluşturulması ve silinmesini
    yöneten Controller sınıfı.

    Bellek Yapısı
    -------------
    self.yorumlar : list[Yorum]  – Tüm yorum nesneleri

    Uygulama açılışında JSON'dan yüklenir;
    her değişiklik sonrası JSON'a geri yazılır.
    """

    YORUM_DOSYA = "data/yorumlar.json"

    def __init__(self) -> None:
        self.json = JsonIsleyicisi()
        self.yorumlar: list[Yorum] = []
        self._verileri_yukle()