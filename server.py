#!/usr/bin/env python3
"""NASA Space Apps 2026 - Field Shift proje sunucu.
HTTP: GET /, GET /static/*, POST /api/analiz, POST /api/rotasyon"""
import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

POWER = "https://power.larc.nasa.gov/api/temporal/daily/point"

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")


def power_veri(lat, lon, start, end, params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M"):
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
    # Retry logic: 3 deneme, exponential backoff
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as ex:
            if attempt == 2:
                raise Exception(f"NASA POWER API hatası (3 deneme sonrası): {ex}")
            import time
            time.sleep(2 ** attempt)  # 1s, 2s
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

        if self.path == "/api/analiz":
            try:
                lat = body["lat"]; lon = body["lon"]; start = body["start"]; end = body["end"]
                veri = power_veri(lat, lon, start, end)
                ort = analiz_et(veri)
                self._json({"ortalama": ort, "raw": veri})
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
                scenario = body.get("scenario")
                constraints = body.get("constraints")
                lang = body.get("lang", "tr")
                sonuc = rotasyon_oneri(ort, oncelikler, mevcut, scenario=scenario, constraints=constraints, lang=lang)
                self._json(sonuc)
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
        else:
            self._json({"error": "bulunamadı"}, 404)


if __name__ == "__main__":
    import os, socket
    port = int(os.environ.get("PORT", 5000))
    # Try port, fall back to 5001 if in use
    s = socket.socket()
    try:
        s.bind(("0.0.0.0", port))
        s.close()
    except OSError:
        port = 5001
    print(f"Sunucu başlatılıyor: http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
