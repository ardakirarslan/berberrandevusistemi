import os
import datetime


calisan_listesi = ["Güncel Sarıman", "Murat Sakal", "Ercüment Güvenç"]

hizmetler = {
    "Saç Kesimi"   : 150,
    "Sakal Tıraşı" : 100,
    "Saç + Sakal"  : 220,
    "Yıkama"       : 80,
    "Boya"         : 350,
}

randevular = []

DOSYA_ADI = "randevular.txt"


def randevulari_dosyaya_kaydet():
    
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        f.write("=== BERBER RANDEVU KAYITLARI ===\n\n")
        if not randevular:
            f.write("Henüz randevu bulunmamaktadır.\n")
        else:
            for i, r in enumerate(randevular, 1):
                f.write(f"Randevu #{i}\n")
                f.write(f"  Müşteri  : {r['musteri']}\n")
                f.write(f"  Tarih    : {r['tarih']}\n")
                f.write(f"  Saat     : {r['saat']}\n")
                f.write(f"  Hizmet   : {r['hizmet']}\n")
                f.write(f"  Ücret    : {r['ucret']} TL\n")
                f.write(f"  Berber   : {r['berber']}\n")
                f.write("-" * 35 + "\n")
    print("\n Randevular 'randevular.txt' dosyasına kaydedildi.")


def randevulari_dosyadan_oku():
    """Dosyadaki randevu kayıtlarını ekrana yazdırır."""
    if not os.path.exists(DOSYA_ADI):
        print("\n  Henüz kayıtlı bir dosya bulunamadı.")
        return
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        icerik = f.read()
    print("\n" + icerik)
    
def randevu_al():
    
    print("\n--- YENİ RANDEVU ---")

    musteri = input("Müşteri adı soyadı: ").strip()
    if not musteri:
        print(" Müşteri adı boş olamaz.")
        return

   
    tarih = input("Randevu tarihi (GG/AA/YYYY): ").strip()
    try:
        datetime.datetime.strptime(tarih, "%d/%m/%Y")
    except ValueError:
        print(" Geçersiz tarih formatı. Lütfen GG/AA/YYYY şeklinde girin.")
        return

    
    saat = input("Randevu saati (SS:DD): ").strip()
    try:
        datetime.datetime.strptime(saat, "%H:%M")
    except ValueError:
        print("❌ Geçersiz saat formatı. Lütfen SS:DD şeklinde girin.")
        return

    print("\nMevcut hizmetler:")
    hizmet_listesi = list(hizmetler.keys())   # sözlük -> liste dönüşümü
    for idx, hizmet in enumerate(hizmet_listesi, 1):
        print(f"  {idx}. {hizmet:15s} - {hizmetler[hizmet]} TL")

    secim = input("Hizmet numarasını seçin: ").strip()
    if not secim.isdigit() or not (1 <= int(secim) <= len(hizmet_listesi)):
        print(" Geçersiz hizmet seçimi.")
        return
    secilen_hizmet = hizmet_listesi[int(secim) - 1]
    ucret = hizmetler[secilen_hizmet]

    print("\nBerberler:")
    for idx, berber in enumerate(calisan_listesi, 1):
        print(f"  {idx}. {berber}")

    berber_secim = input("Berber numarasını seçin: ").strip()
    if not berber_secim.isdigit() or not (1 <= int(berber_secim) <= len(calisan_listesi)):
        print(" Geçersiz berber seçimi.")
        return
    secilen_berber = calisan_listesi[int(berber_secim) - 1]

    yeni_randevu = {
        "musteri" : musteri,
        "tarih"   : tarih,
        "saat"    : saat,
        "hizmet"  : secilen_hizmet,
        "ucret"   : ucret,
        "berber"  : secilen_berber,
    }
    randevular.append(yeni_randevu)

    print(f"\n✅ Randevu alındı! {musteri} - {tarih} {saat} - {secilen_hizmet} ({ucret} TL) - {secilen_berber}")
    randevulari_dosyaya_kaydet()


