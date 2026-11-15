# Field Shift — NASA Space Apps 2026 | v8.0-emo

NASA, USDA, NOAA, ESA ve Copernicus uydu/iklim verilerini birleştiren, çiftçilere **3 yıllık ekim rotasyonu**, stres takvimi, SI trendi analizi ve gelir simülasyonu sunan karar destek sistemi.

## Özellikler
- **23 açık veri kaynağı:** POWER (günlük + aylık iklim), SMAP (toprak nemi, NSIDC CMR), SRTM (eşya/elevasyon, open-elevation), ECOSTRESS (ET / ısı stresi, AppEEARS), Landsat/Sentinel-2 NDVI (USGS M2M / Copernicus OData), GPM IMERG (yağış, NASA PPS), VIIRS (Earthdata Search), CropScape/CropSmart (GMU), PRISM (OSU), NRCS Web Soil Survey / SSURGO, NAIP (USDA ArcGIS Hub), NLCD (USGS EROS), GAEZ (FAO), CoCoRaHS, USGS NWIS, USDA AMS Market News, NASS QuickStats, OpenET, LANDFIRE, GEDI, Copernicus Data Space, ERA5 (CDS).
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
git checkout v8.0-emo
python3 server.py
```
Tarayıcıda: http://localhost:8080 (veya PORT ortam değişkeni)

## API
- `POST /api/analiz` — lat, lon, start, end → NASA POWER günlük + aylık ortalama ve ekstra NASA kaynakları (SMAP, ECOSTRESS, Landsat, SRTM, GPM)
- `POST /api/rotasyon` — ortalama, oncelikler, mevcut, onceki, gecmis_bitkiler, aylik, ekstra, scenario, constraints, lang → 3 strateji, 3 yıllık plan, stres takvimi, SI trendi, belirsizlik, gelir simülasyonu
- `GET /api/bitkiler` — mahsul kataloğu

## API Anahtarı / Kimlik Bilgisi (ortam değişkenleri)
Gerçek NASA/USDA/ESA uydu verisi çekmek için şu ortam değişkenlerini ayarlayın:

```bash
export NASA_EARTHDATA_USR="kullanici_adiniz"
export NASA_EARTHDATA_PWD="sifreniz"        # SMAP granule download + ECOSTRESS AppEEARS
export USGS_API_KEY="anahtarınız"            # Landsat scene search (USGS M2M)
export COPERNICUS_USR="kullanici_adiniz"     # Sentinel-2 OData (Copernicus Data Space)
export COPERNICUS_PWD="sifreniz"             # Sentinel-2 OData (Copernicus Data Space)
```

Kimlik bilgisi girilmeden ilgili kaynaklar şeffaf "kimlik gerekli" notu ile işaretlenir ve kod çalışmaya devam eder.

## Kaynak Tablosu (v7.0-emo)

| Kaynak | Neden Kullanılır | Erişim |
|--------|------------------|--------|
| NASA POWER | Sıcaklık, yağış, güneş, rüzgar, don riski | Açık (API yok) |
| SMAP (NSIDC CMR) | Yüzey toprak nemi, don/dönme durumu | Earthdata login gerekli |
| SRTM (open-elevation) | Eşya, eğim, erozyon riski | Açık |
| ECOSTRESS (AppEEARS) | Yüzey sıcaklık, evapotranspiration | Earthdata login gerekli |
| Landsat NDVI (USGS M2M) | Bitki sağlığı, boş tarla tespiti | USGS API key gerekli |
| Sentinel-2 NDVI (Copernicus) | Bitki sağlığı, boş tarla tespiti | Copernicus login gerekli |
| GPM IMERG (NASA PPS) | Yağış oranı, ekstrem yağış | NASA PPS/Giovanni |
| VIIRS (Earthdata Search) | Bitki vigor, seasonal change | Earthdata search |
| CropScape / CropSmart | Cropland Data Layer (CDL) | GMU kayıt gerekli |
| PRISM (OSU) | İklim normalleri, frost/freeze dates | Açık indirme |
| NRCS Web Soil Survey / SSURGO | Toprak tekstür, organic matter, drawaj | Açık web arayüzü |
| NAIP (USDA ArcGIS Hub) | 1m hava fotoğrafı, tarla sınırı | ArcGIS Hub |
| NLCD (USGS EROS) | Land cover, su gövdesi, entwickelt | Açık indirme |
| GAEZ (FAO) | Agro-ekolojik uygunluk, verim potansiyeli | FAO web sitesi |
| CoCoRaHS | Topluluk yağış gözlemleri | Açık web sitesi |
| USGS NWIS | Grundwasser, akış, su kalitesi | Açık web servisi |
| USDA AMS Market News | Piyasa fiyatı, talep trendi | USDA web sitesi |
| NASS QuickStats | Verim, tarla alanı, tarihsel istatistik | USDA web servisi |
| OpenET | Evapotranspiration, su talebi | Açık web servisi |
| LANDFIRE | Vegitation type, fuel models | USFS web sitesi |
| GEDI | Canopy height, biomass, vegetation density | NASA LP DAAC |
| Copernicus Data Space | Sentinel-2, Sentinel-3, ERA5 | Copernicus kayıt |
| ERA5 (CDS) | Saatlik iklim yeniden analizi | CDS kayıt gerekli |

## Mentör Formu Ölçütleri (1–5)
| Kategori | Hedef |
|----------|-------|
| Etk | 4–5 |
| Yaratıcılık | 4–5 |
| Geçerlilik / Uygulanabilirlik | 4–5 |
| İlgiLilik (NASA veri) | 4–5 (POWER ve SRTM gerçek; diğerleri API anahtarı ile tam entegrasyon) |
| Sunum / İletişim | 4–5 |

## Kimlik Bilgisi Gerekli Kaynaklar
- **SMAP:** NSIDC CMR granule araması kimliksiz; gerçek pixel indirme için NASA_EARTHDATA_USR/PWD gerekir.
- **ECOSTRESS:** AppEEARS task submission için NASA_EARTHDATA_USR/PWD gerekir.
- **Landsat:** USGS M2M scene search için USGS_API_KEY gerekir.
- **Sentinel-2:** Copernicus OData için COPERNICUS_USR/PWD gerekir.
- **GPM IMERG:** NASA PPS/Giovanni endpoint gerekebilir.