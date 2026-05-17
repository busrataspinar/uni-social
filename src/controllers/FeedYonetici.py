from utils.VeriDeposu import VeriDeposu

class FeedYonetici:
    def __init__(self):
        self.depo = VeriDeposu()
        self.kullanicilar = self.depo.tum_kullanicilar
        self.gonderiler = self.depo.tum_gonderiler

    # ---------------------------------------------------------
    # YARDIMCI FONKSİYON
    # ---------------------------------------------------------
    def kullanici_bul(self, kullaniciId):
        """
        Amaç:Verilen kullanıcı ID'sine ait kullanıcıyı bulmak.
        Detay:Kullanıcı listesi üzerinde gezilerek eşleşen ID aranır.
        Parametre:kullaniciId: Aranan kullanıcı ID'si
        Dönüş:dict | None: Kullanıcı bulunursa verisi, bulunamazsa None
        """
        for kullanici in self.kullanicilar or []:
            if kullanici.get("kullaniciId") == kullaniciId:
                return kullanici
        return None

    # ---------------------------------------------------------
    # UC12: TAKİP SİSTEMİ
    # ---------------------------------------------------------
    def kullanici_takip_et(self, aktif_kullaniciId, hedef_kullaniciId):
        """
        Amaç:Aktif kullanıcının başka bir kullanıcıyı takip etmesini sağlamak.
        Detay:- Kullanıcılar kontrol edilir
            - Takip listesine ekleme yapılır
            - Güncel veri JSON dosyasına kaydedilir
        Parametreler:aktif_kullaniciId: Takip eden kullanıcı
            hedef_kullaniciId: Takip edilecek kullanıcı
        Dönüş:bool: İşlem başarılıysa True, değilse False
        """
        aktif_kullanici = self.kullanici_bul(aktif_kullaniciId)
        hedef_kullanici = self.kullanici_bul(hedef_kullaniciId)

        if not aktif_kullanici or not hedef_kullanici or aktif_kullaniciId == hedef_kullaniciId:
            return False

        aktif_kullanici.setdefault("takipEdilenler", [])

        if hedef_kullaniciId not in aktif_kullanici["takipEdilenler"]:
            aktif_kullanici["takipEdilenler"].append(hedef_kullaniciId)
            self.depo.kullanicilari_kaydet()
            return True

        return False

    def takibi_birak(self, aktif_kullaniciId, takipten_cikilacakId):
        """
        Amaç:Aktif kullanıcının bir kullanıcıyı takipten çıkmasını sağlamak.
        Detay:- Takip listesi kontrol edilir
            - İlgili kullanıcı listeden kaldırılır
            - Güncel veri JSON'a kaydedilir
        Parametreler:aktif_kullaniciId: İşlem yapan kullanıcı
            takipten_cikilacakId: Takipten çıkarılacak kullanıcı
        Dönüş:bool: İşlem başarılıysa True, değilse False
        """
        aktif_kullanici = self.kullanici_bul(aktif_kullaniciId)

        if aktif_kullanici:
            takip_listesi = aktif_kullanici.setdefault("takipEdilenler", [])

            if takipten_cikilacakId in takip_listesi:
                takip_listesi.remove(takipten_cikilacakId)
                self.depo.kullanicilari_kaydet()
                return True

        return False

    # ---------------------------------------------------------
    # UC13: ANA SAYFA AKIŞI (FEED)
    # ---------------------------------------------------------
    def ana_akisi_olustur(self, aktif_kullaniciId, yorum_yonetici, begeni_yonetici):
        """
        Amaç: Kullanıcının takip ettiği kişilerin gönderilerini beğeni ve yorum sayılarıyla
              birlikte, tarihe göre sıralı (yeniden eskiye) şekilde getirmek.
        """
        # 1. Kullanıcı kontrolü (Güvenlik Önlemi)
        aktif_kullanici = self.kullanici_bul(aktif_kullaniciId)
        if not aktif_kullanici:
            return {"mesaj": "Kullanıcı bulunamadı.", "gonderiler": []}

        #Takip listesi kontrolü
        takip_listesi = aktif_kullanici.get("takipEdilenler", [])
        if not takip_listesi:
            return {"mesaj": "Akış boş. Takip ederek akışınızı canlandırabilirsiniz.", "gonderiler": []}

        filtrelenmiş_gonderiler = [
            g for g in self.gonderiler or []
            if g.get("yazarId") in takip_listesi
        ]

        if not filtrelenmiş_gonderiler:
            return {"mesaj": "Takip ettikleriniz henüz gönderi paylaşmadı.", "gonderiler": []}


        filtrelenmiş_gonderiler.sort(key=lambda x: x.get("tarih", ""), reverse=True)

        akistan_gelenler = []
        for g in filtrelenmiş_gonderiler:
            gonderi_id = g.get("gonderiId")

            akistan_gelenler.append({
                "gonderi": g,
                "begeni_sayisi": begeni_yonetici.begeni_sayisi_getir(gonderi_id) if begeni_yonetici else 0,
                "yorum_sayisi": yorum_yonetici.gonderi_yorum_sayisi(gonderi_id) if yorum_yonetici else 0
            })

        return {"mesaj": "Akış güncellendi.", "gonderiler": akistan_gelenler}

    def akisi_yenile(self, aktif_kullaniciId, yorum_yonetici, begeni_yonetici):
        """
        Amaç: Kullanıcının akışını güncellemek.
        Detay: VeriDeposu'ndan kullanıcı ve gönderi listeleri yeniden yüklenir,
               beğeni ve yorum yöneticileriyle birlikte ana akış güncellenir.
        Parametreler:
            aktif_kullaniciId (int) – Akışı yenilenecek kullanıcı ID'si
            yorum_yonetici – Güncel yorum sayılarını almak için yorum yönetim nesnesi
            begeni_yonetici – Güncel beğeni sayılarını almak için beğeni yönetim nesnesi
        Dönüş: dict – Mesaj ve güncel, zenginleştirilmiş gönderi listesi
        """
        # Bellekteki havuzun en taze referanslarını senkronize et
        self.kullanicilar = self.depo.tum_kullanicilar
        self.gonderiler = self.depo.tum_gonderiler

        # Yeni eklenen parametreleri ana_akisi_olustur'a güvenli bir şekilde pasla
        return self.ana_akisi_olustur(aktif_kullaniciId, yorum_yonetici, begeni_yonetici)

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
        if not arama_metni or not arama_metni.strip():
            return []

        arama_metni_lower = arama_metni.lower().strip()

        return [
            {
                "kullaniciId": k.get("kullaniciId"),
                "kullaniciAdi": k.get("kullaniciAdi")
            }
            for k in self.kullanicilar or []
            if arama_metni_lower in k.get("kullaniciAdi", "").lower()
        ]

    def hashtag_ile_filtrele(self, hashtag):
        """
        Amaç:Belirli bir hashtag içeren gönderileri filtrelemek.
        Detay:Gönderi içerikleri taranır ve hashtag içerenler listelenir.
        Parametre:hashtag: Aranan etiket (#python gibi)
        Dönüş:list: Filtrelenmiş gönderiler
        """
        if not hashtag or not hashtag.strip() or hashtag.strip() == "#":
            return []

        hashtag = hashtag.strip().lower()

        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag

        sonuclar = [
            g for g in self.gonderiler or []
            if hashtag in g.get("icerik", "").lower()
        ]

        sonuclar.sort(key=lambda x: x.get("tarih", ""), reverse=True)

        return sonuclar

    # ---------------------------------------------------------
    # PROFİL VE LİSTELEME DESTEĞİ
    # ---------------------------------------------------------
    def kullanici_gonderilerini_getir(self, hedef_kullaniciId):
        """
        Amaç:Belirli bir kullanıcıya ait gönderileri getirmek.
        Detay:Tüm gönderiler filtrelenerek sadece ilgili kullanıcıya ait olanlar alınır.
        Parametre:hedef_kullaniciId: Gönderileri alınacak kullanıcı
        Dönüş:list: Kullanıcının gönderileri (tarihe göre sıralı)
        """
        postlar = [
            g for g in self.gonderiler or []
            if g.get("yazarId") == hedef_kullaniciId
        ]

        postlar.sort(key=lambda x: x.get("tarih", ""), reverse=True)

        return postlar

    def istatistikleri_getir(self, kullaniciId):
        """
        Amaç:Kullanıcının profil istatistiklerini hesaplamak.
        Detay:- Gönderi sayısı hesaplanır
            - Takip edilen kullanıcı sayısı alınır
            - Takipçi sayısı diğer kullanıcılar üzerinden hesaplanır
        Parametre:kullaniciId: İstatistikleri hesaplanacak kullanıcı
        Dönüş:dict: Gönderi, takipçi ve takip edilen sayıları
        """
        kullanici = self.kullanici_bul(kullaniciId)

        if not kullanici:
            return {
                "gonderi_sayisi": 0,
                "takipci_sayisi": 0,
                "takip_edilen_sayisi": 0
            }

        gonderi_sayisi = sum(
            1 for g in self.gonderiler or []
            if g.get("yazarId") == kullaniciId
        )

        takip_edilen_sayisi = len(kullanici.get("takipEdilenler", []))

        takipci_sayisi = sum(
            1 for k in self.kullanicilar or []
            if kullaniciId in k.get("takipEdilenler", [])
        )

        return {
            "gonderi_sayisi": gonderi_sayisi,
            "takipci_sayisi": takipci_sayisi,
            "takip_edilen_sayisi": takip_edilen_sayisi
        }

    def takip_listelerini_getir(self, kullaniciId):
        """
        Amaç:Kullanıcının takipçi ve takip ettiği kullanıcı listelerini oluşturmak.
        Detay:- Takip edilen kullanıcılar listelenir
            - Diğer kullanıcılar üzerinden takipçiler bulunur
        Parametre:kullaniciId: Listeleri alınacak kullanıcı
        Dönüş:dict: Takipçiler ve takip edilenler listesi
        """
        kullanici = self.kullanici_bul(kullaniciId)

        if not kullanici:
            return {"takipciler": [], "takip_edilenler": []}

        takip_edilen_idler = kullanici.get("takipEdilenler", [])

        takipciler = []
        takip_edilenler = []

        for k in self.kullanicilar or []:
            k_id = k.get("kullaniciId")
            k_isim = k.get("kullaniciAdi")

            if k_id in takip_edilen_idler:
                takip_edilenler.append({"id": k_id, "isim": k_isim})

            if kullaniciId in k.get("takipEdilenler", []):
                takipciler.append({"id": k_id, "isim": k_isim})

        return {
            "takipciler": takipciler,
            "takip_edilenler": takip_edilenler
        }