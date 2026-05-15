from datetime import datetime


class Begeni:
    """
    Kullanıcılar ile gönderiler arasındaki beğeni etkileşimini belgeler.
    """

    def __init__(self, begenild, gonderild, kullanicild, tarih):
        """
        Begeni nesnesini başlatır.

        Args:
            begenild (int): Beğeni eyleminin benzersiz kayıt numarası.
            gonderild (int): Beğenilen gönderinin ID'si.
            kullanicild (int): Beğeni işlemini yapan kullanıcının ID'si.
            tarih (datetime): Beğeninin yapıldığı tarih ve saat.
        """
        self.begenild = begenild
        self.gonderild = gonderild
        self.kullanicild = kullanicild
        self.tarih = tarih

    def to_dict(self):
        """
        Begeni nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.
        datetime alanı ISO 8601 string formatına çevrilir.

        Returns:
            dict: Beğeni verilerini içeren sözlük.
        """
        return {
            "begenild": self.begenild,
            "gonderild": self.gonderild,
            "kullanicild": self.kullanicild,
            "tarih": self.tarih.isoformat()
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Begeni nesnesine dönüştürür.
        tarih alanı ISO 8601 string'den datetime nesnesine çevrilir.

        Args:
            veri (dict): JSON'dan okunan beğeni verisi.

        Returns:
            Begeni: Oluşturulan Begeni nesnesi.
        """
        return cls(
            begenild=veri["begenild"],
            gonderild=veri["gonderild"],
            kullanicild=veri["kullanicild"],
            tarih=datetime.fromisoformat(veri["tarih"])
        )