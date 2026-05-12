class Begeni:
    """
    Kullanıcılar ile gönderiler arasındaki beğeni etkileşimini belgeler.

    Attributes:
        begenild (int): Beğeni eyleminin benzersiz kayıt numarası.
        gonderild (int): Beğenilen gönderinin ID'si.
        kullanicild (int): Beğeni işlemini yapan kullanıcının ID'si.
        tarih (datetime): Beğeninin yapıldığı zaman damgası.
    """

    def __init__(self, begenild, gonderild, kullanicild, tarih):
        self.begenild = begenild
        self.gonderild = gonderild
        self.kullanicild = kullanicild
        self.tarih = tarih