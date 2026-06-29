import streamlit as st
import json
import os
import time
from datetime import datetime

# --- VERİ TABANI AYARLARI ---
DB_FILE = "depo_lot_skt_nihai_v1.json"

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
                "gecmis": [],
                "aktif_oturumlar": {}
            }
        if "gecmis" not in mevcut_veri:
            mevcut_veri["gecmis"] = []
        if "aktif_oturumlar" not in mevcut_veri:
            mevcut_veri["aktif_oturumlar"] = {}
            
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
        "gecmis": [],
        "aktif_oturumlar": {}
    }

def veri_kaydet(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- HAFIZA BAŞLATMA ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""
if "token" not in st.session_state:
    st.session_state.token = str(time.time()) # Bu cihaza özel geçici anahtar
if "basari_mesaji" not in st.session_state:
    st.session_state.basari_mesaji = None
if "uyari_mesaji" not in st.session_state:
    st.session_state.uyari_mesaji = None
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "m1"

# Dosyadan en taze veriyi anlık çek
global_data = veri_yukle()
depo = global_data["stok"]
kullanicilar = global_data["kullanicilar"]
gecmis_loglari = global_data.get("gecmis", [])
aktif_oturumlar = global_data.get("aktif_oturumlar", {})

# Oturum Güvenlik Zırhı: Eğer kullanıcı giriş yapmışsa ama veritabanında token çakışıyorsa (başka biri girdiyse) otomatik at
if st.session_state.logged_in:
    u_lower = st.session_state.user_display_name.lower()
    if aktif_oturumlar.get(u_lower) != st.session_state.token:
        st.session_state.logged_in = False
        st.session_state.user_display_name = ""
        st.error("⚠️ Oturumunuz Kapatıldı: Bu hesaba başka bir cihazdan giriş yapıldı!")
        st.toast("Başka cihaz girişi algılandı.", icon="🚨")
        time.sleep(2)
        st.rerun()

def login(username, password):
    u_clean = username.strip().lower()
    p_clean = password.strip()
    
    # Çift Giriş Engelleme Mantığı
    temp_data = veri_yukle()
    current_sessions = temp_data.get("aktif_oturumlar", {})
    
    if u_clean in current_sessions and current_sessions[u_clean] != st.session_state.token:
        st.error("❌ Giriş Engellendi: Bu kullanıcı hesabı şu an başka bir operatör tarafından aktif olarak kullanılıyor!")
        return

    if u_clean == "admin" and p_clean == "belkim41":
        st.session_state.logged_in = True
        st.session_state.user_display_name = "Admin"
        temp_data["aktif_oturumlar"][u_clean] = st.session_state.token
        veri_kaydet(temp_data)
        st.rerun()
    elif u_clean in kullanicilar and p_clean == u_clean:
        st.session_state.logged_in = True
        st.session_state.user_display_name = u_clean.capitalize()
        temp_data["aktif_oturumlar"][u_clean] = st.session_state.token
        veri_kaydet(temp_data)
        st.rerun()
    else:
        st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
    u_lower = st.session_state.user_display_name.lower()
    temp_data = veri_yukle()
    if u_lower in temp_data.get("aktif_oturumlar", {}):
        del temp_data["aktif_oturumlar"][u_lower]
    veri_kaydet(temp_data)
    
    st.session_state.logged_in = False
    st.session_state.user_display_name = ""
    st.session_state.active_menu = "m1"
    st.rerun()

# --- GİRİŞ KONTROLÜ ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="Giriş - Canlı Depo", layout="centered")
    st.title("🏭 Canlı Depo Yönetim Sistemi")
    st.subheader("Lütfen Giriş Yapın")
    
    with st.form("kesin_giris_formu_blok"):
        username_input = st.text_input("Kullanıcı Adı")
        password_input = st.text_input("Şifre", type="password")
        submit_login = st.form_submit_button("Giriş Yap", use_container_width=True)
        
        if submit_login:
            login(username_input, password_input)
    st.stop()

# --- ANA UYGULAMA ARAYÜZÜ ---
st.set_page_config(page_title="Canlı Depo Yönetim Sistemi", layout="wide")

col_title, col_user = st.columns([4, 1])
with col_title:
    st.title("🏭 Canlı Depo ve Hammadde Takip Sistemi")
with col_user:
    st.write(f"👤 Giriş Yapan: **{st.session_state.user_display_name}**")
    if st.button("Çıkış Yap"):
        logout()

st.write("---")

if st.session_state.basari_mesaji:
    st.success(st.session_state.basari_mesaji)
    st.session_state.basari_mesaji = None
if st.session_state.uyari_mesaji:
    st.warning(st.session_state.uyari_mesaji)
    st.session_state.uyari_mesaji = None

# --- SOL MENÜ BUTONLARI ---
st.sidebar.header("⚙️ Depo İşlemleri")

if st.sidebar.button("🔍 Arama & Sorgulama", use_container_width=True):
    st.session_state.active_menu = "m1"
    st.rerun()

if st.sidebar.button("📥 Stok Ekle / Güncelle", use_container_width=True):
    st.session_state.active_menu = "m2"
    st.rerun()

if st.sidebar.button("📤 Stok Çıkar / Azalt / Sil", use_container_width=True):
    st.session_state.active_menu = "m3"
    st.rerun()

if st.sidebar.button("➕ Yeni Raf Tanımla", use_container_width=True):
    st.session_state.active_menu = "m4"
    st.rerun()

if st.sidebar.button("👥 Kullanıcı Yönetimi", use_container_width=True):
    st.session_state.active_menu = "m5"
    st.rerun()

if st.sidebar.button("📊 Tüm Depo Durumu", use_container_width=True):
    st.session_state.active_menu = "m6"
    st.rerun()

if st.sidebar.button("📜 Depo Hareket Geçmişi", use_container_width=True):
    st.session_state.active_menu = "m7"
    st.rerun()


# --- ANLIK CANLI VERİ YENİLEME FRAGMENTİ (3 Saniyede bir arka planda dosyayı okur) ---
@st.fragment(run_every=3)
def canlı_raf_durumu_goster(raf_adi, mod="tablo"):
    taze_data = veri_yukle()
    taze_depo = taze_data["stok"]
    mevcut_icerik = []
    if taze_depo.get(raf_adi):
        for hmd, veriler in taze_depo[raf_adi].items():
            if isinstance(veriler, dict):
                for k_key, detay in veriler.items():
                    mevcut_icerik.append({
                        "Hammadde": hmd,
                        "Miktar (kg)": round(detay.get("miktar", 0.0), 1),
                        "LOT No": detay.get("lot", "Girilmedi"),
                        "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                    })
    if mod == "tablo":
        if mevcut_icerik:
            st.table(mevcut_icerik)
        else:
            st.info("Bu raf şu an tamamen boş.")
    return mevcut_icerik

@st.fragment(run_every=3)
def canlı_tüm_depoyu_goster():
    taze_data = veri_yukle()
    taze_depo = taze_data["stok"]
    dolu_raflar = {}
    for k, v in taze_depo.items():
        if v and isinstance(v, dict):
            if any(isinstance(h_v, dict) and h_v for h_k, h_v in v.items()):
                dolu_raflar[k] = v
    
    if dolu_raflar:
        for raf, icerik in sorted(dolu_raflar.items()):
            with st.expander(f"📦 Raf: {raf} (Dolu)"):
                raf_tablo = []
                for hammadde, veriler in icerik.items():
                    if isinstance(veriler, dict):
                        for k_key, detay in veriler.items():
                            raf_tablo.append({
                                "Hammadde": hammadde,
                                "Miktar (kg)": round(detay.get("miktar", 0.0), 1),
                                "LOT No": detay.get("lot", "Girilmedi"),
                                "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                            })
                if raf_tablo:
                    st.table(raf_tablo)
    else:
        st.write("Depodaki tüm raflar şu anda boş.")


# 1. ARAMA & SORGULAMA
if st.session_state.active_menu == "m1":
    st.header("🔍 Hammadde veya Raf Ara")
    arama_turu = st.radio("Arama Yöntemi:", ["Hammaddeye Göre Ara", "Rafa Göre Ara"])

    if arama_turu == "Hammaddeye Göre Ara":
        arama_kelimesi = st.text_input("Aranacak Hammadde Adı:").strip().upper()
        if arama_kelimesi:
            @st.fragment(run_every=3)
            def canlı_hmd_ara(hmd_adi):
                t_data = veri_yukle()
                t_depo = t_data["stok"]
                bulundu = False
                sonuclar = []
                for raf, icerik in t_depo.items():
                    if isinstance(icerik, dict) and hmd_adi in icerik:
                        if isinstance(icerik[hmd_adi], dict):
                            for k_key, detay in icerik[hmd_adi].items():
                                sonuclar.append({
                                    "Raf Adresi": raf,
                                    "Miktar (kg)": round(detay.get("miktar", 0.0), 1),
                                    "LOT No": detay.get("lot", "Girilmedi"),
                                    "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                                })
                                bulundu = True
                if bulundu:
                    st.table(sonuclar)
                else:
                    st.error(f"❌ Depoda '{hmd_adi}' isimli bir hammadde bulunamadı.")
            canlı_hmd_ara(arama_kelimesi)

    elif arama_turu == "Rafa Göre Ara":
        secilen_raf = st.selectbox("Sorgulanacak Rafı Seçin:", sorted(list(depo.keys())))
        st.subheader(f"📍 {secilen_raf} Raf İçeriği (Her 3 sn'de bir canlı güncellenir)")
        canlı_raf_durumu_goster(secilen_raf, mod="tablo")

# 2. STOK GİRİŞİ
elif st.session_state.active_menu == "m2":
    st.header("📥 Rafa Malzeme Girişi")
    hedef_raf = st.selectbox("Malzemenin Konulacağı Raf:", sorted(list(depo.keys())))
    
    st.subheader("📍 Seçilen Rafın Anlık Mevcut İçeriği")
    canlı_raf_durumu_goster(hedef_raf, mod="tablo")
    st.write("---")

    hammadde_adi = st.text_input("Giriş Yapılacak Hammadde Adı:").strip().upper()
    miktar = st.number_input("Eklenecek Miktar (kg):", min_value=0.1, step=0.1, format="%.1f")
    
    lot_opsiyon = st.checkbox("LOT Numarası Girmek İstiyorum")
    lot_no = "Girilmedi"
    if lot_opsiyon:
        lot_no = st.text_input("LOT Numarasını Yazın:").strip().upper()
        if not lot_no:
            lot_no = "Girilmedi"
            
    skt_opsiyon = st.checkbox("Son Kullanma Tarihi Girmek İstiyorum")
    skt_tarihi = "Girilmedi"
    if skt_opsiyon:
        skt_tarihi = st.date_input("Son Kullanma Tarihi Seçin:", min_value=datetime.today()).strftime("%Y-%m-%d")
    
    if st.button("Stoku Kaydet/Ekle", use_container_width=True):
        if hammadde_adi:
            taze_t_data = veri_yukle()
            if hammadde_adi not in taze_t_data["stok"][hedef_raf]:
                taze_t_data["stok"][hedef_raf][hammadde_adi] = {}
            
            parti_anahtari = f"LOT_{lot_no}_SKT_{skt_tarihi}"
            if parti_anahtari in taze_t_data["stok"][hedef_raf][hammadde_adi]:
                taze_t_data["stok"][hedef_raf][hammadde_adi][parti_anahtari]["miktar"] += miktar
            else:
                taze_t_data["stok"][hedef_raf][hammadde_adi][parti_anahtari] = {"miktar": miktar, "lot": lot_no, "skt": skt_tarihi}
            
            taze_t_data["stok"][hedef_raf][hammadde_adi][parti_anahtari]["miktar"] = round(taze_t_data["stok"][hedef_raf][hammadde_adi][parti_anahtari]["miktar"], 1)
            
            zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_mesaji = f"📥 GİRİŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafına {round(miktar, 1)} kg {hammadde_adi} (LOT: {lot_no} | SKT: {skt_tarihi}) eklendi."
            taze_t_data["gecmis"].insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
            
            veri_kaydet(taze_t_data)
            st.session_state.basari_mesaji = f"✅ İŞLEM BAŞARILI: {hedef_raf} rafına {round(miktar, 1)} kg {hammadde_adi} (LOT: {lot_no}) giriş yapıldı."
            st.rerun()
        else:
            st.error("Lütfen hammadde adı girin.")

# 3. STOK SİL / AZALT
elif st.session_state.active_menu == "m3":
    st.header("📤 Raftan Malzeme Çıkarma / Azaltma")
    hedef_raf = st.selectbox("Malzemenin Çıkarılacağı Raf:", sorted(list(depo.keys())))
    
    st.subheader("📍 Seçilen Rafın İçindeki Malzemelerin Listesi")
    canlı_raf_durumu_goster(hedef_raf, mod="tablo")
    st.write("---")
    
    # İşlem yapılacak taze veriyi çek
    t_m3_data = veri_yukle()
    gecerli_hammadde_listesi = [k for k, v in t_m3_data["stok"][hedef_raf].items() if isinstance(v, dict) and v]
    
    if gecerli_hammadde_listesi:
        hammadde_adi = st.selectbox("Çıkarılacak Hammaddeyi Seçin:", gecerli_hammadde_listesi)
        
        parti_secenekleri = {}
        for p_key, p_val in t_m3_data["stok"][hedef_raf][hammadde_adi].items():
            p_lot = p_val.get('lot', 'Girilmedi')
            p_skt = p_val.get('skt', 'Girilmedi')
            p_mik = round(p_val.get('miktar', 0.0), 1)
            etiket = f"Miktar: {p_mik} kg | LOT: {p_lot} | SKT: {p_skt}"
            parti_secenekleri[p_key] = etiket
        
        if len(parti_secenekleri) > 1:
            st.warning("⚠️ UYARI: Bu rafta aynı malzemeden birden fazla LOT bulundu! Lütfen düşüş yapacağınız tam LOT numarasını seçin.")
            
        secilen_parti_key = st.selectbox("Düşüş Yapılacak LOT / SKT Seçimi:", options=list(parti_secenekleri.keys()), format_func=lambda x: parti_secenekleri[x])
        
        mevcut_miktar = round(float(t_m3_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key].get("miktar", 0.0)), 1)
        secilen_lot_no = t_m3_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key].get("lot", "Girilmedi")
        secilen_skt_no = t_m3_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key].get("skt", "Girilmedi")
        
        if mevcut_miktar <= 0.09:
            st.error(f"⚠️ Bu lottaki miktar düşüş yapmak için yetersiz ({mevcut_miktar} kg). Lütfen sağdaki buton ile tamamen silin.")
            if st.button("Bu Ürünü Raftan Tamamen Sil (Miktar Yetersiz)", use_container_width=True):
                t_del_data = veri_yukle()
                zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_mesaji = f"🗑️ SİLİNDİ -> {st.session_state.user_display_name} tarafından {hedef_raf} rafındaki {hammadde_adi} (LOT: {secilen_lot_no}) temizlendi."
                t_del_data["gecmis"].insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                del t_del_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]
                if not t_del_data["stok"][hedef_raf][hammadde_adi]:
                    del t_del_data["stok"][hedef_raf][hammadde_adi]
                veri_kaydet(t_del_data)
                st.session_state.uyari_mesaji = "🗑️ Kayıt tamamen temizlendi."
                st.rerun()
        else:
            cikarilacak_miktar = st.number_input("Çıkarılacak/Azaltılacak Miktar (kg):", min_value=0.1, max_value=mevcut_miktar, step=0.1, format="%.1f")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Seçilen Miktarı Stoktan Düş", use_container_width=True):
                    t_action_data = veri_yukle()
                    t_action_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]["miktar"] -= cikarilacak_miktar
                    t_action_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]["miktar"] = round(t_action_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]["miktar"], 1)
                    
                    zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_mesaji = f"📤 ÇIKIŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafından {round(cikarilacak_miktar, 1)} kg {hammadde_adi} (LOT: {secilen_lot_no} | SKT: {secilen_skt_no}) düşüldü."
                    t_action_data["gecmis"].insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                    
                    if t_action_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]["miktar"] <= 0.09:
                        del t_action_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]
                    if not t_action_data["stok"][hedef_raf][hammadde_adi]:
                        del t_action_data["stok"][hedef_raf][hammadde_adi]
                        
                    veri_kaydet(t_action_data)
                    st.session_state.basari_mesaji = f"📉 İŞLEM BAŞARILI: {hedef_raf} rafından {round(cikarilacak_miktar, 1)} kg {hammadde_adi} (LOT: {secilen_lot_no}) çıkış yapıldı."
                    st.rerun()
                    
            with col2:
                if st.button("Bu Ürünü Raftan Tamamen Sil", use_container_width=True):
                    t_clear_data = veri_yukle()
                    zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_mesaji = f"🗑️ TAMAMEN SİLİNDİ -> {st.session_state.user_display_name} tarafından {hedef_raf} rafındaki tüm {hammadde_adi} (LOT: {secilen_lot_no}) stokları silindi."
                    t_clear_data["gecmis"].insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                    
                    del t_clear_data["stok"][hedef_raf][hammadde_adi][secilen_parti_key]
                    if not t_clear_data["stok"][hedef_raf][hammadde_adi]:
                        del t_clear_data["stok"][hedef_raf][hammadde_adi]
                    
                    veri_kaydet(t_clear_data)
                    st.session_state.uyari_mesaji = f"🗑️ BİLDİRİM: {hedef_raf} rafındaki {hammadde_adi} (LOT: {secilen_lot_no}) tamamen silindi."
                    st.rerun()
    else:
        st.warning("Seçilen rafta çıkarılacak malzeme kalmadı.")

