class Feed:
    """
    Kullanıcıya özel hazırlanan içerik akışını temsil eder.

    Attributes:
        kullanicild (int): Akışın sahibi olan öğrencinin ID'si.
        akisGonderileri (list): Takip edilenlerin gönderilerini içeren liste.
    """

    def __init__(self, kullanicild):
        self.kullanicild = kullanicild
        self.akisGonderileri = []