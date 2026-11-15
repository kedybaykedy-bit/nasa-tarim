import json
import os
import math

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

LANG = {
    "tr": {
        "strategies": {
            "toprak_sagligi": "Toprak Sağlığı Odaklı",
            "su_tasarrufu": "Su Tasarruflu",
            "mevcut_koruma": "Mevcut Rotasyonu Koru",
        },
        "groups": {"bahar": "Bahar", "yaz": "Yaz", "sonbahar": "Sonbahar", "kis": "Kış"},
        "water_need": {"düşük": "Düşük", "orta": "Orta", "yüksek": "Yüksek"},
        "soil_effect": {"iyileştirici": "İyileştirici", "nötr": "Nötr", "tüketici": "Tüketici"},
        "risk_frost": "Don riski", "risk_heat": "Isı dalgası riski", "risk_drought": "Kuraklık riski",
        "advisor_warn": "Bu araç destekleyici bir öneri sunar; final karar çiftçi ve yerel tarım uzmanlığına bırakılır.",
        "nasa_sources": "NASA Veri Kaynakları: POWER (sıcaklık, yağış, güneş, rüzgar) · SMAP (toprak nemi) · GPM (yağış) · Landsat (NDVI) · ECOSTRESS (ısı stresi) · SRTM (eşya yüksekliği)",
        "best_crop": "En iyi bitki", "strategy_score": "Strateji skoru", "crop_score": "Bitki skoru",
        "recommended_crop": "Önerilen bitki", "why": "Neden", "evidence": "Kanıt", "benefits": "Faydalar",
        "risks": "Riskler", "gaps": "Bilgi eksikliği", "rotation_advice": "Rota önerisi",
        "current_crop": "Mevcut bitki", "scenario_label": "Senaryo",
        "scenario_precip": "Yağış değişimi (%)", "scenario_temp": "Sıcaklık değişimi (°C)",
        "constraints": "Çiftçi kısıtları", "irrigation": "Sulama", "equipment": "Ekipman", "market": "Pazar tercihi",
        "stress_calendar": "Stres Takvimi", "month": "Ay", "temp_stress": "Sıcaklık stresi",
        "water_stress": "Su stresi", "ndvi_proxy": "Bitki gelişimi (NDVI proxy)",
        "frost_warning": "⚠ Bu dönemde don riski yüksek — erken tohumlama/koruma önlemi alın.",
        "heat_warning": "⚠ Bu dönemde ısı dalgası riski yüksek — sulama/ölçme planlayın.",
        "drought_warning": "⚠ Bu dönemde kuraklık riski yüksek — su tasarruflu bitki tercih edin.",
        "bare_field_warning": "⚠ Bu dönemde tarla boş kalma riski yüksek — örtü bitki önerilir.",
        "uncertainty_low": "Düşük belirsizlik", "uncertainty_mid": "Orta belirsizlik", "uncertainty_high": "Yüksek belirsizlik",
        "lang_switch": "EN",
    },
    "en": {
        "strategies": {
            "toprak_sagligi": "Soil Health Focused",
            "su_tasarrufu": "Water Saving",
            "mevcut_koruma": "Keep Current Rotation",
        },
        "groups": {"bahar": "Spring", "yaz": "Summer", "sonbahar": "Autumn", "kis": "Winter"},
        "water_need": {"düşük": "Low", "orta": "Medium", "yüksek": "High"},
        "soil_effect": {"iyileştirici": "Improving", "nötr": "Neutral", "tüketici": "Depleting"},
        "risk_frost": "Frost risk", "risk_heat": "Heat wave risk", "risk_drought": "Drought risk",
        "advisor_warn": "This tool provides supportive suggestions; final decisions rest with the farmer and local agronomists.",
        "nasa_sources": "NASA Data Sources: POWER (temp, precip, solar, wind) · SMAP (soil moisture) · GPM (precip) · Landsat (NDVI) · ECOSTRESS (heat stress) · SRTM (elevation)",
        "best_crop": "Best crop", "strategy_score": "Strategy score", "crop_score": "Crop score",
        "recommended_crop": "Recommended crop", "why": "Why", "evidence": "Evidence", "benefits": "Benefits",
        "risks": "Risks", "gaps": "Knowledge gaps", "rotation_advice": "Rotation advice",
        "current_crop": "Current crop", "scenario_label": "Scenario",
        "scenario_precip": "Precipitation change (%)", "scenario_temp": "Temperature change (°C)",
        "constraints": "Farmer constraints", "irrigation": "Irrigation", "equipment": "Equipment", "market": "Market preference",
        "stress_calendar": "Stress Calendar", "month": "Month", "temp_stress": "Temperature stress",
        "water_stress": "Water stress", "ndvi_proxy": "Crop growth (NDVI proxy)",
        "frost_warning": "⚠ High frost risk this period — consider early planting/protection.",
        "heat_warning": "⚠ High heat wave risk this period — plan irrigation/monitoring.",
        "drought_warning": "⚠ High drought risk this period — prefer water-saving crops.",
        "bare_field_warning": "⚠ High bare-field risk this period — consider cover crop.",
        "uncertainty_low": "Low uncertainty", "uncertainty_mid": "Medium uncertainty", "uncertainty_high": "High uncertainty",
        "lang_switch": "TR",
    },
}


