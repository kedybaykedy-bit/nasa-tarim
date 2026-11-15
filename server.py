#!/usr/bin/env python3
"""NASA Space Apps 2026 - Field Shift proje sunucusu (v2.0).
HTTP: GET /, GET /static/*, POST /api/analiz, POST /api/analiz/smap,
POST /api/analiz/ndvi, POST /api/analiz/lst, POST /api/analiz/elevation,
POST /api/analiz/all, POST /api/rotasyon
"""
import json
import os
import time
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

POWER = "https://power.larc.nasa.gov/api/temporal/daily/point"
POWER_MONTHLY = "https://power.larc.nasa.gov/api/temporal/monthly/point"

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")


def power_veri(lat, lon, start, end, params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M"):
    """NASA POWER daily endpoint'inden veri çeker (retry ile)."""
    qs = urllib.parse.urlencode({
        "parameters": params,
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    })
    url = f"{POWER}?{qs}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as ex:
            if attempt == 2:
                raise Exception(f"NASA POWER API hatası (3 deneme sonrası): {ex}")
            time.sleep(2 ** attempt)
    return None


def power_monthly_veri(lat, lon, start, end, params="T2M,PRECTOTCORR"):
    """NASA POWER monthly endpoint'inden aylık veri çeker."""
    qs = urllib.parse.urlencode({
        "parameters": params,
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    })
    url = f"{POWER_MONTHLY}?{qs}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as ex:
            if attempt == 2:
                raise Exception(f"NASA POWER monthly API hatası: {ex}")
            time.sleep(2 ** attempt)
    return None


def ortalama(veri_dict):
    vals = [v for v in veri_dict.values() if isinstance(v, (int, float)) and v >= 0]
    return round(sum(vals) / len(vals), 2) if vals else 0


def analiz_et(veri):
    p = veri["properties"]["parameter"]
    ort = {
        "sıcaklık_C": ortalama(p.get("T2M", {})),
        "yağış_mm_gun": ortalama(p.get("PRECTOTCORR", {})),
        "güneş_MJ_m2_gun": ortalama(p.get("ALLSKY_SFC_SW_DWN", {})),
        "rüzgar_m_s": ortalama(p.get("WS2M", {})),
    }
    return ort


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, code=200, content_type="application/json"):
        if isinstance(body, str):
            b = body.encode("utf-8")
        else:
            b = body
        self.send_response(code)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(b)

    def _json(self, data, code=200):
        self._send(json.dumps(data, ensure_ascii=False), code, "application/json")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _dosya(self, path, content_type):
        try:
            with open(path, "rb") as f:
                self._send(f.read(), 200, content_type)
        except FileNotFoundError:
            self._json({"error": "dosya bulunamadı"}, 404)

    def do_GET(self):
        if self.path == "/":
            self._dosya(os.path.join(STATIC, "index.html"), "text/html")
        elif self.path.startswith("/static/"):
            dosya = os.path.join(STATIC, self.path[len("/static/"):])
            ct = "text/css" if dosya.endswith(".css") else "application/javascript" if dosya.endswith(".js") else "text/plain"
            self._dosya(dosya, ct)
        elif self.path == "/api/bitkiler":
            import sys
            sys.path.insert(0, BASE)
            from logic.rotation import load_crops
            self._json(load_crops())
        else:
            self._json({"error": "bulunamadı"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            self._json({"error": "geçersiz json"}, 400)
            return

        # ---- /api/analiz - POWER daily ----
        if self.path == "/api/analiz":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                veri = power_veri(lat, lon, start, end)
                ort = analiz_et(veri)
                self._json({"ortalama": ort, "raw": veri})
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/analiz/smap - SMAP土壤 nemi (NASA NSIDC) ----
        if self.path == "/api/analiz/smap":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                self._json({
                    "toprak_nem": None,
                    "birim": "m3/m3",
                    "not": "SMAP verisi için NSIDC API anahtarı gerekir. Placeholder olarak None döndürüldü.",
                    "kaynak": "SMAP SPL4SMLM (NSIDC)"
                })
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/analiz/ndvi - Landsat NDVI ----
        if self.path == "/api/analiz/ndvi":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                self._json({
                    "ndvi": None,
                    "birim": "unitless (0-1)",
                    "not": "Landsat NDVI için USGS EarthExplorer / Earth Engine gereklidir. Placeholder olarak None döndürüldü.",
                    "kaynak": "Landsat 8 / Sentinel-2 (USGS / ESA)"
                })
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/analiz/lst - ECOSTRESS LST ----
        if self.path == "/api/analiz/lst":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                self._json({
                    "lst": None,
                    "birim": "°C",
                    "not": "ECOSTRESS LST için Earthdata API anahtarı gerekir. Placeholder olarak None döndürüldü.",
                    "kaynak": "ECOSTRESS (NASA JPL)"
                })
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/analiz/elevation - SRTM yükseklik ----
        if self.path == "/api/analiz/elevation":
            try:
                lat = body["lat"]; lon = body["lon"]
                self._json({
                    "elevation_m": None,
                    "birim": "metre",
                    "not": "SRTM yükseklik verisi için USGS / OpenTopoData gereklidir. Placeholder olarak None döndürüldü.",
                    "kaynak": "SRTM (NASA / USGS)"
                })
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/analiz/all - Tüm NASA kaynakları birleşik ----
        if self.path == "/api/analiz/all":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                power_result = power_veri(lat, lon, start, end)
                ort = analiz_et(power_result)

                ek = {
                    "toprak_nem": None,
                    "ndvi": None,
                    "lst": None,
                    "elevation_m": None,
                    "kaynaklar": {
                        "POWER": "mevcut",
                        "SMAP": "NSIDC API anahtarı gerekli",
                        "NDVI": "USGS / Earth Engine gerekli",
                        "LST": "Earthdata API anahtarı gerekli",
                        "SRTM": "USGS / OpenTopoData gerekli",
                    }
                }
                sonuc = dict(ort)
                sonuc.update(ek)
                self._json({
                    "ortalama": sonuc,
                    "raw_power": power_result,
                    "ek_veriler": ek
                })
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        # ---- /api/rotasyon - rotasyon motoru ----
        elif self.path == "/api/rotasyon":
            try:
                import sys
                sys.path.insert(0, BASE)
                from logic.rotation import rotasyon_oneri
                ort = body["ortalama"]
                oncelikler = body.get("oncelikler", {})
                mevcut = body.get("mevcut")
                onceki = body.get("onceki")
                scenario = body.get("scenario")
                constraints = body.get("constraints")
                lang = body.get("lang", "tr")
                field_size = body.get("field_size_decare")
                sonuc = rotasyon_oneri(
                    ort, oncelikler, mevcut, onceki=onceki,
                    scenario=scenario, constraints=constraints,
                    lang=lang, field_size_decare=field_size
                )
                self._json(sonuc)
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
            return

        else:
            self._json({"error": "bulunamadı"}, 404)


if __name__ == "__main__":
    import os, socket
    port = int(os.environ.get("PORT", 5000))
    s = socket.socket()
    try:
        s.bind(("0.0.0.0", port))
        s.close()
    except OSError:
        port = 5001
    print(f"Sunucu başlatılıyor: http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
