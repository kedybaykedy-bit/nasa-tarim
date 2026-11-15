import json
import os

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
        "risk_frost": "Don riski",
        "risk_heat": "Isı dalgası riski",
        "risk_drought": "Kuraklık riski",
        "advisor_warn": "Bu araç destekleyici bir öneri sunar; final karar çiftçi ve yerel tarım uzmanlığına bırakılır.",
        "nasa_sources": "NASA Veri Kaynakları: POWER (sıcaklık, yağış, güneş, rüzgar) · SMAP (toprak nemi) · GPM (yağış) · Landsat (NDVI) · ECOSTRESS (ısı stresi) · SRTM (eşya yüksekliği)",
        "best_crop": "En iyi bitki",
        "strategy_score": "Strateji skoru",
        "crop_score": "Bitki skoru",
        "recommended_crop": "Önerilen bitki",
        "why": "Neden",
        "evidence": "Kanıt",
        "benefits": "Faydalar",
        "risks": "Riskler",
        "gaps": "Bilgi eksikliği",
        "rotation_advice": "Rota önerisi",
        "current_crop": "Mevcut bitki",
        "scenario_label": "Senaryo",
        "scenario_precip": "Yağış değişimi (%)",
        "scenario_temp": "Sıcaklık değişimi (°C)",
        "constraints": "Çiftçi kısıtları",
        "irrigation": "Sulama",
        "equipment": "Ekipman",
        "market": "Pazar tercihi",
        "stress_calendar": "Stres Takvimi",
        "month": "Ay",
        "temp_stress": "Sıcaklık stresi",
        "water_stress": "Su stresi",
        "ndvi_proxy": "Bitki gelişimi (NDVI proxy)",
        "frost_warning": "⚠ Bu dönemde don riski yüksek — erken tohumlama/koruma önlemi alın.",
        "heat_warning": "⚠ Bu dönemde ısı dalgası riski yüksek — sulama/ölçme planlayın.",
        "drought_warning": "⚠ Bu dönemde kuraklık riski yüksek — su tasarruflu bitki tercih edin.",
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
        "risk_frost": "Frost risk",
        "risk_heat": "Heat wave risk",
        "risk_drought": "Drought risk",
        "advisor_warn": "This tool provides supportive suggestions; final decisions rest with the farmer and local agronomists.",
        "nasa_sources": "NASA Data Sources: POWER (temp, precip, solar, wind) · SMAP (soil moisture) · GPM (precip) · Landsat (NDVI) · ECOSTRESS (heat stress) · SRTM (elevation)",
        "best_crop": "Best crop",
        "strategy_score": "Strategy score",
        "crop_score": "Crop score",
        "recommended_crop": "Recommended crop",
        "why": "Why",
        "evidence": "Evidence",
        "benefits": "Benefits",
        "risks": "Risks",
        "gaps": "Knowledge gaps",
        "rotation_advice": "Rotation advice",
        "current_crop": "Current crop",
        "scenario_label": "Scenario",
        "scenario_precip": "Precipitation change (%)",
        "scenario_temp": "Temperature change (°C)",
        "constraints": "Farmer constraints",
        "irrigation": "Irrigation",
        "equipment": "Equipment",
        "market": "Market preference",
        "stress_calendar": "Stress Calendar",
        "month": "Month",
        "temp_stress": "Temperature stress",
        "water_stress": "Water stress",
        "ndvi_proxy": "Crop growth (NDVI proxy)",
        "frost_warning": "⚠ High frost risk this period — consider early planting/protection.",
        "heat_warning": "⚠ High heat wave risk this period — plan irrigation/monitoring.",
        "drought_warning": "⚠ High drought risk this period — prefer water-saving crops.",
        "lang_switch": "TR",
    },
}


def load_crops():
    with open(os.path.join(DATA_DIR, "crops.json"), encoding="utf-8") as f:
        return json.load(f)