def load_crops():
    with open(os.path.join(DATA_DIR, "crops.json"), encoding="utf-8") as f:
        return json.load(f)


def clima_uygunluk(ort, crop, ekstra=None):
    """0-100 arası klima uygunluk skoru. SMAP/SRTM verileri varsa düzeltme uygular."""
    t_min, t_max = crop["sıcaklık"]
    p_min, p_max = crop["yağış"]
    s_min, s_max = crop["güneş"]
    t = ort["sıcaklık_C"]; p = ort["yağış_mm_gun"]; s = ort["güneş_MJ_m2_gun"]

    def skalala(deger, d_min, d_max):
        if d_max == d_min:
            return 100 if deger == d_min else 0
        if deger < d_min:
            return max(0, 70 - (d_min - deger) * 30)
        if deger > d_max:
            return max(0, 70 - (deger - d_max) * 30)
        orta = (d_min + d_max) / 2
        yaricap = (d_max - d_min) / 2
        uzaklik = abs(deger - orta) / yaricap
        return 70 + 30 * (1 - uzaklik)

    st = skalala(t, t_min, t_max)
    sp = skalala(p, p_min, p_max)
    ss = skalala(s, s_min, s_max)
    skor = round((st * 0.5 + sp * 0.3 + ss * 0.2), 1)

    # SRTM elevasyonu: yüksek taraflarda kurak toleranslı bitkilere bonus
    if ekstra and ekstra.get("srtm", {}).get("available"):
        elev = ekstra["srtm"].get("elevation_m") or 0
        if elev > 800 and crop["su_ihtiyacı"] == "düşük":
            skor = min(100, skor + 5)
        elif elev > 1200 and crop["toprak_etkisi"] == "tüketici":
            skor = max(0, skor - 5)

    return skor


def si_trend_analiz(aylik_veri, ort_s):
    """NASA POWER aylık verisinden sıcaklık ve yağış trendi (OLS eğim + R² + son yıl anomali)."""
    L = None  # dil sonradan eklenir
    if not aylik_veri or "properties" not in aylik_veri:
        return {
            "sicaklik_trend": {"slope": 0.0, "r2": 0.0, "anomali": None},
            "yagis_trend": {"slope": 0.0, "r2": 0.0, "anomali": None},
            "guven_duzeyi": 0,
            "yorumlama": "Yeterli aylık veri yok; trend hesaplanamadı.",
            "yillar": [],
        }

    pdata = aylik_veri["properties"].get("parameter", {})
    t_vals = pdata.get("T2M", {})
    p_vals = pdata.get("PRECTOTCORR", {})

    years = sorted({int(k[:4]) for k in list(t_vals.keys()) + list(p_vals.keys())})
    if len(years) < 2:
        return {
            "sicaklik_trend": {"slope": 0.0, "r2": 0.0, "anomali": None},
            "yagis_trend": {"slope": 0.0, "r2": 0.0, "anomali": None},
            "guven_duzeyi": 0,
            "yorumlama": "En az 2 yıllık veri gerekli; trend hesaplanamadı.",
            "yillar": years,
        }

    def ols(series):
        # series: {YYYYMM: value}
        xs = []
        ys = []
        for k, v in series.items():
            if isinstance(v, (int, float)) and v >= 0:
                xs.append(float(k[:4]) + (int(k[4:6]) - 1) / 12.0)
                ys.append(float(v))
        if len(xs) < 2:
            return 0.0, 0.0, None
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        slope = sxy / sxx if sxx != 0 else 0.0
        syy = sum((y - my) ** 2 for y in ys)
        r2 = (sxy ** 2) / (sxx * syy) if (sxx * syy) != 0 else 0.0
        # Son değerden anomali
        last_x = max(xs)
        last_y = ys[xs.index(last_x)]
        pred = mx + slope * (last_x - mx)
        resid = last_y - pred
        std = math.sqrt(syy / (n - 2)) if n > 2 else 0.0
        z = resid / std if std > 0 else 0.0
        anomaly = {"z": round(z, 2), "anomaly": abs(z) > 1.5,
                   "direction": "above" if z > 1.5 else ("below" if z < -1.5 else "normal")}
        return round(slope, 4), round(r2, 3), anomaly

    t_slope, t_r2, t_anom = ols(t_vals)
    p_slope, p_r2, p_anom = ols(p_vals)

    guven = round(min(100, max(0, ((t_r2 + p_r2) / 2) * 100)), 1)
    if guven >= 60:
        yorum = "Trendler istatistiksel olarak anlamlıdır; decennial planlama için güvenilir."
    elif guven >= 30:
        yorum = "Trendler orta seydede; yerel gözlemle desteklenmelidir."
    else:
        yorum = "Trendler zayıf; tek yılNASA verisine dayanılarak yorumlanmalıdır."

    return {
        "sicaklik_trend": {"slope": t_slope, "r2": t_r2, "anomali": t_anom},
        "yagis_trend": {"slope": p_slope, "r2": p_r2, "anomali": p_anom},
        "guven_duzeyi": guven,
        "yorumlama": yorum,
        "yillar": years,
    }


