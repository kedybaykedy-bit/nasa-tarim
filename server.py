#!/usr/bin/env python3
"""NASA Space Apps 2026 - Field Shift emo_v3.0 sunucu.
HTTP: GET /, GET /static/*, POST /api/analiz, POST /api/rotasyon
NASA kaynakları: POWER, SMAP, ECOSTRESS, Landsat NDVI, SRTM, GPM"""
import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

POWER_DAILY = "https://power.larc.nasa.gov/api/temporal/daily/point"
POWER_MONTHLY = "https://power.larc.nasa.gov/api/temporal/monthly/point"

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")


def _get_json(url, timeout=30):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def power_veri(lat, lon, start, end, params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M"):
    qs = urllib.parse.urlencode({
        "parameters": params, "community": "AG", "longitude": lon,
        "latitude": lat, "start": start, "end": end, "format": "JSON",
    })
    url = f"{POWER_DAILY}?{qs}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as ex:
            if attempt == 2:
                raise Exception(f"NASA POWER hatası: {ex}")
            import time
            time.sleep(2 ** attempt)
    return None


def power_aylik(lat, lon, year="2023", params="T2M,PRECTOTCORR"):
    qs = urllib.parse.urlencode({
        "parameters": params, "community": "AG", "longitude": lon,
        "latitude": lat, "start": year, "end": year, "format": "JSON",
    })
    return _get_json(f"{POWER_MONTHLY}?{qs}", timeout=20)


def smap_veri(lat, lon, start, end):
    return {"source": "SMAP", "soil_moisture": None, "note": "SMAP entegrasyonu için Earthdata token gerekli"}


def ecostress_veri(lat, lon, start, end):
    return {"source": "ECOSTRESS", "lst_c": None, "et_mm_day": None, "note": "ECOSTRESS AppEEARS entegrasyonu gerekli"}


def landsat_ndvi(lat, lon, start, end):
    return {"source": "Landsat/S2", "ndvi": None, "note": "USGS / Copernicus API entegrasyonu gerekli"}


def srtm_elevation(lat, lon):
    return {"source": "SRTM", "elevation_m": None, "note": "SRTM DEM entegrasyonu gerekli"}


def gpm_precip(lat, lon, start, end):
    return {"source": "GPM", "precip_mm_day": None, "note": "GPM IMERG entegrasyonu gerekli"}


def ortalama(veri_dict):
    vals = [v for v in veri_dict.values() if isinstance(v, (int, float)) and v >= 0]
    return round(sum(vals) / len(vals), 2) if vals else 0


def analiz_et(veri):
    p = veri["properties"]["parameter"]
    return {
        "sıcaklık_C": ortalama(p.get("T2M", {})),
        "yağış_mm_gun": ortalama(p.get("PRECTOTCORR", {})),
        "güneş_MJ_m2_gun": ortalama(p.get("ALLSKY_SFC_SW_DWN", {})),
        "rüzgar_m_s": ortalama(p.get("WS2M", {})),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, code=200, content_type="application/json"):
        b = body.encode("utf-8") if isinstance(body, str) else body
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

        if self.path == "/api/analiz":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                veri = power_veri(lat, lon, start, end)
                ort = analiz_et(veri)
                yil = str(start)[:4]
                aylik = power_aylik(lat, lon, year=yil)
                ekstra = {
                    "smap": smap_veri(lat, lon, start, end),
                    "ecostress": ecostress_veri(lat, lon, start, end),
                    "landsat_ndvi": landsat_ndvi(lat, lon, start, end),
                    "srtm": srtm_elevation(lat, lon),
                    "gpm": gpm_precip(lat, lon, start, end),
                }
                self._json({"ortalama": ort, "raw": veri, "aylik": aylik, "ekstra": ekstra})
            except Exception as ex:
                self._json({"error": str(ex)}, 500)

        elif self.path == "/api/rotasyon":
            try:
                import sys
                sys.path.insert(0, BASE)
                from logic.rotation import rotasyon_oneri
                ort = body["ortalama"]
                oncelikler = body.get("oncelikler", {})
                mevcut = body.get("mevcut")
                onceki = body.get("onceki")
                gecmis_bitkiler = body.get("gecmis_bitkiler", [])
                aylik = body.get("aylik")
                ekstra = body.get("ekstra", {})
                scenario = body.get("scenario")
                constraints = body.get("constraints")
                lang = body.get("lang", "tr")
                sonuc = rotasyon_oneri(
                    ort, oncelikler, mevcut, onceki=onceki,
                    gecmis_bitkiler=gecmis_bitkiler, aylik=aylik, ekstra=ekstra,
                    scenario=scenario, constraints=constraints, lang=lang
                )
                self._json(sonuc)
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
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