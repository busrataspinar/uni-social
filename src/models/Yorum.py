from datetime import datetime


class Yorum:
    """
    Gönderilere yapılan geri bildirimlerin verilerini saklar.
    """

    def __init__(self, yorumId, gonderiId, yazarId, icerik, tarih):
        """
        Yorum nesnesini başlatır.

        Args:
            yorumId (int): Her yoruma verilen özel kimlik numarası.
            gonderiId (int): Yorumun hangi gönderiye ait olduğunu belirten ID.
            yazarId (int): Yorumu yazan öğrencinin kullanıcı ID'si.
            icerik (str): Yorum metninin içeriği.
            tarih (str): Yorumun sisteme girildiği tarih ve saat (ISO 8601 string).
        """
        self.yorumId = yorumId
        self.gonderiId = gonderiId
        self.yazarId = yazarId
        self.icerik = icerik
        self.tarih = tarih

    def to_dict(self):
        """
        Yorum nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.

        Returns:
            dict: Yorum verilerini içeren sözlük.
        """
        return {
            "yorumId": self.yorumId,
            "gonderiId": self.gonderiId,
            "yazarId": self.yazarId,
            "icerik": self.icerik,
            "tarih": self.tarih if isinstance(self.tarih, str) else self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Yorum nesnesine dönüştürür.

        Args:
            veri (dict): JSON'dan okunan yorum verisi.

        Returns:
            Yorum: Oluşturulan Yorum nesnesi.
        """
        return cls(
            yorumId=veri["yorumId"],
            gonderiId=veri["gonderiId"],
            yazarId=veri["yazarId"],
            icerik=veri["icerik"],
            tarih=veri["tarih"]
        )