def clima_uygunluk(ort, crop):
    """0-100 arası klima uygunluk skoru."""
    t_min, t_max = crop["sıcaklık"]
    p_min, p_max = crop["yağış"]
    s_min, s_max = crop["güneş"]

    t = ort["sıcaklık_C"]
    p = ort["yağış_mm_gun"]
    s = ort["güneş_MJ_m2_gun"]

    def skalala(deger, d_min, d_max):
        if d_max == d_min:
            return 100 if deger == d_min else 0
        if deger < d_min:
            mesafe = d_min - deger
            return max(0, 70 - mesafe * 30)
        if deger > d_max:
            mesafe = deger - d_max
            return max(0, 70 - mesafe * 30)
        orta = (d_min + d_max) / 2
        yaricap = (d_max - d_min) / 2
        uzaklik = abs(deger - orta) / yaricap
        return 70 + 30 * (1 - uzaklik)

    st = skalala(t, t_min, t_max)
    sp = skalala(p, p_min, p_max)
    ss = skalala(s, s_min, s_max)
    return round((st * 0.5 + sp * 0.3 + ss * 0.2), 1)


# Strateji tanımları
STRATEJILER = {
    "toprak_sagligi": {
        "anahtar": "toprak_sagligi",
        "ad_tr": "Toprak Sağlığı Odaklı Rotasyon",
        "ad_en": "Soil Health Focused Rotation",
        "grup_vurgu": ["iyileştirici", "nötr"],
        "aciklama_tr": "Azot bağlayıcı ve örtü bitkileri öne çıkaran, toprağı dinlendiren ve erozyonu azaltan bir döngü.",
        "aciklama_en": "Rotation emphasizing nitrogen-fixers and cover crops to rest soil and reduce erosion.",
        "neden_tr": "NASA POWER yağış ve sıcaklık verilerine göre en az su stresi olan mevsimlerde azot bağlayıcılar (nohut, bezelye) ve örtü bitkileri yerleştirilerek toprağın organik madde içeriği artırılır.",
        "neden_en": "Based on NASA POWER precipitation and temperature data, nitrogen-fixers (chickpea, pea) and cover crops are placed in low water-stress seasons to increase soil organic matter.",
        "kanit_tr": "NASA SMAP toprak nemi ve POWER yağış verileri; azot bağlayıcıların toprağa ~40-60 kg/ha azot bıraktığı tarımsal literatür.",
        "kanit_en": "NASA SMAP soil moisture and POWER precipitation data; agronomic literature shows nitrogen-fixers contribute ~40-60 kg/ha N.",
        "faydalar_tr": ["Toprak organik maddesi artar", "Erozyon riski azalır", "Kimyasal gübre ihtiyacı düşer", "Su tutma kapasitesi artar"],
        "faydalar_en": ["Soil organic matter increases", "Erosion risk decreases", "Chemical fertilizer need drops", "Water retention improves"],
        "riskler_tr": ["Kısa vadede geliri azaltabilir", "Yerel pazar talebi sınırlı olabilir", "Uzman danışmanlık gerekebilir"],
        "riskler_en": ["May reduce short-term income", "Local market demand may be limited", "Expert advisory may be needed"],
        "bilgi_eksikligi_tr": "Yerel toprak testi ve tarım mühendisi onayı gerekli.",
        "bilgi_eksikligi_en": "Local soil test and agronomist approval required.",
    },
    "su_tasarrufu": {
        "anahtar": "su_tasarrufu",
        "ad_tr": "Su Tasarruflu Rotasyon",
        "ad_en": "Water Saving Rotation",
        "grup_vurgu": ["düşük", "orta"],
        "aciklama_tr": "Düşük su ihtiyacı ve kurak dayanıklılığı yüksek bitkilerle su tüketimini minimize eden bir döngü.",
        "aciklama_en": "Rotation minimizing water use with low-water, drought-tolerant crops.",
        "neden_tr": "NASA POWER düşük yağış ve yüksek sıcaklık verilerine göre, mercan, nohut ve arpa gibi düşük-su ihtiyacı bitkiler tercih edilir.",
        "neden_en": "Based on NASA POWER low precipitation and high temperature data, low-water crops (lentil, chickpea, barley) are preferred.",
        "kanit_tr": "NASA GPM yağış ve POWER sıcaklık verileri; mercan ve nohutun diğer tahıllara kıyasla %30-50 daha az su torduğu araştırmalar.",
        "kanit_en": "NASA GPM precipitation and POWER temperature data; studies show lentil and chickpea use 30-50% less water than cereals.",
        "faydalar_tr": ["Su tüketimi %30-50 azalır", "Kuraklığa dayanıklılık artar", "Sulama maliyeti düşer"],
        "faydalar_en": ["Water use reduced 30-50%", "Drought resilience increases", "Irrigation cost drops"],
        "riskler_tr": ["Verim daha düşük olabilir", "Pazar talebi değişken olabilir", "Toprak tuzluluğu riski"],
        "riskler_en": ["Yield may be lower", "Market demand may vary", "Soil salinity risk"],
        "bilgi_eksikligi_tr": "Yerel sulama altyapısı ve su hakları kontrolü gerekli.",
        "bilgi_eksikligi_en": "Local irrigation infrastructure and water rights check required.",
    },
    "mevcut_koruma": {
        "anahtar": "mevcut_koruma",
        "ad_tr": "Mevcut Rotasyonu Koru",
        "ad_en": "Keep Current Rotation",
        "grup_vurgu": None,
        "aciklama_tr": "Şu anki bitkiye en uygun, minimum değişimli ve en düşük riskli bir rota.",
        "aciklama_en": "Minimum-change, low-risk rotation suited to current crop.",
        "neden_tr": "NASA POWER iklim verileri mevcut bitkinin sıcaklık/yağış aralığıyla uyumlu olduğu takdirde, değişiklik riski alınmadan mevcut döngü sürdürülür.",
        "neden_en": "If NASA POWER climate data matches current crop's temp/precip range, continue current rotation without change risk.",
        "kanit_tr": "NASA POWER sıcaklık ve yağış verilerinin mevcut bitkinin ideal aralık içine düşmesi.",
        "kanit_en": "NASA POWER temperature and precipitation data falling within current crop's ideal range.",
        "faydalar_tr": ["Değişim riski yok", "Ekipman ve bilgi altyapısı mevcut", "Hızlı uygulanabilir"],
        "faydalar_en": ["No change risk", "Existing equipment and knowledge base", "Quick to implement"],
        "riskler_tr": ["Toprak yorumu uzun vadede artabilir", "Aşınma ve hastalık döngüsü devam edebilir", "Yeni fırsatlar kaçabilir"],
        "riskler_en": ["Soil fatigue may increase long-term", "Pest/disease cycles may persist", "New opportunities may be missed"],
        "bilgi_eksikligi_tr": "Toprak testleri ve uzun vadeli verim kaydı gerekli.",
        "bilgi_eksikligi_en": "Soil tests and long-term yield records required.",
    },
}


