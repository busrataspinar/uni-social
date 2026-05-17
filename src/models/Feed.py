# Feed.py

class Feed:
    """
    Kullanıcıya özel hazırlanan içerik akışını temsil eder.
    Takip edilen kişilerin gönderilerinden oluşan listeyi barındırır.
    """

    def __init__(self, kullaniciId):
        """
        Feed nesnesini başlatır.

        Args:
            kullaniciId (int): Bu akışın ait olduğu öğrencinin ID'si.
        """
        self.kullaniciId = kullaniciId
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

        Returns:
            dict: Feed verilerini içeren sözlük.
        """
        return {
            "kullaniciId": self.kullaniciId,
            "akisGonderileri": [g.to_dict() for g in self.akisGonderileri]
        }

    @classmethod
    def from_dict(cls, veri):
        """
        Sözlük verisinden Feed nesnesi oluşturur.
        """
        feed = cls(veri["kullaniciId"])
        feed.akisGonderileri = veri.get("akisGonderileri", [])
        return feed