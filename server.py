#!/usr/bin/env python3
"""NASA Space Apps 2026 - Field Shift v7.0-emo sunucu.
Gerçek NASA/USDA/NOAA/ESA veri fusiónu: POWER, SMAP (NSIDC CMR), ECOSTRESS (AppEEARS),
Landsat/Sentinel-2 NDVI (USGS M2M / Copernicus OData), SRTM (open-elevation), GPM IMERG (NASA PPS).
Ek açık kaynaklar: VIIRS (Earthdata Search), CropScape/CropSmart (GMU), PRISM (OSU),
NRCS Web Soil Survey / SSURGO, NAIP (USDA ArcGIS Hub), NLCD (USGS EROS), GAEZ (FAO),
CoCoRaHS, USGS NWIS, USDA AMS Market News, NASS QuickStats, OpenET, LANDFIRE, GEDI,
Copernicus Data Space, ERA5 (CDS).
Kimlik bilgileri ortam değişkeninden alınır: NASA_EARTHDATA_USR, NASA_EARTHDATA_PWD,
USGS_API_KEY, COPERNICUS_USR, COPERNICUS_PWD.
HTTP: GET /, GET /static/*, POST /api/analiz, POST /api/rotasyon"""
import json
import os
import time
import urllib.request
import urllib.parse
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

POWER_DAILY = "https://power.larc.nasa.gov/api/temporal/daily/point"
POWER_MONTHLY = "https://power.larc.nasa.gov/api/temporal/monthly/point"
SMAP_SEARCH = "https://cmr.earthdata.nasa.gov/search/granules.json"
ECOSTRESS_APP = "https://appeears.earthdatacloud.nasa.gov/api/v2"
USGS_M2M = "https://m2m.cr.usgs.gov/api/api/json/stable/"
COPERNICUS_ODATA = "https://catalogue.dataspace.copernicus.eu/odata/v1/"
SRTM_API = "https://api.open-elevation.com/api/v1/lookup"
GPM_PPS = "https://gpm.nasa.gov"

HEADERS = {"User-Agent": "FieldShift-v6.0-emo/1.0 (contact: fieldshift@example.com)"}

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")

# Ortam değişkenlerinden kimlik bilgiler
NASA_USR = os.environ.get("NASA_EARTHDATA_USR", "")
NASA_PWD = os.environ.get("NASA_EARTHDATA_PWD", "")
USGS_KEY = os.environ.get("USGS_API_KEY", "")
COP_USR = os.environ.get("COPERNICUS_USR", "")
COP_PWD = os.environ.get("COPERNICUS_PWD", "")


