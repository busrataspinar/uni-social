from datetime import datetime


class Yorum:
    """
    Gönderilere yapılan geri bildirimlerin verilerini saklar.
    """

    def __init__(self, yorumId, gonderild, yazarld, icerik, tarih):
        """
        Yorum nesnesini başlatır.

        Args:
            yorumId (int): Her yoruma verilen özel kimlik numarası.
            gonderild (int): Yorumun hangi gönderiye ait olduğunu belirten ID.
            yazarld (int): Yorumu yazan öğrencinin kullanıcı ID'si.
            icerik (str): Yorum metninin içeriği.
            tarih (datetime): Yorumun sisteme girildiği tarih ve saat.
        """
        self.yorumId = yorumId
        self.gonderild = gonderild
        self.yazarld = yazarld
        self.icerik = icerik
        self.tarih = tarih

    def to_dict(self):
        """
        Yorum nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.
        datetime alanı ISO 8601 string formatına çevrilir.

        Returns:
            dict: Yorum verilerini içeren sözlük.
        """
        return {
            "yorumId": self.yorumId,
            "gonderild": self.gonderild,
            "yazarld": self.yazarld,
            "icerik": self.icerik,
            "tarih": self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Yorum nesnesine dönüştürür.
        tarih alanı ISO 8601 string'den datetime nesnesine çevrilir.

        Args:
            veri (dict): JSON'dan okunan yorum verisi.

        Returns:
            Yorum: Oluşturulan Yorum nesnesi.
        """
        return cls(
            yorumId=veri["yorumId"],
            gonderild=veri["gonderild"],
            yazarld=veri["yazarld"],
            icerik=veri["icerik"],
            tarih=datetime.fromisoformat(veri["tarih"])
        )