def bare_field_tespit(stres_takvimi):
    """12 aylık stres takviminden boş tarla riskli ayları belirler (yüksek stres + düşük yağış)."""
    riskli = []
    for gun in stres_takvimi:
        if gun["stres"] in ("yüksek", "kurak") and gun["yağış"] < 1.0:
            riskli.append(gun["ay"])
    return riskli


def belirsizlik_degerlendir(ekstra):
    """Kaç NASA kaynağı gerçek veri verdiğine göre belirsizlik seviyesi."""
    sayac = 1  # POWER her zaman var
    for kaynak in ("smap", "ecostress", "landsat_ndvi", "srtm", "gpm"):
        if ekstra.get(kaynak, {}).get("available"):
            sayac += 1
    if sayac >= 5:
        return "düşük"
    if sayac >= 3:
        return "orta"
    return "yüksek"


def strategi_skoru(ort, oncelikler, crop, onceki, constraints, crops_global, ekstra=None):
    skor = clima_uygunluk(ort, crop, ekstra)

    if constraints:
        if constraints.get("irrigation") == "yok":
            if crop["su_ihtiyacı"] == "yüksek":
                skor *= 0.6
            elif crop["su_ihtiyacı"] == "orta":
                skor *= 0.85
        if constraints.get("equipment") == "sınırlı":
            if crop["grup"] == "yazlık" and crop["toprak_etkisi"] == "tüketici":
                skor *= 0.8
        if constraints.get("market") == "düşük" and crop.get("fiyat_tl_kg", 0) > 30:
            skor *= 0.85

    if onceki and onceki in crops_global:
        onceki_etki = crops_global[onceki].get("toprak_etkisi", "nötr")
        if onceki_etki == "tüketici" and crop["toprak_etkisi"] == "iyileştirici":
            skor += 10
        elif onceki_etki == "tüketici" and crop["toprak_etkisi"] == "tüketici":
            skor -= 15

    if oncelikler:
        if oncelikler.get("su_tasarrufu") and crop["su_ihtiyacı"] == "düşük":
            skor += 8
        if oncelikler.get("verim") and crop.get("verim_kg_donum", 0) > 1000:
            skor += 8
        if oncelikler.get("pazar_geliri") and crop.get("fiyat_tl_kg", 0) > 25:
            skor += 6

    # SMAP土壌 nemi varsa su-stresli bitkilere ceza
    if ekstra and ekstra.get("smap", {}).get("available"):
        if crop["su_ihtiyacı"] == "yüksek":
            skor = max(0, skor - 5)

    return round(min(100, max(0, skor)), 1)


