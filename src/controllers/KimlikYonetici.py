import re
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from models.Kullanici import Kullanici
from models.Oturum import Oturum
from utils.VeriDeposu import VeriDeposu


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
    Veri kalıcılığını VeriDeposu üzerinden sağlar.
    """

    def __init__(self) -> None:
        self.depo = VeriDeposu()

        # Merkezi veri deposundaki kullanıcı listesini kullan
        self._kullanicilar: list[dict] = self.depo.tum_kullanicilar

        self._aktif_oturum: Oturum | None = None

    # UC1 - KAYIT OL

    def kayit_ol(
            self,
            kullanici_adi: str,
            email: str,
            uni: str,
            sifre: str
    ) -> dict:
        """
        Gerekli doğrulamaları yaparak yeni kullanıcı kaydı oluşturur.
        """

        # BOŞ ALAN KONTROLLERİ

        if not kullanici_adi or not str(kullanici_adi).strip():
            return {
                "basarili": False,
                "hata": "Kullanıcı adı boş bırakılamaz."
            }

        if not email or not str(email).strip():
            return {
                "basarili": False,
                "hata": "E-posta adresi boş bırakılamaz."
            }

        if not sifre or not str(sifre).strip():
            return {
                "basarili": False,
                "hata": "Şifre boş bırakılamaz."
            }

        if not uni or not str(uni).strip():
            return {
                "basarili": False,
                "hata": "Üniversite seçimi boş bırakılamaz."
            }

        # TEMİZLEME

        email = email.strip().lower()
        kullanici_adi = kullanici_adi.strip()

        # DOĞRULAMALAR

        if not _edu_mail_gecerli_mi(email):
            return {
                "basarili": False,
                "hata": "Yalnızca üniversite e-postası (.edu / .edu.tr) kabul edilmektedir."
            }

        if self._email_kayitli_mi(email):
            return {
                "basarili": False,
                "hata": "Bu e-posta adresi zaten kayıtlı."
            }

        if self._kullanici_adi_kayitli_mi(kullanici_adi):
            return {
                "basarili": False,
                "hata": "Bu kullanıcı adı zaten alınmış."
            }

        if len(sifre) < 6:
            return {
                "basarili": False,
                "hata": "Şifre en az 6 karakter olmalıdır."
            }

        # KULLANICI OLUŞTUR

        yeni_kullanici = Kullanici(
            kullaniciId=self._benzersiz_id_uret(),
            kullaniciAdi=kullanici_adi,
            email=email,
            sifreHash=generate_password_hash(sifre),
        )

        # Listeye ekle
        self._kullanicilar.append(
            self._kullanici_to_dict(yeni_kullanici)
        )

        # JSON kaydet
        self._kaydet()

        return {
            "basarili": True,
            "kullanici": yeni_kullanici
        }

    # UC2 - GİRİŞ YAP

    def giris_yap(self, email: str, sifre: str) -> dict:
        """
        Kullanıcı bilgilerini doğrular ve oturum başlatır.
        """

        if not email or not sifre:
            return {
                "basarili": False,
                "hata": "E-posta ve şifre zorunludur."
            }

        email = email.strip().lower()

        kullanici = self._kullanici_bul_email(email)

        if kullanici is None:
            return {
                "basarili": False,
                "hata": "Bu e-posta adresiyle kayıtlı kullanıcı bulunamadı."
            }

        if not check_password_hash(
                kullanici.get("sifreHash", ""),
                sifre
        ):
            return {
                "basarili": False,
                "hata": "Şifre hatalı. Lütfen tekrar deneyin."
            }

        oturum = self._oturum_baslat(
            kullanici["kullaniciId"]
        )

        return {
            "basarili": True,
            "oturum": oturum,
            "kullanici": kullanici
        }

    # UC18 - ÇIKIŞ YAP

    def cikis_yap(self) -> dict:
        """
        Aktif oturumu sonlandırır.
        """

        if self._aktif_oturum is None:
            return {
                "basarili": False,
                "mesaj": "Zaten oturum açık değil."
            }

        self._aktif_oturum = None

        return {
            "basarili": True,
            "mesaj": "Oturum başarıyla sonlandırıldı."
        }

    # UC5 - OTURUM KONTROL

    def oturum_aktif_mi(self) -> bool:
        """
        Aktif oturum var mı kontrol eder.
        """

        if self._aktif_oturum is not None:
            if self._aktif_oturum.aktifMi():
                return True

        return False

    def aktif_kullanici_id(self) -> int | None:
        """
        Aktif oturumdaki kullanıcı ID'sini döndürür.
        """

        if self.oturum_aktif_mi():
            return self._aktif_oturum.aktifKullaniciId

        return None

    # UC3 - ŞİFRE SIFIRLA

    def sifre_sifirla(
            self,
            email: str,
            yeni_sifre: str
    ) -> dict:
        """
        Kullanıcının şifresini günceller.
        """

        if not email or not email.strip():
            return {
                "basarili": False,
                "hata": "E-posta adresi boş bırakılamaz."
            }

        email = email.strip().lower()

        kullanici = self._kullanici_bul_email(email)

        if kullanici is None:
            return {
                "basarili": False,
                "hata": "Kayıtlı kullanıcı bulunamadı."
            }

        if len(yeni_sifre) < 6:
            return {
                "basarili": False,
                "hata": "Yeni şifre en az 6 karakter olmalıdır."
            }

        kullanici["sifreHash"] = generate_password_hash(
            yeni_sifre
        )

        self._kaydet()

        return {
            "basarili": True,
            "mesaj": "Şifreniz başarıyla güncellendi."
        }

    # =========================================================
    # PRIVATE YARDIMCI METOTLAR
    # =========================================================

    def _oturum_baslat(
            self,
            kullanici_id: int
    ) -> Oturum:
        """
        Yeni güvenli oturum oluşturur.
        """

        import secrets

        oturum = Oturum(
            aktifKullaniciId=kullanici_id,
            baslangicZamani=datetime.now(),
            token=secrets.token_hex(32),
        )

        self._aktif_oturum = oturum

        return oturum

    def _kullanici_bul_email(
            self,
            email: str
    ) -> dict | None:
        """
        E-posta adresine göre kullanıcı bulur.
        """

        for kullanici in self._kullanicilar:
            if kullanici.get("email", "").lower() == email:
                return kullanici

        return None

    def _email_kayitli_mi(
            self,
            email: str
    ) -> bool:
        """
        E-posta sistemde kayıtlı mı kontrol eder.
        """

        for kullanici in self._kullanicilar:
            if kullanici.get("email", "").lower() == email:
                return True

        return False

    def _kullanici_adi_kayitli_mi(
            self,
            kullanici_adi: str
    ) -> bool:
        """
        Kullanıcı adı sistemde kayıtlı mı kontrol eder.
        """

        for kullanici in self._kullanicilar:
            if (
                kullanici.get("kullaniciAdi", "").lower()
                == kullanici_adi.lower()
            ):
                return True

        return False

    def _benzersiz_id_uret(self) -> int:
        """
        Çakışmayan benzersiz kullanıcı ID'si üretir.
        """

        mevcut_idler = []

        for kullanici in self._kullanicilar:
            mevcut_idler.append(
                kullanici.get("kullaniciId")
            )

        while True:
            yeni_id = _yeni_id()

            if yeni_id not in mevcut_idler:
                return yeni_id

    @staticmethod
    def _kullanici_to_dict(
            yeni_kullanici: Kullanici
    ) -> dict:
        """
        Kullanici nesnesini dict yapısına dönüştürür.
        """

        return {
            "kullaniciId": yeni_kullanici.kullaniciId,
            "kullaniciAdi": yeni_kullanici.kullaniciAdi,
            "email": yeni_kullanici.email,
            "sifreHash": yeni_kullanici.sifreHash,
            "takipEdilenler": yeni_kullanici.takipEdilenler,
        }

    def _kaydet(self) -> None:
        """
        Kullanıcı listesini JSON dosyasına kaydeder.
        """

        self.depo.kullanicilari_kaydet()