import streamlit as st
import json
import os
from datetime import datetime

# --- VERİ TABANI AYARLARI ---
DB_FILE = "depo_sistemi_guncel.json"

# Excel'den gelen tüm raf adresleri
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
            try:
                mevcut_veri = json.load(f)
            except:
                mevcut_veri = {}
        
        if not isinstance(mevcut_veri, dict) or "stok" not in mevcut_veri:
            mevcut_veri = {
                "stok": {raf: {} for raf in EXCEL_RAFLARI},
                "kullanicilar": ["sinem", "vedat", "halim", "yasin"],
                "gecmis": []
            }
        
        if "gecmis" not in mevcut_veri:
            mevcut_veri["gecmis"] = []
            
        for raf in EXCEL_RAFLARI:
            if raf not in mevcut_veri["stok"] or not isinstance(mevcut_veri["stok"][raf], dict):
                mevcut_veri["stok"][raf] = {}
            else:
                for hmd in list(mevcut_veri["stok"][raf].keys()):
                    if not isinstance(mevcut_veri["stok"][raf][hmd], dict):
                        mevcut_veri["stok"][raf][hmd] = {}
                        
        return mevcut_veri
    
    return {
        "stok": {raf: {} for raf in EXCEL_RAFLARI},
        "kullanicilar": ["sinem", "vedat", "halim", "yasin"],
        "gecmis": []
    }