STRATEJILER = {
    "toprak_sagligi": {
        "anahtar": "toprak_sagligi",
        "ad_tr": "Toprağı Dinlendiren ve Güçlendiren Ekim",
        "ad_en": "Soil Health & Regeneration Rotation",
        "grup_vurgu": ["iyileştirici", "nötr"],
        "aciklama_tr": "Toprağı yormayan, nohut ve mercimek gibi baklagillerle toprağa doğal gübre bırakan ve tarlayı dinlendiren yol.",
        "aciklama_en": "Rotation emphasizing nitrogen-fixers and cover crops to rest soil and reduce erosion.",
        "neden_tr": "NASA POWER yağış ve sıcaklık verilerine göre bu mevsimde tarlayı yormayan baklagiller (nohut, mercimek) ekilirse, toprağa doğal gübre bırakır ve seneye ekeceğiniz buğdayın verimini artırır. SMAP土壌 nemi düşükse su tasarruflu baklagiller tercih edilir.",
        "neden_en": "Based on NASA POWER precipitation and temperature data, nitrogen-fixers (chickpea, pea) and cover crops are placed in low water-stress seasons to increase soil organic matter. SMAP soil moisture guides water-saving legume selection.",
        "kanit_tr": "Tarımsal araştırmalar, nohut ve mercimeğin dekara yaklaşık 4-6 kg saf doğal azot (gübre) kazandırdığını kanıtlamaktadır. NASA SMAP土壌 nemi ve POWER yağış verileri bunu desteklemektedir.",
        "kanit_en": "NASA SMAP soil moisture and POWER precipitation data; agronomic literature shows nitrogen-fixers contribute ~40-60 kg/ha N.",
        "faydalar_tr": ["Seneye atacağınız gübre masrafı düşer", "Toprağın su tutma gücü artar", "Tarlanın bereketi uzun yıllar korunur"],
        "faydalar_en": ["Soil organic matter increases", "Erosion risk decreases", "Chemical fertilizer need drops", "Water retention improves"],
        "riskler_tr": ["İlk hasatta buğday kadar hızlı nakit getirmeyebilir", "Tüccar/pazar fiyatı mevsime göre oynayabilir"],
        "riskler_en": ["May reduce short-term income", "Local market demand may be limited", "Expert advisory may be needed"],
        "bilgi_eksikligi_tr": "Toprak yapınıza göre tohum seçimi için ilçe tarıma danışın.",
        "bilgi_eksikligi_en": "Local soil test and agronomist approval required.",
    },
    "su_tasarrufu": {
        "anahtar": "su_tasarrufu",
        "ad_tr": "Susuzluğa Dayanıklı (Az Masraflı) Ekim",
        "ad_en": "Water Saving & Drought Hardy Rotation",
        "grup_vurgu": ["düşük", "orta"],
        "aciklama_tr": "Az su isteyen, kuraklığa kafa tutan nohut, arpa veya mercimek ile su ve elektrik/mazot faturasını düşüren yol.",
        "aciklama_en": "Rotation minimizing water use with low-water, drought-tolerant crops.",
        "neden_tr": "Bölgenizin NASA yağış ve sıcaklık geçmişi kuraklık eğilimi gösterdiği için, suyu az tüketen ve sıcağa dayanıklı çeşitler önerildi. SMAP土壌 nemi mevcutsa su açığı aylarında bu bitkilere öncelik verilir.",
        "neden_en": "Based on NASA POWER low precipitation and high temperature data, low-water crops (lentil, chickpea, barley) are preferred. SMAP soil moisture flags dry months for water-saving crop priority.",
        "kanit_tr": "NASA yağış ölçümleri ve tarla denemelerine göre nohut ve arpa, mısır veya pamuğa kıyasla %40-60 daha az suya ihtiyaç duyar.",
        "kanit_en": "NASA GPM precipitation and POWER temperature data; studies show lentil and chickpea use 30-50% less water than cereals.",
        "faydalar_tr": ["Sulama ve elektrik/mazot masrafı yarı yarıha düşer", "Kurak yılda bile ürün tarlada yanmaz", "Kuyu suyunu tüketmez"],
        "faydalar_en": ["Water use reduced 30-50%", "Drought resilience increases", "Irrigation cost drops"],
        "riskler_tr": ["Sulu mısır kadar tonaj getirisi yüksek olmayabilir"],
        "riskler_en": ["Yield may be lower", "Market demand may vary", "Soil salinity risk"],
        "bilgi_eksikligi_tr": "Kuru tarım tohum desteği için bölgenizdeki kooperatife başvurun.",
        "bilgi_eksikligi_en": "Local irrigation infrastructure and water rights check required.",
    },
    "mevcut_koruma": {
        "anahtar": "mevcut_koruma",
        "ad_tr": "Alışılmış Düzen (Düşük Riskli Yol)",
        "ad_en": "Keep Current Rotation",
        "grup_vurgu": None,
        "aciklama_tr": "Mevcut alışkanlığınızı ve ekipmanınızı bozmadan, en az riskle devam edebileceğiniz güvenli yol.",
        "aciklama_en": "Minimum-change, low-risk rotation suited to current crop.",
        "neden_tr": "NASA iklim verileri bölgenizde olağanüstü bir risk göstermediği için bildiğiniz ve elinizde alet-edevatı hazır olan döngüyü sürdürebilirsiniz.",
        "neden_en": "If NASA POWER climate data matches current crop's temp/precip range, continue current rotation without change risk.",
        "kanit_tr": "NASA geçmiş 20 yıllık verilerinde bu bölgede standart döngünün ortalama hava şartlarında tutarlı sonuç vermesi.",
        "kanit_en": "NASA POWER temperature and precipitation data falling within current crop's ideal range.",
        "faydalar_tr": ["Alışık olduğunuz düzen, acemilik çekilmez", "Yeni makine/ekipman masrafı çıkarmaz", "Tüccarı ve pazarı bellidir"],
        "faydalar_en": ["No change risk", "Existing equipment and knowledge base", "Quick to implement"],
        "riskler_tr": ["Üst üste aynı ürün ekilirse toprak yorulur ve kök hastalıkları artabilir"],
        "riskler_en": ["Soil fatigue may increase long-term", "Pest/disease cycles may persist", "New opportunities may be missed"],
        "bilgi_eksikligi_tr": "Aynı tarlaya 2 yıldan fazla üst üste aynı ürünü ekmemeye dikkat edin.",
        "bilgi_eksikligi_en": "Soil tests and long-term yield records required.",
    },
}


