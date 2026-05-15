class Feed:
    """
    Kullanıcıya özel hazırlanan içerik akışını temsil eder.
    Takip edilen kişilerin gönderilerinden oluşan listeyi barındırır.
    """

    def __init__(self, kullanicild):
        """
        Feed nesnesini başlatır.

        Args:
            kullanicild (int): Bu akışın ait olduğu öğrencinin ID'si.
        """
        self.kullanicild = kullanicild
        self.akisGonderileri = []

    def gonderi_ekle(self, gonderi):
        """
        Akışa yeni bir gönderi ekler.

        Args:
            gonderi (Gonderi): Akışa eklenecek Gonderi nesnesi.
        """
        self.akisGonderileri.append(gonderi)

    def to_dict(self):
        """
        Feed nesnesini JSON'a yazılabilir sözlük formatına dönüştürür.
        İçindeki tüm Gonderi nesneleri de sözlüğe çevrilir.

        Returns:
            dict: Feed verilerini içeren sözlük.
        """
        return {
            "kullanicild": self.kullanicild,
            "akisGonderileri": [g.to_dict() for g in self.akisGonderileri]
        }