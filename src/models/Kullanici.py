class Kullanici:
    """
    Sistemdeki öğrencilerin dijital kimlik bilgilerini ve sosyal ağlarını tutar.
    """

    def __init__(self, kullanicild, kullaniciAdi, email, sifreHash, uni=""):
        """
        Kullanici nesnesini başlatır.

        Args:
            kullanicild (int): Kullanıcıyı diğerlerinden ayıran benzersiz kayıt numarası.
            kullaniciAdi (str): Profilde görünen ve aramalarda kullanılan kullanıcı ismi.
            email (str): Giriş için kullanılan .edu uzantılı resmi e-posta adresi.
            sifreHash (str): Şifrenin güvenlik amacıyla hashlenmiş hali.
            uni (str): Kullanıcının kayıtlı olduğu üniversite adı. Varsayılan boş string.
        """
        self.kullanicild = kullanicild
        self.kullaniciAdi = kullaniciAdi
        self.email = email
        self.sifreHash = sifreHash
        self.uni = uni
        self.takipEdilenler = []

    def to_dict(self):
        """
        Kullanici nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.

        Returns:
            dict: Kullanıcı verilerini içeren sözlük.
        """
        return {
            "kullanicild": self.kullanicild,
            "kullaniciAdi": self.kullaniciAdi,
            "email": self.email,
            "sifreHash": self.sifreHash,
            "uni": self.uni,
            "takipEdilenler": self.takipEdilenler
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük formatındaki veriyi Kullanici nesnesine dönüştürür.

        Args:
            veri (dict): JSON'dan okunan kullanıcı verisi.

        Returns:
            Kullanici: Oluşturulan Kullanici nesnesi.
        """
        k = cls(
            kullanicild=veri["kullanicild"],
            kullaniciAdi=veri["kullaniciAdi"],
            email=veri["email"],
            sifreHash=veri["sifreHash"],
            uni=veri.get("uni", "")
        )
        k.takipEdilenler = veri.get("takipEdilenler", [])
        return k