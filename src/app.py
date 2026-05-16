# app.py - UniSocial Flask Ana Çalıştırma Dosyası (Arayüz Test Aşaması)
# Bu dosya, templates klasöründeki HTML sayfalarını tarayıcıya sunar ve rotaları yönetir.
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "unisocial_gecici_test_anahtari"

# 1. GİRİŞ YAPMA ROTASI
@app.route('/', methods=['GET', 'POST'])
def login():
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
    # Arayüzün listeleme yapısını görsel test edebilmek adına oluşturulmuş sahte post listesi
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        post_content = request.form.get('content')        
        flash('Gönderiniz başarıyla paylaşıldı! (Simülasyon)', 'success')
        
    return redirect(url_for('feed'))

# 5. GEÇİCİ PROFİL ROTASI
@app.route('/profile')
def profile():
    return "<h1>Profil Sayfası Geçici Taslak</h1>"

# 6. OTURUM KAPATMA ROTASI
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)