from datetime import datetime


class Gonderi:
    """
    Öğrencilerin paylaştığı metinsel içeriklerin ana veri yapısıdır.
    """

    def __init__(self, gonderild, yazarld, icerik, tarih):
        """
        Gonderi nesnesini başlatır.

        Args:
            gonderild (int): Gönderinin sistemdeki benzersiz ID'si.
            yazarld (int): Gönderiyi paylaşan kullanıcının ID'si.
            icerik (str): Paylaşımın içindeki asıl metin mesajı.
            tarih (datetime): Paylaşımın yapıldığı tarih ve saat.
        """
        self.gonderild = gonderild
        self.yazarld = yazarld
        self.icerik = icerik
        self.tarih = tarih

    def to_dict(self):
        """
        Gonderi nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.
        datetime alanı ISO 8601 string formatına çevrilir.

        Returns:
            dict: Gönderi verilerini içeren sözlük.
        """
        return {
            "gonderild": self.gonderild,
            "yazarld": self.yazarld,
            "icerik": self.icerik,
            "tarih": self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Gonderi nesnesine dönüştürür.
        tarih alanı ISO 8601 string'den datetime nesnesine çevrilir.

        Args:
            veri (dict): JSON'dan okunan gönderi verisi.

        Returns:
            Gonderi: Oluşturulan Gonderi nesnesi.
        """
        return cls(
            gonderild=veri["gonderild"],
            yazarld=veri["yazarld"],
            icerik=veri["icerik"],
            tarih=datetime.fromisoformat(veri["tarih"])
        )