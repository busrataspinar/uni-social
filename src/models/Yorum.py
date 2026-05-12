class Yorum:
    """
    Gönderilere yapılan geri bildirimlerin verilerini saklar.

    Attributes:
        yorumId (int): Yoruma verilen özel kimlik numarası.
        gonderild (int): Yorumun hangi gönderiye ait olduğunu belirten ID.
        yazarld (int): Yorumu yazan öğrencinin kullanıcı ID'si.
        icerik (str): Yorum metninin içeriği.
        tarih (datetime): Yorumun yapıldığı zaman damgası.
    """

    def __init__(self, yorumId, gonderild, yazarld, icerik, tarih):
        self.yorumId = yorumId
        self.gonderild = gonderild
        self.yazarld = yazarld
        self.icerik = icerik
        self.tarih = tarih