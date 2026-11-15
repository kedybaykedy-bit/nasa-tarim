# Field Shift — NASA Space Apps 2026 | v4.5

NASA POWER, SMAP, SRTM, ECOSTRESS, Landsat NDVI, GPM verilerini birleştiren, çiftçilere 3 yıllık ekim rotasyonu, stres takvimi, SI trendi analizi, gelir simülasyonu ve belirsizlik değerlendirmesi sunan karar destek sistemi.

## v4.5 Yenilikleri (main + v4.0 birleştirmesi)

- **6 NASA veri kaynağı:** POWER (günlük + aylık), SMAP (NSIDC CMR), SRTM (open-elevation), ECOSTRESS, Landsat/Sentinel-2 (NDVI), GPM
- **3 Yıllık Rotasyon Dizisi:** Yıl 1 toprağı dinlendiren baklagil, Yıl 2 su tasarruflu, Yıl 3 ekonomik denge. Her yıl için rol, verim ve gelir tahmini.
- **Dinamik Önceki Mahsul Girişi:** Çiftçi geçmişini ekleyebilir; azot bonusu otomatik hesaplanır.
- **17 Türk Mahsul Kataloğu:** Her biri için verim (kg/dönüm) ve fiyat (₺/kg) ile gelir simülasyonu.
- **Senaryo Kaydırıcıları:** Yağış (% değişim) ve sıcaklık (°C değişim) ile anlık rotasyon yeniden hesaplama.
- **12 Aylık Stres Takvimi:** Don, ısı dalgası ve kuraklık uyarıları; boş tarla riskli ayları tespit.
- **SI Trendi Analizi:** NASA POWER aylık verisinden sıcaklık ve yağış OLS trendi, R², son yıl anomali (Z-skoru) ve güven düzeyi.
- **Belirsizlik Değerlendirmesi:** Kullanılan NASA kaynağı sayısına göre düşük/orta/yüksek sınıflandırması.
- **İkili Dil (TR/EN)** ve çiftçi dostu Leaflet harita arayüzü.
- **Gelir Simülasyonu:** Verim × fiyat ile brüt hasat geliri tahmini.

## Kurulum

```
git clone https://github.com/kedybaykedy-bit/nasa-tarim.git
cd nasa-tarim
git checkout v4.5
python3 server.py
```

Tarayıcıda: http://localhost:8080 (veya `PORT` ortam değişkeni)

## API

- `POST /api/analiz` — lat, lon, start, end → NASA POWER günlük + aylık ortalama ve ekstra NASA kaynakları (SMAP, ECOSTRESS, Landsat, SRTM, GPM)
- `POST /api/rotasyon` — ortalama, oncelikler, mevcut, onceki, gecmis_bitkiler, ekstra, aylik, scenario, constraints, lang → 3 strateji, 3 yıllık plan, stres takvimi, SI trendi, belirsizlik, gelir simülasyonu
- `GET /api/bitkiler` — mahsul kataloğu

## Proje Mimarisi

* `server.py` : Hafif yerel HTTP sunucusu. NASA POWER API ve ekstra NASA çağrıları, rotasyon motoru ve statik dosya sunumu.
* `logic/rotation.py` : İklim uygunluk skorlama, 3 yıllık ekim döngüsü algoritması, SI trendi, belirsizlik, gelir simülasyonu.
* `data/crops.json` : 17 Türk mahsulün biyolojik limitleri, verim ve fiyat parametreleri.
* `static/` : Leaflet harita, Chart.js grafikleri, i18n (TR/EN), 3 yıllık rotasyon kartları ve gelir paneli.

## Mentör Formu Ölçütleri (1–5)

| Kategori | Hedef |
|---|---|
| Etki | 4–5 |
| Yaratıcılık | 4–5 |
| Geçerlilik / Uygulanabilirlik | 4–5 |
| İlgiLilik (NASA veri) | 5 (POWER gerçek; SMAP/SRTM/ECOSTRESS/GPM entegrasyonu) |
| Sunum / İletişim | 5 |
