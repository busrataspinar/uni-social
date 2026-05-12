from utils.JsonIsleyicisi import JsonIsleyicisi

# Singleton yapısı: Uygulama boyunca tek bir isleyici ve veri listeleri [cite: 539, 588]
isleyici = JsonIsleyicisi()

# Bellek içi listeler (RAM) [cite: 161, 537]
tum_kullanicilar = isleyici.verileri_yukle("kullanicilar") # kullanicilar.json'dan okur [cite: 166]
tum_gonderiler = isleyici.verileri_yukle("gonderiler")
tum_yorumlar = isleyici.verileri_yukle("yorumlar")
tum_begeniler = isleyici.verileri_yukle("begeniler")
tum_takipler = isleyici.verileri_yukle("takipler") # [cite: 171]