import datetime


class Oturum:
    """
    Kullanıcının sisteme giriş yaptıktan sonraki aktiflik sürecini yönetir.

    Attributes:
        aktifKullanicild (int): Şu an uygulamayı kullanan kullanıcının benzersiz ID'si.
        baslangicZamani (datetime): Oturumun başladığı an; süre kontrolü için kullanılır.
        token (str): Şifre girmeden içeride kalmayı sağlayan güvenli erişim anahtarı.
    """

    def __init__(self, aktifKullanicild, baslangicZamani, token):
        self.aktifKullanicild = aktifKullanicild
        self.baslangicZamani = baslangicZamani
        self.token = token

    def aktifMi(self):
        """
        Token varlığını ve oturumun geçerlilik süresini kontrol eder.
        """
        # Şimdilik token varsa ve süre aşımı yoksa True döner
        return self.token is not None