def get_str_text(key, lang):
    s = STRATEJILER[key]
    return s.get(f"{key.split('_')[-1]}_{lang}") or s.get(f"ad_{lang}") or s["ad_tr"]


def apply_scenario(ort, scenario):
    if not scenario:
        return ort
    yeni = dict(ort)
    precip_change = scenario.get("precip_change_pct", 0) / 100.0
    temp_change = scenario.get("temp_change_c", 0)
    yeni["yağış_mm_gun"] = round(yeni["yağış_mm_gun"] * (1 + precip_change), 2)
    yeni["sıcaklık_C"] = round(yeni["sıcaklık_C"] + temp_change, 2)
    return yeni


def apply_constraints(crops, constraints):
    if not constraints:
        return crops
    sonuc = {}
    for key, c in crops.items():
        if constraints.get("su_ihtiyaci") and c["su_ihtiyacı"] != constraints["su_ihtiyaci"]:
            continue
        if constraints.get("toprak_etkisi") and c["toprak_etkisi"] != constraints["toprak_etkisi"]:
            continue
        sonuc[key] = c
    return sonuc or crops


def stres_takvimi(ort, lang, aylik_veri=None):
    L = LANG[lang]
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    takvim = []
    for i, ay in enumerate(aylar, start=1):
        t = ort["sıcaklık_C"]
        p = ort["yağış_mm_gun"]
        if aylik_veri and "properties" in aylik_veri:
            pdata = aylik_veri["properties"].get("parameter", {})
            t_vals = pdata.get("T2M", {})
            p_vals = pdata.get("PRECTOTCORR", {})
            t = t_vals.get(str(i), t)
            p = p_vals.get(str(i), p)
        stres = "düşük"
        if t > 32:
            stres = "yüksek"
        elif t < 2:
            stres = "don"
        elif p < 1:
            stres = "kurak"
        takvim.append({
            "ay": ay,
            "sıcaklık": round(t, 1),
            "yağış": round(p, 2),
            "stres": stres,
            "uyarı": {
                "don": L["frost_warning"],
                "yüksek": L["heat_warning"],
                "kurak": L["drought_warning"],
            }.get(stres, ""),
        })
    return takvim


def risk_uyarilari(ort, lang):
    L = LANG[lang]
    uyarilar = []
    if ort["sıcaklık_C"] > 28:
        uyarilar.append(L["heat_warning"])
    if ort["yağış_mm_gun"] < 1.5:
        uyarilar.append(L["drought_warning"])
    if ort["sıcaklık_C"] < 8:
        uyarilar.append(L["frost_warning"])
    return uyarilar


