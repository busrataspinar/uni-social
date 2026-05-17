from datetime import datetime


class Begeni:
    """
    Kullanıcılar ile gönderiler arasındaki beğeni etkileşimini belgeler.
    """

    def __init__(self, begeniId, gonderiId, kullaniciId, tarih):
        """
        Begeni nesnesini başlatır.

        Args:
            begeniId (int): Beğeni eyleminin benzersiz kayıt numarası.
            gonderiId (int): Beğenilen gönderinin ID'si.
            kullaniciId (int): Beğeni işlemini yapan kullanıcının ID'si.
            tarih (str): Beğeninin yapıldığı tarih ve saat (ISO 8601 string).
        """
        self.begeniId = begeniId
        self.gonderiId = gonderiId
        self.kullaniciId = kullaniciId
        self.tarih = tarih

    def to_dict(self):
        """
        Begeni nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.

        Returns:
            dict: Beğeni verilerini içeren sözlük.
        """
        return {
            "begeniId": self.begeniId,
            "gonderiId": self.gonderiId,
            "kullaniciId": self.kullaniciId,
            "tarih": self.tarih if isinstance(self.tarih, str) else self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Begeni nesnesine dönüştürür.

        Args:
            veri (dict): JSON'dan okunan beğeni verisi.

        Returns:
            Begeni: Oluşturulan Begeni nesnesi.
        """
        return cls(
            begeniId=veri["begeniId"],
            gonderiId=veri["gonderiId"],
            kullaniciId=veri["kullaniciId"],
            tarih=veri["tarih"]
        )