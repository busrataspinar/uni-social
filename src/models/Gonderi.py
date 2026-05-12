class Gonderi:
    """
    Öğrencilerin paylaştığı metinsel içeriklerin ana yapısıdır.

    Attributes:
        gonderild (int): Gönderinin sistemdeki benzersiz ID'si.
        yazarld (int): Gönderiyi paylaşan kullanıcının ID'si.
        icerik (str): Paylaşımın içindeki asıl metin mesajı.
        tarih (datetime): Paylaşımın yapıldığı kesin tarih ve saat.
    """

    def __init__(self, gonderild, yazarld, icerik, tarih):
        self.gonderild = gonderild
        self.yazarld = yazarld
        self.icerik = icerik
        self.tarih = tarih