
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

    # Yorum Silme
    # Tasarım dokümanı: yorumSil(yorumId) : boolean
    def yorumSil(self, yorumId: int, aktif_kullanicild: int) -> dict:
        """
        Belirtilen yorumu siler.
        Yalnızca yorumun sahibi silebilir.

        Parametreler
        ------------
        yorumId            : Silinecek yorumun ID'si
        aktif_kullanicild  : İşlemi yapan (oturumda olan) kullanıcının ID'si

        Dönüş
        -----
        {"basarili": True,  "mesaj": str}
        {"basarili": False, "mesaj": str}
        """
        yorum = self._yorum_bul(yorumId)

        if yorum is None:
            return {"basarili": False, "mesaj": "Yorum bulunamadı."}

        # Sahiplik kontrolü (Tasarım dok. 2.6.3 → Yetki ihlali)
        if yorum.yazarld != aktif_kullanicild:
            return {"basarili": False, "mesaj": "Bu yorumu silme yetkiniz yok."}

        self.yorumlar.remove(yorum)
        self._yorumlari_kaydet()

        return {"basarili": True, "mesaj": "Yorum başarıyla silindi."}

    # Yardımcı sorgular  (5. kişi / route katmanı tarafından kullanılır)
    # ==================================================================
    def gonderi_yorumlari_getir(self, gonderild: int) -> list[Yorum]:
        """
        Bir gönderiye ait tüm yorumları eskiden yeniye sıralı döndürür.
        Gönderi detay sayfasında yorum listesi için kullanılır.
        """
        ilgili = [y for y in self.yorumlar if y.gonderild == gonderild]
        ilgili.sort(key=lambda y: y.tarih)
        return ilgili

    def kullanici_yorumlari_getir(self, yazarld: int) -> list[Yorum]:
        """
        Bir kullanıcının yaptığı tüm yorumları döndürür.
        Profil sayfası için kullanılabilir.
        """
        return [y for y in self.yorumlar if y.yazarld == yazarld]

    def gonderi_yorum_sayisi(self, gonderild: int) -> int:
        """Bir gönderinin toplam yorum sayısını döndürür."""
        return len([y for y in self.yorumlar if y.gonderild == gonderild])

    def gonderi_silinince_temizle(self, gonderild: int) -> None:
        """
        Bir gönderi silindiğinde ona ait tüm yorumları temizler.
        GonderiYonetici.gonderi_sil() tarafından çağrılır.
        """
        self.yorumlar = [y for y in self.yorumlar if y.gonderild != gonderild]
        self._yorumlari_kaydet()


import random
from datetime import datetime
from models.Gonderi import Gonderi
from utils.JsonIsleyicisi import JsonIsleyicisi


class GonderiYonetici:
    """
    Gönderi iş mantığını yöneten Controller sınıfı.
    Veriler bellekte liste olarak tutulur; her işlemde
    JsonIsleyicisi aracılığıyla gonderiler.json'a yazılır.
    """

    def __init__(self):
        self._json = JsonIsleyicisi()
        # JSON'dan gelen dict listesini Gonderi nesnelerine çevir
        self.gonderiler: list[Gonderi] = self._json_to_gonderiler(
            self._json.oku("gonderiler")
        )

    # ------------------------------------------------------------------
    # UC6 – Gönderi Paylaş
    # ------------------------------------------------------------------
    def gonderi_olustur(self, yazarld: int, icerik: str) -> dict:
        """
        Yeni bir gönderi oluşturur.

        Parametreler:
            yazarld : Gönderiyi paylaşan kullanıcının ID'si (int)
            icerik  : Gönderi metni (str)

        Dönüş:
            {"basarili": True,  "gonderi": Gonderi}
            {"basarili": False, "hata": str}
        """
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

    # ------------------------------------------------------------------
    # UC7 – Gönderi Sil
    # ------------------------------------------------------------------
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

        Parametreler:
            gonderild       : Silinecek gönderinin ID'si (int)
            yazarld         : İşlemi yapan kullanıcının ID'si (int)
            yorum_yonetici  : YorumYonetici örneği (opsiyonel)
            begeni_yonetici : BegeniYonetici örneği (opsiyonel)

        Dönüş:
            {"basarili": True}
            {"basarili": False, "hata": str}
        """
        gonderi = self._gonderi_bul(gonderild)
        if gonderi is None:
            return {"basarili": False, "hata": "Gönderi bulunamadı."}

        if gonderi.yazarld != yazarld:
            return {"basarili": False, "hata": "Bu gönderiyi silme yetkiniz yok."}

        self.gonderiler.remove(gonderi)
        self._kaydet()

        # Bağlı yorumları temizle
        if yorum_yonetici is not None:
            yorum_yonetici.gonderi_silinince_yorumlari_temizle(gonderild)

        # Bağlı beğenileri temizle
        if begeni_yonetici is not None:
            begeni_yonetici.gonderi_silinince_begenileri_temizle(gonderild)

        return {"basarili": True}

    # ------------------------------------------------------------------
    # UC9 – Gönderi Düzenle
    # ------------------------------------------------------------------
    def gonderi_duzenle(self, gonderild: int, yazarld: int, yeni_icerik: str) -> dict:
        """
        Mevcut bir gönderinin içeriğini günceller.
        Yalnızca gönderinin sahibi düzenleyebilir.

        Parametreler:
            gonderild   : Düzenlenecek gönderinin ID'si (int)
            yazarld     : İşlemi yapan kullanıcının ID'si (int)
            yeni_icerik : Güncellenmiş içerik (str)

        Dönüş:
            {"basarili": True,  "gonderi": Gonderi}
            {"basarili": False, "hata": str}
        """
        if not yeni_icerik or not yeni_icerik.strip():
            return {"basarili": False, "hata": "Güncellenmiş içerik boş olamaz."}

        gonderi = self._gonderi_bul(gonderild)
        if gonderi is None:
            return {"basarili": False, "hata": "Gönderi bulunamadı."}

        if gonderi.yazarld != yazarld:
            return {"basarili": False, "hata": "Bu gönderiyi düzenleme yetkiniz yok."}

        gonderi.icerik = yeni_icerik.strip()
        gonderi.tarih = datetime.now()   # düzenleme zamanı güncellenir

        self._kaydet()

        return {"basarili": True, "gonderi": gonderi}

    # ------------------------------------------------------------------
    # Yardımcı – Sorgulama
    # ------------------------------------------------------------------
    def tum_gonderileri_getir(self) -> list:
        """Tüm gönderileri döndürür."""
        return list(self.gonderiler)

    def kullanici_gonderilerini_getir(self, yazarld: int) -> list:
        """Belirli bir kullanıcının gönderilerini döndürür (profil sayfası)."""
        return [g for g in self.gonderiler if g.yazarld == yazarld]

    def gonderi_getir(self, gonderild: int):
        """ID'ye göre tekil gönderi döndürür; bulunamazsa None."""
        return self._gonderi_bul(gonderild)

    # ------------------------------------------------------------------
    # İç yardımcı metotlar
    # ------------------------------------------------------------------
    def _gonderi_bul(self, gonderild: int):
        for g in self.gonderiler:
            if g.gonderild == gonderild:
                return g
        return None

    def _yeni_id_uret(self) -> int:
        """8 haneli benzersiz rastgele ID üretir (JSON yapısıyla uyumlu)."""
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
        self._json.yaz("gonderiler", veri)