def randevulari_listele():
    """Bellekteki tüm randevuları ekrana yazar."""
    print("\n--- TÜM RANDEVULAR ---")
    if not randevular:
        print("Henüz randevu bulunmamaktadır.")
        return
    for i, r in enumerate(randevular, 1):
        print(f"\n#{i}  {r['musteri']:20s} | {r['tarih']} {r['saat']} | {r['hizmet']:15s} | {r['ucret']} TL | {r['berber']}")
    print()


def randevu_sil():
    """Seçilen randevuyu listeden siler."""
    randevulari_listele()
    if not randevular:
        return
    secim = input("Silmek istediğiniz randevu numarası: ").strip()
    if not secim.isdigit() or not (1 <= int(secim) <= len(randevular)):
        print("❌ Geçersiz numara.")
        return
    silinen = randevular.pop(int(secim) - 1)
    print(f"\n🗑️  '{silinen['musteri']}' adlı müşterinin randevusu silindi.")
    randevulari_dosyaya_kaydet()


def musteri_ara():
    """İsme göre randevu arar."""
    aranan = input("\nAranacak müşteri adı: ").strip().lower()
    bulunanlar = [r for r in randevular if aranan in r["musteri"].lower()]
    if not bulunanlar:
        print("⚠️  Eşleşen randevu bulunamadı.")
    else:
        print(f"\n{len(bulunanlar)} randevu bulundu:")
        for r in bulunanlar:
            print(f"  → {r['musteri']} | {r['tarih']} {r['saat']} | {r['hizmet']} | {r['berber']}")


def gunluk_rapor():
    """Belirli bir tarihteki randevuları ve toplam geliri gösterir."""
    tarih = input("\nRapor tarihi (GG/AA/YYYY): ").strip()
    gun_randevulari = [r for r in randevular if r["tarih"] == tarih]

    print(f"\n--- {tarih} TARİHİ RAPORU ---")
    if not gun_randevulari:
        print("Bu tarihe ait randevu bulunamadı.")
        return

    toplam = 0
    for r in gun_randevulari:
        print(f"  {r['saat']} | {r['musteri']:20s} | {r['hizmet']:15s} | {r['ucret']} TL | {r['berber']}")
        toplam += r["ucret"]

    print(f"\n  Toplam randevu : {len(gun_randevulari)}")
    print(f"  Toplam gelir   : {toplam} TL")


def hizmet_listesi_goster():
    """Hizmetleri ve fiyatlarını ekrana yazar."""
    print("\n--- HİZMET FİYAT LİSTESİ ---")
    for hizmet, fiyat in hizmetler.items():
        print(f"  {hizmet:20s} : {fiyat} TL")



def ana_menu():
    """Programın ana döngüsü."""
    print("=" * 45)
    print("      BERBER RANDEVU SİSTEMİNE HOŞGELDİNİZ")
    print("=" * 45)

    while True:
        print("\n--- ANA MENÜ ---")
        print("  1. Randevu Al")
        print("  2. Randevuları Listele")
        print("  3. Randevu Sil")
        print("  4. Müşteri Ara")
        print("  5. Günlük Rapor")
        print("  6. Hizmet Listesi")
        print("  7. Dosyadan Oku")
        print("  0. Çıkış")

        secim = input("\nSeçiminiz: ").strip()

        if secim == "1":
            randevu_al()
        elif secim == "2":
            randevulari_listele()
        elif secim == "3":
            randevu_sil()
        elif secim == "4":
            musteri_ara()
        elif secim == "5":
            gunluk_rapor()
        elif secim == "6":
            hizmet_listesi_goster()
        elif secim == "7":
            randevulari_dosyadan_oku()
        elif secim == "0":
            print("\nProgramdan çıkılıyor. Güle güle!")
            break
        else:
            print("❌ Geçersiz seçim. Lütfen tekrar deneyin.")


if __name__ == "__main__":
    ana_menu()