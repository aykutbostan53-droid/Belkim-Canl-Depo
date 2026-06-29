def stok_dus_islem(raf_kodu, hammadde_kodu, dusulecek_miktar):
    # 1. İlgili raftaki hammaddeye ait tüm aktif lotları ve stok miktarlarını getir
    aktif_lotlar = depo_veritabani.query(
        "SELECT lot_no, miktar, son_kullanma_tarihi FROM stoklar "
        "WHERE raf_kodu = ? AND hammadde_kodu = ? AND miktar > 0 "
        "ORDER BY son_kullanma_tarihi ASC", (raf_kodu, hammadde_kodu)
    )
    
    if not aktif_lotlar:
        return {"status": "error", "message": "Bu rafta ilgili hammaddeye ait stok bulunamadı."}
    
    # Kural 1: Rafta sadece tek bir lot varsa doğrudan düş
    if len(aktif_lotlar) == 1:
        secilen_lot = aktif_lotlar[0]['lot_no']
        stok_guncelle(raf_kodu, hammadde_kodu, secilen_lot, dusulecek_miktar)
        return {"status": "success", "message": f"{secilen_lot} lotundan {dusulecek_miktar} düşüldü."}
    
    # Kural 2: Birden fazla lot varsa kullanıcıya seçenek sunması için listeyi arayüze fırlat
    else:
        # FEFO uyarınca son kullanma tarihi en yakın olanı sistem otomatik "onerilen" seçer
        onerilen_lot = aktif_lotlar[0]['lot_no'] 
        
        return {
            "status": "user_confirmation_required",
            "message": "Aynı rafta birden fazla lot bulundu. Lütfen düşüş yapacağınız lotu seçin.",
            "onerilen_lot": onerilen_lot,
            "lot_listesi": aktif_lotlar # Arayüzde listelenecek tüm lotlar, miktarlar ve SKT'ler
        }

def kullanıcı_lot_onay_verdi(raf_kodu, hammadde_kodu, kullanici_secimi_lot, dusulecek_miktar):
    # Kullanıcı arayüzden lotu seçip onayladığında tetiklenecek fonksiyon
    stok_guncelle(raf_kodu, hammadde_kodu, kullanici_secimi_lot, dusulecek_miktar)
    return {"status": "success", "message": f"Kullanıcı seçimiyle {kullanici_secimi_lot} lotundan düşüş yapıldı."}