def rotasyon_dizisi_uret(tum_bitkiler, crops, gecmis_list=None, lang="tr"):
    gecmis_list = gecmis_list or []
    son_etki = "nötr"
    if gecmis_list:
        son_etki = crops[gecmis_list[-1]].get("toprak_etkisi", "nötr")

    y1_candidates = [b for b in tum_bitkiler if b["toprak_etkisi"] == "iyileştirici"] or tum_bitkiler
    y1 = y1_candidates[0]

    y2_candidates = [b for b in tum_bitkiler if b["su_ihtiyacı"] in ("düşük", "orta") and b["anahtar"] != y1["anahtar"]]
    y2 = y2_candidates[0] if y2_candidates else (tum_bitkiler[1] if len(tum_bitkiler) > 1 else tum_bitkiler[0])

    y3_candidates = [b for b in tum_bitkiler if b["anahtar"] not in (y1["anahtar"], y2["anahtar"])]
    y3 = y3_candidates[0] if y3_candidates else tum_bitkiler[-1]

    rolleri = {
        1: ("toprağı dinlendirici baklagil", "soil-restoring nitrogen fixer",
            "Toprağa azot bırakarak sonraki yıllar için bereketi hazırlar.",
            "Adds nitrogen to soil, preparing fertility for following years."),
        2: ("su tasarruflu ve verim odaklı", "water-saving and yield-focused",
            "Kuraklık riskini azaltırken verimi korur.",
            "Reduces drought risk while maintaining yield."),
        3: ("ekonomi ve toprağe müteakip karar", "economy and soil compatibility",
            "Pazar fiyatı ve toprağın dayanım bakımdan dengeli seçim.",
            "Balanced choice for market price and soil resilience."),
    }

    plan = []
    for idx, b in enumerate([y1, y2, y3], start=1):
        rol_tr, rol_en, aciklama_tr, aciklama_en = rolleri[idx]
        plan.append({
            "yil": idx,
            "bitki": b["bitki"],
            "anahtar": b["anahtar"],
            "skor": b["skor"],
            "rol": rol_tr,
            "rol_en": rol_en,
            "aciklama": aciklama_tr,
            "aciklama_en": aciklama_en,
            "verim_kg": b["verim_kg"],
            "fiyat_tl": b["fiyat_tl"],
            "gelir_tl": round(b["verim_kg"] * b["fiyat_tl"], 2),
        })
    return plan