def get_str_text(key, lang):
    """STRATEJILER içinden dil özelliğini al."""
    s = STRATEJILER[key]
    return s.get(f"{key.split('_')[-1]}_{lang}") or s.get(f"ad_{lang}") or s["ad_tr"]


def apply_scenario(ort, scenario):
    """Senaryo (yağış/sıcaklık değişimi) uygula, yeni ortalama döndür."""
    if not scenario:
        return ort
    yeni = dict(ort)
    precip_change = scenario.get("precip_change_pct", 0) / 100.0
    temp_change = scenario.get("temp_change_c", 0)
    yeni["yağış_mm_gun"] = round(yeni["yağış_mm_gun"] * (1 + precip_change), 2)
    yeni["sıcaklık_C"] = round(yeni["sıcaklık_C"] + temp_change, 2)
    return yeni


def apply_constraints(crops, constraints):
    """Çiftçi kısıtlarına göre bitki listesini filtrele/cezala."""
    if not constraints:
        return crops
    filtered = {}
    for k, c in crops.items():
        penalty = 0
        # Sulama yoksa yüksek su ihtiyacı ceza
        if constraints.get("irrigation") == "yok" and c["su_ihtiyacı"] == "yüksek":
            penalty += 30
        # Ekipman kısıtı: özel ekipman gerektiren bitkiler (şimdilik basit)
        # Pazar tercihi: istenen gruba bonus
        market_pref = constraints.get("market_preference")
        if market_pref and c["grup"] == market_pref:
            penalty -= 10  # bonus
        c2 = dict(c)
        c2["_constraint_penalty"] = penalty
        filtered[k] = c2
    return filtered


