# app.py - UniSocial Flask Ana Çalıştırma Dosyası (Arayüz Test Aşaması)
# Bu dosya, templates klasöründeki HTML sayfalarını tarayıcıya sunar ve rotaları yönetir.
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

from controllers.KimlikYonetici import KimlikYonetici
from controllers.GonderiYonetici import GonderiYonetici
from controllers.FeedYonetici import FeedYonetici
from controllers.BegeniYonetici import BegeniYonetici
from controllers.YorumYonetici import YorumYonetici

app = Flask(__name__)
app.secret_key = "unisocial_gecici_test_anahtari"

# Her sınıftan sistem genelinde kullanılacak birer nesne türetiyoruz
kimlik_yonetici = KimlikYonetici()
gonderi_yonetici = GonderiYonetici()
feed_yonetici = FeedYonetici()
begeni_yonetici = BegeniYonetici()
yorum_yonetici = YorumYonetici()

# 1. GİRİŞ YAPMA ROTASI
@app.route('/', methods=['GET', 'POST'])
def login():
    """Bu rota, kullanıcıların giriş yapmasını sağlar. POST isteği ile gönderilen e-posta ve şifre bilgilerini alır ve geçici olarak session'a kaydeder.
    GET isteği ile login.html sayfasını render eder.
    Return: Kullanıcı giriş yaptıktan sonra feed sayfasına yönlendirilir. GET isteği ile login sayfası gösterilir.
    """
    if 'user_id' in session:
        return redirect(url_for('feed'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sonuc = kimlik_yonetici.giris_yap(email, password)
        
        if sonuc.get("basarili"):
            kullanici_verisi = sonuc.get("kullanici")
            session['user_id'] = kullanici_verisi.kullanicild
            session['username'] = kullanici_verisi.kullaniciAdi
            flash('Başarıyla giriş yapıldı, kampüse hoş geldiniz!', 'success')
            return redirect(url_for('feed'))
        else:
            flash(sonuc.get("hata", "Giriş başarısız!"), 'danger')
            
    return render_template('login.html')

# 2. KAYIT OLMA ROTASI
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Bu rota, yeni kullanıcıların kayıt olmasını sağlar. POST isteği ile gönderilen isim ve e-posta bilgilerini alır ve geçici olarak loglar.
    GET isteği ile register.html sayfasını render eder.
    Return: Kullanıcı kayıt olduktan sonra login sayfasına yönlendirilir. GET isteği ile kayıt sayfası gösterilir.
    """
    if 'user_id' in session:
        return redirect(url_for('feed'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        password = request.form.get('password')
        sonuc = kimlik_yonetici.kayit_ol(email, password, name, department)
        
        if sonuc.get("basarili"):
            flash('Hesabınız başarıyla oluşturuldu! Şimdi .edu e-postanızla giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        else:
            flash(sonuc.get("hata", "Kayıt işlemi başarısız oldu."), 'danger')
            
    return render_template('register.html')

# 3. ANA AKIŞ (FEED) ROTASI
@app.route('/feed')
def feed():
    """Bu rota, kullanıcıların ana akış sayfasını görüntülemesini sağlar. Sadece giriş yapmış kullanıcılar erişebilir.
    GET isteği ile feed.html sayfasını render eder ve mock gönderi verilerini şablona gönderir.
    Return: Giriş yapmış kullanıcılar için ana akış sayfası gösterilir.
    """
    if 'user_id' not in session:
        flash('Lütfen önce giriş yapın!', 'warning')
        return redirect(url_for('login'))
        
    # [KRİTİK ENTEGRASYON] Arkadaşının FeedYonetici.py içindeki ham listesini alıp
    # HTML şablonumuzun okuyabileceği (author_name, content, likes_count vb.) temiz bir yapıya dönüştürüyoruz
    ham_gonderiler = feed_yonetici.gonderiler
    canli_posts = []
    
    for h_gonderi in ham_gonderiler:
        # Her gönderinin yazar ID'si üzerinden ismini buluyoruz
        yazar = feed_yonetici.kullanici_bul(h_gonderi.yazarld)
        yazar_isim = yazar.get("kullaniciAdi") if yazar else "Bilinmeyen Üye"
        
        canli_posts.append({
            "author_name": yazar_isim,
            "content": h_gonderi.icerik,
            "timestamp": h_gonderi.tarih.strftime("%d %B %Y - %H:%M") if hasattr(h_gonderi.tarih, 'strftime') else h_gonderi.tarih,
            "likes_count": begeni_yonetici.begeni_sayisi_getir(h_gonderi.gonderild),
            "comments_count": len([y for y in yorum_yonetici.yorumlar if y.gonderild == h_gonderi.gonderild])
        })
        
    return render_template('feed.html', posts=canli_posts)

# 4. YENİ GÖNDERİ OLUŞTURMA ROTASI
@app.route('/create_post', methods=['POST'])
def create_post():
    """Bu rota, kullanıcıların yeni gönderi oluşturmasını sağlar. POST isteği ile gönderilen içerik bilgilerini alır ve simüle edilmiş bir başarı mesajı gösterir.
    Return: Gönderi oluşturulduktan sonra ana akış sayfasına yönlendirilir.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        post_content = request.form.get('content')
        aktif_user_id = session.get('user_id')
        
        # GonderiYonetici.py içindeki gerçek gonderi_olustur metodunu tetikliyoruz
        # Bu metot veriyi belleğe ekleyecek ve otomatik olarak data/gonderiler.json'a yazacaktır.
        sonuc = gonderi_yonetici.gonderi_olustur(yazarld=aktif_user_id, icerik=post_content)
        
        if sonuc.get("basarili"):
            flash('Kampüs duyurunuz başarıyla paylaşıldı!', 'success')
        else:
            flash(sonuc.get("hata", "Gönderi paylaşılırken bir sorun oluştu."), 'danger')
            
    return redirect(url_for('feed'))

# 5. PROFİL ROTASI (Dinamik Arayüz Test Sürümü)
@app.route('/profile')
def profile():
    """Bu rota, kullanıcıların kendi profil sayfalarını görüntülemesini sağlar. Sadece giriş yapmış kullanıcılar erişebilir.
    GET isteği ile profile.html sayfasını render eder ve simüle edilmiş kullanıcı gönderi verilerini şablona gönderir.
    Return: Giriş yapmış kullanıcılar için profil sayfası gösterilir.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    aktif_user_id = session.get('user_id')
    
    # Kendi paylaşımlarımızı süzüyoruz
    kendi_ham_gonderileri = [g for g in gonderi_yonetici.gonderiler if g.yazarld == aktif_user_id]
    kendi_posts = []
    
    for kg in kendi_ham_gonderileri:
        kendi_posts.append({
            "content": kg.icerik,
            "timestamp": kg.tarih.strftime("%d %B %Y - %H:%M") if hasattr(kg.tarih, 'strftime') else kg.tarih,
            "likes_count": begeni_yonetici.begeni_sayisi_getir(kg.gonderild),
            "comments_count": len([y for y in yorum_yonetici.yorumlar if y.gonderild == kg.gonderild])
        })
        
    return render_template('profile.html', user_posts=kendi_posts)

# 6. OTURUM KAPATMA ROTASI
@app.route('/logout')
def logout():
    """Bu rota, kullanıcıların oturumlarını kapatmasını sağlar. Session'ı temizler ve kullanıcıyı giriş sayfasına yönlendirir.
    Return: Kullanıcı oturum kapattıktan sonra login sayfasına yönlendirilir.
    """
    session.clear()
    flash('Oturumunuz güvenli bir şekilde kapatıldı.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)