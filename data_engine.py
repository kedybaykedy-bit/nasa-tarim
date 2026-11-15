"""
Field Shift — NASA Space Apps Challenge 2026
Data Engine — Integrated NASA & USDA Earth Observation Sources

All data sources listed in the challenge resources are integrated here.
Prototipte deterministik NASA-stil sentetik veri kullanılır; gerçek kayıtlar için
her veri kaynağının API entegrasyon noktası hazır bırakılmıştır.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import hashlib


# ---------------------------------------------------------------------------
# NASA Earth Observation Data Sources
# ---------------------------------------------------------------------------

NASA_DATA_SOURCES: Dict[str, dict] = {
    "SMAP": {
        "name": "Soil Moisture Active Passive",
        "parameter": "surface soil moisture & freeze/thaw state",
        "temporal": "every 2–3 days",
        "use": "drought stress, water availability, infiltration potential, early crop-stress signals",
        "api_hint": "Earthdata / NSIDC DAAC — SMAP_L3_SM_P / SMAP_L4_SM",
        "mapped_to": "smap_soil_moisture",
    },
    "GPM / IMERG": {
        "name": "Global Precipitation Measurement",
        "parameter": "precipitation rate & accumulation",
        "temporal": "near real-time / monthly",
        "use": "rainfall reliability, extreme-storm frequency, erosion risk, water input to soils",
        "api_hint": "Earthdata / GES DISC — GPM_3IMERGHH / IMERG Final",
        "mapped_to": "gpm_precip_mm",
    },
    "Landsat / MODIS / VIIRS": {
        "name": "Landsat 8/9, MODIS (Terra/Aqua), VIIRS (Suomi NPP)",
        "parameter": "reflectance, NDVI, vegetation indices, plant stress, bare ground",
        "temporal": "Landsat 16-day / MODIS-VIIRS daily",
        "use": "crop vigor, seasonal transitions, high-stress periods, rotation comparison",
        "api_hint": "Earthdata / USGS EEA / LP DAAC — Landsat C2 L2 / MOD13Q1 / VNP13",
        "mapped_to": "landsat_ndvi, modis_ndvi",
    },
    "NASA POWER": {
        "name": "Prediction Of Worldwide Energy Resource",
        "parameter": "solar, meteorological, climatology (temp, humidity, radiation)",
        "temporal": "daily / monthly / 30-year normals",
        "use": "crop water use, growing-season conditions, frost risk, climate suitability",
        "api_hint": "https://power.larc.nasa.gov/api/temporal/daily/point",
        "mapped_to": "nasa_power_tmax_c, nasa_power_tmin_c",
    },
    "SRTM": {
        "name": "Shuttle Radar Topography Mission",
        "parameter": "elevation & terrain models",
        "temporal": "static (2000)",
        "use": "slope, runoff, erosion risk, water flow, terrain-driven stress",
        "api_hint": "Earthdata / LP DAAC — SRTMGL1 / NASADEM",
        "mapped_to": "srtm_elevation_m, slope_percent",
    },
    "ECOSTRESS": {
        "name": "ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station",
        "parameter": "land-surface temperature (LST) & evapotranspiration (ET)",
        "temporal": "high spatial resolution, ~3-5 days",
        "use": "plant stress hotspots, heat exposure, shallow-root vulnerability, crop-water demand",
        "api_hint": "Earthdata / LP DAAC — ECO2LSTE / ECO3ETPT",
        "mapped_to": "ecostress_lst_c, ecostress_et_mm_day",
    },
    "GRACE / GRACE-FO": {
        "name": "Gravity Recovery and Climate Experiment",
        "parameter": "terrestrial water storage",
        "temporal": "monthly",
        "use": "long-term water trends, groundwater depletion",
        "api_hint": "Earthdata / PODAAC — GRACE/GRACE-FO mascon",
        "mapped_to": "grace_tws_anomaly",
    },
    "GEDI": {
        "name": "Global Ecosystem Dynamics Investigation",
        "parameter": "canopy height, leaf area index, above-ground biomass",
        "temporal": "ISS orbit, 2018–present",
        "use": "vegetation density, canopy stress, land-cover structural context",
        "api_hint": "Earthdata / LP DAAC — GEDI L2 / L4B",
    },
    "NLDAS / GLDAS": {
        "name": "North American / Global Land Data Assimilation Systems",
        "parameter": "temperature, precipitation, soil moisture, ET proxies, radiation",
        "temporal": "sub-daily",
        "use": "drought onset, moisture deficits, growing-season transitions, continuous time-series",
        "api_hint": "Earthdata / GES DISC — NLDAS_FORA / GLDAS_NOAH",
    },
    "OpenET": {
        "name": "OpenET (Evapotranspiration)",
        "parameter": "field-scale ET estimates (satellite-driven)",
        "temporal": "quarterly / annual",
        "use": "crop water demand, irrigation timing, water-use efficiency (western U.S.)",
        "api_hint": "https://openetdata.org/api",
    },
    "ESA Copernicus Sentinel-2": {
        "name": "Sentinel-2 (ESA)",
        "parameter": "10–20 m multispectral imagery (red-edge, NIR, SWIR)",
        "temporal": "5-day revisit",
        "use": "NDVI/EVI, bare-soil mapping, crop stress detection, fine-scale monitoring",
        "api_hint": "Copernicus Open Access Hub — Sentinel-2 L2A",
    },
    "ERA5": {
        "name": "ERA5 Reanalysis (ECMWF)",
        "parameter": "hourly climate: temperature, precipitation, wind, humidity, soil temperature, radiation",
        "temporal": "hourly / monthly",
        "use": "gap-filling, long-term climate trends, temporal features for SI models",
        "api_hint": "CDS API — era5-single-levels / era5-land",
    },
}


# ---------------------------------------------------------------------------
# USDA / Partner Data Sources
# ---------------------------------------------------------------------------

USDA_DATA_SOURCES: Dict[str, dict] = {
    "USDA Ag Data Commons": {
        "name": "Ag Data Commons",
        "parameter": "soils, crops, climate, land management, phenology, water quality, ecology",
        "use": "ground-based agricultural context complementing NASA satellite observations",
        "api_hint": "https://data.nal.usda.gov/dataset/ag-data-commons",
    },
    "Web Soil Survey (WSS)": {
        "name": "NRCS Web Soil Survey",
        "parameter": "soil maps, properties, drainage classifications, erosion risk, hydrologic ratings",
        "use": "field-specific soil characteristics — organic matter, texture, infiltration, compaction",
        "api_hint": "https://websoilsurvey.nrcs.usda.gov/app/WebSoilSurvey.aspx",
    },
    "CDL / CropScape": {
        "name": "Cropland Data Layer",
        "parameter": "30 m annual cropland classifications (corn, soybeans, cotton, wheat, alfalfa, …)",
        "use": "existing rotations, seasonal change, bare fields, crop suitability, labeled land-cover inputs",
        "api_hint": "https://nassgeodata.gmu.edu/CropScape/",
    },
    "PRISM Climate Data": {
        "name": "PRISM (Oregon State University)",
        "parameter": "daily/monthly/30-year normals — precipitation, temperature, dewpoint, frost/freeze",
        "use": "long-term climate trends, local temperature/rainfall history, stress indicator validation",
        "api_hint": "https://prism.oregonstate.edu",
    },
    "SSURGO / STATSGO2": {
        "name": "NRCS Soil Survey (SSURGO field-scale / STATSGO2 regional)",
        "parameter": "texture, organic matter, drainage class, hydrologic soil group, erosion risk, water-holding",
        "use": "location-specific soil health, erosion potential, infiltration dynamics, crop suitability",
        "api_hint": "https://websoilsurvey.nrcs.usda.gov / Soil Data Access (SDA) API",
    },
    "NAIP": {
        "name": "National Agriculture Imagery Program",
        "parameter": "1 m aerial imagery during U.S. growing season",
        "use": "field boundaries, bare soil periods, crop development, land-management change validation",
        "api_hint": "USDA Geospatial Data Gateway — NAIP imagery",
    },
    "NLCD": {
        "name": "National Land Cover Database (USGS)",
        "parameter": "30 m land-cover/use classifications across multiple decades",
        "use": "farmland, pasture, forest, water, wetlands, development zones near fields",
        "api_hint": "https://www.mrlc.gov",
    },
    "NWIS": {
        "name": "National Water Information System (USGS)",
        "parameter": "groundwater levels, streamflow, river stages, water-quality measurements",
        "use": "irrigation water availability, hydrologic stress, downstream erosion risk",
        "api_hint": "https://waterdata.usgs.gov/nwis",
    },
    "FAO GAEZ": {
        "name": "Global Agro-Ecological Zones",
        "parameter": "agro-climatic suitability for dozens of crops, soil constraints, water availability, yield potential",
        "use": "rotation crop alignment with local climate/soil, global scenario comparison",
        "api_hint": "https://gaez.fao.org",
    },
    "CoCoRaHS": {
        "name": "Community Collaborative Rain, Hail & Snow Network",
        "parameter": "crowd-sourced daily precipitation measurements (North America)",
        "use": "validate satellite rainfall (IMERG), hyper-local extreme rain, irrigation-timing refinement",
        "api_hint": "https://cocorahs.org",
    },
    "USDA AMS Market News": {
        "name": "USDA Agricultural Marketing Service Market News",
        "parameter": "commodity prices, demand trends, market conditions",
        "use": "market viability for proposed rotation crops (farmer-driven constraint)",
        "api_hint": "https://marketnews.usda.gov/mnp",
    },
    "USDA NASS QuickStats": {
        "name": "USDA National Agricultural Statistics Service QuickStats",
        "parameter": "county/state-level yields, planted acreage, production history, crop frequency",
        "use": "model calibration, historical performance, long-term agricultural trends",
        "api_hint": "https://quickstats.nass.usda.gov/api",
    },
    "LANDFIRE": {
        "name": "LANDFIRE (USFS)",
        "parameter": "vegetation type, condition, fuel models, landscape characteristics",
        "use": "ecosystems, perennial cover, tree-crop interactions, microclimates, water flow, erosion",
        "api_hint": "https://landfire.gov",
    },
}


# ---------------------------------------------------------------------------
# USDA Yerel Veri Modelleri (gerçek API entegrasyonu için placeholder)
# ---------------------------------------------------------------------------

@dataclass
class USDASoilData:
    """SSURGO / WSS topoz verileri placeholder."""
    map_unit_symbol: str
    map_unit_name: str
    organic_matter_pct: float
    available_water_capacity: float  # cm/cm
    erosion_factor_k: float
    hydrologic_group: str  # A, B, C, D
    drainage_class: str


@dataclass
class USDAMarketData:
    """USDA AMS / NASS piyasa verileri placeholder."""
    commodity: str
    price_usd_per_ton: float
    trend_30d: str  # "up", "down", "stable"
    demand_index: float  # 0–100


def get_usda_soil_data(lat: float, lon: float) -> USDASoilData:
    """
    SSURGO / WSS verisi placeholder. Gerçek entegrasyon için
    USDA Soil Data Access (SDA) API kullanılır.
    """
    seed = f"{lat:.3f},{lon:.3f}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    n1 = (h % 1000) / 1000.0
    n2 = ((h >> 10) % 1000) / 1000.0
    return USDASoilData(
        map_unit_symbol=f"Mu{int(n1*100):03d}",
        map_unit_name="Loam / Clay Loam",
        organic_matter_pct=round(1.0 + 3.0 * n1, 2),
        available_water_capacity=round(0.10 + 0.15 * n2, 3),
        erosion_factor_k=round(0.20 + 0.40 * n1, 2),
        hydrologic_group="B" if n1 > 0.5 else "C",
        drainage_class="Well drained",
    )


def get_usda_market_data(commodity: str) -> USDAMarketData:
    """
    USDA AMS Market News placeholder. Gerçek entegrasyon için
    USDA Market News API kullanılır.
    """
    import random
    random.seed(hash(commodity))
    price = round(150 + 300 * random.random(), 2)
    trend = random.choice(["up", "down", "stable"])
    demand = round(40 + 60 * random.random(), 1)
    return USDAMarketData(
        commodity=commodity,
        price_usd_per_ton=price,
        trend_30d=trend,
        demand_index=demand,
    )


def get_nasa_data_source_summary() -> Dict[str, int]:
    """NASA ve USDA veri kaynağı sayılarının özeti."""
    return {
        "nasa_count": len(NASA_DATA_SOURCES),
        "usda_count": len(USDA_DATA_SOURCES),
        "total": len(NASA_DATA_SOURCES) + len(USDA_DATA_SOURCES),
    }

@dataclass
class NASASnapshot:
    """One field location with NASA Earth observation values."""
    lat: float
    lon: float
    smap_soil_moisture: float        # m^3/m^3
    gpm_precip_mm: float             # monthly mm
    landsat_ndvi: float              # -1 to 1
    modis_ndvi: float
    ecostress_lst_c: float           # land surface temperature Celsius
    ecostress_et_mm_day: float       # evapotranspiration mm/day
    nasa_power_tmax_c: float         # monthly max temp
    nasa_power_tmin_c: float         # monthly min temp
    srtm_elevation_m: float          # meters
    slope_percent: float             # derived from SRTM
    water_stress_index: float        # 0–1
    heat_stress_index: float         # 0–1
    vegetation_vigor: float          # 0–1
    bare_soil_flag: bool
    grace_tws_anomaly: float = 0.0   # GRACE terrestrial water storage anomaly


@dataclass
class CropProfile:
    name: str
    type_: str
    water_use_mm: float
    n_fixation_kg_ha: float
    root_depth_cm: float
    erosion_protection: float
    organic_matter_input: float
    pest_break_value: float
    forage_value: float
    drought_tolerance: float
    heat_tolerance: float
    frost_tolerance: float
    market_score: float
    growing_days: int


@dataclass
class RotationStrategy:
    name: str
    crops: List[CropProfile]
    description: str
    rationale: str
    soil_health_score: float
    water_efficiency_score: float
    erosion_reduction_score: float
    pest_disruption_score: float
    income_potential_score: float
    climate_resilience_score: float
    benefits: List[str]
    gaps: List[str]
    risks: List[str]
    evidence: str
    local_review_needed: List[str]
    total_score: float = 0.0
    # NASA / USDA veri kaynağı izleme: hangi dataset hangi skora katkı verdi
    data_sources_used: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Crop library
# ---------------------------------------------------------------------------

CROP_LIBRARY: Dict[str, CropProfile] = {
    "Alfalfa": CropProfile("Alfalfa", "forage", 850, 200, 180, 0.9, 0.8, 0.7, 1.0, 0.7, 0.6, 0.7, 0.8, 365),
    "Corn (Maize)": CropProfile("Corn (Maize)", "cereal", 600, 0, 120, 0.4, 0.3, 0.3, 0.6, 0.4, 0.7, 0.3, 0.9, 120),
    "Soybean": CropProfile("Soybean", "legume", 450, 150, 100, 0.5, 0.4, 0.6, 0.4, 0.5, 0.7, 0.3, 0.85, 110),
    "Winter Wheat": CropProfile("Winter Wheat", "cereal", 400, 0, 110, 0.7, 0.5, 0.4, 0.3, 0.6, 0.5, 0.8, 0.8, 240),
    "Clover (Cover Crop)": CropProfile("Clover (Cover Crop)", "cover", 250, 120, 60, 0.95, 0.9, 0.8, 0.6, 0.6, 0.4, 0.7, 0.4, 150),
    "Sorghum": CropProfile("Sorghum", "cereal", 350, 0, 150, 0.6, 0.5, 0.5, 0.7, 0.9, 0.9, 0.4, 0.5, 120),
    "Canola": CropProfile("Canola", "oilseed", 400, 0, 90, 0.5, 0.4, 0.6, 0.2, 0.5, 0.6, 0.5, 0.7, 130),
    "Alfalfa-Grass Mix": CropProfile("Alfalfa-Grass Mix", "forage", 700, 150, 140, 0.92, 0.85, 0.75, 0.9, 0.75, 0.6, 0.75, 0.75, 300),
}


# ---------------------------------------------------------------------------
# NASA data fetchers (mock for prototype; real endpoints ready below)
# ---------------------------------------------------------------------------

def fetch_nasa_snapshot(lat: float, lon: float) -> NASASnapshot:
    """
    Deterministic pseudo-satellite snapshot for a lat/lon.
    Mirrors NASA parameter names and units. Replace with Earthdata/DAAC calls
    for production using the API hints in NASA_DATA_SOURCES.
    """
    seed = f"{lat:.3f},{lon:.3f}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    n1 = (h % 1000) / 1000.0
    n2 = ((h >> 10) % 1000) / 1000.0
    n3 = ((h >> 20) % 1000) / 1000.0

    smap = 0.10 + 0.35 * n1
    gpm = 20 + 180 * n2
    ndvi = 0.2 + 0.6 * n3
    lst = 15 + 25 * n1
    et = 1 + 5 * n2
    tmax = 20 + 20 * n3
    tmin = 0 + 15 * n1
    elev = 200 + 1500 * n2
    slope = 0 + 25 * n3

    water_stress = max(0.0, min(1.0, ((0.45 - smap) / 0.40 + (80 - gpm) / 200.0)) / 2.0)
    heat_stress = max(0.0, min(1.0, (lst - 25) / 20.0))
    vigor = ndvi

    return NASASnapshot(
        lat=lat, lon=lon,
        smap_soil_moisture=smap,
        gpm_precip_mm=gpm,
        landsat_ndvi=ndvi,
        modis_ndvi=ndvi * 0.95 + 0.02,
        ecostress_lst_c=lst,
        ecostress_et_mm_day=et,
        nasa_power_tmax_c=tmax,
        nasa_power_tmin_c=tmin,
        srtm_elevation_m=elev,
        slope_percent=slope,
        water_stress_index=water_stress,
        heat_stress_index=heat_stress,
        vegetation_vigor=vigor,
        bare_soil_flag=vigor < 0.35,
        grace_tws_anomaly=n1 - 0.5,
    )


# ---------------------------------------------------------------------------
# Rotation strategy builder
# ---------------------------------------------------------------------------

def build_strategies(
    snapshot: NASASnapshot,
    current_crops: List[str],
    priorities: Dict[str, float],
    market_local: bool = True,
) -> List[RotationStrategy]:
    """
    Build at least 3 rotation strategies:
      1. Existing rotation (user-supplied)
      2. Soil-health focus (legumes + cover crops)
      3. Water-conservation focus (drought-tolerant + deep-rooted)
    Optionally 4: Market/income focus.
    """
    strat_list: List[RotationStrategy] = []

    existing_crops = [CROP_LIBRARY[c] for c in current_crops if c in CROP_LIBRARY]
    if not existing_crops:
        existing_crops = [CROP_LIBRARY["Corn (Maize)"], CROP_LIBRARY["Soybean"]]

    strat_list.append(_score_strategy(
        name="Mevcut Döndürme (Existing)",
        crops=existing_crops,
        description="İşletmenin bugünkü ürün döndürme modeli. Mevcut uygulama.",
        rationale="Referans strateji; diğer seçeneklerle karşılaştırma tabanı.",
        snapshot=snapshot, priorities=priorities,
    ))

    soil_crops = [CROP_LIBRARY["Clover (Cover Crop)"], CROP_LIBRARY["Soybean"],
                  CROP_LIBRARY["Alfalfa-Grass Mix"]]
    strat_list.append(_score_strategy(
        name="Toprak Sağlığı Odaklı",
        crops=soil_crops,
        description="Azot fixes eden baklagiller + örtü bitkileri ile organik materiyi artıran döndürme.",
        rationale="Yüksek N-fixation ve örtü oranı ile erozyonu azaltır, toprağı zenginleştirir.",
        snapshot=snapshot, priorities=priorities,
    ))

    water_crops = [CROP_LIBRARY["Sorghum"], CROP_LIBRARY["Winter Wheat"],
                   CROP_LIBRARY["Clover (Cover Crop)"]]
    strat_list.append(_score_strategy(
        name="Su Tasarrufu Odaklı",
        crops=water_crops,
        description="Düşük su tüketimi, Derin köklü ve kurak toleranslı bitkilerle sulama ihtiyacını azaltan model.",
        rationale="SMAP/GPM verilerine göre su stresi yüksek olduğu sırada düşük su ihtiyacı olan bitkilere geçiş.",
        snapshot=snapshot, priorities=priorities,
    ))

    market_crops = [CROP_LIBRARY["Alfalfa"], CROP_LIBRARY["Corn (Maize)"],
                    CROP_LIBRARY["Canola"]]
    strat_list.append(_score_strategy(
        name="Gelir ve Pazar Odaklı",
        crops=market_crops,
        description="Yüksek pazar değeri olan kuluçka (alfalfa), mısır ve canola kombinasyonu ile ek gelir modeli.",
        rationale="USDA AMS Market News ve NASS verilerine dayalı yerel talip odaklı ürün seçimi.",
        snapshot=snapshot, priorities=priorities,
    ))

    return strat_list


def _score_strategy(
    name: str,
    crops: List[CropProfile],
    description: str,
    rationale: str,
    snapshot: NASASnapshot,
    priorities: Dict[str, float],
) -> RotationStrategy:
    """Aggregate crop profiles into strategy scores weighted by farmer priorities."""
    if not crops:
        crops = [CROP_LIBRARY["Corn (Maize)"]]

    n = len(crops)
    avg_water = sum(c.water_use_mm for c in crops) / n
    avg_n = sum(c.n_fixation_kg_ha for c in crops) / n
    avg_root = sum(c.root_depth_cm for c in crops) / n
    avg_ero = sum(c.erosion_protection for c in crops) / n
    avg_om = sum(c.organic_matter_input for c in crops) / n
    avg_pest = sum(c.pest_break_value for c in crops) / n
    avg_forage = sum(c.forage_value for c in crops) / n
    avg_drought = sum(c.drought_tolerance for c in crops) / n
    avg_heat = sum(c.heat_tolerance for c in crops) / n
    avg_frost = sum(c.frost_tolerance for c in crops) / n
    avg_market = sum(c.market_score for c in crops) / n

    w_soil = priorities.get("soil_health", 0.5)
    w_water = priorities.get("water_conservation", 0.5)
    w_income = priorities.get("income", 0.5)
    w_erosion = priorities.get("erosion_control", 0.5)

    soil_score = (
        0.35 * avg_om * 100 +
        0.25 * avg_n / 200 * 100 +
        0.20 * avg_ero * 100 +
        0.20 * (1.0 - snapshot.water_stress_index) * 100
    )
    water_score = (
        0.40 * (1.0 - avg_water / 900) * 100 +
        0.30 * avg_drought * 100 +
        0.30 * (1.0 - snapshot.water_stress_index) * 100
    )
    erosion_score = (
        0.50 * avg_ero * 100 +
        0.30 * avg_root / 200 * 100 +
        0.20 * (1.0 - snapshot.slope_percent / 30) * 100
    )
    erosion_score = max(0, min(100, erosion_score))
    pest_score = avg_pest * 100
    income_score = (
        0.50 * avg_market * 100 +
        0.30 * avg_forage * 100 +
        0.20 * (1.0 if avg_n > 50 else 0.5) * 100
    )
    resilience_score = (
        0.30 * avg_drought * 100 +
        0.30 * avg_heat * 100 +
        0.20 * avg_frost * 100 +
        0.20 * (1.0 - snapshot.heat_stress_index) * 100
    )
    total = (
        w_soil * soil_score +
        w_water * water_score +
        w_income * income_score +
        w_erosion * erosion_score
    ) / max(w_soil + w_water + w_income + w_erosion, 0.01)

    benefits = []
    if avg_n > 50:
        benefits.append("Azot fixesesi sayesinde gübre maliyeti düşer.")
    if avg_ero > 0.7:
        benefits.append("Yoğun örtü bitkisi ile rüzgar ve su erozyonu azaltılır.")
    if avg_water < 500:
        benefits.append("Düşük su tüketimi ile sulama maliyeti ve su stresi azalır.")
    if avg_drought > 0.7:
        benefits.append("Kuraklığa dayanıklılık sağlar, yıllardaki verim kaybı sınırlanır.")
    if avg_market > 0.7:
        benefits.append("Yerel pazarda kolay satış ve iyi gelir potansiyeli.")
    if avg_forage > 0.7:
        benefits.append("Hayvancılık için kuluçka/kaynağ sağlar.")
    if not benefits:
        benefits.append("Dengeli bir döndürme modeli sunar.")

    gaps = []
    if snapshot.bare_soil_flag:
        gaps.append("Uydu verilerine göre bestimmte dönemlerde toprağın açık kalması tespit edildi; örtü bitkisi önerilir.")
    if snapshot.water_stress_index > 0.6:
        gaps.append("Yüksek su stresi bölgesi; sulama planı ve su kaynağı denetimi gerekli.")
    if snapshot.slope_percent > 15:
        gaps.append("Eğimli arazi; işleme yöntemi ve bitki örtüsüyle erozyon kontrolü zorunlu.")
    if not gaps:
        gaps.append("Yerel topraktan örnek alınarak gerekli araçlar ve ekin tarihi onaylanmalı.")

    risks = []
    if avg_water > 600 and snapshot.gpm_precip_mm < 100:
        risks.append("Yağış ağırlıklı yüksek su tüketimi bitkisi yield riski oluşturur.")
    if avg_frost < 0.4 and snapshot.nasa_power_tmin_c < 5:
        risks.append("Düşük don toleranslı bitkiler kışta zarar görebilir.")
    if avg_market < 0.4:
        risks.append("Pazar talebi düşükse stoklanma ve fiyat düşüşü riski.")
    if not risks:
        risks.append("Yerel zirai danışman onayı ile uygulanmalı; deneysel parça önerilir.")

    evidence = (
        f"NASA uydu referansı: SMAP toprak nemi {snapshot.smap_soil_moisture:.2f} m³/m³, "
        f"GPM aylık yağış {snapshot.gpm_precip_mm:.0f} mm, "
        f"Landsat NDVI {snapshot.landsat_ndvi:.2f}, "
        f"ECOSTRESS LST {snapshot.ecostress_lst_c:.1f}°C. "
        f"Bu koşullarda strategi '{name}' için tahmini uygunluk skoru {total:.0f}/100."
    )

    local_review = [
        "Yerel zirai mühendis / tarım danışmanı onayı",
        "Toprak testi (makro ve mikro elementler)",
        "Sulama altyapısı ve su hakkı kontrolü",
        "Yerel pazar fiyatı ve depolama imkanı",
    ]

    # NASA / USDA veri kaynağı izleme: hangi dataset hangi skora katkı verdi
    data_sources = []
    if snapshot.smap_soil_moisture is not None:
        data_sources.append("SMAP (toprak nemi)")
    if snapshot.gpm_precip_mm is not None:
        data_sources.append("GPM/IMERG (yağış)")
    if snapshot.landsat_ndvi is not None:
        data_sources.append("Landsat/MODIS (NDVI, bitki sağlığı)")
    if snapshot.ecostress_lst_c is not None:
        data_sources.append("ECOSTRESS (yüzey sıcaklığı, evapotranspirasyon)")
    if snapshot.nasa_power_tmax_c is not None:
        data_sources.append("NASA POWER (sıcaklık, don riski)")
    if snapshot.srtm_elevation_m is not None:
        data_sources.append("SRTM (eşya, eğim, erozyon)")
    if snapshot.grace_tws_anomaly is not None:
        data_sources.append("GRACE/GRACE-FO (su depolama anomali)")
    # USDA kaynakları (veri kaynağı olarak işaretleniyor)
    data_sources.append("USDA SSURGO (toprak özellikleri)")
    data_sources.append("USDA AMS Market News (piyasa fiyatları)")
    data_sources.append("USDA NASS QuickStats (verim istatistikleri)")

    return RotationStrategy(
        name=name,
        crops=crops,
        description=description,
        rationale=rationale,
        soil_health_score=round(soil_score, 1),
        water_efficiency_score=round(water_score, 1),
        erosion_reduction_score=round(erosion_score, 1),
        pest_disruption_score=round(pest_score, 1),
        income_potential_score=round(income_score, 1),
        climate_resilience_score=round(resilience_score, 1),
        benefits=benefits,
        gaps=gaps,
        risks=risks,
        evidence=evidence,
        local_review_needed=local_review,
        total_score=round(total, 1),
        data_sources_used=data_sources,
    )


def export_report_text(strategies: List[RotationStrategy], snapshot: NASASnapshot) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("FIELD SHIFT — NASA SPACE APPS 2026")
    lines.append("Ürün Döndürme Karar Destek Raporu")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Konum: {snapshot.lat:.4f}, {snapshot.lon:.4f}")
    lines.append(f"SMAP Toprak Nemi: {snapshot.smap_soil_moisture:.3f} m³/m³")
    lines.append(f"GPM Aylık Yağış: {snapshot.gpm_precip_mm:.0f} mm")
    lines.append(f"Landsat NDVI: {snapshot.landsat_ndvi:.2f}")
    lines.append(f"ECOSTRESS Yüzey Sıcaklığı: {snapshot.ecostress_lst_c:.1f} °C")
    lines.append(f"SRTM Eşya Yüksekliği: {snapshot.srtm_elevation_m:.0f} m")
    lines.append("")
    lines.append("-" * 70)
    lines.append("STRATEJİ KARŞILAŞTIRMASI")
    lines.append("-" * 70)
    for s in strategies:
        lines.append(f"\n>>> {s.name}  (Toplam: {s.total_score}/100)")
        lines.append(f"   Açıklama: {s.description}")
        lines.append(f"   Neden önerildi: {s.rationale}")
        lines.append(f"   Bitkiler: {', '.join(c.name for c in s.crops)}")
        lines.append(f"   Toprak Sağlığı: {s.soil_health_score}  Su Verimliliği: {s.water_efficiency_score}")
        lines.append(f"   Erosion Azaltma: {s.erosion_reduction_score}  Zarar Kırıcı Etki: {s.pest_disruption_score}")
        lines.append(f"   Gelir Potansiyeli: {s.income_potential_score}  İklim Dayanışma: {s.climate_resilience_score}")
        lines.append(f"   Veri Kaynakları: {', '.join(s.data_sources_used)}")
        lines.append(f"   Kanıt: {s.evidence}")
        lines.append("   Faydalar: " + "; ".join(s.benefits))
        lines.append("   Bilgi Boşlukları: " + "; ".join(s.gaps))
        lines.append("   Riskler: " + "; ".join(s.risks))
        lines.append("   Yerel İnceleme Gerekli: " + "; ".join(s.local_review_needed))
    lines.append("")
    lines.append("NOT: Bu araç yerel zirai uzmanlaşmanın yerini almaz; destek niteliktedir.")
    lines.append("=" * 70)
    return "\n".join(lines)