def strategi_skoru(ort, oncelikler, crop, strateji_key, constraints=None):
    """Tek bir strateji için bitki bazlı 0-100 skor hesaplar."""
    base = clima_uygunluk(ort, crop)

    su = oncelikler.get("su_tasarimi", 0) / 100.0
    toprak = oncelikler.get("toprak_sagligi", 0) / 100.0
    kararlilik = oncelikler.get("kararli_verim", 0) / 100.0
    guclu = oncelikler.get("guclu_koşullar", 0) / 100.0

    bonus = 0
    if su > 0:
        su_skor = {"düşük": 100, "orta": 60, "yüksek": 20}.get(crop["su_ihtiyacı"], 50)
        bonus += su_skor * su * 0.4
    if toprak > 0:
        top_skor = {"iyileştirici": 100, "nötr": 60, "tüketici": 20}.get(crop["toprak_etkisi"], 50)
        bonus += top_skor * toprak * 0.3
    if kararlilik > 0:
        t_genislik = crop["sıcaklık"][1] - crop["sıcaklık"][0]
        p_genislik = crop["yağış"][1] - crop["yağış"][0]
        kar_skor = min(100, (t_genislik + p_genislik) * 4)
        bonus += kar_skor * kararlilik * 0.2
    if guclu > 0:
        gcl_skor = min(100, crop["sıcaklık"][1] + (10 - crop["yağış"][1]) * 10)
        bonus += gcl_skor * guclu * 0.1

    # Kısıtlama cezası
    penalty = crop.get("_constraint_penalty", 0)
    if penalty > 0:
        bonus -= penalty

    return round(max(0, min(100, base + bonus)), 1)


def risk_uyarilari(ort, lang="tr"):
    """Don, ısı dalgası, kuraklık risk uyarıları."""
    uyarilar = []
    t = ort["sıcaklık_C"]
    p = ort["yağış_mm_gun"]
    L = LANG[lang]

    # Basit kural: ortalama sıcaklık < 5°C -> don riski
    if t < 5:
        uyarilar.append({"tip": "don", "mesaj": L["frost_warning"], "severity": "high"})
    # Sıcaklık > 30°C -> ısı dalgası
    if t > 30:
        uyarilar.append({"tip": "isi", "mesaj": L["heat_warning"], "severity": "high"})
    # Yağış < 1 mm/gün -> kuraklık
    if p < 1.0:
        uyarilar.append({"tip": "kuraklik", "mesaj": L["drought_warning"], "severity": "medium"})
    return uyarilar


def stres_takvimi(ort, lang="tr"):
    """
    Yıl boyu stres takvimi (12 ay).
    NASA POWER'dan aylık ortalamalar yok, bu yüzden mevcut ortalamadan proxy üretiriz.
    Gerçek uygulamada POWER monthly endpoint kullanılmalı.
    """
    L = LANG[lang]
    t_ort = ort["sıcaklık_C"]
    p_ort = ort["yağış_mm_gun"]

    aylar = list(range(1, 13))
    takvim = []

    for ay in aylar:
        # Basit mevsimsellik modeli (kuzey yarımküresi)
        if ay in [12, 1, 2]:  # Kış
            t_ay = t_ort - 8
            p_ay = p_ort * 0.8
            ndvi = 0.15
        elif ay in [3, 4, 5]:  # Bahar
            t_ay = t_ort - 2
            p_ay = p_ort * 1.2
            ndvi = 0.55
        elif ay in [6, 7, 8]:  # Yaz
            t_ay = t_ort + 6
            p_ay = p_ort * 0.6
            ndvi = 0.75
        else:  # Sonbahar
            t_ay = t_ort
            p_ay = p_ort * 1.0
            ndvi = 0.40

        # Stres hesaplama
        temp_stress = max(0, min(100, (max(0, 35 - t_ay) if t_ay > 30 else max(0, 5 - t_ay)) * 10))
        water_stress = max(0, min(100, (2.0 - p_ay) * 40))

        takvim.append({
            "ay": ay,
            "ay_adi": L["groups"]["kis" if ay in [12,1,2] else "bahar" if ay in [3,4,5] else "yaz" if ay in [6,7,8] else "sonbahar"],
            "sıcaklık_C": round(t_ay, 1),
            "yağış_mm_gun": round(p_ay, 2),
            "ndvi_proxy": round(ndvi, 2),
            "temp_stress": round(temp_stress),
            "water_stress": round(water_stress),
        })

    return {
        "aylar": takvim,
        "labels": [L["groups"]["kis"], L["groups"]["bahar"], L["groups"]["yaz"], L["groups"]["sonbahar"]],
    }


