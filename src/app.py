# app.py - UniSocial Flask Ana Çalıştırma Dosyası (Arayüz Test Aşaması)
# Bu dosya, templates klasöründeki HTML sayfalarını tarayıcıya sunar ve rotaları yönetir.

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "unisocial_gecici_test_anahtari"

# 1. GİRİŞ ROTASI (Kök Dizin)
# Kullanıcı siteye ilk girdiğinde login.html sayfasını görecek
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

# 2. ANA AKIŞ (FEED) ROTASI (Geçici Boş Taslak)
@app.route('/feed')
def feed():
    return "<h1>Akış Sayfası Geçici Taslak (Giriş Başarılı!)</h1>"

# 3. KAYIT ROTASI (Geçici Boş Taslak)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Form doldurulup "Hesap Oluştur" butonuna basıldığında tetiklenir
    if request.method == 'POST':
        # Form elemanlarından verileri topluyoruz
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        password = request.form.get('password')
        
        # [TEST LOG] Terminalde verilerin geldiğini doğrulamak için basıyoruz
        print("\n" + "="*40)
        print("[TEST LOG] VERİLER BAŞARIYLA YAKALANDI!")
        print(f"-> İsim: {name}")
        print(f"-> E-posta: {email}")
        print(f"-> Bölüm: {department}")
        print("="*40 + "\n")
        
        # Kullanıcıya bir sonraki sayfada parlayacak başarı mesajını ekliyoruz
        flash('Kayıt simülasyonu başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        
        # İşlem tamamlanınca kullanıcıyı giriş ekranına yönlendiriyoruz
        return redirect(url_for('login'))
        
    # Sayfaya düz tıklandığında sadece formu ekrana getirir
    return render_template('register.html')

# 4. PROFİL ROTASI (Geçici Boş Taslak)
@app.route('/profile')
def profile():
    return "<h1>Profil Sayfası Geçici Taslak</h1>"

# 5. ÇIKIŞ ROTASI
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # debug=True modu, kodda değişiklik yaptıkça sunucunun otomatik yenilenmesini sağlar
    app.run(debug=True)