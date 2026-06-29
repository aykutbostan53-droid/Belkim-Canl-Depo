import streamlit as st
import json
import os
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

# --- HAFIZA BAŞLATMA ---
if "depo_data" not in st.session_state:
    st.session_state.depo_data = veri_yukle()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = ""
if "basari_mesaji" not in st.session_state:
    st.session_state.basari_mesaji = None
if "uyari_mesaji" not in st.session_state:
    st.session_state.uyari_mesaji = None
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "m1"

data = st.session_state.depo_data
depo = data["stok"]
kullanicilar = data["kullanicilar"]
gecmis_loglari = data.get("gecmis", [])

def login(username, password):
    u_clean = username.strip().lower()
    p_clean = password.strip()
    
    if u_clean == "admin" and p_clean == "belkim41":
        st.session_state.logged_in = True
        st.session_state.user_display_name = "Yönetici (Admin)"
        st.rerun()
    elif u_clean in kullanicilar and p_clean == u_clean:
        st.session_state.logged_in = True
        st.session_state.user_display_name = u_clean.capitalize()
        st.rerun()
    else:
        st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
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

# 1. ARAMA & SORGULAMA
if st.session_state.active_menu == "m1":
    st.header("🔍 Hammadde veya Raf Ara")
    arama_turu = st.radio("Arama Yöntemi:", ["Hammaddeye Göre Ara", "Rafa Göre Ara"])

    if arama_turu == "Hammaddeye Göre Ara":
        arama_kelimesi = st.text_input("Aranacak Hammadde Adı:").strip().upper()
        if arama_kelimesi:
            bulundu = False
            sonuclar = []
            for raf, icerik in depo.items():
                if isinstance(icerik, dict) and arama_kelimesi in icerik:
                    if isinstance(icerik[arama_kelimesi], dict):
                        for k_key, detay in icerik[arama_kelimesi].items():
                            sonuclar.append({
                                "Raf Adresi": raf,
                                "Miktar (kg)": detay.get("miktar", 0),
                                "LOT No": detay.get("lot", "Girilmedi"),
                                "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                            })
                            bulundu = True
            if bulundu:
                st.table(sonuclar)
            else:
                st.error(f"❌ Depoda '{arama_kelimesi}' isimli bir hammadde bulunamadı.")

    elif arama_turu == "Rafa Göre Ara":
        secilen_raf = st.selectbox("Sorgulanacak Rafı Seçin:", sorted(list(depo.keys())))
        st.subheader(f"📍 {secilen_raf} Raf İçeriği")
        if depo.get(secilen_raf):
            raf_icerik = []
            for hammadde, veriler in depo[secilen_raf].items():
                if isinstance(veriler, dict):
                    for k_key, detay in veriler.items():
                        raf_icerik.append({
                            "Hammadde": hammadde,
                            "Miktar (kg)": detay.get("miktar", 0),
                            "LOT No": detay.get("lot", "Girilmedi"),
                            "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                        })
            if raf_icerik:
                st.table(raf_icerik)
            else:
                st.warning("Boş")
        else:
            st.warning("Boş")

# 2. STOK GİRİŞİ
elif st.session_state.active_menu == "m2":
    st.header("📥 Rafa Malzeme Girişi")
    hedef_raf = st.selectbox("Malzemenin Konulacağı Raf:", sorted(list(depo.keys())))
    
    st.subheader("📍 Seçilen Rafın Anlık Mevcut İçeriği")
    mevcut_icerik = []
    if depo.get(hedef_raf):
        for hmd, veriler in depo[hedef_raf].items():
            if isinstance(veriler, dict):
                for k_key, detay in veriler.items():
                    mevcut_icerik.append({
                        "Hammadde": hmd,
                        "Miktar (kg)": detay.get("miktar", 0),
                        "LOT No": detay.get("lot", "Girilmedi"),
                        "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                    })
    if mevcut_icerik:
        st.table(mevcut_icerik)
    else:
        st.info("Bu raf şu an tamamen boş.")
    st.write("---")

    hammadde_adi = st.text_input("Giriş Yapılacak Hammadde Adı:").strip().upper()
    miktar = st.number_input("Eklenecek Miktar (kg):", min_value=1, step=1)
    
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
            if hammadde_adi not in depo[hedef_raf] or not isinstance(depo[hedef_raf][hammadde_adi], dict):
                depo[hedef_raf][hammadde_adi] = {}
            
            parti_anahtari = f"LOT_{lot_no}_SKT_{skt_tarihi}"
            if parti_anahtari in depo[hedef_raf][hammadde_adi]:
                depo[hedef_raf][hammadde_adi][parti_anahtari]["miktar"] += miktar
            else:
                depo[hedef_raf][hammadde_adi][parti_anahtari] = {"miktar": miktar, "lot": lot_no, "skt": skt_tarihi}
            
            zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_mesaji = f"📥 GİRİŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafına {miktar} kg {hammadde_adi} (LOT: {lot_no} | SKT: {skt_tarihi}) eklendi."
            gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
            
            veri_kaydet(data)
            st.session_state.basari_mesaji = f"✅ İŞLEM BAŞARILI: {hedef_raf} rafına {miktar} kg {hammadde_adi} (LOT: {lot_no}) giriş yapıldı."
            st.rerun()
        else:
            st.error("Lütfen hammadde adı girin.")

# 3. STOK SİL / AZALT (ZERO DIVISION ERROR TAMAMEN ÇÖZÜLDÜ)
elif st.session_state.active_menu == "m3":
    st.header("📤 Raftan Malzeme Çıkarma / Azaltma")
    hedef_raf = st.selectbox("Malzemenin Çıkarılacağı Raf:", sorted(list(depo.keys())))
    
    st.subheader("📍 Seçilen Rafın İçindeki Malzemelerin Listesi")
    raf_listesi = []
    if depo.get(hedef_raf) and isinstance(depo[hedef_raf], dict):
        for hmd, veriler in depo[hedef_raf].items():
            if isinstance(veriler, dict):
                for k_key, detay in veriler.items():
                    raf_listesi.append({
                        "Hammadde": hmd,
                        "Miktar (kg)": detay.get("miktar", 0),
                        "LOT No": detay.get("lot", "Girilmedi"),
                        "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                    })
    
    if raf_listesi:
        st.table(raf_listesi)
        st.write("---")
        
        gecerli_hammadde_listesi = [k for k, v in depo[hedef_raf].items() if isinstance(v, dict) and v]
        if gecerli_hammadde_listesi:
            hammadde_adi = st.selectbox("Çıkarılacak Hammaddeyi Seçin:", gecerli_hammadde_listesi)
            
            parti_secenekleri = {}
            for p_key, p_val in depo[hedef_raf][hammadde_adi].items():
                p_lot = p_val.get('lot', 'Girilmedi')
                p_skt = p_val.get('skt', 'Girilmedi')
                p_mik = p_val.get('miktar', 0)
                etiket = f"Miktar: {p_mik} kg | LOT: {p_lot} | SKT: {p_skt}"
                parti_secenekleri[p_key] = etiket
            
            if len(parti_secenekleri) > 1:
                st.warning("⚠️ UYARI: Bu rafta aynı malzemeden birden fazla LOT bulundu! Lütfen düşüş yapacağınız tam LOT numarasını seçin.")
                
            secilen_parti_key = st.selectbox("Düşüş Yapılacak LOT / SKT Seçimi:", options=list(parti_secenekleri.keys()), format_func=lambda x: parti_secenekleri[x])
            
            # Değerleri güvenli şekilde çekiyoruz
            mevcut_miktar = depo[hedef_raf][hammadde_adi][secilen_parti_key].get("miktar", 0)
            secilen_lot_no = depo[hedef_raf][hammadde_adi][secilen_parti_key].get("lot", "Girilmedi")
            secilen_skt_no = depo[hedef_raf][hammadde_adi][secilen_parti_key].get("skt", "Girilmedi")
            
            max_sinir = int(mevcut_miktar)
            
            # SIFIRA BÖLÜNME VE DEĞER HATALARINI ENGELLEYEN HÜCRESEL KONTROL
            if max_sinir < 1:
                st.error(f"⚠️ Bu lottaki miktar düşüş yapmak için tam sayı sınırının altında ({mevcut_miktar} kg). Lütfen sağdaki buton ile tamamen silin.")
                if st.button("Bu Ürünü Raftan Tamamen Sil (Miktar Yetersiz)", use_container_width=True):
                    zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_mesaji = f"🗑️ SİLİNDİ -> {st.session_state.user_display_name} tarafından {hedef_raf} rafındaki {hammadde_adi} (LOT: {secilen_lot_no}) kalıntısı temizlendi."
                    gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                    del depo[hedef_raf][hammadde_adi][secilen_parti_key]
                    if not depo[hedef_raf][hammadde_adi]:
                        del depo[hedef_raf][hammadde_adi]
                    veri_kaydet(data)
                    st.session_state.uyari_mesaji = "🗑️ Kayıt tamamen temizlendi."
                    st.rerun()
            else:
                cikarilacak_miktar = st.number_input("Çıkarılacak/Azaltılacak Miktar (kg):", min_value=1, max_value=max_sinir, step=1)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Seçilen Miktarı Stoktan Düş", use_container_width=True):
                        # Stok düşümü yapılıyor
                        depo[hedef_raf][hammadde_adi][secilen_parti_key]["miktar"] -= cikarilacak_miktar
                        
                        zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_mesaji = f"📤 ÇIKIŞ YAPILDI -> {st.session_state.user_display_name} tarafından {hedef_raf} rafından {cikarilacak_miktar} kg {hammadde_adi} (LOT: {secilen_lot_no} | SKT: {secilen_skt_no}) düşüldü."
                        gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                        
                        # Eğer miktar bittiyse kaydı güvenli şekilde yok ediyoruz
                        if depo[hedef_raf][hammadde_adi][secilen_parti_key]["miktar"] <= 0:
                            del depo[hedef_raf][hammadde_adi][secilen_parti_key]
                        if not depo[hedef_raf][hammadde_adi]:
                            del depo[hedef_raf][hammadde_adi]
                            
                        veri_kaydet(data)
                        st.session_state.basari_mesaji = f"📉 İŞLEM BAŞARILI: {hedef_raf} rafından {cikarilacak_miktar} kg {hammadde_adi} (LOT: {secilen_lot_no}) çıkış yapıldı."
                        st.rerun() # Sayfayı hemen yenileyerek sıfıra bölünme riskini kökten siliyoruz.
                        
                with col2:
                    if st.button("Bu Ürünü Raftan Tamamen Sil", use_container_width=True):
                        zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_mesaji = f"🗑️ TAMAMEN SİLİNDİ -> {st.session_state.user_display_name} tarafından {hedef_raf} rafındaki tüm {hammadde_adi} (LOT: {secilen_lot_no}) stokları silindi."
                        gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": log_mesaji})
                        
                        del depo[hedef_raf][hammadde_adi][secilen_parti_key]
                        if not depo[hedef_raf][hammadde_adi]:
                            del depo[hedef_raf][hammadde_adi]
                            
                        veri_kaydet(data)
                        st.session_state.uyari_mesaji = f"🗑️ BİLDİRİM: {hedef_raf} rafındaki {hammadde_adi} (LOT: {secilen_lot_no}) tamamen silindi."
                        st.rerun()
    else:
        st.warning("Seçilen raf zaten şu anda tamamen boş. Çıkarılacak hammadde yok.")

# 4. YENİ RAF TANIMLA
elif st.session_state.active_menu == "m4":
    st.header("➕ Yeni Ekstra Raf Adresi Oluştur")
    yeni_raf = st.text_input("Oluşturulacak Raf Adı (Örn: E111):").strip().upper()
    
    if st.button("Rafı Sisteme Ekle", use_container_width=True):
        if yeni_raf:
            if yeni_raf not in depo:
                depo[yeni_raf] = {}
                zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                gecmis_loglari.insert(0, {"tarih": zaman_damgasi, "islem": f"➕ YENİ RAF -> {st.session_state.user_display_name} tarafından sisteme yeni {yeni_raf} rafı tanımlandı."})
                veri_kaydet(data)
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
        if yeni_user and yeni_user not in kullanicilar and yeni_user != "admin":
            kullanicilar.append(yeni_user)
            veri_kaydet(data)
            st.success(f"✅ '{yeni_user}' kullanıcısı eklendi. (Şifre: '{yeni_user}')")
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
                if st.button("Sil", key=f"del_u_{user}_{idx}"):
                    kullanicilar.remove(user)
                    veri_kaydet(data)
                    st.warning(f"🗑️ {user.capitalize()} kullanıcısı sistemden silindi.")
                    st.rerun()

# 6. TÜM DEPO DURUMU
elif st.session_state.active_menu == "m6":
    st.header("📊 Anlık Depo Durum Raporu")
    dolu_raflar = {}
    for k, v in depo.items():
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
                                "Miktar (kg)": detay.get("miktar", 0),
                                "LOT No": detay.get("lot", "Girilmedi"),
                                "Son Kullanma Tarihi": detay.get("skt", "Girilmedi")
                            })
                if raf_tablo:
                    st.table(raf_tablo)
    else:
        st.write("Depodaki tüm raflar şu anda boş.")

# 7. DEPO HAREKET GEÇMİŞİ
elif st.session_state.active_menu == "m7":
    st.header("📜 Canlı Depo Hareket Geçmişi (Log Kayıtları)")
    st.write("Depoda yapılan tüm stok giriş, çıkış ve silme işlemleri anlık olarak aşağıda listelenir:")
    if gecmis_loglari:
        for idx, log in enumerate(gecmis_loglari):
            st.text(f"[{log.get('tarih', 'Bilinmiyor')}] {log.get('islem', '')}")
    else:
        st.info("Henüz hiçbir depo hareketi kaydedilmedi.")
