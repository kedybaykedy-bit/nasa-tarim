# Field Shift — NASA Space Apps Challenge 2026 (v2.0)

## Hakkında
NASA POWER iklim verileri ile çiftçilere akıllı bitki döngüsü (crop rotation) önerisi sunan decision-support prototipi. v2.0 ile 3 yıllık rotasyon dizisi, gelir tahmini ve genişletilmiş bitki veritabanı eklendi.

## Klasör yapısı
```
field-shift-nasa-space-apps--main/
  server.py          # HTTP API + arayüz sunucu (port 5000)
  data/crops.json    # Türkiye odaklı 20+ bitki veritabanı (iklim koşulları, verim, fiyat)
  logic/rotation.py  # İklim skoru + öncelik ağırlıklı rotasyon motoru + 3 yıllık rotasyon dizisi + gelir tahmini
  static/
    index.html       # Tek sayfa arayüz (Leaflet harita, rotasyon dizisi, gelir kartı)
    style.css        # Stil
    app.js           # İstemci mantığı (API entegrasyonu, grafikler)
```

## Nasıl çalıştırılır
```bash
cd "C:/Users/musaf/field-shift-nasa-space-apps--main"
python server.py
# tarayıcıda: http://localhost:5000
```

Gerekli Python paketleri: sadece standart kütüphane (`http.server`, `json`, `urllib`).

## API Endpoint'leri
- `GET /` — arayüz
- `GET /api/bitkiler` — 20+ bitki veritabanı (JSON)
- `POST /api/analiz` — `{lat, lon, start, end}` → NASA POWER ortalama iklim verisi
- `POST /api/analiz/smap` — SMAP土壤 nemi (placeholder, NSIDC API anahtarı gerekli)
- `POST /api/analiz/ndvi` — Landsat NDVI (placeholder, USGS/Earth Engine gerekli)
- `POST /api/analiz/lst` — ECOSTRESS LST (placeholder, Earthdata API anahtarı gerekli)
- `POST /api/analiz/elevation` — SRTM yükseklik (placeholder, USGS/OpenTopoData gerekli)
- `POST /api/analiz/all` — tüm NASA kaynakları birleşik
- `POST /api/rotasyon` — `{ortalama, oncelikler, mevcut, onceki, scenario, constraints, lang, field_size_decare}` → 3 strateji + 3 yıllık rotasyon dizisi + gelir tahmini + stres takvimi + risk uyarıları

## Veri Kaynakları
- **NASA POWER Daily API** (`power.larc.nasa.gov`): sıcaklık, yağış, güneş ışınması, rüzgar (anahtarsız)
- **NASA POWER Monthly API**: aylık iklim verileri (stres takvimi için)
- **SMAP, Landsat, ECOSTRESS, SRTM**: endpoint'leri eklendi, gerçek veri için ilgili NASA/USGS API anahtarları gerekli

## Bitki Veritabanı (data/crops.json)
20+ Türkiye odaklı bitki. Her bitkide: sıcaklık/yağış/güneş aralıkları, su ihtiyacı, toprak etkisi, beklenen verim (kg/decare), pazar fiyatı (₺/kg).

## Özellikler (v2.0)
- **3 Rotasyon Stratejisi:** Toprak Sağlığı Odaklı, Su Tasarruflu, Mevcut Rotasyonu Koru
- **3 Yıllık Rotasyon Dizisi:** Yıl 1 (ana ürün) → Yıl 2 (azot bağlayıcı/örtü) → Yıl 3 (düşük su)
- **Gelir Tahmini:** verim (kg/decare) × alan (decare) × fiyat (₺/kg)
- **Geçen Yıl Bitkisi (`onceki`):** tüketici bitki sonrası iyileştirici bitkilere otomatik bonus
- **Tarla Alanı Girişi:** decare cinsinden, gelir hesaplamasında kullanılır
- **Stres Takvimi:** 12 aylık sıcaklık/su/NDVI stres grafiği
- **Risk Uyarıları:** don, ısı dalgası, kuraklık,土壤 nemi, bitki stresi
- **Harita:** Leaflet ile konum seçimi, sürüklenebilir marker
- **Çoklu Dil:** Türkçe / İngilizce
- **Rapor İndirme:** .txt formatında analiz raporu

## Space Apps Kriterleriyle İlişki
- **NASA Veri Entegrasyonu:** POWER API'dan sıcaklık, yağış, güneş, rüzgar; SMAP/NDVI/LST/SRTM endpoint'leri eklendi
- **Yerel Bilgi:** `data/crops.json` içinde Türkiye bitkileri ve iklim koşulları
- **Çiftçi Öncelikleri:** Su tasarrufu, sağlıklı toprak, kararlı verim, koşula dayanıklılık ağırlıkları
- **Rotasyon:** En az 3 strateji + 3 yıllık dizis + mevcut rotasyonu koruma seçeneği
- **Neden/Kanıt/Fayda/Risk/Eksiklik:** Her strateji için ayrı ayrı
- **Çiftçi Kararı:** "Final karar çiftçi ve yerel tarım uzmanlığına bırakılır" uyarısı mevcut

## Versiyonlar
- **v1.0:** `field-shift-nasa-space-apps--main_v1.0/` — İlk prototip, 8 bitki, sadece POWER API, tek bitki önerisi
- **v2.0:** `field-shift-nasa-space-apps--main_v2.0/` (bu klasör) — 20+ bitki, 3 yıllık rotasyon dizisi, gelir tahmini, yeni NASA endpoint'leri, Leaflet harita
