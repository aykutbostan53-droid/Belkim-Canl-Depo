import streamlit as st
import json
import os
from datetime import datetime

# --- VERİ TABANI AYARLARI ---
DB_FILE = "depo_verisi.json"

# Excel'den otomatik olarak çekilen tüm raf adresleri listesi
EXCEL_RAFLARI = [
    "A111", "A112", "A113", "A121", "A122", "A123", "A131", "A132", "A133",
    "A211", "A212", "A213", "A221", "A222", "A223", "A231", "A232", "A233",
    "A311", "A312", "A313", "A321", "A322", "A323", "A331", "A332", "A333",
    "A411", "A412", "A413", "A421", "A422", "A423", "A431", "A432", "A433",
    "A511", "A512", "A513", "A521", "A522", "A523", "A531", "A532", "A533",
    "B111", "B112", "B113", "B121", "B122", "B123", "B131", "B132", "B133",
    "B211", "B212", "B213", "B221", "B222", "B223", "B231", "B232", "B233",
    "B311", "B312", "B313", "B321", "B322", "B323", "B331", "B332", "B333",
    "B411", "B412", "B413", "B421", "B422", "B423", "B431", "B432", "B433",
    "C111", "C112", "C113", "C121", "C122", "C123", "C131", "C132", "C133",
    "C211", "C212", "C213", "C221", "C222", "C223", "C231", "C232", "C233",
    "C311", "C312", "C313", "C321", "C322", "C323", "C331", "C332", "C333",
    "C411", "C412", "C413", "C421", "C422", "C423", "C431", "C432", "C433",
    "C511", "C512", "C513", "C521", "C522", "C523", "C531", "C532", "C533",
    "D111", "D112", "D113", "D121"
]

def veri_yukle():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            mevcut_veri = json.load(f)
        
        # Eğer yapıda 'stok' veya 'kullanicilar' anahtarı yoksa eski yapıdan yeni yapıya dönüştür
        if "stok" not in mevcut_veri:
            eski_veri = mevcut_veri.copy()
            mevcut_veri = {
                "stok": eski_veri,
                "kullanicilar": ["sinem", "vedat", "halim", "yasin"]  # Varsayılan başlangıç listesi
            }
        
        # Boş rafları kontrol et ve ekle
        for raf in EXCEL_RAFLARI:
            if raf not in mevcut_veri["stok"]:
                mevcut_veri["stok"][raf] = {}
        return mevcut_veri
    
    # Sıfırdan kuruluyorsa varsayılan yapı
    return {
        "stok": {raf: {} for raf in EXCEL_RAFLARI},
        "kullanicilar": ["sinem", "vedat", "halim", "yasin"]
    }