# 4. YENİ RAF TANIMLA
elif st.session_state.active_menu == "m4":
    st.header("➕ Yeni Ekstra Raf Adresi Oluştur")
    yeni_raf = st.text_input("Oluşturulacak Raf Adı (Örn: E111):").strip().upper()
    
    if st.button("Rafı Sisteme Ekle", use_container_width=True):
        if yeni_raf:
            t_raf_data = veri_yukle()
            if yeni_raf not in t_raf_data["stok"]:
                t_raf_data["stok"][yeni_raf] = {}
                zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_mesaji = f"➕ YENİ RAF -> {st.session_state.user_display_name} tarafından sisteme yeni {yeni_raf} rafı tanımlandı."
                t_raf_data["gecmis"].insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                veri_kaydet(t_raf_data)
                st.session_state.basari_mesaji = f"✅ Raf {yeni_raf} sisteme başarıyla tanımlandı."
                st.rerun()
            else:
                st.warning(f"⚠️ {yeni_raf} adresi zaten mevcut.")
        else:
            st.error("Raf adı boş bırakılamaz.")

# 5. KULLANICI YÖNETİMİ
elif st.session_state.active_menu == "m5":
    st.header("👥 Kullanıcı Hesapları Yönetimi")
    yeni_user = st.text_input("Eklenecek Kullanıcı Adı (Küçük harf, Türkçe karaktersiz):").strip().lower()
    if st.button("Kullanıcıyı Kaydet", use_container_width=True):
        t_u_data = veri_yukle()
        if yeni_user and yeni_user not in t_u_data["kullanicilar"] and yeni_user != "admin":
            t_u_data["kullanicilar"].append(yeni_user)
            veri_kaydet(t_u_data)
            st.success(f"✅ '{yeni_user}' kullanıcısı eklendi. (Şifre: '{yeni_user}')")
            st.rerun()
        else:
            st.error("Geçersiz kullanıcı adı veya bu kullanıcı zaten mevcut.")
            
    st.write("---")
    st.subheader("Mevcut Kullanıcı Listesi")
    
    t_list_data = veri_yukle()
    if t_list_data["kullanicilar"]:
        for idx, user in enumerate(t_list_data["kullanicilar"]):
            col_u_name, col_u_del = st.columns([3, 1])
            with col_u_name:
                st.write(f"👤 {user.capitalize()} (Şifre: {user})")
            with col_u_del:
                if st.button("Sil", key=f"del_u_{user}_{idx}"):
                    t_del_u = veri_yukle()
                    if user in t_del_u["kullanicilar"]:
                        t_del_u["kullanicilar"].remove(user)
                    if user in t_del_u.get("aktif_oturumlar", {}):
                        del t_del_u["aktif_oturumlar"][user]
                    veri_kaydet(t_del_u)
                    st.warning(f"🗑️ {user.capitalize()} kullanıcısı sistemden silindi.")
                    st.rerun()

# 6. TÜM DEPO DURUMU
elif st.session_state.active_menu == "m6":
    st.header("📊 Anlık Depo Durum Raporu (Her 3 sn'de bir canlı güncellenir)")
    canlı_tüm_depoyu_goster()

# 7. DEPO HAREKET GEÇMİŞİ
elif st.session_state.active_menu == "m7":
    st.header("📜 Canlı Depo Hareket Geçmişi (Log Kayıtları)")
    st.write("Depoda yapılan tüm stok giriş, çıkış ve silme işlemleri anlık olarak aşağıda listelenir:")
    
    t_log_data = veri_yukle()
    if t_log_data["gecmis"]:
        for idx, log in enumerate(t_log_data["gecmis"]):
            st.text(f"[{log.get('tarih', 'Bilinmiyor')}] {log.get('islem', '')}")
    else:
        st.info("Henüz hiçbir depo hareketi kaydedilmedi.")
