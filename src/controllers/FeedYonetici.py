class FeedYonetici:
    """
    takip et/çıkar
    ana sayfa akisi
    kullanıcı arama
    hastag filtreleme
    """
    def __init__(self,json_isleyici):
        self.json_isleyici = json_isleyici #veri okuma/yazma araci
        self._takipler = [] #takipler.json'dan gelicek
        self._gonderiler = [] #gonderiler.json'dan gelicek
        self._kullanicilar = [] #kullaniciler.json dan gelicek

    #UC12
    def kullaniciTakipEt(self,kullaniciId,hedefId):
        pass
    def takiptenCik(self,kullaniciId,hedefId):
        pass

    def anaAkisiOlustur(self,kullaniciId):
        pass

    def kullaniciAra(self,aranankisi):
        pass

    def hashtagFilterele(self,hashtag):
        pass
