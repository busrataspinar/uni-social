# Oturum.py

from datetime import datetime


class Oturum:
    """
    Kullanıcının sisteme giriş yaptıktan sonraki aktiflik sürecini yönetir.
    """

    def __init__(self, aktifKullaniciId, baslangicZamani, token):
        """
        Oturum nesnesini başlatır.

        Args:
            aktifKullaniciId (int): Şu an uygulamayı kullanan kullanıcının ID'si.
            baslangicZamani (datetime): Oturumun başladığı an.
            token (str): Güvenli erişim anahtarı.
        """
        self.aktifKullaniciId = aktifKullaniciId
        self.baslangicZamani = baslangicZamani
        self.token = token

    def aktifMi(self, sure_dakika=60):
        """
        Token varlığını ve oturumun geçerlilik süresini kontrol eder.

        Args:
            sure_dakika (int): Oturumun geçerli sayılacağı maksimum süre.

        Returns:
            bool: Oturum geçerliyse True, aksi halde False.
        """
        if not self.token:
            return False

        gecen_sure = datetime.now() - self.baslangicZamani
        return gecen_sure.total_seconds() < sure_dakika * 60

    def to_dict(self):
        """
        Oturum nesnesini sözlük formatına dönüştürür.
        """
        return {
            "aktifKullaniciId": self.aktifKullaniciId,
            "baslangicZamani": self.baslangicZamani.isoformat(),
            "token": self.token
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük verisinden Oturum nesnesi oluşturur.
        """
        return cls(
            aktifKullaniciId=veri["aktifKullaniciId"],
            baslangicZamani=datetime.fromisoformat(veri["baslangicZamani"]),
            token=veri["token"]
        )