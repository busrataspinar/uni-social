from src.utils.VeriDeposu import isleyici, tum_kullanicilar, tum_gonderiler, tum_takipler

class FeedYonetici:
    def __init__(self):
        # JSON verileri ve veri işleyici yüklenir
        self.isleyici     = isleyici
        self.kullanicilar = tum_kullanicilar or []
        self.gonderiler   = tum_gonderiler or []

    # ---------------------------------------------------------
    # YARDIMCI FONKSİYON
    # ---------------------------------------------------------
    def kullanici_bul(self, kullanicild):
        """
        Amaç:Verilen kullanıcı ID'sine ait kullanıcıyı bulmak.

        Detay:Kullanıcı listesi üzerinde gezilerek eşleşen ID aranır.

        Parametre:kullanicild: Aranan kullanıcı ID'si

        Dönüş:dict | None: Kullanıcı bulunursa verisi, bulunamazsa None
        """
        pass
    # ---------------------------------------------------------
    # UC12: TAKİP SİSTEMİ
    # ---------------------------------------------------------
    def kullanici_takip_et(self, aktif_kullanicild, hedef_kullanicild):
        """
        Amaç:Aktif kullanıcının başka bir kullanıcıyı takip etmesini sağlamak.

        Detay:- Kullanıcılar kontrol edilir
            - Takip listesine ekleme yapılır
            - Güncel veri JSON dosyasına kaydedilir

        Parametreler:aktif_kullanicild: Takip eden kullanıcı
            hedef_kullanicild: Takip edilecek kullanıcı

        Dönüş:bool: İşlem başarılıysa True, değilse False
        """
        pass

    def takibi_birak(self, aktif_kullanicild, takipten_cikilacakld):
        """
        Amaç:Aktif kullanıcının bir kullanıcıyı takipten çıkmasını sağlamak.

        Detay:- Takip listesi kontrol edilir
            - İlgili kullanıcı listeden kaldırılır
            - Güncel veri JSON'a kaydedilir

        Parametreler:aktif_kullanicild: İşlem yapan kullanıcı
            takipten_cikilacakld: Takipten çıkarılacak kullanıcı

        Dönüş:bool: İşlem başarılıysa True, değilse False
        """
        pass
    # ---------------------------------------------------------
    # UC13: ANA SAYFA AKIŞI (FEED)
    # ---------------------------------------------------------
    def ana_akisi_olustur(self, aktif_kullanicild):
        """
        Amaç:Kullanıcının ana sayfa akışını oluşturmak.

        Detay:- Kullanıcının takip ettiği kişiler alınır
            - Bu kişilere ait gönderiler filtrelenir
            - Gönderiler tarihe göre (yeniden eskiye) sıralanır

        Parametre:aktif_kullanicild: Akışı oluşturulacak kullanıcı

        Dönüş:dict: Mesaj ve gönderi listesi içerir
        """
        pass
    def akisi_yenile(self, aktif_kullanicild):
        """
        Amaç:Güncel verileri JSON'dan tekrar yükleyerek akışı yenilemek.

        Detay:Kullanıcı ve gönderi verileri yeniden okunur ve akış tekrar oluşturulur.

        Parametre:aktif_kullanicild: Akışı yenilenecek kullanıcı

        Dönüş:dict: Güncellenmiş akış verisi
        """
        pass
    # ---------------------------------------------------------
    # UC14 & UC15: ARAMA VE FİLTRELEME
    # ---------------------------------------------------------
    def kullanici_ara(self, arama_metni):
        """
        Amaç:Kullanıcı adına göre arama yapmak.

        Detay:Girilen metin kullanıcı adları içinde aranır ve eşleşen sonuçlar döndürülür.

        Parametre:arama_metni: Aranacak ifade

        Dönüş:list: Eşleşen kullanıcıların ID ve kullanıcı adı bilgileri
        """
        pass

    def hashtag_ile_filtrele(self, hashtag):
        """
        Amaç:Belirli bir hashtag içeren gönderileri filtrelemek.

        Detay:Gönderi içerikleri taranır ve hashtag içerenler listelenir.

        Parametre:hashtag: Aranan etiket (#python gibi)

        Dönüş:list: Filtrelenmiş gönderiler
        """
        pass
    # ---------------------------------------------------------
    # PROFİL VE LİSTELEME DESTEĞİ
    # ---------------------------------------------------------
    def kullanici_gonderilerini_getir(self, hedef_kullanicild):
        """
        Amaç:Belirli bir kullanıcıya ait gönderileri getirmek.

        Detay:Tüm gönderiler filtrelenerek sadece ilgili kullanıcıya ait olanlar alınır.

        Parametre:hedef_kullanicild: Gönderileri alınacak kullanıcı

        Dönüş:list: Kullanıcının gönderileri (tarihe göre sıralı)
        """
        pass

    def istatistikleri_getir(self, kullanicild):
        """
        Amaç:Kullanıcının profil istatistiklerini hesaplamak.

        Detay:- Gönderi sayısı hesaplanır
            - Takip edilen kullanıcı sayısı alınır
            - Takipçi sayısı diğer kullanıcılar üzerinden hesaplanır

        Parametre:kullanicild: İstatistikleri hesaplanacak kullanıcı

        Dönüş:dict: Gönderi, takipçi ve takip edilen sayıları
        """
        pass

    def takip_listelerini_getir(self, kullanicild):
        """
        Amaç:Kullanıcının takipçi ve takip ettiği kullanıcı listelerini oluşturmak.

        Detay:- Takip edilen kullanıcılar listelenir
            - Diğer kullanıcılar üzerinden takipçiler bulunur

        Parametre:kullanicild: Listeleri alınacak kullanıcı

        Dönüş:dict: Takipçiler ve takip edilenler listesi
        """
        pass