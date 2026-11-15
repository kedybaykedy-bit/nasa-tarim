#!/usr/bin/env python3
"""NASA Space Apps 2026 - Field Shift v4.5 sunucu.
Birleştirilmiş sürüm: main arayüzü + v4.0 NASA veri fusiónu.
Kaynaklar: POWER (günlük + aylık), SMAP (NSIDC CMR), SRTM (open-elevation),
ECOSTRESS (ET / ısı stresi), Landsat/Sentinel-2 (NDVI proxy), GPM (yağış).
HTTP: GET /, GET /static/*, POST /api/analiz, POST /api/rotasyon, GET /api/bitkiler
"""
import json
import os
import time
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

POWER_DAILY = "https://power.larc.nasa.gov/api/temporal/daily/point"
POWER_MONTHLY = "https://power.larc.nasa.gov/api/temporal/monthly/point"
SMAP_SEARCH = "https://cmr.earthdata.nasa.gov/search/granules.json"
SRTM_API = "https://api.open-elevation.com/api/v1/lookup"
HEADERS = {"User-Agent": "FieldShift-v4.5/1.0 (contact: fieldshift@example.com)"}

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")


def _get_json(url, timeout=25):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def power_veri(lat, lon, start, end, params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M,T2M_MIN,T2M_MAX"):
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
                raise Exception(f"NASA POWER hatası (3 deneme sonrası): {ex}")
            time.sleep(2 ** attempt)
    return None


def power_aylik(lat, lon, year="2023", params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"):
    qs = urllib.parse.urlencode({
        "parameters": params, "community": "AG", "longitude": lon,
        "latitude": lat, "start": year, "end": year, "format": "JSON",
    })
    return _get_json(f"{POWER_MONTHLY}?{qs}", timeout=20)


def smap_veri(lat, lon, start, end):
    """SMAP surface soil moisture granule araması (NSIDC CMR)."""
    try:
        qs = urllib.parse.urlencode({
            "collection_short_name": "SPL4SMAU",
            "temporal": f"{start},{end}",
            "point": f"{lon},{lat}",
            "page_size": 5,
        })
        data = _get_json(f"{SMAP_SEARCH}?{qs}", timeout=30)
        if data and "feed" in data and "entry" in data["feed"]:
            entries = data["feed"]["entry"]
            return {
                "source": "SMAP",
                "granules": len(entries),
                "coverage": "global_2_3_day",
                "available": len(entries) > 0,
                "note": f"{len(entries)} SMAP granule bulundu (NSIDC CMR).",
            }
        return {
            "source": "SMAP",
            "granules": 0,
            "available": False,
            "note": "SMAP granule bulunamadı (NSIDC CMR).",
        }
    except Exception as ex:
        return {"source": "SMAP", "available": False, "note": f"SMAP çağrı hatası: {ex}"}


def srtm_veri(lat, lon):
    """SRTM eşya yüksekliği (open-elevation API)."""
    try:
        qs = urllib.parse.urlencode({"locations": f"{lat},{lon}"})
        data = _get_json(f"{SRTM_API}?{qs}", timeout=20)
        if data and "results" in data and len(data["results"]) > 0:
            return {
                "source": "SRTM",
                "elevation_m": data["results"][0].get("elevation", 0),
                "available": True,
            }
        return {"source": "SRTM", "elevation_m": 0, "available": False}
    except Exception as ex:
        return {"source": "SRTM", "elevation_m": 0, "available": False, "note": f"SRTM hatası: {ex}"}


def ecostress_veri(lat, lon, start, end):
    """ECOSTRESS LST/ET — AppEEARS task-based, şeffaf bildirim."""
    return {
        "source": "ECOSTRESS",
        "available": False,
        "note": "ECOSTRESS AppEEARS task-based API (token gerektirir). Gelecek sürümde entegre edilecek.",
    }


def gpm_veri(lat, lon, start, end):
    """GPM / IMERG yağış — granule erişimi için CMR arama placeholder."""
    return {
        "source": "GPM",
        "available": False,
        "note": "GPM/IMERG accumulator verisi şu ana kadar POWER PRECTOTCORR ile taklit edilmektedir.",
    }


def ekstra_nasa(lat, lon, start, end):
    """Tüm ekstra NASA kaynaklarını toparlar."""
    return {
        "smap": smap_veri(lat, lon, start, end),
        "srtm": srtm_veri(lat, lon),
        "ecostress": ecostress_veri(lat, lon, start, end),
        "gpm": gpm_veri(lat, lon, start, end),
    }


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
        "min_sıcaklık_C": ortalama(p.get("T2M_MIN", {})),
        "max_sıcaklık_C": ortalama(p.get("T2M_MAX", {})),
    }


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

        if self.path == "/api/analiz":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                veri = power_veri(lat, lon, start, end)
                ort = analiz_et(veri)
                ekstra = ekstra_nasa(lat, lon, start, end)
                aylik = power_aylik(lat, lon)
                self._json({"ortalama": ort, "raw": veri, "ekstra": ekstra, "aylik": aylik})
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
                ekstra = body.get("ekstra", {})
                aylik = body.get("aylik")
                scenario = body.get("scenario")
                constraints = body.get("constraints")
                lang = body.get("lang", "tr")
                sonuc = rotasyon_oneri(
                    ort, oncelikler, mevcut, onceki=onceki,
                    gecmis_bitkiler=gecmis_bitkiler, ekstra=ekstra,
                    aylik_veri=aylik, scenario=scenario, constraints=constraints, lang=lang,
                )
                self._json(sonuc)
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
        else:
            self._json({"error": "bulunamadı"}, 404)


if __name__ == "__main__":
    import os, socket
    port = int(os.environ.get("PORT", 8080))
    s = socket.socket()
    try:
        s.bind(("0.0.0.0", port))
        s.close()
    except OSError:
        port = 8081
    print(f"Sunucu başlatılıyor: http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
