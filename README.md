# Field Shift — NASA Space Apps 2026 | emo_v3.0

NASA POWER, SMAP, ECOSTRESS, Landsat NDVI, SRTM ve GPM verilerini birleştiren, çiftçilere **3 yıllık ekim rotasyonu**, stres takvimi ve gelir simülasyonu sunan karar destek sistemi.

## Özellikler
- **5 NASA veri kaynağı:** POWER (iklim), SMAP (toprak nemi), ECOSTRESS (ET / ısı stresi), Landsat/Sentinel-2 (NDVI), SRTM (eşya), GPM (yağış).
- **3 Yıllık Rotasyon Takvimi:** Yıl 1 toprağı dinlendiren baklagil, Yıl 2 su tasarruflu, Yıl 3 ekonomik denge.
- **Dinamik Önceki Mahsul Girişi:** Çiftçi geçmişini ekleyebilir; azot bonusu otomatik hesaplanır.
- **16 Türk Mahsul Kataloğu:** Her biri için verim (kg/dönüm) ve fiyat (₺/kg) ile gelir simülasyonu.
- **Senaryo Kaydırıcıları:** Yağış (% değişim) ve sıcaklık (°C değişim) ile anlık rotasyon yeniden hesaplama.
- **12 Aylık Stres Takvimi:** Don, ısı dalgası ve kuraklık uyarıları.
- **İkili Dil (TR/EN) ve çiftçi dostu arayüz.**

## Kurulum
```bash
git clone https://github.com/kedybaykedy-bit/nasa-tarim.git
cd nasa-tarim
git checkout emo_v3.0
python3 server.py
```
Tarayıcıda: http://localhost:5000

## API
- `POST /api/analiz` — lat, lon, start, end → NASA POWER günlük + aylık ortalama ve ekstra NASA kaynakları (SMAP, ECOSTRESS, Landsat, SRTM, GPM)
- `POST /api/rotasyon` — ortalama, oncelikler, mevcut, onceki, gecmis_bitkiler, aylik, ekstra, scenario, constraints, lang → 3 strateji, 3 yıllık plan, stres takvimi, gelir simülasyonu
- `GET /api/bitkiler` — mahsul kataloğu