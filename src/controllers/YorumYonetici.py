
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
        # ==================================================================
        # PRIVATE – Yükleme / Kaydetme
        # ==================================================================

    def _verileri_yukle(self) -> None:
        """Uygulama başında JSON'dan tüm yorumları belleğe yükler."""
        ham = self.json.oku(self.YORUM_DOSYA)
        for d in ham:
            self.yorumlar.append(Yorum(
                yorumId=d["yorumId"],
                gonderild=d["gonderild"],
                yazarld=d["yazarld"],
                icerik=d["icerik"],
                tarih=d["tarih"],
            ))

    def _yorumlari_kaydet(self) -> None:
        """Bellekteki yorum listesini JSON dosyasına yazar."""
        veri = []
        for y in self.yorumlar:
            veri.append({
                "yorumId": y.yorumId,
                "gonderild": y.gonderild,
                "yazarld": y.yazarld,
                "icerik": y.icerik,
                "tarih": y.tarih,
            })
        self.json.yaz(self.YORUM_DOSYA, veri)

        # PRIVATE – Yardımcı arama
        # ==================================================================

    def _yorum_bul(self, yorumId: int) -> Yorum | None:
        """ID'ye göre yorum nesnesi döndürür; bulamazsa None."""
        for y in self.yorumlar:
            if y.yorumId == yorumId:
                return y
        return None

        # Tasarım dokümanı: yorumEkle(postId, yazarId, icerik) : void
        # ==================================================================

        def yorumEkle(self, gonderild: int, yazarld: int, icerik: str) -> dict:
            """
            Bir gönderiye yeni bir yorum ekler.

            Parametreler
            ------------
            gonderild : Yorum yapılacak gönderinin ID'si
            yazarld   : Yorumu yapan kullanıcının ID'si
            icerik    : Yorum metni

            Dönüş
            -----
            {"basarili": True,  "yorum": Yorum}
            {"basarili": False, "mesaj": str}
            """
            # Kural: İçerik boş olamaz (Tasarım dok. 2.6.3 → Hata Durumları)
            if not icerik or not icerik.strip():
                return {"basarili": False, "mesaj": "Yorum içeriği boş olamaz."}

            yeni_yorum = Yorum(
                yorumId=_yeni_id(),
                gonderild=gonderild,
                yazarld=yazarld,
                icerik=icerik.strip(),
                tarih=datetime.now().isoformat(),
            )

            self.yorumlar.append(yeni_yorum)
            self._yorumlari_kaydet()

            return {"basarili": True, "yorum": yeni_yorum}

