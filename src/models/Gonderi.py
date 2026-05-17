from datetime import datetime


class Gonderi:
    """
    Öğrencilerin paylaştığı metinsel içeriklerin ana veri yapısıdır.
    """

    def __init__(self, gonderiId, yazarId, icerik, tarih):
        """
        Gonderi nesnesini başlatır.

        Args:
            gonderiId (int): Gönderinin sistemdeki benzersiz ID'si.
            yazarId (int): Gönderiyi paylaşan kullanıcının ID'si.
            icerik (str): Paylaşımın içindeki asıl metin mesajı.
            tarih (datetime): Paylaşımın yapıldığı tarih ve saat.
        """
        self.gonderiId = gonderiId
        self.yazarId = yazarId
        self.icerik = icerik
        self.tarih = tarih

    def to_dict(self):
        """
        Gonderi nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.

        Returns:
            dict: Gönderi verilerini içeren sözlük.
        """
        return {
            "gonderiId": self.gonderiId,
            "yazarId": self.yazarId,
            "icerik": self.icerik,
            "tarih": self.tarih if isinstance(self.tarih, str) else self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Gonderi nesnesine dönüştürür.

        Args:
            veri (dict): JSON'dan okunan gönderi verisi.

        Returns:
            Gonderi: Oluşturulan Gonderi nesnesi.
        """
        return cls(
            gonderiId=veri["gonderiId"],
            yazarId=veri["yazarId"],
            icerik=veri["icerik"],
            tarih=veri["tarih"]
        )