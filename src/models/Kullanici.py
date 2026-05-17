class Kullanici:
    """
    Sistemdeki öğrencilerin dijital kimlik bilgilerini ve sosyal ağlarını tutar.
    """

    def __init__(self, kullaniciId, kullaniciAdi, email, sifreHash, uni=""):
        """
        Kullanici nesnesini başlatır.

        Args:
            kullaniciId (int): Kullanıcıyı diğerlerinden ayıran benzersiz kayıt numarası.
            kullaniciAdi (str): Profilde görünen ve aramalarda kullanılan kullanıcı ismi.
            email (str): Giriş için kullanılan .edu uzantılı resmi e-posta adresi.
            sifreHash (str): Şifrenin güvenlik amacıyla hashlenmiş hali.
            uni (str): Kullanıcının kayıtlı olduğu üniversite adı. Varsayılan boş string.
        """
        self.kullaniciId = kullaniciId
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
            "kullaniciId": self.kullaniciId,
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
            kullaniciId=veri["kullaniciId"],
            kullaniciAdi=veri["kullaniciAdi"],
            email=veri["email"],
            sifreHash=veri["sifreHash"],
            uni=veri.get("uni", "")
        )
        k.takipEdilenler = veri.get("takipEdilenler", [])
        return k