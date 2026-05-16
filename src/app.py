# app.py - UniSocial Flask Ana Çalıştırma Dosyası (Arayüz Test Aşaması)
# Bu dosya, templates klasöründeki HTML sayfalarını tarayıcıya sunar ve rotaları yönetir.
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "unisocial_gecici_test_anahtari"

# 1. GİRİŞ YAPMA ROTASI
@app.route('/', methods=['GET', 'POST'])
def login():
    """Bu rota, kullanıcıların giriş yapmasını sağlar. POST isteği ile gönderilen e-posta ve şifre bilgilerini alır ve geçici olarak session'a kaydeder.
    GET isteği ile login.html sayfasını render eder.
    Return: Kullanıcı giriş yaptıktan sonra feed sayfasına yönlendirilir. GET isteği ile login sayfası gösterilir.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"[TEST LOG] Giriş deneniyor - E-posta: {email}, Şifre: {password}")
        
        session['user_id'] = "test_id_123"
        session['username'] = "Test Kullanıcısı"
        return redirect(url_for('feed'))
        
    return render_template('login.html')

# 2. KAYIT OLMA ROTASI
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Bu rota, yeni kullanıcıların kayıt olmasını sağlar. POST isteği ile gönderilen isim ve e-posta bilgilerini alır ve geçici olarak loglar.
    GET isteği ile register.html sayfasını render eder.
    Return: Kullanıcı kayıt olduktan sonra login sayfasına yönlendirilir. GET isteği ile kayıt sayfası gösterilir.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        print(f"[TEST LOG] Yeni Kayıt Yakalandı -> İsim: {name}, E-posta: {email}")
        
        flash('Kayıt simülasyonu başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

# 3. ANA AKIŞ (FEED) ROTASI
@app.route('/feed')
def feed():
    """Bu rota, kullanıcıların ana akış sayfasını görüntülemesini sağlar. Sadece giriş yapmış kullanıcılar erişebilir.
    GET isteği ile feed.html sayfasını render eder ve mock gönderi verilerini şablona gönderir.
    Return: Giriş yapmış kullanıcılar için ana akış sayfası gösterilir.
    """
    mock_posts = [
        {
            "author_name": "Ahmet Yılmaz",
            "content": "Yazılım Mühendisliği projesinin Flask entegrasyonu üzerinde çalışıyorum. 1.5 gün çok az ama başaracağız! 🚀 #UniSocial",
            "timestamp": "16 Mayıs 2026 - 14:45",
            "likes_count": 8,
            "comments_count": 3
        },
        {
            "author_name": "Ayşe Demir",
            "content": "Kütüphanede BIL204 vize sınavına çalışan var mı? Ortak not paylaşımları için UniSocial harika bir yer.",
            "timestamp": "16 Mayıs 2026 - 12:20",
            "likes_count": 15,
            "comments_count": 7
        }
    ]
    return render_template('feed.html', posts=mock_posts)

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
        flash('Gönderiniz başarıyla paylaşıldı! (Simülasyon)', 'success')
        
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
    
    mock_user_posts = [
        {
            "content": "BIL204 Yazılım Mühendisliği dersi projemiz için GitHub Desktop kullanım kılavuzu hazırladım. İhtiyacı olan profilimden ulaşabilir! 📝",
            "timestamp": "15 Mayıs 2026 - 18:30",
            "likes_count": 12,
            "comments_count": 2
        },
        {
            "content": "Kampüsteki yemekhane sıraları için bir yoğunluk takip algoritması yazsak çok iyi olmaz mıydı? 🤔 #KampusHayati",
            "timestamp": "14 Mayıs 2026 - 13:15",
            "likes_count": 24,
            "comments_count": 9
        }
    ]
    return render_template('profile.html', user_posts=mock_user_posts)

# 6. OTURUM KAPATMA ROTASI
@app.route('/logout')
def logout():
    """Bu rota, kullanıcıların oturumlarını kapatmasını sağlar. Session'ı temizler ve kullanıcıyı giriş sayfasına yönlendirir.
    Return: Kullanıcı oturum kapattıktan sonra login sayfasına yönlendirilir.
    """
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)