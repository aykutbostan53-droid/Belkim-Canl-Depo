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
        st.error("❌
