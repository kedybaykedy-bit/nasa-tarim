# Field Shift — NASA Space Apps Challenge 2026

## Hakkında
NASA POWER iklim verileri ile çiftçilere akıllı bitki döngüsü (crop rotation) önerisi sunan decision-support prototipi.

## Klasör yapısı
```
spaceapps_proj/
  server.py          # HTTP API + arayüz sunucu (port 5000)
  data/crops.json    # Türkiye odaklı bitki veritabanı (iklim koşulları)
  logic/rotation.py  # İklim skoru + öncelik ağırlıklı rotasyon motoru
  static/
    index.html       # Tek sayfa arayüz
    style.css        # Stil
    app.js           # İstemci mantığı
```

## Nasıl çalıştırılır
```bash
cd ~/temp/nasa/spaceapps_proj
python3 server.py
# tarayıcıda: http://localhost:5000
```

## API
- `GET /` — arayüz
- `GET /api/bitkiler` — bitki veritabanı
- `POST /api/analiz` — `{lat, lon, start, end}` → NASA POWER ortalama iklim verisi
- `POST /api/rotasyon` — `{ortalama, oncelikler, mevcut}` → skorlu bitki önerileri + rota önerisi

## Veri kaynağı
NASA POWER Daily API (`power.larc.nasa.gov`), kimsecretsiz, sıcaklık/yağış/güneş/rüzgar.

## Space Apps kriterleriyle ilişki
- **NASA Veri Entegrasyonu:** POWER API'dan alınan sıcaklık, yağış, güneş ışınması.
- **Yerel bilgi:** `data/crops.json` içinde Türkiye bitkileri ve toplantı koşulları.
- **Çiftçi öncelikleri:** Su tasarrufu, toprak sağlığı, kararlı verim, koşula dayanıklılık ağırlıkları.
- **Rotasyon:** Mevcut bitkiye göre farklı grubun bir sonraki önerisi.
