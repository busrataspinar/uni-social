from datetime import datetime


class Oturum:
    """
    Kullanıcının sisteme giriş yaptıktan sonraki aktiflik sürecini yönetir.
    """

    def __init__(self, aktifKullanicild, baslangicZamani, token):
        """
        Oturum nesnesini başlatır.

        Args:
            aktifKullanicild (int): Şu an uygulamayı kullanan kullanıcının ID'si.
            baslangicZamani (datetime): Oturumun başladığı an; süre kontrolü için kullanılır.
            token (str): Şifre girmeden içeride kalmayı sağlayan güvenli erişim anahtarı.
        """
        self.aktifKullanicild = aktifKullanicild
        self.baslangicZamani = baslangicZamani
        self.token = token

    def aktifMi(self, sure_dakika=60):
        """
        Token varlığını ve oturumun geçerlilik süresini kontrol eder.

        Args:
            sure_dakika (int): Oturumun geçerli sayılacağı maksimum süre (dakika).
                               Varsayılan değer 60 dakikadır.

        Returns:
            bool: Oturum geçerliyse True, süresi dolmuşsa veya token yoksa False.
        """
        if not self.token:
            return False
        gecen_sure = datetime.now() - self.baslangicZamani
        return gecen_sure.total_seconds() < sure_dakika * 60