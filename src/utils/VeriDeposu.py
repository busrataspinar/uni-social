from JsonIsleyicisi import JsonIsleyicisi


class VeriDeposu:
    """
    Uygulamanın tüm bellek içi veri listelerini ve JSON senkronizasyonunu
    merkezi olarak yöneten Singleton sınıfıdır.
    Uygulama boyunca yalnızca tek bir örneği oluşturulur.
    """

    _instance = None

    def __new__(cls):
        """
        Singleton desenini uygular. Sınıfın yalnızca bir örneğinin
        oluşturulmasını garanti eder.

        Returns:
            VeriDeposu: Mevcut tek örnek.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._baslat()
        return cls._instance

    def _baslat(self):
        """
        Uygulama açılışında JSON dosyalarından verileri belleğe yükler.
        Dosya yoksa ilgili liste boş başlar.
        """
        self.isleyici = JsonIsleyicisi()
        self.tum_kullanicilar = self.isleyici.veriOku("kullanicilar")
        self.tum_gonderiler   = self.isleyici.veriOku("gonderiler")
        self.tum_yorumlar     = self.isleyici.veriOku("yorumlar")
        self.tum_begeniler    = self.isleyici.veriOku("begeniler")
        self.tum_takipler     = self.isleyici.veriOku("takipler")

    def yeni_kullanici_id(self):
        """
        Mevcut kullanıcılar arasındaki en büyük ID'ye 1 ekleyerek
        yeni ve benzersiz bir kullanıcı ID'si üretir.

        Returns:
            int: Yeni kullanıcı ID'si.
        """
        if not self.tum_kullanicilar:
            return 1
        return max(k["kullaniciId"] for k in self.tum_kullanicilar) + 1

    def yeni_gonderi_id(self):
        """
        Mevcut gönderiler arasındaki en büyük ID'ye 1 ekleyerek
        yeni ve benzersiz bir gönderi ID'si üretir.

        Returns:
            int: Yeni gönderi ID'si.
        """
        if not self.tum_gonderiler:
            return 1
        return max(g["gonderiId"] for g in self.tum_gonderiler) + 1

    def yeni_yorum_id(self):
        """
        Mevcut yorumlar arasındaki en büyük ID'ye 1 ekleyerek
        yeni ve benzersiz bir yorum ID'si üretir.

        Returns:
            int: Yeni yorum ID'si.
        """
        if not self.tum_yorumlar:
            return 1
        return max(y["yorumId"] for y in self.tum_yorumlar) + 1

    def yeni_begeni_id(self):
        """
        Mevcut beğeniler arasındaki en büyük ID'ye 1 ekleyerek
        yeni ve benzersiz bir beğeni ID'si üretir.

        Returns:
            int: Yeni beğeni ID'si.
        """
        if not self.tum_begeniler:
            return 1
        return max(b["begeniId"] for b in self.tum_begeniler) + 1

    def kullanicilari_kaydet(self):
        """
        Bellekteki kullanıcı listesini kullanicilar.json dosyasına yazar.
        """
        self.isleyici.veriYaz("kullanicilar", self.tum_kullanicilar)

    def gonderileri_kaydet(self):
        """
        Bellekteki gönderi listesini gonderiler.json dosyasına yazar.
        """
        self.isleyici.veriYaz("gonderiler", self.tum_gonderiler)

    def yorumlari_kaydet(self):
        """
        Bellekteki yorum listesini yorumlar.json dosyasına yazar.
        """
        self.isleyici.veriYaz("yorumlar", self.tum_yorumlar)

    def begenileri_kaydet(self):
        """
        Bellekteki beğeni listesini begeniler.json dosyasına yazar.
        """
        self.isleyici.veriYaz("begeniler", self.tum_begeniler)

    def takipleri_kaydet(self):
        """
        Bellekteki takip listesini takipler.json dosyasına yazar.
        """
        self.isleyici.veriYaz("takipler", self.tum_takipler)