def veri_kaydet(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "depo_data" not in st.session_state:
    st.session_state.depo_data = veri_yukle()

data = st.session_state.depo_data
depo = data["stok"]
kullanicilar = data["kullanicilar"]

# --- KULLANICI DOĞRULAMA (LOGIN) SİSTEMİ ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_display_name = ""
    st.session_state.role = None

def login(username, password):
    u_clean = username.strip().lower()
    p_clean = password.strip()
    
    if u_clean == "admin" and p_clean == "belkim41":
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.session_state.user_display_name = "Yönetici (Admin)"
        st.success("Yönetici girişi başarılı!")
        st.rerun()
    elif u_clean in kullanicilar and p_clean == u_clean:
        st.session_state.logged_in = True
        st.session_state.role = "Operatör"
        st.session_state.user_display_name = u_clean.capitalize()
        st.success(f"Giriş başarılı! Hoş geldin, {st.session_state.user_display_name}.")
        st.rerun()
    else:
        st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_display_name = ""
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
    st.stop()

# --- ANA UYGULAMA ARAYÜZÜ ---
st.set_page_config(page_title="Canlı Depo Yönetim Sistemi", layout="wide")

col_title, col_user = st.columns([4, 1])
with col_title:
    st.title("🏭 Canlı Depo ve Hammadde Takip Sistemi")
with col_user:
    st.write(f"👤 Kullanıcı: **{st.session_state.user_display_name}**")
    if st.button("Çıkış Yap"):
        logout()

st.write("---")

# --- MENÜ SEÇENEKLERİ ---
st.sidebar.header("⚙️ Depo İşlemleri")
if st.session_state.role == "Operatör":
    menü_secenekleri = ["🔍 Arama & Sorgulama", "📊 Tüm Depo Durumu"]
else:
    menü_secenekleri = ["🔍 Arama & Sorgulama", "📥 Stok Ekle / Güncelle", "📤 Stok Çıkar / Azalt / Sil", "➕ Yeni Raf Tanımla", "👥 Kullanıcı Yönetimi", "📊 Tüm Depo Durumu"]

islem = st.sidebar.radio("Bir işlem seçin:", menü_secenekleri)

# --- 1. ARAMA & SORGULAMA ---
if islem == "🔍 Arama & Sorgulama":
    st.header("🔍 Hammadde veya Raf Ara")
    arama_turu = st.radio("Arama Yöntemi:", ["Hammaddeye Göre Ara", "Rafa Göre Ara"])

    if arama_turu == "Hammaddeye Göre Ara":
        arama_kelimesi = st.text_input("Aranacak Hammadde Adı:").strip().upper()
        if arama_kelimesi:
            bulundu = False
            sonuclar = []
            
            for raf, icerik in depo.items():
                if arama_kelimesi in icerik:
                    for s_key, detay in icerik[arama_kelimesi].items():
                        sonuclar.append({
                            "Raf Adresi": raf,
                            "Miktar (kg)": detay["miktar"],
                            "Son Kullanma Tarihi": detay["skt"]
                        })
                        bulundu = True
            
            if bulundu:
                st.table(sonuclar)
            else:
                st.error(f"❌ Depoda '{arama_kelimesi}' isimli bir hammadde bulunamadı.")

    elif arama_turu == "Rafa Göre Ara":
        secilen_raf = st.selectbox("Sorgulanacak Rafı Seçin:", sorted(list(depo.keys())))
        st.subheader(f"📍 {secilen_raf} Raf İçeriği")
        if depo[secilen_raf]:
            raf_icerik = []
            for hammadde, veriler in depo[secilen_raf].items():
                for s_key, detay in veriler.items():
                    raf_icerik.append({
                        "Hammadde": hammadde,
                        "Miktar (kg)": detay["miktar"],
                        "Son Kullanma Tarihi": detay["skt"]
                    })
            st.table(raf_icerik)
        else:
            st.warning("Bu raf şu anda boş.")

# --- 2. STOK GİRİŞİ (ADMIN) ---
elif islem == "📥 Stok Ekle / Güncelle" and st.session_state.role == "Admin":
    st.header("📥 Rafa Malzeme Girişi")
    hedef_raf = st.selectbox("Malzemenin Konulacağı Raf:", sorted(list(depo.keys())))
    hammadde_adi = st.text_input("Hammadde Adı:").strip().upper()
    miktar = st.number_input("Eklenecek Miktar (kg):", min_value=1, step=1)
    
    skt_opsiyon = st.checkbox("Son Kullanma Tarihi Girmek İstiyorum")
    skt_tarihi = "Girilmedi"
    if skt_opsiyon:
        skt_tarihi = st.date_input("Son Kullanma Tarihi Seçin:", min_value=datetime.today()).strftime("%Y-%m-%d")
    
    if st.button("Stoku Kaydet/Ekle", use_container_width=True):
        if hammadde_adi:
            if hammadde_adi not in depo[hedef_raf]:
                depo[hedef_raf][hammadde_adi] = {}
            
            if skt_tarihi in depo[hedef_raf][hammadde_adi]:
                depo[hedef_raf][hammadde_adi][skt_tarihi]["miktar"] += miktar
            else:
                depo[hedef_raf][hammadde_adi][skt_tarihi] = {"miktar": miktar, "skt": skt_tarihi}
                
            veri_kaydet(data)
            st.success(f"✅ {hedef_raf} rafına {miktar} kg {hammadde_adi} (SKT: {skt_tarihi}) başarıyla eklendi!")
        else:
            st.error("Lütfen hammadde adı girin.")

# --- 3. STOK ÇIKAR / SİL (ADMIN) ---
elif islem == "📤 Stok Çıkar / Azalt / Sil" and st.session_state.role == "Admin":
    st.header("📤 Raftan Malzeme Çıkarma / Azaltma")
    hedef_raf = st.selectbox("Malzemenin Çıkarılacağı Raf:", sorted(list(depo.keys())))
    
    if depo[hedef_raf]:
        hammadde_adi = st.selectbox("Çıkarılacak Hammaddeyi Seçin:", list(depo[hedef_raf].keys()))
        skt_listesi = list(depo[hedef_raf][hammadde_adi].keys())
        secilen_skt = st.selectbox("Hangi SKT'li Ürün Çıkarılacak?", skt_listesi)
        
        mevcut_miktar = depo[hedef_raf][hammadde_adi][secilen_skt]["miktar"]
        st.info(f"💡 Bu rafta seçilen üründen şu an **{mevcut_miktar} kg** var.")
        
        cikarilacak_miktar = st.number_input("Çıkarılacak/Azaltılacak Miktar (kg):", min_value=1, max_value=int(mevcut_miktar), step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Seçilen Miktarı Stoktan Düş", use_container_width=True):
                depo[hedef_raf][hammadde_adi][secilen_skt]["miktar"] -= cikarilacak_miktar
                if depo[hedef_raf][hammadde_adi][secilen_skt]["miktar"] <= 0:
                    del depo[hedef_raf][hammadde_adi][secilen_skt]
                if not depo[hedef_raf][hammadde_adi]:
                    del depo[hedef_raf][hammadde_adi]
                    
                veri_kaydet(data)
                st.success(f"📉 Raftan {cikarilacak_miktar} kg düşüldü.")
                st.rerun()
                
        with col2:
            if st.button("Bu Ürünü Raftan Tamamen Sil", use_container_width=True):
                del depo[hedef_raf][hammadde_adi][secilen_skt]
                if not depo[hedef_raf][hammadde_adi]:
                    del depo[hedef_raf][hammadde_adi]
                veri_kaydet(data)
                st.warning("🗑️ Ürün raftan tamamen temizlendi.")
                st.rerun()
    else:
        st.warning("Seçilen raf zaten şu anda tamamen boş.")

# --- 4. YENİ RAF TANIMLA (ADMIN) ---
elif islem == "➕ Yeni Raf Tanımla" and st.session_state.role == "Admin":
    st.header("➕ Yeni Ekstra Raf Adresi Oluştur")
    yeni_raf = st.text_input("Oluşturulacak Raf Adı (Örn: E111):").strip().upper()
    
    if st.button("Rafı Sisteme Ekle"):
        if yeni_raf:
            if yeni_raf not in depo:
                depo[yeni_raf] = {}
                veri_kaydet(data)
                st.success(f"✅ {yeni_raf} adresi sisteme başarıyla tanımlandı.")
                st.rerun()
            else:
                st.warning(f"⚠️ {yeni_raf} adresi zaten mevcut.")
        else:
            st.error("Raf adı boş bırakılamaz.")

# --- 5. KULLANICI YÖNETİMİ (YALNIZCA ADMIN) ---
elif islem == "👥 Kullanıcı Yönetimi" and st.session_state.role == "Admin":
    st.header("👥 Kullanıcı Hesapları Yönetimi")
    
    st.subheader("Yeni Kullanıcı Ekle")
    yeni_user = st.text_input("Eklenecek Kullanıcı Adı (Küçük harf, Türkçe karaktersiz):").strip().lower()
    if st.button("Kullanıcıyı Kaydet"):
        if yeni_user and yeni_user not in kullanicilar and yeni_user != "admin":
            kullanicilar.append(yeni_user)
            veri_kaydet(data)
            st.success(f"✅ '{yeni_user}' kullanıcısı eklendi. (Şifresi de otomatik olarak '{yeni_user}' olmuştur.)")
            st.rerun()
        else:
            st.error("Geçersiz kullanıcı adı veya bu kullanıcı zaten mevcut.")
            
    st.write("---")
    st.subheader("Mevcut Kullanıcı Listesi")
    if kullanicilar:
        for idx, user in enumerate(kullanicilar):
            col_u_name, col_u_del = st.columns([3, 1])
            with col_u_name:
                st.write(f"👤 {user.capitalize()} (Şifre: {user})")
            with col_u_del:
                if st.button("Sil", key=f"del_{idx}"):
                    kullanicilar.remove(user)
                    veri_kaydet(data)
                    st.warning(f"🗑️ {user.capitalize()} kullanıcısı sistemden silindi.")
                    st.rerun()
    else:
        st.write("Sistemde admin dışında tanımlı kullanıcı yok.")

# --- 6. TÜM DEPO DURUMU ---
elif islem == "📊 Tüm Depo Durumu":
    st.header("📊 Anlık Depo Durum Raporu")
    dolu_raflar = {k: v for k, v in depo.items() if v}
    
    if dolu_raflar:
        for raf, icerik in sorted(dolu_raflar.items()):
            with st.expander(f"📦 Raf: {raf} (Dolu)"):
                raf_tablo = []
                for hammadde, veriler in icerik.items():
                    for s_key, detay in veriler.items():
                        raf_tablo.append({
                            "Hammadde": hammadde,
                            "Miktar (kg)": detay["miktar"],
                            "Son Kullanma Tarihi": detay["skt"]
                        })
                st.table(raf_tablo)
    else:
        st.write("Depodaki tüm raflar şu anda boş.")