def rotasyon_oneri(ort, oncelikler, mevcut=None, crops=None, scenario=None, constraints=None, lang="tr"):
    """
    3 farklı rotasyon stratejisi + stres takvimi + risk uyarıları + dil desteği.
    """
    L = LANG[lang]

    if crops is None:
        crops = load_crops()

    # Senaryo uygula
    ort_s = apply_scenario(ort, scenario)

    # Kısıtlamaları uygula
    crops_c = apply_constraints(crops, constraints)

    # Tüm bitkileri skora göre sırala
    tum_bitkiler = []
    for anahtar, c in crops_c.items():
        skor = strategi_skoru(ort_s, oncelikler, c, None, constraints)
        tum_bitkiler.append({
            "bitki": c["ad"],
            "anahtar": anahtar,
            "grup": c["grup"],
            "skor": skor,
            "su_ihtiyacı": c["su_ihtiyacı"],
            "toprak_etkisi": c["toprak_etkisi"],
            "not": c["not"],
        })
    tum_bitkiler.sort(key=lambda x: x["skor"], reverse=True)

    # Strateji 1: Toprak Sağlığı
    ts_secim = [b for b in tum_bitkiler if b["toprak_etkisi"] in ("iyileştirici", "nötr")]
    ts_bitki = ts_secim[0] if ts_secim else tum_bitkiler[0]
    ts = dict(STRATEJILER["toprak_sagligi"])
    ts["bitki"] = ts_bitki["bitki"]
    ts["skor"] = round((ts_bitki["skor"] + 10) / 2, 1)
    ts["bitki_skor"] = ts_bitki["skor"]
    ts["ad"] = L["strategies"]["toprak_sagligi"]

    # Strateji 2: Su Tasarrufu
    su_secim = [b for b in tum_bitkiler if b["su_ihtiyacı"] in ("düşük", "orta")]
    su_bitki = su_secim[0] if su_secim else tum_bitkiler[-1]
    su_str = dict(STRATEJILER["su_tasarrufu"])
    su_str["bitki"] = su_bitki["bitki"]
    su_str["skor"] = round((su_bitki["skor"] + 10) / 2, 1)
    su_str["bitki_skor"] = su_bitki["skor"]
    su_str["ad"] = L["strategies"]["su_tasarrufu"]

    # Strateji 3: Mevcut Rotasyonu Koru
    if mevcut and mevcut in crops:
        mevcut_ad = crops[mevcut]["ad"]
        mevcut_skor = next((b["skor"] for b in tum_bitkiler if b["anahtar"] == mevcut), tum_bitkiler[0]["skor"])
        mevcut_anahtar = mevcut
    else:
        mevcut_ad = L["current_crop"] + " (seçilmedi)"
        mevcut_skor = tum_bitkiler[0]["skor"]
        mevcut_anahtar = None

    mk = dict(STRATEJILER["mevcut_koruma"])
    mk["bitki"] = mevcut_ad
    mk["skor"] = round(mevcut_skor * 0.95, 1)
    mk["bitki_skor"] = mevcut_skor
    mk["mevcut_anahtar"] = mevcut_anahtar
    mk["ad"] = L["strategies"]["mevcut_koruma"]

    # Dil çevirileri için metinleri güncelle
    for s in [ts, su_str, mk]:
        s["neden"] = s[f"neden_{lang}"] if f"neden_{lang}" in s else s["neden_tr"]
        s["kanit"] = s[f"kanit_{lang}"] if f"kanit_{lang}" in s else s["kanit_tr"]
        s["faydalar"] = s[f"faydalar_{lang}"] if f"faydalar_{lang}" in s else s["faydalar_tr"]
        s["riskler"] = s[f"riskler_{lang}"] if f"riskler_{lang}" in s else s["riskler_tr"]
        s["bilgi_eksikligi"] = s[f"bilgi_eksikligi_{lang}"] if f"bilgi_eksikligi_{lang}" in s else s["bilgi_eksikligi_tr"]

    en_iyi = tum_bitkiler[0]

    return {
        "stratejiler": [ts, su_str, mk],
        "en_iyi_bitki": en_iyi,
        "tum_bitkiler": tum_bitkiler[:5],
        "stres_takvimi": stres_takvimi(ort_s, lang),
        "risk_uyarilari": risk_uyarilari(ort_s, lang),
        "dil": lang,
        "senaryo": scenario,
        "kisitlamalar": constraints,
    }