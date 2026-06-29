import streamlit as st
import json
import os

# --- VERİ TABANI AYARLARI ---
DB_FILE = "depo_verisi.json"

def veri_yukle():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def veri_kaydet(depo):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(depo, f, ensure_ascii=False, indent=4)

if "depo" not in st.session_state:
    st.session_state.depo = veri_yukle()

depo = st.session_state.depo

# --- KULLANICI DOĞRULAMA (LOGIN) SİSTEMİ ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login(username, password):
    # Basit kullanıcı adı ve şifre tanımları
    if username == "admin" and password == "belkim41":
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.success("Yönetici girişi başarılı!")
        st.rerun()
    elif username == "operator" and password == "depo123":
        st.session_state.logged_in = True
        st.session_state.role = "Operatör"
        st.success("Kullanıcı girişi başarılı!")
        st.rerun()
    else:
        st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# --- GİRİŞ EKRANI ARAYÜZÜ ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="Giriş - Canlı Depo", layout="centered")
    st.title("🏭 Canlı Depo Yönetim Sistemi")
    st.subheader("Lütfen Giriş Yapın")
    
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş Yap", use_container_width=True):
        login(username, password)
        
    st.info("💡 Not: Admin yetkisiyle stok güncelleyebilir, Operatör yetkisiyle sadece arama yapabilirsiniz.")
    st.stop()

# --- ANA UYGULAMA ARAYÜZÜ (GİRİŞ YAPILDIKTAN SONRA) ---
st.set_page_config(page_title="Canlı Depo Yönetim Sistemi", layout="wide")

# Sağ üst köşeye çıkış butonu ve kullanıcı bilgisi ekleyelim
col_title, col_user = st.columns([4, 1])
with col_title:
    st.title("🏭 Canlı Depo ve Hammadde Takip Sistemi")
with col_user:
    st.write(f"👤 Rol: **{st.session_state.role}**")
    if st.button("Çıkış Yap"):
        logout()

st.write("---")

# --- MENÜ SEÇENEKLERİ (ROLE GÖRE FİLTRELEME) ---
st.sidebar.header("⚙️ Depo İşlemleri")

# Operatör sadece arama ve listelemeyi görebilir
if st.session_state.role == "Operatör":
    menü_secenekleri = ["🔍 Arama & Sorgulama", "📊 Tüm Depo Durumu"]
else:
    menü_secenekleri = ["🔍 Arama & Sorgulama", "📥 Stok Girişi / Güncelleme", "➕ Yeni Raf Tanımla", "📊 Tüm Depo Durumu"]

islem = st.sidebar.radio("Bir işlem seçin:", menü_secenekleri)

# --- 1. ARAMA & SORGULAMA ---
if islem == "🔍 Arama & Sorgulama":
    st.header("🔍 Hammadde veya Raf Ara")
    arama_turu = st.radio("Arama Yöntemi:", ["Hammaddeye Göre Ara", "Rafa Göre Ara"])

    if arama_turu == "Hammaddeye Göre Ara":
        arama_kelimesi = st.text_input("Aranacak Hammadde Adı:").strip().upper()
        if arama_kelimesi:
            bulundu = False
            toplam_stok = 0
            sonuclar = []
            
            for raf, icerik in depo.items():
                if arama_kelimesi in icerik:
                    miktar = icerik[arama_kelimesi]
                    sonuclar.append({"Raf Adresi": raf, "Miktar (kg)": miktar})
                    toplam_stok += miktar
                    bulundu = True
            
            if bulundu:
                st.success(f"📊 Toplam Depo Stoğu: **{toplam_stok} kg**")
                st.table(sonuclar)
            else:
                st.error(f"❌ Depoda '{arama_kelimesi}' isimli bir hammadde bulunamadı.")

    elif arama_turu == "Rafa Göre Ara":
        if depo:
            secilen_raf = st.selectbox("Sorgulanacak Rafı Seçin:", list(depo.keys()))
            st.subheader(f"📍 {secilen_raf} Raf İçeriği")
            if depo[secilen_raf]:
                raf_icerik = [{"Hammadde": k, "Miktar (kg)": v} for k, v in depo[secilen_raf].items()]
                st.table(raf_icerik)
            else:
                st.warning("Bu raf şu anda boş.")
        else:
            st.warning("Sistemde henüz tanımlı raf yok.")

# --- 2. STOK GİRİŞİ (YALNIZCA ADMIN) ---
elif islem == "📥 Stok Girişi / Güncelleme" and st.session_state.role == "Admin":
    st.header("📥 Rafa Malzeme Girişi")
    if depo:
        hedef_raf = st.selectbox("Malzemenin Konulacağı Raf:", list(depo.keys()))
        hammadde_adi = st.text_input("Hammadde Adı:").strip().upper()
        miktar = st.number_input("Miktar (kg):", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Stok Ekle (Var olanın üstüne ekler)", use_container_width=True):
                if hammadde_adi:
                    if hammadde_adi in depo[hedef_raf]:
                        depo[hedef_raf][hammadde_adi] += miktar
                    else:
                        depo[hedef_raf][hammadde_adi] = miktar
                    veri_kaydet(depo)
                    st.success(f"✅ {hedef_raf} rafına {miktar} kg {hammadde_adi} eklendi.")
                    st.rerun()
                else:
                    st.error("Lütfen hammadde adı girin.")
                    
        with col2:
            if st.button("Stoku Tamamen Sıfırla/Sil", use_container_width=True):
                if hammadde_adi in depo[hedef_raf]:
                    del depo[hedef_raf][hammadde_adi]
                    veri_kaydet(depo)
                    st.warning(f"🗑️ {hammadde_adi} malzemesi {hedef_raf} rafından tamamen silindi.")
                    st.rerun()
                else:
                    st.error("Bu rafta silinecek böyle bir malzeme bulunamadı.")
    else:
        st.warning("Önce 'Yeni Raf Tanımla' menüsünden sisteme raf eklemelisiniz.")

# --- 3. YENİ RAF TANIMLA (YALNIZCA ADMIN) ---
elif islem == "➕ Yeni Raf Tanımla" and st.session_state.role == "Admin":
    st.header("➕ Yeni Raf Adresi Oluştur")
    yeni_raf = st.text_input("Oluşturulacak Raf Adı (Örn: A-01-01, B-03-02):").strip().upper()
    
    if st.button("Rafı Sisteme Ekle"):
        if yeni_raf:
            if yeni_raf not in depo:
                depo[yeni_raf] = {}
                veri_kaydet(depo)
                st.success(f"✅ {yeni_raf} adresi sisteme başarıyla tanımlandı.")
                st.rerun()
            else:
                st.warning(f"⚠️ {yeni_raf} adresi zaten mevcut.")
        else:
            st.error("Raf adı boş bırakılamaz.")

# --- 4. TÜM DEPO DURUMU ---
elif islem == "📊 Tüm Depo Durumu":
    st.header("📊 Anlık Depo Durum Raporu")
    if depo:
        for raf, icerik in depo.items():
            with st.expander(f"📦 Raf: {raf}"):
                if icerik:
                    st.table([{"Hammadde": k, "Miktar (kg)": v} for k, v in icerik.items()])
                else:
                    st.write("Bu raf boş.")
    else:
        st.write("Depo henüz boş. Ekranın solundaki menüden raf ve stok ekleyerek başlayın.")
