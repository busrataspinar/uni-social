import re
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from models.Kullanici import Kullanici
from models.Oturum import Oturum
from utils.JsonIsleyicisi import JsonIsleyicisi

def _yeni_id() -> int:
    """8 haneli benzersiz rastgele ID üretir."""
    return random.randint(10_000_000, 99_999_999)


def _edu_mail_gecerli_mi(email: str) -> bool:
    """UC4 - Regex ile .edu veya .edu.tr uzantılı e-posta denetimi."""
    desen = r"^[\w\.-]+@[\w\.-]+\.edu(\.tr)?$"
    return re.match(desen, email.strip().lower()) is not None

class KimlikYonetici:
    """
    Kullanıcı güvenliğini, kayıt, giriş ve oturum süreçlerini yöneten Control sınıfı.
    Veri kalıcılığını JsonIsleyicisi üzerinden sağlar.
    """
    KULLANICI_DOSYA = "kullanicilar"

    def __init__(self) -> None:
        self._json = JsonIsleyicisi()
        self._kullanicilar: list[dict] = self._json.veriOku(self.KULLANICI_DOSYA)
        self._aktif_oturum: Oturum | None = None

    def kayit_ol(self, kullanici_adi: str, email: str, sifre: str, uni: str) -> dict:
        """UC1 - Gerekli doğrulamaları yaparak yeni öğrenci kaydı oluşturur."""

        # Boş alan kontrolleri (Açık if blokları)
        if not kullanici_adi or not str(kullanici_adi).strip():
            return {"basarili": False, "hata": "Kullanıcı adı boş bırakılamaz."}

        if not email or not str(email).strip():
            return {"basarili": False, "hata": "E-posta adresi boş bırakılamaz."}

        if not sifre or not str(sifre).strip():
            return {"basarili": False, "hata": "Şifre boş bırakılamaz."}

        if not uni or not str(uni).strip():
            return {"basarili": False, "hata": "Üniversite seçimi boş bırakılamaz."}

        email = email.strip().lower()
        kullanici_adi = kullanici_adi.strip()

        if not _edu_mail_gecerli_mi(email):
            return {"basarili": False, "hata": "Yalnızca üniversite e-postası (.edu / .edu.tr) kabul edilmektedir."}

        if self._email_kayitli_mi(email):
            return {"basarili": False, "hata": "Bu e-posta adresi zaten kayıtlı."}

        if self._kullanici_adi_kayitli_mi(kullanici_adi):
            return {"basarili": False, "hata": "Bu kullanıcı adı zaten alınmış."}

        if len(sifre) < 6:
            return {"basarili": False, "hata": "Şifre en az 6 karakter olmalıdır."}

        yeni_id = self._benzersiz_id_uret()

        yeni_kullanici = Kullanici(
            kullanicild=yeni_id,
            kullaniciAdi=kullanici_adi,
            email=email,
            sifreHash=generate_password_hash(sifre),
            # uni verisi modelinize eklendiğinde buraya dahil edilebilirsiniz
        )

        self._kullanicilar.append(self._kullanici_to_dict(yeni_kullanici))
        self._kaydet()

        return {"basarili": True, "kullanici": yeni_kullanici}

    def giris_yap(self, email: str, sifre: str) -> dict:
        """UC2 - Kullanıcı kimliğini doğrular ve aktif oturum başlatır."""
        if not email or not sifre:
            return {"basarili": False, "hata": "E-posta ve şifre zorunludur."}

        email = email.strip().lower()
        kullanici = self._kullanici_bul_email(email)

        if kullanici is None:
            return {"basarili": False, "hata": "Bu e-posta adresiyle kayıtlı kullanıcı bulunamadı."}

        if not check_password_hash(kullanici.get("sifreHash", ""), sifre):
            return {"basarili": False, "hata": "Şifre hatalı. Lütfen tekrar deneyin."}

        oturum = self._oturum_baslat(kullanici["kullanicild"])
        return {"basarili": True, "oturum": oturum, "kullanici": kullanici}

    def cikis_yap(self) -> dict:
        """UC18 - Aktif oturumu bellekten temizleyerek sonlandırır."""
        if self._aktif_oturum is None:
            return {"basarili": False, "mesaj": "Zaten oturum açık değil."}

        self._aktif_oturum = None
        return {"basarili": True, "mesaj": "Oturum başarıyla sonlandırıldı."}

    def oturum_aktif_mi(self) -> bool:
        """UC5 - Mevcut işlemler için aktif bir oturumun varlığını denetler."""
        if self._aktif_oturum is not None:
            if self._aktif_oturum.aktifMi():
                return True
        return False

    def aktif_kullanici_id(self) -> int | None:
        """Mevcut oturumdaki kullanıcının ID değerini döndürür."""
        if self.oturum_aktif_mi():
            return self._aktif_oturum.aktifKullanicild
        return None

    def sifre_sifirla(self, email: str, yeni_sifre: str) -> dict:
        """UC3 - Kayıtlı e-posta adresine ait şifreyi güvenli bir şekilde günceller."""
        if not email or not email.strip():
            return {"basarili": False, "hata": "E-posta adresi boş bırakılamaz."}

        email = email.strip().lower()
        kullanici = self._kullanici_bul_email(email)

        if kullanici is None:
            return {"basarili": False, "hata": "Kayıtlı kullanıcı bulunamadı."}

        if len(yeni_sifre) < 6:
            return {"basarili": False, "hata": "Yeni şifre en az 6 karakter olmalıdır."}

        kullanici["sifreHash"] = generate_password_hash(yeni_sifre)
        self._kaydet()

        return {"basarili": True, "mesaj": "Şifreniz başarıyla güncellendi."}

    # ──────────────────────────────────────────────────────────────────────────
    # YARDIMCI METOTLAR (PRIVATE)
    # ──────────────────────────────────────────────────────────────────────────

    def _oturum_baslat(self, kullanicild: int) -> Oturum:
        import secrets
        oturum = Oturum(
            aktifKullanicild=kullanicild,
            baslangicZamani=datetime.now(),
            token=secrets.token_hex(32),
        )
        self._aktif_oturum = oturum
        return oturum

    def _kullanici_bul_email(self, email: str) -> dict | None:
        """E-posta adresi ile kullanıcı arar (Geleneksel for döngüsü)."""
        for kullanici in self._kullanicilar:
            if kullanici.get("email", "").lower() == email:
                return kullanici
        return None

    def _email_kayitli_mi(self, email: str) -> bool:
        """E-postanın sistemde olup olmadığını kontrol eder (Geleneksel for döngüsü)."""
        for kullanici in self._kullanicilar:
            if kullanici.get("email", "").lower() == email:
                return True
        return False

    def _kullanici_adi_kayitli_mi(self, kullanici_adi: str) -> bool:
        """Kullanıcı adının sistemde olup olmadığını kontrol eder (Geleneksel for döngüsü)."""
        for kullanici in self._kullanicilar:
            if kullanici.get("kullaniciAdi", "").lower() == kullanici_adi.lower():
                return True
        return False

    def _benzersiz_id_uret(self) -> int:
        """Benzersiz bir ID üretir ve çakışma kontrolü yapar (Geleneksel for döngüsü)."""
        mevcut_idler = []
        for kullanici in self._kullanicilar:
            mevcut_idler.append(kullanici.get("kullanicild"))

        while True:
            yeni_id = _yeni_id()
            if yeni_id not in mevcut_idler:
                return yeni_id

    @staticmethod
    def _kullanici_to_dict(yeni_kullanici: Kullanici) -> dict:
        return {
            "kullanicild": yeni_kullanici.kullanicild,
            "kullaniciAdi": yeni_kullanici.kullaniciAdi,
            "email": yeni_kullanici.email,
            "sifreHash": yeni_kullanici.sifreHash,
            "takipEdilenler": yeni_kullanici.takipEdilenler,
        }

    def _kaydet(self) -> None:
        self._json.veriYaz(self.KULLANICI_DOSYA, self._kullanicilar)