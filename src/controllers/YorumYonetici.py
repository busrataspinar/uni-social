import random
from datetime import datetime

from models.Yorum import Yorum
from utils.JsonIsleyicisi import JsonIsleyicisi


def _yeni_id() -> int:
    """8 haneli rastgele tam sayı üretir."""
    return random.randint(10_000_000, 99_999_999)


class YorumYonetici:
    """
    Gönderilere yapılan yorumların oluşturulması ve silinmesini
    yöneten Controller sınıfı.
    """

    # Güncelleme: Klasör yapısı ve uzantı kaldırıldı.
    YORUM_DOSYA = "yorumlar"

    def __init__(self) -> None:
        self.json = JsonIsleyicisi()
        self.yorumlar: list[Yorum] = []
        self._verileri_yukle()

    # ==================================================================
    # PRIVATE – Yükleme / Kaydetme
    # ==================================================================

    def _verileri_yukle(self) -> None:
        """Uygulama başında JSON'dan tüm yorumları belleğe yükler."""
        # Güncelleme: .oku yerine .veriOku kullanıldı
        ham = self.json.veriOku(self.YORUM_DOSYA)
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
        # Güncelleme: .yaz yerine .veriYaz kullanıldı
        self.json.veriYaz(self.YORUM_DOSYA, veri)

    def _yorum_bul(self, yorumId: int) -> Yorum | None:
        """ID'ye göre yorum nesnesi döndürür; bulamazsa None."""
        for y in self.yorumlar:
            if y.yorumId == yorumId:
                return y
        return None

    def yorumEkle(self, gonderild: int, yazarld: int, icerik: str) -> dict:
        """Bir gönderiye yeni bir yorum ekler."""
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

    def yorumSil(self, yorumId: int, aktif_kullanicild: int) -> dict:
        """Belirtilen yorumu siler. Yalnızca yorumun sahibi silebilir."""
        yorum = self._yorum_bul(yorumId)

        if yorum is None:
            return {"basarili": False, "mesaj": "Yorum bulunamadı."}

        if yorum.yazarld != aktif_kullanicild:
            return {"basarili": False, "mesaj": "Bu yorumu silme yetkiniz yok."}

        self.yorumlar.remove(yorum)
        self._yorumlari_kaydet()

        return {"basarili": True, "mesaj": "Yorum başarıyla silindi."}

    def gonderi_yorumlari_getir(self, gonderild: int) -> list[Yorum]:
        """Bir gönderiye ait tüm yorumları eskiden yeniye sıralı döndürür."""
        ilgili = [y for y in self.yorumlar if y.gonderild == gonderild]
        ilgili.sort(key=lambda y: y.tarih)
        return ilgili

    def kullanici_yorumlari_getir(self, yazarld: int) -> list[Yorum]:
        """Bir kullanıcının yaptığı tüm yorumları döndürür."""
        return [y for y in self.yorumlar if y.yazarld == yazarld]

    def gonderi_yorum_sayisi(self, gonderild: int) -> int:
        """Bir gönderinin toplam yorum sayısını döndürür."""
        return len([y for y in self.yorumlar if y.gonderild == gonderild])

    def gonderi_silinince_temizle(self, gonderild: int) -> None:
        """Bir gönderi silindiğinde ona ait tüm yorumları temizler."""
        self.yorumlar = [y for y in self.yorumlar if y.gonderild != gonderild]
        self._yorumlari_kaydet()