def rotasyon_oneri(ort, oncelikler, mevcut=None, onceki=None, gecmis_bitkiler=None,
                   aylik=None, ekstra=None, scenario=None, constraints=None, lang="tr"):
    L = LANG[lang]
    if ort is None:
        ort = {}
    if ekstra is None:
        ekstra = {}
    crops = load_crops()

    ort_s = apply_scenario(ort, scenario)
    crops_c = apply_constraints(crops, constraints)

    tum_bitkiler = []
    for anahtar, c in crops_c.items():
        skor = strategi_skoru(ort_s, oncelikler, c, onceki, constraints, crops, ekstra)
        tum_bitkiler.append({
            "bitki": c["ad"],
            "anahtar": anahtar,
            "grup": c["grup"],
            "skor": skor,
            "su_ihtiyacı": c["su_ihtiyacı"],
            "toprak_etkisi": c["toprak_etkisi"],
            "verim_kg": c.get("verim_kg_donum", 300),
            "fiyat_tl": c.get("fiyat_tl_kg", 15.0),
            "not": c.get("not", ""),
        })
    tum_bitkiler.sort(key=lambda x: x["skor"], reverse=True)

    gecmis_list = [g for g in (gecmis_bitkiler or []) if g in crops]
    if onceki and onceki in crops:
        gecmis_list.append(onceki)
    if gecmis_list:
        son_etki = crops[gecmis_list[-1]].get("toprak_etkisi", "nötr")
        if son_etki in ("tüketici", "nötr"):
            for b in tum_bitkiler:
                if b["toprak_etkisi"] == "iyileştirici":
                    b["skor"] = min(100, b["skor"] + 8)
            tum_bitkiler.sort(key=lambda x: x["skor"], reverse=True)

    rotasyon_plani = rotasyon_dizisi_uret(tum_bitkiler, crops, gecmis_list=gecmis_list, lang=lang)

    ts_secim = [b for b in tum_bitkiler if b["toprak_etkisi"] in ("iyileştirici", "nötr")]
    ts_bitki = ts_secim[0] if ts_secim else tum_bitkiler[0]
    ts = dict(STRATEJILER["toprak_sagligi"])
    ts["bitki"] = ts_bitki["bitki"]
    ts["anahtar"] = ts_bitki["anahtar"]
    ts["skor"] = round((ts_bitki["skor"] + 10) / 2, 1)
    ts["bitki_skor"] = ts_bitki["skor"]
    ts["ad"] = L["strategies"]["toprak_sagligi"]
    ts["gelir_tl"] = round(ts_bitki["verim_kg"] * ts_bitki["fiyat_tl"], 2)

    su_secim = [b for b in tum_bitkiler if b["su_ihtiyacı"] in ("düşük", "orta")]
    su_bitki = su_secim[0] if su_secim else tum_bitkiler[-1]
    su_str = dict(STRATEJILER["su_tasarrufu"])
    su_str["bitki"] = su_bitki["bitki"]
    su_str["anahtar"] = su_bitki["anahtar"]
    su_str["skor"] = round((su_bitki["skor"] + 10) / 2, 1)
    su_str["bitki_skor"] = su_bitki["skor"]
    su_str["ad"] = L["strategies"]["su_tasarrufu"]
    su_str["gelir_tl"] = round(su_bitki["verim_kg"] * su_bitki["fiyat_tl"], 2)

    if mevcut and mevcut in crops:
        mevcut_ad = crops[mevcut]["ad"]
        mevcut_skor = next((b["skor"] for b in tum_bitkiler if b["anahtar"] == mevcut), tum_bitkiler[0]["skor"])
        mevcut_anahtar = mevcut
        mevcut_verim = crops[mevcut].get("verim_kg_donum", 300)
        mevcut_fiyat = crops[mevcut].get("fiyat_tl_kg", 15.0)
    else:
        mevcut_ad = L["current_crop"] + " (seçilmedi)"
        mevcut_skor = tum_bitkiler[0]["skor"]
        mevcut_anahtar = None
        mevcut_verim = 0
        mevcut_fiyat = 0

    mk = dict(STRATEJILER["mevcut_koruma"])
    mk["bitki"] = mevcut_ad
    mk["anahtar"] = mevcut_anahtar
    mk["skor"] = round(mevcut_skor * 0.95, 1)
    mk["bitki_skor"] = mevcut_skor
    mk["mevcut_anahtar"] = mevcut_anahtar
    mk["ad"] = L["strategies"]["mevcut_koruma"]
    mk["gelir_tl"] = round(mevcut_verim * mevcut_fiyat, 2)

    for s in [ts, su_str, mk]:
        s["neden"] = s[f"neden_{lang}"] if f"neden_{lang}" in s else s["neden_tr"]
        s["kanit"] = s[f"kanit_{lang}"] if f"kanit_{lang}" in s else s["kanit_tr"]
        s["faydalar"] = s[f"faydalar_{lang}"] if f"faydalar_{lang}" in s else s["faydalar_tr"]
        s["riskler"] = s[f"riskler_{lang}"] if f"riskler_{lang}" in s else s["riskler_tr"]
        s["bilgi_eksikligi"] = s[f"bilgi_eksikligi_{lang}"] if f"bilgi_eksikligi_{lang}" in s else s["bilgi_eksikligi_tr"]

    en_iyi = tum_bitkiler[0]

    stres_tak = stres_takvimi(ort_s, lang, aylik_veri=aylik)
    si_analiz = si_trend_analiz(aylik, ort_s)

    return {
        "rotasyon_plani": rotasyon_plani,
        "stratejiler": [ts, su_str, mk],
        "en_iyi_bitki": en_iyi,
        "tum_bitkiler": tum_bitkiler[:8],
        "stres_takvimi": stres_tak,
        "bare_field_aylari": bare_field_tespit(stres_tak),
        "si_analiz": si_analiz,
        "belirsizlik": belirsizlik_degerlendir(ekstra),
        "risk_uyarilari": risk_uyarilari(ort_s, lang),
        "dil": lang,
        "senaryo": scenario,
        "kisitlamalar": constraints,
        "nasa_kaynaklari": L["nasa_sources"],
        "advisor_warn": L["advisor_warn"],
        "ekstra_kullanildi": ekstra,
    }