def veri_kaydet(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "depo_data" not in st.session_state:
    st.session_state.depo_data = veri_yukle()

data = st.session_state.depo_data
depo = data["stok"]
kullanicilar = data["kullanicilar"]
gecmis_loglari = data.get("gecmis", [])

if "basari_mesaji" not in st.session_state:
    st.session_state.basari_mesaji = None
if "uyari_mesaji" not in st.session_state:
    st.session_state.uyari_mesaji = None

# --- KULLANICI DOĞRULAMA (LOGIN) SİSTEMİ ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_display_name = ""

def login(username, password):
    u_clean = username.strip().lower()
    p_clean = password.strip()
    
    if u_clean == "admin" and p_clean == "belkim41":
        st.session_state.logged_in = True
        st.session_state.user_display_name = "Yönetici (Admin)"
        st.success("Giriş başarılı!")
        st.rerun()
    elif u_clean in kullanicilar and p_clean == u_clean:
        st.session_state.logged_in = True
        st.session_state.user_display_name = u_clean.capitalize()
        st.success(f"Giriş başarılı! Hoş geldin, {st.session_state.user_display_name}.")
        st.rerun()
    else:
        st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_display_name = ""
    st.rerun()

# --- GİRİŞ EKRANI ARAYÜZÜ ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="Giriş - Canlı Depo", layout="centered")
    st.title("🏭 Canlı Depo Yönetim Sistemi")
    st.subheader("Lütfen Giriş Yapın")
    
    username = st.text_input("Kullanıcı Adı", key="login_username_input")
    password = st.text_input("Şifre", type="password", key="login_password_input")
    
    if st.button("Giriş Yap", use_container_width=True, key="login_submit_btn"):
        login(username, password)
    st.stop()

# --- ANA UYGULAMA ARAYÜZÜ ---
st.set_page_config(page_title="Canlı Depo Yönetim Sistemi", layout="wide")

col_title, col_user = st.columns([4, 1])
with col_title:
    st.title("🏭 Canlı Depo ve Hammadde Takip Sistemi")
with col_user:
    st.write(f"👤 Giriş Yapan: **{st.session_state.user_display_name}**")
    if st.button("Çıkış Yap", key="logout_action_btn"):
        logout()

st.write("---")

if st.session_state.basari_mesaji:
    st.success(st.session_state.basari_mesaji)
    st.session_state.basari_mesaji = None
if st.session_state.uyari_mesaji:
    st.warning(st.session_state.uyari_mesaji)
    st.session_state.uyari_mesaji = None

# --- MENÜ SEÇENEKLERİ ---
st.sidebar.header("⚙️ Depo İşlemleri")

# Sunucunun dil karmaşasını önlemek için arka plan anahtarları (Key) ekledik
menü_secenekleri = {
    "m1": "🔍 Arama & Sorgulama", 
    "m2": "📥 Stok Ekle / Güncelle", 
    "m3": "📤 Stok Çıkar / Azalt / Sil", 
    "m4": "➕ Yeni Raf Tanımla", 
    "m5": "👥 Kullanıcı Yönetimi", 
    "m6": "📊 Tüm Depo Durumu",
    "m7": "📜 Depo Hareket Geçmişi"
}

secilen_key = st.sidebar.radio(
    "Bir işlem seçin:", 
    options=list(menü_secenekleri.keys()), 
    format_func=lambda x: menü_secenekleri[x],
    key="main_navigation_sidebar"
)

# --- 1. ARAMA & SORGULAMA ---
if secilen_key == "m1":
    st.header("🔍 Hammadde veya Raf Ara")
    arama_turu = st.radio("Arama Yöntemi:", ["Hammaddeye Göre Ara", "Rafa Göre Ara"], key="search_type_selector")

    if arama_turu == "Hammaddeye Göre Ara":
        arama_kelimesi = st.text_input("Aranacak Hammadde Adı:", key="search_raw_material_input").strip().upper()
        if arama_kelimesi:
            bulundu = False
            sonuclar = []
            
            for raf, icerik in depo.items():
                if isinstance(icerik, dict) and arama_kelimesi in icerik:
                    if isinstance(icerik[arama_kelimesi], dict):
                        for s_key, detay in icerik[arama_kelimesi].items():
                            sonuclar.append({
                                "Raf Adresi": raf,
                                "Miktar (kg)": detay.get("miktar", 0),
                                "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                            })
                            bulundu = True
            
            if bulundu:
                st.table(sonuclar)
            else:
                st.error(f"❌ Depoda '{arama_kelimesi}' isimli bir hammadde bulunamadı.")

    elif arama_turu == "Rafa Göre Ara":
        secilen_raf = st.selectbox("Sorgulanacak Rafı Seçin:", sorted(list(depo.keys())), key="search_shelf_selectbox")
        st.subheader(f"📍 {secilen_raf} Raf İçeriği")
        if depo.get(secilen_raf):
            raf_icerik = []
            for hammadde, veriler in depo[secilen_raf].items():
                if isinstance(veriler, dict):
                    for s_key, detay in veriler.items():
                        raf_icerik.append({
                            "Hammadde": hammadde,
                            "Miktar (kg)": detay.get("miktar", 0),
                            "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                        })
            if raf_icerik:
                st.table(raf_icerik)
            else:
                st.warning("Boş")
        else:
            st.warning("Boş")

# --- 2. STOK GİRİŞİ ---
elif secilen_key == "m2":
    st.header("📥 Rafa Malzeme Girişi")
    hedef_raf = st.selectbox("Malzemenin Konulacağı Raf:", sorted(list(depo.keys())), key="add_stock_shelf_select")
    hammadde_adi = st.text_input("Hammadde Adı:", key="add_stock_material_input").strip().upper()
    miktar = st.number_input("Eklenecek Miktar (kg):", min_value=1, step=1, key="add_stock_qty_input")
    
    skt_opsiyon = st.checkbox("Son Kullanma Tarihi Girmek İstiyorum", key="add_stock_skt_checkbox")
    skt_tarihi = "Girilmedi"
    if skt_opsiyon:
        skt_tarihi = st.date_input("Son Kullanma Tarihi Seçin:", min_value=datetime.today(), key="add_stock_skt_date").strftime("%Y-%m-%d")
    
    if st.button("Stoku Kaydet/Ekle", use_container_width=True, key="add_stock_submit_btn"):
        if hammadde_adi:
            if hammadde_adi not in depo[hedef_raf] or not isinstance(depo[hedef_raf][hammadde_adi], dict):
                depo[hedef_raf][hammadde_adi] = {}
            
            if skt_tarihi in depo[hedef_raf][hammadde_adi]:
                depo[hedef_raf][hammadde_adi][skt_tarihi]["miktar"] += miktar
            else:
                depo[hedef_raf][hammadde_adi][skt_tarihi] = {"miktar": miktar, "skt": skt_tarihi}
            
            zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_mesaji = f"📥 GİRİŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafına {miktar} kg {hammadde_adi} (SKT: {skt_tarihi}) eklendi."
            gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
            
            veri_kaydet(data)
            st.session_state.basari_mesaji = f"✅ İŞLEM BAŞARILI: {hedef_raf} rafına {miktar} kg {hammadde_adi} giriş yapıldı."
            st.rerun()
        else:
            st.error("Lütfen hammadde adı girin.")

# --- 3. STOK SİL / AZALT ---
elif secilen_key == "m3":
    st.header("📤 Raftan Malzeme Çıkarma / Azaltma")
    hedef_raf = st.selectbox("Malzemenin Çıkarılacağı Raf:", sorted(list(depo.keys())), key="remove_stock_shelf_select")
    
    if depo.get(hedef_raf) and isinstance(depo[hedef_raf], dict):
        gecerli_hammadde_listesi = [k for k, v in depo[hedef_raf].items() if isinstance(v, dict) and v]
        
        if gecerli_hammadde_listesi:
            hammadde_adi = st.selectbox("Çıkarılacak Hammaddeyi Seçin:", gecerli_hammadde_listesi, key="remove_stock_material_select")
            skt_listesi = list(depo[hedef_raf][hammadde_adi].keys())
            secilen_skt = st.selectbox("Hangi SKT'li Ürün Çıkarılacak?", skt_listesi, key="remove_stock_skt_select")
            
            mevcut_miktar = depo[hedef_raf][hammadde_adi][secilen_skt]["miktar"]
            st.info(f"💡 Bu rafta seçilen üründen şu an **{mevcut_miktar} kg** var.")
            
            cikarilacak_miktar = st.number_input("Çıkarılacak/Azaltılacak Miktar (kg):", min_value=1, max_value=int(mevcut_miktar), step=1, key="remove_stock_qty_input")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Seçilen Miktarı Stoktan Düş", use_container_width=True, key="remove_stock_deduct_btn"):
                    depo[hedef_raf][hammadde_adi][secilen_skt]["miktar"] -= cikarilacak_miktar
                    
                    zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_mesaji = f"📤 ÇIKIŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafından {cikarilacak_miktar} kg {hammadde_adi} (SKT: {secilen_skt}) düşüldü."
                    gecmis
