# Field Shift — NASA Space Apps 2026 | v4.0

NASA POWER, SMAP, ECOSTRESS, Landsat NDVI, SRTM ve GPM verilerini birleştiren, çiftçilere **3 yıllık ekim rotasyonu**, stres takvimi, SI trendi analizi ve gelir simülasyonu sunan karar destek sistemi.

## Özellikler
- **6 NASA veri kaynağı:** POWER (günlük + aylık iklim), SMAP (toprak nemi granulesi, NSIDC CMR), SRTM (eşya/elevasyon, open-elevation), ECOSTRESS (ET / ısı stresi), Landsat/Sentinel-2 (NDVI), GPM (yağış).
- **3 Yıllık Rotasyon Takvimi:** Yıl 1 toprağı dinlendiren baklagil, Yıl 2 su tasarruflu, Yıl 3 ekonomik denge. Her yıl için rol, verim ve gelir tahmini.
- **Dinamik Önceki Mahsul Girişi:** Çiftçi geçmişini ekleyebilir; azot bonusu otomatik hesaplanır.
- **16 Türk Mahsul Kataloğu:** Her biri için verim (kg/dönüm) ve fiyat (₺/kg) ile gelir simülasyonu.
- **Senaryo Kaydırıcıları:** Yağış (% değişim) ve sıcaklık (°C değişim) ile anlık rotasyon yeniden hesaplama.
- **12 Aylık Stres Takvimi:** Don, ısı dalgası ve kuraklık uyarıları; boş tarla riskli ayları tespit.
- **SI Trendi Analizi:** NASA POWER aylık verisinden sıcaklık ve yağış OLS trendi, R², son yıl anomali (Z-skoru) ve güven düzeyi.
- **Belirsizlik Değerlendirmesi:** Kullanılan NASA kaynağı sayısına göre düşük/orta/yüksek belirsirk sınıflandırması.
- **İkili Dil (TR/EN) ve çiftçi dostu arayüz.**

## Kurulum
```bash
git clone https://github.com/kedybaykedy-bit/nasa-tarim.git
cd nasa-tarim
git checkout v4.0
python3 server.py
```
Tarayıcıda: http://localhost:8080 (veya PORT ortam değişkeni)

## API
- `POST /api/analiz` — lat, lon, start, end → NASA POWER günlük + aylık ortalama ve ekstra NASA kaynakları (SMAP, ECOSTRESS, Landsat, SRTM, GPM)
- `POST /api/rotasyon` — ortalama, oncelikler, mevcut, onceki, gecmis_bitkiler, aylik, ekstra, scenario, constraints, lang → 3 strateji, 3 yıllık plan, stres takvimi, SI trendi, belirsizlik, gelir simülasyonu
- `GET /api/bitkiler` — mahsul kataloğu

## Mentör Formu Ölçütleri (1–5)
| Kategori | Hedef |
|----------|-------|
| Etk | 3–4 |
| Yaratıcılık | 4–5 |
| Geçerlilik / Uygulanabilirlik | 3–4 |
| İlgiLilik (NASA veri) | 3–4 (POWER gerçek; SMAP/SRTM granule/elevation çağrıları varsa) |
| Sunum / İletişim | 4–5 |