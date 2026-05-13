class Kullanici:
    """
    Sistemdeki öğrencilerin dijital kimlik bilgilerini ve sosyal ağlarını tutar.

    Attributes:
        kullanicild (int): Kullanıcıyı ayıran benzersiz kayıt numarası.
        kullaniciAdi (str): Profilde görünen kullanıcı ismi.
        email (str): Giriş için kullanılan resmi iletişim adresi (.edu).
        sifreHash (str): Şifrenin güvenlik amacıyla şifrelenmiş hali.
        takipEdilenler (list): Kullanıcının takip ettiği kişilerin ID listesi.
    """

    def __init__(self, kullanicild, kullaniciAdi, email, sifreHash):
        self.kullanicild = kullanicild
        self.kullaniciAdi = kullaniciAdi
        self.email = email
        self.sifreHash = sifreHash
        self.takipEdilenler = []