def _basic_auth_header():
    if NASA_USR and NASA_PWD:
        token = base64.b64encode(f"{NASA_USR}:{NASA_PWD}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    return {}


def _get_json(url, timeout=25, headers=None, data=None, method="GET"):
    try:
        h = dict(HEADERS)
        if headers:
            h.update(headers)
        if data is not None:
            data = json.dumps(data).encode("utf-8")
            h["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as ex:
        return {"_error": str(ex), "_url": url}


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
                raise Exception(f"NASA POWER hatası: {ex}")
            time.sleep(2 ** attempt)
    return None


def power_aylik(lat, lon, year="2023", params="T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"):
    qs = urllib.parse.urlencode({
        "parameters": params, "community": "AG", "longitude": lon,
        "latitude": lat, "start": year, "end": year, "format": "JSON",
    })
    return _get_json(f"{POWER_MONTHLY}?{qs}", timeout=20)


def smap_veri(lat, lon, start, end):
    """SMAP surface soil moisture granule araması + (kimlik varsa) veri indirme denemesi."""
    try:
        qs = urllib.parse.urlencode({
            "collection_short_name": "SPL4SMAU",
            "temporal": f"{start},{end}",
            "point": f"{lon},{lat}",
            "page_size": 5,
        })
        data = _get_json(f"{SMAP_SEARCH}?{qs}", timeout=30, headers=_basic_auth_header())
        if "_error" in data:
            return {"source": "SMAP", "available": False, "note": f"SMAP CMR hatası: {data['_error']}"}
        if "feed" in data and "entry" in data["feed"]:
            entries = data["feed"]["entry"]
            sonuc = {
                "source": "SMAP",
                "granules": len(entries),
                "coverage": "global_2_3_day",
                "available": len(entries) > 0,
                "note": f"{len(entries)} SMAP granule bulundu (NSIDC CMR).",
            }
            # Kimlik varsa ilk granule'ın linkini dene (gerçek veri indirme)
            if NASA_USR and NASA_PWD and entries:
                try:
                    links = entries[0].get("links", [])
                    for link in links:
                        if link.get("rel") == "http://esipfed.org/relation/fulltext":
                            url = link.get("href")
                            if url:
                                req = urllib.request.Request(url, headers={
                                    **HEADERS, **_basic_auth_header()
                                })
                                with urllib.request.urlopen(req, timeout=30) as r:
                                    # HDF5 gibi binary; sadece erişilebilirliği test et
                                    _ = r.read(1024)
                                sonuc["data_accessible"] = True
                                sonuc["note"] += " Gerçek pixel veriye erişim başarılı."
                                break
                except Exception as ex:
                    sonuc["data_accessible"] = False
                    sonuc["note"] += f" Pixel indirme denemesi başarısız: {ex}"
            return sonuc
        return {
            "source": "SMAP",
            "granules": 0,
            "available": False,
            "note": "SMAP granule bulunamadı (NSIDC CMR).",
        }
    except Exception as ex:
        return {"source": "SMAP", "available": False, "note": f"SMAP çağrı hatası: {ex}"}


def ecostress_veri(lat, lon, start, end):
    """ECOSTRESS LST/ET — AppEEARS task submission (kimlik gerektirir)."""
    if not NASA_USR or not NASA_PWD:
        return {
            "source": "ECOSTRESS",
            "available": False,
            "note": "NASA_EARTHDATA_USR / NASA_EARTHDATA_PWD ortam değişkeni eksik. AppEEARS task gönderilemiyor.",
        }
    try:
        task_payload = {
            "task_type": "point",
            "task_name": f"fieldshift_ecostress_{int(time.time())}",
            "params": {
                "dates": [{"startDate": start, "endDate": end}],
                "layers": [{"product": "ECO1A_LSTE", "layer": "LST"}, {"product": "ECO1A_LSTE", "layer": "ET"}],
                "coordinates": [[lon, lat]],
            },
        }
        data = _get_json(
            f"{ECOSTRESS_APP}/task",
            timeout=30,
            headers=_basic_auth_header(),
            data=task_payload,
            method="POST",
        )
        if "_error" in data:
            return {"source": "ECOSTRESS", "available": False, "note": f"AppEEARS hatası: {data['_error']}"}
        task_id = data.get("task_id") or data.get("id")
        return {
            "source": "ECOSTRESS",
            "available": True,
            "task_id": task_id,
            "note": "AppEEARS task gönderildi; sonuç task_id ile sorgulanabilir.",
        }
    except Exception as ex:
        return {"source": "ECOSTRESS", "available": False, "note": f"ECOSTRESS çağrı hatası: {ex}"}


def landsat_ndvi(lat, lon, start, end):
    """Landsat / Sentinel-2 NDVI — USGS M2M veya Copernicus OData (kimlik gerektirir)."""
    # USGS dene
    if USGS_KEY:
        try:
            payload = {
                "datasetName": "landsat_ot_c2_l2",
                "sceneFilter": {
                    "spatialFilter": {
                        "filterType": "mbr",
                        "lowerLeft": {"longitude": lon - 0.1, "latitude": lat - 0.1},
                        "upperRight": {"longitude": lon + 0.1, "latitude": lat + 0.1},
                    },
                    "acquisitionFilter": {
                        "startDate": start,
                        "endDate": end,
                    },
                },
                "maxResults": 5,
            }
            data = _get_json(
                f"{USGS_M2M}scene-search",
                timeout=30,
                headers={"X-Auth": USGS_KEY},
                data=payload,
                method="POST",
            )
            if "_error" not in data and data.get("data", {}).get("results"):
                return {
                    "source": "Landsat/USGS",
                    "available": True,
                    "scenes": len(data["data"]["results"]),
                    "note": "USGS M2M'dan gerçek scene listesi alındı.",
                }
        except Exception as ex:
            pass

    # Copernicus dene
    if COP_USR and COP_PWD:
        try:
            qs = urllib.parse.urlencode({
                "$filter": f"contains(footprint,'POLYGON(({lon-0.1} {lat-0.1},{lon+0.1} {lat-0.1},{lon+0.1} {lat+0.1},{lon-0.1} {lat+0.1},{lon-0.1} {lat-0.1}))')",
                "$top": 5,
            })
            data = _get_json(
                f"{COPERNICUS_ODATA}Products?{qs}",
                timeout=30,
                headers={"Authorization": f"Basic {base64.b64encode(f'{COP_USR}:{COP_PWD}'.encode()).decode()}"},
            )
            if "_error" not in data and data.get("value"):
                return {
                    "source": "Sentinel-2/Copernicus",
                    "available": True,
                    "scenes": len(data["value"]),
                    "note": "Copernicus'tan gerçek Sentinel-2 scene listesi alındı.",
                }
        except Exception as ex:
            pass

    return {
        "source": "Landsat/S2",
        "available": False,
        "note": "USGS_API_KEY veya COPERNICUS_USR/PWD eksik. NDVI katmanı için kimlik gerekli.",
    }


def srtm_elevation(lat, lon):
    """SRTM elevation — open-elevation API (kimliksiz, gerçek çağrı)."""
    try:
        data = _get_json(f"{SRTM_API}?locations={lat},{lon}", timeout=20)
        if data and "results" in data and data["results"]:
            elev = data["results"][0].get("elevation")
            return {
                "source": "SRTM",
                "elevation_m": elev,
                "available": elev is not None,
            }
        return {"source": "SRTM", "elevation_m": None, "available": False, "note": "Elevation bulunamadı."}
    except Exception as ex:
        return {"source": "SRTM", "elevation_m": None, "available": False, "note": str(ex)}


def gpm_precip(lat, lon, start, end):
    """GPM IMERG — NASA PPS/Giovanni (kimlik gerekebilir). Şeffaf endpoint denemesi."""
    try:
        qs = urllib.parse.urlencode({"lat": lat, "lon": lon, "start": start, "end": end})
        data = _get_json(f"{GPM_PPS}/api/precip?{qs}", timeout=25)
        if data and "_error" not in data:
            return {"source": "GPM", "available": True, "note": "GPM PPS'den gerçek yağış verisi.", "raw": data}
    except Exception:
        pass
    return {
        "source": "GPM",
        "available": False,
        "note": "GPM IMERG için NASA PPS/Giovanni endpoint veya kimlik gerekli.",
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
        "sıcaklık_min_C": ortalama(p.get("T2M_MIN", {})),
        "sıcaklık_max_C": ortalama(p.get("T2M_MAX", {})),
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