// ============================================================================
// Field Shift — NASA POWER Agroclimatology Interface Logic
// ============================================================================

const I18N = {
  en: {
    lang_code: 'Türkçe',
    loc_title: 'Field Location',
    btn_locate: 'Use Device Location',
    ph_address: 'Enter address or place name…',
    lbl_lat: 'Latitude',
    lbl_lon: 'Longitude',
    lbl_field_size: 'Field Size',
    lbl_decare: 'decare',
    date_title: 'Planting & Observation Period',
    lbl_start: 'Planting Date',
    lbl_end: 'Harvest Date',
    pref_title: 'Field Priorities',
    lbl_current_crop: 'Current crop on field',
    opt_empty_crop: 'Fallow / Empty',
    lbl_prev_crop: 'Previous crop',
    opt_prev_none: 'None / First year',
    p_water: 'Water Need',
    p_soil: 'Soil Health',
    p_yield: 'Target Yield',
    p_resilience: 'Climate Resilience',
    opt_water_any: 'Any',
    opt_water_mid: 'Low Water',
    opt_water_high: 'Dryland',
    opt_soil_any: 'Any',
    opt_soil_mid: 'Rest Soil',
    opt_soil_high: 'Nitrogen Fix',
    opt_yield_any: 'Any',
    opt_yield_mid: 'Balanced',
    opt_yield_high: 'Maximum',
    opt_res_normal: 'Normal',
    opt_res_mid: 'Heat & Frost',
    opt_res_high: 'Extreme Climate',
    advanced_title: 'Irrigation & Climate Scenario',
    lbl_precip_change: 'Rainfall Delta',
    lbl_temp_change: 'Temperature Delta',
    lbl_irrigation: 'Irrigation',
    opt_irr_any: 'Not specified',
    opt_irr_yes: 'Irrigated',
    opt_irr_no: 'Rainfed only',
    lbl_market: 'Season Type',
    opt_mkt_any: 'Any season',
    opt_mkt_kislik: 'Winter Crop',
    opt_mkt_yazlik: 'Summer Crop',
    opt_mkt_bahar: 'Spring Crop',
    btn_run_analysis: 'Analyse Field with NASA Data',
    btn_running: 'Querying NASA Satellite Data…',
    welcome_title: 'NASA POWER Agroclimatology Crop Rotation Planner',
    welcome_desc: 'Select your field location on the map and choose observation dates. NASA climate metrics are processed to provide sustainable rotation recommendations.',
    pil_1_title: 'Soil Health',
    pil_1_desc: 'Legumes fix atmospheric nitrogen to restore depleted soil.',
    pil_2_title: 'Water Efficiency',
    pil_2_desc: 'Matches crops to regional rainfall regimes to optimize irrigation costs.',
    pil_3_title: 'Risk Shield',
    pil_3_desc: 'Detects extreme heat and frost risks during critical growth stages.',
    m_temp: 'Mean Temp',
    m_precip: 'Daily Rain',
    m_solar: 'Solar Energy',
    m_wind: 'Wind Speed',
    best_match_badge: 'Primary Recommendation',
    lbl_yield_ratio: 'Yield Ratio',
    lbl_yield_per_dec: 'Est. Harvest / decare',
    strategies_heading: 'Rotation Strategies',
    tab_stress: '12-Month Field Risk & Growth Proxy',
    tab_timeline: 'Daily NASA Climate Series',
    btn_report: 'Download Field Report (.txt)',
    leg_temp: 'Heat Stress Risk',
    leg_water: 'Moisture Deficit',
    leg_ndvi: 'Crop Greenness Rate',
    income_title: 'Estimated Income',
    income_total_yield: 'Total Yield',
    income_price_per_kg: 'Avg. Market Price',
    income_gross: 'Gross Revenue',
    drought_title: 'Drought Risk Assessment',
    drought_level: 'Risk Level',
    drought_desc: 'Recommendation',
    rotation_plan_title: '3-Year Scientific Crop Rotation Plan',
    rotation_plan_badge: 'Soil Health & Nitrogen Cycle',
    btn_add_history: '+ Add Previous Year Crop',
    lbl_year_prev: 'Years Ago',
    eco_nitrogen: 'Natural N-Fix & Fertilizer Saved',
    eco_water: 'Groundwater & Pump Fuel Saved',
    eco_soil: 'Soil Vitality Preservation',
    btn_print: 'Print / Export Field Report',
    provenance_heading: 'NASA Earth Science Integration & Methodology',
    prov_t2m: 'Thermal threshold triggers identify early seedling viability, late spring frost, and extreme heatwaves.',
    prov_precip: 'NASA daily & monthly precipitation regimes identify drought risks and filter rainfed vs irrigated crops.',
    prov_solar: 'Solar irradiance models photosynthetic potential and validates the 12-month vegetative NDVI curve.',
    prov_monthly: 'Eliminates guesswork by anchoring the stress timeline directly to NASA Monthly point climate series.',
    prov_sentinel: '10–20m multispectral imagery. Red-edge, NIR and SWIR bands enable NDVI/EVI computation and field-scale vegetation stress mapping.',
    prov_era5: 'Hourly global reanalysis: temperature, humidity, wind, soil moisture. Fills temporal gaps and sparse-station regions as complementary time series.',
    prov_smap: 'Global surface soil moisture and freeze/thaw mapping every 2–3 days. Complementary layer for drought early-warning and irrigation scheduling.',
    prov_srtm_gpm: 'SRTM: global slope/terrain for erosion risk and runoff modelling. GPM/IMERG: global precipitation accumulation for extreme-rainfall frequency assessment.',
    si_title: 'Statistical Trend Analysis (SI)',
    si_badge: 'NASA POWER 5-Year Dataset',
    si_uncertainty: 'Model uncertainty: long-term trends evaluated via R² coefficient. Local micro-climate variation may affect estimates; consult a regional agronomist.',
    si_temp_trend: 'Temperature Trend',
    si_precip_trend: 'Precipitation Trend',
    si_confidence: 'Model Fit (R²)',
    si_per_year: '/yr',
    glossary_title: 'Scientific Terms Glossary',
    gls_ndvi: 'Normalized Difference Vegetation Index. Scale -1 to +1; above 0.6 = healthy green cover, below 0 = bare soil. Computed from Sentinel-2 and Landsat NIR/red bands.',
    gls_et: 'Evapotranspiration: soil evaporation + plant transpiration. Direct measure of crop water demand. ECOSTRESS + NASA POWER together estimate ET at field scale.',
    gls_sma: 'Soil Moisture Anomaly: deviation of current soil moisture from long-term mean (Z-score). Positive = excess moisture; negative = drought stress.',
    gls_frost: 'Period when minimum temperature drops below 0°C. Frost in the first 2 weeks post-germination can destroy the crop entirely. This tool flags NASA POWER T2M below 5°C.',
    gls_wb: 'Water Balance: Precipitation minus evapotranspiration. Positive = excess water / runoff; negative = irrigation need.',
    gls_sat_vs_ground: 'Satellite data covers large areas but averages pixels (250m–10km). Ground sensors measure at a point but offer less coverage. Best results come from combining both.',
    gls_uncertainty: "This tool's recommendations are probabilistic estimates based on NASA climate statistics. Local soil chemistry, seed quality, and micro-climate variation can affect outcomes; expert consultation advised.",
    advisory_note: 'Decision-support tool based on NASA POWER agroclimatology. Field-specific soil test validation is advised.',
  },
  tr: {
    lang_code: 'English',
    loc_title: 'Tarla Konumu',
    btn_locate: 'Cihaz Konumu',
    ph_address: 'Adres veya yer adı girin…',
    lbl_lat: 'Enlem',
    lbl_lon: 'Boylam',
    lbl_field_size: 'Tarla Büyüklüğü',
    lbl_decare: 'dönüm',
    date_title: 'Ekim ve Gözlem Dönemi',
    lbl_start: 'Ekim Tarihi',
    lbl_end: 'Hasat Tarihi',
    pref_title: 'Tarla Öncelikleri',
    lbl_current_crop: 'Mevcut Ürün',
    opt_empty_crop: 'Boş / Nadas',
    lbl_prev_crop: 'Geçen Yıl Ekilen Ürün',
    opt_prev_none: 'Yok / İlk Yıl',
    p_water: 'Su İhtiyacı',
    p_soil: 'Toprak Sağlığı',
    p_yield: 'Verim Hedefi',
    p_resilience: 'Hava Koşullarına Dayanıklılık',
    opt_water_any: 'Fark Etmez',
    opt_water_mid: 'Az Su',
    opt_water_high: 'Kuru Tarım',
    opt_soil_any: 'Fark Etmez',
    opt_soil_mid: 'Toprağı Dinlendir',
    opt_soil_high: 'Azot Katkısı',
    opt_yield_any: 'Fark Etmez',
    opt_yield_mid: 'Dengeli Verim',
    opt_yield_high: 'Yüksek Verim',
    opt_res_normal: 'Normal',
    opt_res_mid: 'Sıcak & Don',
    opt_res_high: 'Aşırı Hava Koşulları',
    advanced_title: 'Sulama ve İklim Simülasyonu',
    lbl_precip_change: 'Yağış Sapması',
    lbl_temp_change: 'Sıcaklık Sapması',
    lbl_irrigation: 'Sulama Durumu',
    opt_irr_any: 'Belirtilmemiş',
    opt_irr_yes: 'Sulu Tarım',
    opt_irr_no: 'Kuru Tarım',
    lbl_market: 'Ürün Grubu',
    opt_mkt_any: 'Tüm Sezonlar',
    opt_mkt_kislik: 'Kışlık',
    opt_mkt_yazlik: 'Yazlık',
    opt_mkt_bahar: 'Bahar',
    btn_run_analysis: 'NASA Verileriyle Analiz Et',
    btn_running: 'NASA Uydu Verileri İnceleniyor…',
    welcome_title: 'NASA POWER Uydu Verileriyle Ekim Nöbeti Planlayıcı',
    welcome_desc: 'Haritadan tarla konumunuzu seçin ve ekim dönemini belirleyin. NASA iklim göstergeleri analiz edilerek toprağı yormayan en uygun rotasyon yolları listelenir.',
    pil_1_title: 'Toprak Sağlığı',
    pil_1_desc: 'Ekim nöbetinde baklagiller toprağa doğal azot bağlar.',
    pil_2_title: 'Su Dengesi',
    pil_2_desc: 'Bölgesel yağış rejimine uygun tohum seçimiyle sulama maliyetini azaltır.',
    pil_3_title: 'İklim Riski',
    pil_3_desc: 'Kritik dönemlerde don ve aşırı sıcak risklerini önceden tespit eder.',
    m_temp: 'Ortalama Sıcaklık',
    m_precip: 'Günlük Yağış',
    m_solar: 'Güneş Gücü',
    m_wind: 'Rüzgar Hızı',
    best_match_badge: 'Öncelikli Tavsiye',
    lbl_yield_ratio: 'Bereket Oranı',
    lbl_yield_per_dec: 'Tahmini Hasat / dönüm',
    strategies_heading: 'Ekim Nöbeti Stratejileri',
    tab_stress: '12 Aylık Risk & Büyüme Takvimi',
    tab_timeline: 'Günlük NASA İklim Serisi',
    btn_report: 'Raporu İndir (.txt)',
    leg_temp: 'Sıcak Stresi Riski',
    leg_water: 'Su Açığı Riski',
    leg_ndvi: 'Bitki Gelişimi (NDVI)',
    income_title: 'Tahmini Gelir',
    income_total_yield: 'Toplam Hasat',
    income_price_per_kg: 'Ortalama Piyasa Fiyatı',
    income_gross: 'Brüt Gelir',
    drought_title: 'Kuraklık Riski Analizi',
    drought_level: 'Risk Düzeyi',
    drought_desc: 'Çiftçi Tavsiyesi',
    rotation_plan_title: '3 Yıllık Bilimsel Rotasyon Takvimi',
    rotation_plan_badge: 'Toprak Sağlığı & Azot Döngüsü',
    btn_add_history: '+ Daha Önceki Yılı Ekle',
    lbl_year_prev: 'Yıl Önceki Ürün',
    eco_nitrogen: 'Doğal Azot & Gübre Tasarrufu',
    eco_water: 'Yeraltı Suyu & Pompa Tasarrufu',
    eco_soil: 'Toprak Verimliliği Koruması',
    btn_print: 'Yazdır / PDF Rapor',
    provenance_heading: 'NASA Veri Entegrasyonu & Bilimsel Metodoloji',
    prov_t2m: 'Hava sıcaklık eşikleri bitki çimlenmesi, ilkbahar geç donları ve aşırı ısı dalgası risklerini tespit eder.',
    prov_precip: 'Günlük ve aylık yağış rejimleri kuraklık stresini belirler; kuru tarım / sulu tarım rotasını filtreler.',
    prov_solar: 'Yüzey güneş ışınımı verisi fotosentez potansiyelini ve 12 aylık fenolojik bitki gelişim (NDVI) eğrisini modeller.',
    prov_monthly: 'Sentetik tahminler yerine NASA\'nın 12 aylık gerçek iklim serisiyle gerçeğe tam uygun stres takvimi üretir.',
    prov_sentinel: '10–20m çözünürlüklü multispektral görüntü. Red-edge, NIR ve SWIR bantlarıyla NDVI/EVI hesabı ve tarla ölçeğinde bitki stresi haritalaması.',
    prov_era5: 'Saatlik küresel reanaliz: sıcaklık, nem, rüzgar, toprak sıcaklığı/nemi. NASA gözlemlerinin kapsamadığı dönemler ve seyrek istasyon bölgelerinde tamamlayıcı zaman serisi kaynağı.',
    prov_smap: '2–3 günde bir küresel yüzey toprak nemi ve don/çözülme ölçümü. Kuraklık erken uyarısı ve sulama zamanlaması için tamamlayıcı katman.',
    prov_srtm_gpm: 'SRTM: Küresel eğim/topoğrafya — erozyon riski ve yüzey akışı modellemesi. GPM/IMERG: küresel yağış birikimi ve ekstrem yağış frekansı değerlendirmesi.',
    si_title: 'İstatistiksel Trend Analizi (SI)',
    si_badge: 'NASA POWER 5 Yıllık Veri',
    si_uncertainty: 'Model belirsizliği: Uzun dönem trendler R² katsayısıyla değerlendirilmiştir. Yerel mikro-iklim farklılıkları bu tahmini etkileyebilir; bölgenizin tarım uzmanına danışın.',
    si_temp_trend: 'Sıcaklık Trendi',
    si_precip_trend: 'Yağış Trendi',
    si_confidence: 'Model Uyumu (R²)',
    si_per_year: '/yıl',
    glossary_title: 'Bilimsel Terimler Sözlüğü',
    gls_ndvi: 'Normalize Fark Bitki Örtüsü İndeksi. -1 ile +1 arası ölçek; 0.6 üzeri sağlıklı yeşil örtüyü, 0 altı çıplak toprağı gösterir. Sentinel-2 ve Landsat NIR/kırmızı bantlarından hesaplanır.',
    gls_et: 'Evapotranspirasyon: toprak buharlaşması + bitki terlemesinin toplamı. Bitki su gereksiniminin doğrudan ölçüsü. ECOSTRESS ve NASA POWER ET\'yi tarla ölçeğinde tahmin eder.',
    gls_sma: 'Toprak Nemi Anomalisi: mevcut toprak neminin uzun dönem ortalamasından sapma (Z-skoru). Pozitif = aşırı ıslaklık; negatif = kuraklık stresi.',
    gls_frost: 'Minimum sıcaklığın 0°C altına düştüğü dönem. Çimlenmeden sonraki ilk 2 haftada don bitkiyi tamamen yok edebilir. Bu araç NASA POWER T2M 5°C altını işaretler.',
    gls_wb: 'Su Dengesi: Yağış eksi evapotranspirasyon. Pozitif = fazla su/taşma; negatif = sulama ihtiyacı.',
    gls_sat_vs_ground: 'Uydu verileri geniş alanı kapsar ancak piksel ortalaması alır (250m–10km). Yerüstü sensörler nokta-ölçüm yapar ama daha az kapsam sunar. En doğru sonuç ikisinin birlikte kullanılmasıyla elde edilir.',
    gls_uncertainty: 'Bu aracın önerileri NASA iklim istatistiklerine dayalı ihtimaliyet tahminleridir. Yerel toprak kimyası, tohum kalitesi ve mikro-iklim farklılıkları sonucu değiştirebilir; uzman danışmanlığı tavsiye edilir.',
    advisory_note: 'Bu sistem karar destek amaçlıdır. Nihai ekim öncesi yerel toprak kimyasal analizlerinin yapılması tavsiye edilir.',
  }
};

// Market price estimates (TRY / kg) — approximate for demo
const CROP_MARKET_PRICES = {
  nohut:   { price: 28, unit: '₺/kg' },
  mercan:  { price: 30, unit: '₺/kg' },
  buğday:  { price: 10, unit: '₺/kg' },
  arpa:    { price: 8,  unit: '₺/kg' },
  mısır:   { price: 7,  unit: '₺/kg' },
  bezelye: { price: 25, unit: '₺/kg' },
  patates: { price: 9,  unit: '₺/kg' },
  domates: { price: 6,  unit: '₺/kg' },
};

// Yield data per decare
const CROP_METRICS = {
  nohut:   { ratio_en: 'Yields 1:10', ratio_tr: "1'e 10 Verir", yield_en: '160 - 200 kg / decare', yield_tr: '160 - 200 kg / dönüm', yield_mid: 180 },
  mercan:  { ratio_en: 'Yields 1:12', ratio_tr: "1'e 12 Verir", yield_en: '180 - 230 kg / decare', yield_tr: '180 - 230 kg / dönüm', yield_mid: 205 },
  buğday:  { ratio_en: 'Yields 1:8',  ratio_tr: "1'e 8 Verir",  yield_en: '280 - 380 kg / decare', yield_tr: '280 - 380 kg / dönüm', yield_mid: 330 },
  arpa:    { ratio_en: 'Yields 1:9',  ratio_tr: "1'e 9 Verir",  yield_en: '300 - 420 kg / decare', yield_tr: '300 - 420 kg / dönüm', yield_mid: 360 },
  mısır:   { ratio_en: 'Yields 1:14', ratio_tr: "1'e 14 Verir", yield_en: '950 - 1250 kg / decare', yield_tr: '950 - 1250 kg / dönüm', yield_mid: 1100 },
  bezelye: { ratio_en: 'Yields 1:10', ratio_tr: "1'e 10 Verir", yield_en: '200 - 260 kg / decare', yield_tr: '200 - 260 kg / dönüm', yield_mid: 230 },
  patates: { ratio_en: 'Yields 1:6',  ratio_tr: "1'e 6 Verir",  yield_en: '2500 - 3500 kg / decare', yield_tr: '2500 - 3500 kg / dönüm', yield_mid: 3000 },
  domates: { ratio_en: 'Yields 1:15', ratio_tr: "1'e 15 Verir", yield_en: '4000 - 6000 kg / decare', yield_tr: '4000 - 6000 kg / dönüm', yield_mid: 5000 },
};

function getFarmerJudgment(score, lang) {
  if (score >= 75) {
    return {
      title: lang === 'tr' ? 'Tam Tarlanın Malı' : 'Prime Field Match',
      sub: lang === 'tr' ? 'Bu hava ve toprakta gözün kapalı ekebilirsin' : 'Ideal climate & soil conditions with minimum risk'
    };
  } else if (score >= 50) {
    return {
      title: lang === 'tr' ? 'Güzel Tutar (Bakım İster)' : 'Good Fit (Requires Care)',
      sub: lang === 'tr' ? 'Sulamayı ve bakımı aksatmazsan iyi ürün verir' : 'Healthy yields expected with steady irrigation & care'
    };
  } else {
    return {
      title: lang === 'tr' ? 'Tarlayı Yorma (Riskli)' : 'High Risk for Field',
      sub: lang === 'tr' ? 'Bu sezon iklim ve su şartları masrafını zor kurtarır' : 'Climate stress may suppress yield below investment cost'
    };
  }
}

function getDroughtAssessment(precipMmDay, lang) {
  // daily average precipitation
  if (precipMmDay >= 2.5) {
    return {
      levelClass: 'status-low',
      level: lang === 'tr' ? 'Düşük' : 'Low',
      desc: lang === 'tr'
        ? 'Yağış yeterli. Kuraklık riski minimal, çoğu ürün güvenli.'
        : 'Rainfall is sufficient. Drought risk is minimal; most crops are safe.'
    };
  } else if (precipMmDay >= 1.2) {
    return {
      levelClass: 'status-mid',
      level: lang === 'tr' ? 'Orta' : 'Moderate',
      desc: lang === 'tr'
        ? 'Yağış sınırda. Su tasarruflu ürün tercih edin veya sulama planlayın.'
        : 'Rainfall is borderline. Prefer drought-tolerant crops or plan supplemental irrigation.'
    };
  } else {
    return {
      levelClass: 'status-high',
      level: lang === 'tr' ? 'Yüksek' : 'High',
      desc: lang === 'tr'
        ? 'Ciddi kuraklık riski. Yalnızca kurak dayanıklı ürün ekin, sulamayı güvence altına alın.'
        : 'Serious drought risk. Plant only drought-resistant crops and secure irrigation.'
    };
  }
}

let currentLang = 'tr';
let appState = {
  ort: null,
  raw: null,
  aylik: null,
  cok_yillik: null,
  rotationResult: null
};

// DOM references
const latInput = document.getElementById('latInput');
const lonInput = document.getElementById('lonInput');
const fieldSizeInput = document.getElementById('fieldSizeInput');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const mevcutCropSelect = document.getElementById('mevcutCrop');
const previousCropSelect = document.getElementById('previousCrop');
const addressInput = document.getElementById('addressInput');
const btnGeocode = document.getElementById('btnGeocode');

const pSu = document.getElementById('p_su');
const pToprak = document.getElementById('p_toprak');
const pKara = document.getElementById('p_kara');
const pGuclu = document.getElementById('p_guclu');

const judgmentTitle = document.getElementById('judgmentTitle');
const judgmentSub = document.getElementById('judgmentSub');
const bestYieldRatio = document.getElementById('bestYieldRatio');
const bestYieldPerDecare = document.getElementById('bestYieldPerDecare');

const scPrecip = document.getElementById('sc_precip');
const scTemp = document.getElementById('sc_temp');
const valScPrecip = document.getElementById('val_sc_precip');
const valScTemp = document.getElementById('val_sc_temp');

const cIrrigation = document.getElementById('c_irrigation');
const cMarket = document.getElementById('c_market');

const btnAnalyze = document.getElementById('btnAnalyze');
const btnLang = document.getElementById('btnLang');
const langText = document.getElementById('langText');
const statusBanner = document.getElementById('statusBanner');
const statusBannerText = document.getElementById('statusBannerText');

const welcomePlaceholder = document.getElementById('welcomePlaceholder');
const analysisContent = document.getElementById('analysisContent');

const valTemp = document.getElementById('valTemp');
const valPrecip = document.getElementById('valPrecip');
const valSolar = document.getElementById('valSolar');
const valWind = document.getElementById('valWind');

const bestCropName = document.getElementById('bestCropName');
const bestCropSub = document.getElementById('bestCropSub');

const strategiesContainer = document.getElementById('strategiesContainer');
const riskWarningsRow = document.getElementById('riskWarningsRow');

const incTotalYield = document.getElementById('incTotalYield');
const incPricePerKg = document.getElementById('incPricePerKg');
const incGrossRevenue = document.getElementById('incGrossRevenue');

const droughtLevel = document.getElementById('droughtLevel');
const droughtDesc = document.getElementById('droughtDesc');

let stressChartInstance = null;
let timelineChartInstance = null;
let leafletMap = null;
let mapMarker = null;

function showBanner(msg, isSuccess = false) {
  statusBannerText.textContent = msg;
  statusBanner.className = 'status-banner' + (isSuccess ? ' success' : '');
  statusBanner.style.display = 'block';
  setTimeout(() => { statusBanner.style.display = 'none'; }, 5000);
}

function formatDateForAPI(dateStr) {
  return dateStr.replace(/-/g, '');
}

function initLeaflet() {
  const initLat = parseFloat(latInput.value) || 37.8746;
  const initLon = parseFloat(lonInput.value) || 32.4932;

  leafletMap = L.map('map', {
    zoomControl: false,
    scrollWheelZoom: true
  }).setView([initLat, initLon], 7);

  L.control.zoom({ position: 'bottomright' }).addTo(leafletMap);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap'
  }).addTo(leafletMap);

  mapMarker = L.marker([initLat, initLon], { draggable: true }).addTo(leafletMap);

  leafletMap.on('click', (e) => { updateCoords(e.latlng.lat, e.latlng.lng); });
  mapMarker.on('dragend', (e) => {
    const latlng = e.target.getLatLng();
    updateCoords(latlng.lat, latlng.lng);
  });

  // --- NASA uydu overlay katmanları (NDVI +土壌 nem) ---
  window.ndviLayer = null;
  window.soilLayer = null;

  // UI toggle ekle (haritanın sağ alt köşesine)
  const toggleContainer = document.createElement('div');
  toggleContainer.style.position = 'absolute';
  toggleContainer.style.bottom = '10px';
  toggleContainer.style.right = '10px';
  toggleContainer.style.background = 'rgba(255,255,255,0.95)';
  toggleContainer.style.padding = '10px';
  toggleContainer.style.borderRadius = '6px';
  toggleContainer.style.border = '1px solid #bac6b4';
  toggleContainer.style.fontFamily = '"Plus Jakarta Sans", sans-serif';
  toggleContainer.style.fontSize = '12px';
  toggleContainer.style.zIndex = '1000';
  toggleContainer.innerHTML = `
    <div style="font-weight:600; margin-bottom:6px; color:#161c16;">NASA Uydu Katmanları</div>
    <label style="display:flex; align-items:center; gap:6px; margin-bottom:4px; cursor:pointer;">
      <input type="checkbox" id="toggleNdvi" />
      <span>NDVI / Bitki Yeşilişi (Landsat/S2)</span>
    </label>
    <label style="display:flex; align-items:center; gap:6px; margin-bottom:4px; cursor:pointer;">
      <input type="checkbox" id="toggleSoil" />
      <span>Toprak Nem (SMAP)</span>
    </label>
    <div id="overlayStatus" style="font-size:11px; color:#5e6b5f; margin-top:6px;"></div>
  `;
  document.body.appendChild(toggleContainer);

  const toggleNdvi = document.getElementById('toggleNdvi');
  const toggleSoil = document.getElementById('toggleSoil');
  const overlayStatus = document.getElementById('overlayStatus');

  async function fetchEkstra(lat, lon) {
    const start = formatDateForAPI('2023-01-01');
    const end = formatDateForAPI('2023-12-31');
    const res = await fetch('/api/analiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lat, lon, start, end })
    });
    if (!res.ok) return null;
    return await res.json();
  }

  function clearLayers() {
    if (window.ndviLayer) { leafletMap.removeLayer(window.ndviLayer); window.ndviLayer = null; }
    if (window.soilLayer) { leafletMap.removeLayer(window.soilLayer); window.soilLayer = null; }
  }

  async function applyOverlays(lat, lon) {
    clearLayers();
    const data = await fetchEkstra(lat, lon);
    if (!data) {
      overlayStatus.textContent = 'Veri alınamadı.';
      return;
    }
    const ekstra = data.ekstra || {};
    const msgs = [];

    // NDVI katmanı
    if (toggleNdvi.checked) {
      const ndvi = ekstra.landsat_ndvi || {};
      if (ndvi.available) {
        window.ndviLayer = L.circle([lat, lon], {
          radius: 1500,
          color: '#255d36',
          fillColor: '#255d36',
          fillOpacity: 0.35,
          weight: 2
        }).addTo(leafletMap);
        window.ndviLayer.bindPopup(`<b>Landsat/S2 NDVI</b><br>Mevcut: ${ndvi.scenes || 0} scene<br>${ndvi.note || ''}`);
        msgs.push('NDVI katmanı aktif');
      } else {
        window.ndviLayer = L.circle([lat, lon], {
          radius: 1500,
          color: '#9e3223',
          fillColor: '#9e3223',
          fillOpacity: 0.2,
          weight: 2,
          dashArray: '5, 5'
        }).addTo(leafletMap);
        window.ndviLayer.bindPopup('<b>NDVI</b><br>API anahtarı gerekli (USGS / Copernicus)');
        msgs.push('NDVI: kimlik gerekli');
      }
    }

    // Toprak nem katmanı
    if (toggleSoil.checked) {
      const smap = ekstra.smap || {};
      if (smap.available && smap.data_accessible) {
        window.soilLayer = L.circle([lat, lon], {
          radius: 2000,
          color: '#245c6e',
          fillColor: '#245c6e',
          fillOpacity: 0.4,
          weight: 2
        }).addTo(leafletMap);
        window.soilLayer.bindPopup(`<b>SMAP Toprak Nem</b><br>${smap.granules || 0} granule<br>${smap.note || ''}`);
        msgs.push('Toprak nem katmanı aktif');
      } else {
        window.soilLayer = L.circle([lat, lon], {
          radius: 2000,
          color: '#9e3223',
          fillColor: '#9e3223',
          fillOpacity: 0.2,
          weight: 2,
          dashArray: '5, 5'
        }).addTo(leafletMap);
        window.soilLayer.bindPopup('<b>SMAP</b><br>NASA Earthdata girişi gerekli');
        msgs.push('SMAP: giriş gerekli');
      }
    }

    overlayStatus.textContent = msgs.length ? msgs.join(' · ') : 'Seçili katman yok.';
  }

  toggleNdvi.addEventListener('change', async () => {
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);
    if (!isNaN(lat) && !isNaN(lon)) await applyOverlays(lat, lon);
  });

  toggleSoil.addEventListener('change', async () => {
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);
    if (!isNaN(lat) && !isNaN(lon)) await applyOverlays(lat, lon);
  });

  // Koordinat değişince overlay'leri yeniden çiz
  const origUpdateCoords = updateCoords;
  window.updateCoords = function(lat, lon) {
    origUpdateCoords(lat, lon);
    if (toggleNdvi.checked || toggleSoil.checked) {
      applyOverlays(lat, lon);
    }
  };
}

function updateCoords(lat, lon) {
  const roundedLat = parseFloat(lat.toFixed(4));
  const roundedLon = parseFloat(lon.toFixed(4));
  latInput.value = roundedLat;
  lonInput.value = roundedLon;
  if (mapMarker) mapMarker.setLatLng([roundedLat, roundedLon]);
}

async function geocodeAddress() {
  const query = addressInput.value.trim();
  if (!query) return;

  btnGeocode.disabled = true;
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;
    const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
    const data = await res.json();
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lon = parseFloat(data[0].lon);
      updateCoords(lat, lon);
      if (leafletMap) leafletMap.setView([lat, lon], 11);
      showBanner(data[0].display_name, true);
    } else {
      showBanner(currentLang === 'tr' ? 'Adres bulunamadı.' : 'Address not found.');
    }
  } catch {
    showBanner(currentLang === 'tr' ? 'Adres araması başarısız.' : 'Address search failed.');
  } finally {
    btnGeocode.disabled = false;
  }
}

let loadedCropsData = {};

async function loadCrops() {
  try {
    const res = await fetch('/api/bitkiler');
    if (!res.ok) throw new Error('Crops could not be loaded');
    loadedCropsData = await res.json();

    const emptyOpt = `<option value="">${I18N[currentLang].opt_empty_crop}</option>`;
    mevcutCropSelect.innerHTML = emptyOpt;

    populateHistorySelects();

    for (const [key, crop] of Object.entries(loadedCropsData)) {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = (currentLang === 'en' && crop.ad_en) ? crop.ad_en : crop.ad;
      mevcutCropSelect.appendChild(opt);
    }
  } catch (err) {
    console.error(err);
  }
}

function populateHistorySelects() {
  const selects = document.querySelectorAll('.previous-crop-select');
  selects.forEach(sel => {
    const currentVal = sel.value;
    sel.innerHTML = `<option value="">${I18N[currentLang].opt_prev_none}</option>`;
    for (const [key, crop] of Object.entries(loadedCropsData)) {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = (currentLang === 'en' && crop.ad_en) ? crop.ad_en : crop.ad;
      sel.appendChild(opt);
    }
    sel.value = currentVal;
  });
}

function getSelectedCropHistory() {
  const history = [];
  document.querySelectorAll('.previous-crop-select').forEach(sel => {
    if (sel.value) history.push(sel.value);
  });
  return history;
}

let historyCount = 1;
function addHistoryCropRow() {
  if (historyCount >= 4) return; // En fazla 4 yıl geçmiş
  historyCount++;
  const container = document.getElementById('cropHistoryContainer');
  const row = document.createElement('div');
  row.className = 'field-select-row crop-history-row';
  row.setAttribute('data-history-idx', historyCount);

  const labelText = currentLang === 'tr' 
    ? `${historyCount}. ${I18N.tr.lbl_year_prev}` 
    : `${historyCount} ${I18N.en.lbl_year_prev}`;

  row.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <label class="cell-label">${labelText}</label>
      <button type="button" class="subtle-link remove-hist-btn" style="color:var(--c-risk-red); font-size:11px;">✕</button>
    </div>
    <select class="field-select previous-crop-select">
      <option value="">${I18N[currentLang].opt_prev_none}</option>
    </select>
  `;

  const sel = row.querySelector('.previous-crop-select');
  for (const [key, crop] of Object.entries(loadedCropsData)) {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = (currentLang === 'en' && crop.ad_en) ? crop.ad_en : crop.ad;
    sel.appendChild(opt);
  }

  row.querySelector('.remove-hist-btn').addEventListener('click', () => {
    row.remove();
    historyCount--;
    if (appState.ort) debounceRotation();
  });

  sel.addEventListener('change', () => {
    if (appState.ort) debounceRotation();
  });

  container.appendChild(row);
}

function initPills() {
  document.querySelectorAll('.choice-pills').forEach(group => {
    const parentRow = group.closest('.weight-row');
    const hiddenInput = parentRow.querySelector('input[type="hidden"]');
    group.querySelectorAll('.choice-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        group.querySelectorAll('.choice-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        hiddenInput.value = btn.dataset.val;
        if (appState.ort) debounceRotation();
      });
    });
  });

  scPrecip.addEventListener('input', () => {
    valScPrecip.textContent = `${scPrecip.value}%`;
    if (appState.ort) debounceRotation();
  });

  scTemp.addEventListener('input', () => {
    valScTemp.textContent = `${scTemp.value}°C`;
    if (appState.ort) debounceRotation();
  });

  mevcutCropSelect.addEventListener('change', () => { if (appState.ort) debounceRotation(); });
  document.querySelectorAll('.previous-crop-select').forEach(sel => {
    sel.addEventListener('change', () => { if (appState.ort) debounceRotation(); });
  });
  cIrrigation.addEventListener('change', () => { if (appState.ort) debounceRotation(); });
  cMarket.addEventListener('change', () => { if (appState.ort) debounceRotation(); });
  fieldSizeInput.addEventListener('change', () => { if (appState.rotationResult) updateIncomeCard(appState.rotationResult); });
}

let debounceTimer = null;
function debounceRotation() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => runRotationCalculation(), 250);
}

function setLanguage(lang) {
  currentLang = lang;
  langText.textContent = I18N[lang].lang_code;
  document.documentElement.lang = lang;

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (I18N[lang][key]) el.textContent = I18N[lang][key];
  });

  // Update placeholders
  if (addressInput) {
    addressInput.placeholder = I18N[lang].ph_address;
  }

  // Update crop select option labels for language
  updateSelectOptionsLanguage(lang);

  // Update history crop labels
  document.querySelectorAll('.crop-history-row').forEach(row => {
    const idx = row.getAttribute('data-history-idx');
    const lbl = row.querySelector('.cell-label');
    if (lbl) {
      if (idx === '1') {
        lbl.textContent = I18N[lang].lbl_prev_crop;
      } else {
        lbl.textContent = lang === 'tr' ? `${idx}. ${I18N.tr.lbl_year_prev}` : `${idx} ${I18N.en.lbl_year_prev}`;
      }
    }
  });

  const btnAdd = document.getElementById('btnAddHistoryCrop');
  if (btnAdd && I18N[lang].btn_add_history) {
    btnAdd.textContent = I18N[lang].btn_add_history;
  }

  if (appState.ort) {
    runRotationCalculation();
  }
}

function updateSelectOptionsLanguage(lang) {
  // Update fallow option in mevcut
  if (mevcutCropSelect && mevcutCropSelect.options.length > 0) {
    mevcutCropSelect.options[0].textContent = I18N[lang].opt_empty_crop;
    for (let i = 1; i < mevcutCropSelect.options.length; i++) {
      const opt = mevcutCropSelect.options[i];
      const crop = loadedCropsData[opt.value];
      if (crop) {
        opt.textContent = (lang === 'en' && crop.ad_en) ? crop.ad_en : crop.ad;
      }
    }
  }

  // Update history selects
  document.querySelectorAll('.previous-crop-select').forEach(sel => {
    if (sel.options.length > 0) {
      sel.options[0].textContent = I18N[lang].opt_prev_none;
      for (let i = 1; i < sel.options.length; i++) {
        const opt = sel.options[i];
        const crop = loadedCropsData[opt.value];
        if (crop) {
          opt.textContent = (lang === 'en' && crop.ad_en) ? crop.ad_en : crop.ad;
        }
      }
    }
  });
}

async function runFullAnalysis() {
  const lat = parseFloat(latInput.value);
  const lon = parseFloat(lonInput.value);
  const start = formatDateForAPI(startDateInput.value);
  const end = formatDateForAPI(endDateInput.value);

  if (isNaN(lat) || isNaN(lon)) {
    showBanner(currentLang === 'tr' ? 'Lütfen geçerli koordinat girin.' : 'Please enter valid coordinates.');
    return;
  }

  if (!start || !end || start >= end) {
    showBanner(currentLang === 'tr' ? 'Bitiş tarihi başlangıçtan sonra olmalı.' : 'End date must be after start date.');
    return;
  }

  btnAnalyze.disabled = true;
  btnAnalyze.querySelector('.btn-spinner').style.display = 'inline-block';
  btnAnalyze.querySelector('.btn-label').textContent = I18N[currentLang].btn_running;

  try {
    const res = await fetch('/api/analiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lat, lon, start, end })
    });

    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || 'NASA POWER data unavailable.');

    appState.ort = data.ortalama;
    appState.raw = data.raw;
    appState.aylik = data.aylik || null;
    appState.cok_yillik = data.cok_yillik || null;

    valTemp.textContent = appState.ort.sıcaklık_C;
    valPrecip.textContent = appState.ort.yağış_mm_gun;
    valSolar.textContent = appState.ort.güneş_MJ_m2_gun;
    valWind.textContent = appState.ort.rüzgar_m_s;

    // Drought risk
    updateDroughtCard(appState.ort.yağış_mm_gun);

    welcomePlaceholder.style.display = 'none';
    analysisContent.style.display = 'block';

    renderTimelineChart(appState.raw);
    await runRotationCalculation();

    showBanner(currentLang === 'tr' ? 'NASA iklim verileri başarıyla işlendi!' : 'NASA climate data loaded successfully!', true);
  } catch (err) {
    showBanner(`Error: ${err.message}`);
  } finally {
    btnAnalyze.disabled = false;
    btnAnalyze.querySelector('.btn-spinner').style.display = 'none';
    btnAnalyze.querySelector('.btn-label').textContent = I18N[currentLang].btn_run_analysis;
  }
}

function updateDroughtCard(precipMmDay) {
  const assessment = getDroughtAssessment(precipMmDay, currentLang);
  droughtLevel.innerHTML = `<span class="status-indicator ${assessment.levelClass}"></span><span>${assessment.level}</span>`;
  droughtDesc.textContent = assessment.desc;
}

function updateIncomeCard(data) {
  if (!data || !data.en_iyi_bitki) return;
  const bitkiKey = data.en_iyi_bitki.anahtar || '';
  const cropInfo = loadedCropsData[bitkiKey] || {};
  const fieldSize = parseFloat(fieldSizeInput.value) || 50;

  const verim = cropInfo.verim_kg_donum || 300;
  const fiyat = cropInfo.fiyat_tl_kg || 15.0;

  const totalYield = Math.round(verim * fieldSize);
  const gross = Math.round(totalYield * fiyat);

  incTotalYield.textContent = `${totalYield.toLocaleString()} kg`;
  incPricePerKg.textContent = `${fiyat} ₺/kg`;
  incGrossRevenue.textContent = `${gross.toLocaleString()} ₺`;
}

async function runRotationCalculation() {
  if (!appState.ort) return;

  const oncelikler = {
    su_tasarimi: parseInt(pSu.value),
    toprak_sagligi: parseInt(pToprak.value),
    kararli_verim: parseInt(pKara.value),
    guclu_koşullar: parseInt(pGuclu.value)
  };

  const scenario = {
    precip_change_pct: parseFloat(scPrecip.value),
    temp_change_c: parseFloat(scTemp.value)
  };

  const constraints = {
    irrigation: cIrrigation.value || null,
    market_preference: cMarket.value || null
  };

  const historyList = getSelectedCropHistory();

  const payload = {
    ortalama: appState.ort,
    aylik: appState.aylik || null,
    cok_yillik: appState.cok_yillik || null,
    oncelikler,
    mevcut: mevcutCropSelect.value || null,
    onceki: historyList.length > 0 ? historyList[0] : null,
    gecmis_bitkiler: historyList,
    scenario,
    constraints,
    lang: currentLang
  };

  try {
    const res = await fetch('/api/rotasyon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || 'Rotation could not be calculated.');

    appState.rotationResult = data;
    renderResultsUI(data);

    // Also update drought card with fresh lang
    if (appState.ort) updateDroughtCard(appState.ort.yağış_mm_gun);
  } catch (err) {
    console.error(err);
  }
}

function renderResultsUI(data) {
  // Risk notices
  riskWarningsRow.innerHTML = '';
  if (data.risk_uyarilari && data.risk_uyarilari.length > 0) {
    riskWarningsRow.style.display = 'flex';
    data.risk_uyarilari.forEach((risk) => {
      const box = document.createElement('div');
      box.className = 'risk-notice-entry';
      box.textContent = risk.mesaj;
      riskWarningsRow.appendChild(box);
    });
  } else {
    riskWarningsRow.style.display = 'none';
  }

  // Hero Crop Card
  if (data.en_iyi_bitki) {
    const bitkiKey = data.en_iyi_bitki.anahtar || '';
    const cropInfo = loadedCropsData[bitkiKey] || {};
    bestCropName.textContent = (currentLang === 'en' && cropInfo.ad_en) ? cropInfo.ad_en : data.en_iyi_bitki.bitki;

    const judgment = getFarmerJudgment(data.en_iyi_bitki.skor, currentLang);
    judgmentTitle.textContent = judgment.title;
    judgmentSub.textContent = judgment.sub;

    const metrics = CROP_METRICS[bitkiKey] || {
      ratio_en: cropInfo.oran_en || 'Yields 1:8', ratio_tr: cropInfo.oran || "1'e 8 Verir",
      yield_en: `${cropInfo.verim_kg_donum || 300} kg / decare`, yield_tr: `${cropInfo.verim_kg_donum || 300} kg / dönüm`
    };
    bestYieldRatio.textContent = currentLang === 'tr' ? metrics.ratio_tr : metrics.ratio_en;
    bestYieldPerDecare.textContent = currentLang === 'tr' ? metrics.yield_tr : metrics.yield_en;

    const grup = data.en_iyi_bitki.grup ? ` · ${data.en_iyi_bitki.grup.toUpperCase()}` : '';
    bestCropSub.textContent = (currentLang === 'tr'
      ? 'Mevcut iklim rejimine ve toprak hedeflerinize en yüksek bereketi sağlayan ana ürün'
      : 'Highest yielding and most suitable crop for your field conditions') + grup;

    // Income card
    updateIncomeCard(data);
  }

  // Statistical Trend Analysis (SI) Panel
  renderSITrendUI(data.si_analiz);

  // 3-Year Rotation Plan Roadmap Cards
  const rotationGrid = document.getElementById('rotationCardsGrid');
  if (rotationGrid && data.rotasyon_plani) {
    rotationGrid.innerHTML = '';
    data.rotasyon_plani.forEach(item => {
      const card = document.createElement('div');
      card.className = 'roadmap-year-card';
      const isHealing = item.toprak_etkisi === 'iyileştirici';
      const roleText = currentLang === 'tr' ? item.rol : (item.rol_en || item.rol);
      const descText = currentLang === 'tr' ? item.aciklama : (item.aciklama_en || item.aciklama);
      const yearLabel = currentLang === 'tr' ? `${item.yil}. Yıl` : `Year ${item.yil}`;

      const cropInfo = loadedCropsData[item.anahtar] || {};
      const cropName = (currentLang === 'en' && cropInfo.ad_en) ? cropInfo.ad_en : item.bitki;

      card.innerHTML = `
        <span class="year-pill">${yearLabel}</span>
        <h4 class="year-crop-name">${cropName}</h4>
        <span class="year-role-tag ${isHealing ? '' : 'neutral'}">${roleText}</span>
        <p class="year-desc">${descText}</p>
        <div class="year-metrics-strip">
          <span>${currentLang === 'tr' ? 'Tahmini Verim:' : 'Est. Yield:'} <strong>${item.verim_kg} kg/da</strong></span>
          <span>${currentLang === 'tr' ? 'Piyasa:' : 'Market:'} <strong>${item.fiyat_tl} ₺/kg</strong></span>
        </div>
      `;
      rotationGrid.appendChild(card);
    });

    // Update dynamic ecological impact strip
    const hasLegume = data.rotasyon_plani.some(item => item.toprak_etkisi === 'iyileştirici');
    const ecoNitrogen = document.getElementById('ecoNitrogenSave');
    const ecoWater = document.getElementById('ecoWaterSave');
    const ecoSoil = document.getElementById('ecoSoilHealth');

    if (ecoNitrogen) ecoNitrogen.textContent = hasLegume ? '~%32' : '~%15';
    if (ecoWater) ecoWater.textContent = (appState.ort && appState.ort.yağış_mm_gun < 1.5) ? '~%38' : '~%25';
    if (ecoSoil) ecoSoil.textContent = hasLegume ? (currentLang === 'tr' ? 'Onarıcı (+%1.8)' : 'Restorative (+1.8%)') : (currentLang === 'tr' ? 'Dengeli' : 'Balanced');
  }

  // 3 Strategy Cards
  strategiesContainer.innerHTML = '';
  if (data.stratejiler) {
    data.stratejiler.forEach((strat, idx) => {
      const card = document.createElement('div');
      card.className = 'strategy-column-card';
      const stratCropInfo = loadedCropsData[strat.anahtar || ''] || {};
      const stratCropName = (currentLang === 'en' && stratCropInfo.ad_en) ? stratCropInfo.ad_en : strat.bitki;

      card.innerHTML = `
        <span class="strat-card-tag">${currentLang === 'tr' ? (idx + 1) + '. Yol' : 'Route ' + (idx + 1)}</span>
        <h4 class="strat-card-title">${strat.ad}</h4>
        <div class="strat-crop-row">
          <span class="strat-crop-name">${stratCropName}</span>
          <span class="strat-crop-score">${strat.skor} / 100</span>
        </div>
        <p class="strat-narrative">${strat.neden}</p>
        <ul class="strat-points">
          <li><strong>${currentLang === 'tr' ? 'Kanıt:' : 'Evidence:'}</strong> ${strat.kanit || '--'}</li>
          <li><strong>${currentLang === 'tr' ? 'Kazanım:' : 'Gain:'}</strong> ${(strat.faydalar || []).join(', ')}</li>
          <li><strong>${currentLang === 'tr' ? 'Önlem:' : 'Precaution:'}</strong> ${(strat.riskler || []).join(', ')}</li>
        </ul>
      `;
      strategiesContainer.appendChild(card);
    });
  }

  // Stress Chart
  if (data.stres_takvimi) renderStressChart(data.stres_takvimi);
}

function renderSITrendUI(si) {
  const section = document.getElementById('siTrendSection');
  const cardsContainer = document.getElementById('siTrendCards');
  const interpEl = document.getElementById('siInterpretation');
  const badgeEl = document.getElementById('siConfidenceBadge');

  if (!section || !cardsContainer) return;

  if (!si || !si.sicaklik_trend || !si.yagis_trend) {
    section.style.display = 'none';
    return;
  }

  section.style.display = 'block';

  const tTrend = si.sicaklik_trend;
  const pTrend = si.yagis_trend;
  const tSlopeStr = `${tTrend.slope > 0 ? '+' : ''}${tTrend.slope.toFixed(2)}°C${I18N[currentLang].si_per_year}`;
  const pSlopeStr = `${pTrend.slope > 0 ? '+' : ''}${pTrend.slope.toFixed(3)} mm${I18N[currentLang].si_per_year}`;

  const tAnom = tTrend.anomali;
  const pAnom = pTrend.anomali;

  function anomalyBadge(anom) {
    if (!anom) return '';
    if (anom.anomaly) {
      const dirText = anom.direction === 'above' 
        ? (currentLang === 'tr' ? 'Ortalama Üstü (+Z)' : 'Above Mean (+Z)')
        : (currentLang === 'tr' ? 'Ortalama Altı (-Z)' : 'Below Mean (-Z)');
      return `<span class="si-card-anomaly anomaly-warn">Z=${anom.z} · ${dirText}</span>`;
    }
    return `<span class="si-card-anomaly anomaly-norm">${currentLang === 'tr' ? 'Normal Aralık (Z=' + anom.z + ')' : 'Normal Range (Z=' + anom.z + ')'}</span>`;
  }

  cardsContainer.innerHTML = `
    <div class="si-card">
      <span class="si-card-label">${I18N[currentLang].si_temp_trend}</span>
      <div class="si-card-metric">${tSlopeStr}</div>
      <span class="si-card-sub">OLS: R² = ${tTrend.r2.toFixed(2)}</span>
      ${anomalyBadge(tAnom)}
    </div>
    <div class="si-card">
      <span class="si-card-label">${I18N[currentLang].si_precip_trend}</span>
      <div class="si-card-metric">${pSlopeStr}</div>
      <span class="si-card-sub">OLS: R² = ${pTrend.r2.toFixed(2)}</span>
      ${anomalyBadge(pAnom)}
    </div>
    <div class="si-card">
      <span class="si-card-label">${I18N[currentLang].si_confidence}</span>
      <div class="si-card-metric">${si.guven_duzeyi}%</div>
      <span class="si-card-sub">${currentLang === 'tr' ? 'Ortalama Korelasyon Uyumu' : 'Mean Correlation Fit'}</span>
    </div>
  `;

  if (interpEl) interpEl.textContent = si.yorumlama || '';
  if (badgeEl && si.yillar && si.yillar.length) {
    badgeEl.textContent = currentLang === 'tr' 
      ? `NASA POWER ${si.yillar[0]}–${si.yillar[si.yillar.length - 1]} (${si.yillar.length} Yıl)`
      : `NASA POWER ${si.yillar[0]}–${si.yillar[si.yillar.length - 1]} (${si.yillar.length} Years)`;
  }
}

function renderStressChart(stress) {
  const ctx = document.getElementById('stressChart').getContext('2d');
  if (stressChartInstance) stressChartInstance.destroy();

  const labels = stress.aylar.map(a => a.ay_adi);
  const tempStress = stress.aylar.map(a => a.temp_stress);
  const waterStress = stress.aylar.map(a => a.water_stress);
  const ndvi = stress.aylar.map(a => Math.round(a.ndvi_proxy * 100));

  stressChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: currentLang === 'tr' ? 'Sıcaklık Stresi (%)' : 'Thermal Stress (%)',
          data: tempStress,
          borderColor: '#b47b2b',
          backgroundColor: 'rgba(180,123,43,0.08)',
          fill: true, tension: 0.3, pointRadius: 3
        },
        {
          label: currentLang === 'tr' ? 'Su Stresi (%)' : 'Moisture Deficit (%)',
          data: waterStress,
          borderColor: '#236477',
          backgroundColor: 'rgba(35,100,119,0.08)',
          fill: true, tension: 0.3, pointRadius: 3
        },
        {
          label: currentLang === 'tr' ? 'NDVI Büyüme Eğrisi' : 'NDVI Phenology',
          data: ndvi,
          borderColor: '#255d36',
          backgroundColor: 'transparent',
          borderDash: [4, 4], tension: 0.3, pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, max: 100, grid: { color: '#e5ebe0' }, ticks: { font: { family: 'JetBrains Mono', size: 11 }, color: '#5e6b5f' } },
        x: { grid: { display: false }, ticks: { font: { family: 'Plus Jakarta Sans', size: 11 }, color: '#5e6b5f' } }
      }
    }
  });
}

function renderTimelineChart(raw) {
  const ctx = document.getElementById('timelineChart').getContext('2d');
  if (timelineChartInstance) timelineChartInstance.destroy();

  const p = raw.properties?.parameter || {};
  const dates = Object.keys(p.T2M || {}).sort();
  if (!dates.length) return;

  const labels = dates.map(d => `${d.slice(6, 8)}/${d.slice(4, 6)}`);
  const t2mData = dates.map(d => p.T2M[d]);
  const precData = dates.map(d => p.PRECTOTCORR[d]);

  timelineChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: currentLang === 'tr' ? 'Sıcaklık (°C)' : 'Temperature (°C)',
          data: t2mData, borderColor: '#b47b2b',
          backgroundColor: 'transparent', tension: 0.2, yAxisID: 'y'
        },
        {
          label: currentLang === 'tr' ? 'Yağış (mm/gün)' : 'Rain (mm/day)',
          data: precData, borderColor: '#236477',
          backgroundColor: 'rgba(35,100,119,0.15)', tension: 0.2, yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { type: 'linear', position: 'left', grid: { color: '#e5ebe0' }, ticks: { font: { family: 'JetBrains Mono', size: 11 } } },
        y1: { type: 'linear', position: 'right', grid: { display: false }, ticks: { font: { family: 'JetBrains Mono', size: 11 } } },
        x: { grid: { display: false }, ticks: { font: { family: 'JetBrains Mono', size: 10 } } }
      }
    }
  });
}

function downloadReport() {
  if (!appState.ort || !appState.rotationResult) {
    showBanner(currentLang === 'tr' ? 'Lütfen önce analizi tamamlayın.' : 'Please complete analysis first.');
    return;
  }
  const ort = appState.ort;
  const res = appState.rotationResult;
  const fieldSize = parseFloat(fieldSizeInput.value) || 50;
  const lines = [
    '=====================================================',
    '  FIELD SHIFT — NASA SPACE APPS DECISION REPORT    ',
    '=====================================================',
    `Date: ${new Date().toLocaleString()}`,
    `Location: Lat ${latInput.value}°N, Lon ${lonInput.value}°E`,
    `Period: ${startDateInput.value} → ${endDateInput.value}`,
    `Field size: ${fieldSize} decare`,
    '',
    '1. NASA POWER CLIMATE OBSERVATIONS (DAILY AVG)',
    '-----------------------------------------------------',
    `- Mean Temperature: ${ort.sıcaklık_C} °C`,
    `- Daily Rainfall: ${ort.yağış_mm_gun} mm/day`,
    `- Solar Radiation: ${ort.güneş_MJ_m2_gun} MJ/m²/day`,
    `- Wind Speed: ${ort.rüzgar_m_s} m/s`,
    '',
    '2. ROTATION STRATEGIES',
    '-----------------------------------------------------'
  ];

  (res.stratejiler || []).forEach((strat, i) => {
    lines.push(`Route ${i + 1}: ${strat.ad}`);
    lines.push(`  Crop: ${strat.bitki} (Score: ${strat.skor}/100)`);
    lines.push(`  Rationale: ${strat.neden}`);
    lines.push(`  Evidence: ${strat.kanit}`);
    lines.push(`  Gains: ${(strat.faydalar || []).join(', ')}`);
    lines.push(`  Precautions: ${(strat.riskler || []).join(', ')}`);
    lines.push('');
  });

  if (res.si_analiz) {
    const si = res.si_analiz;
    lines.push('3. STATISTICAL INFERENCE (SI) & 5-YEAR CLIMATE TREND');
    lines.push('-----------------------------------------------------');
    lines.push(`- Temperature Trend: ${si.sicaklik_trend.slope > 0 ? '+' : ''}${si.sicaklik_trend.slope}°C/yr (R²=${si.sicaklik_trend.r2})`);
    if (si.sicaklik_trend.anomali) {
      lines.push(`  Anomaly (latest year): Z=${si.sicaklik_trend.anomali.z} (${si.sicaklik_trend.anomali.anomaly ? 'Significant Anomaly' : 'Normal Range'})`);
    }
    lines.push(`- Precipitation Trend: ${si.yagis_trend.slope > 0 ? '+' : ''}${si.yagis_trend.slope} mm/day/yr (R²=${si.yagis_trend.r2})`);
    if (si.yagis_trend.anomali) {
      lines.push(`  Anomaly (latest year): Z=${si.yagis_trend.anomali.z} (${si.yagis_trend.anomali.anomaly ? 'Significant Anomaly' : 'Normal Range'})`);
    }
    lines.push(`- Model Fit / Confidence: ${si.guven_duzeyi}%`);
    lines.push(`- Interpretation: ${si.yorumlama}`);
    lines.push('');
  }

  if (res.risk_uyarilari && res.risk_uyarilari.length) {
    lines.push('4. RISK WARNINGS');
    lines.push('-----------------------------------------------------');
    res.risk_uyarilari.forEach(r => lines.push(`- ${r.mesaj}`));
    lines.push('');
  }

  lines.push('Data Source: NASA POWER Daily Agroclimatology (power.larc.nasa.gov)');
  lines.push('Note: This report is a decision support simulation.');

  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `field_shift_report_${formatDateForAPI(startDateInput.value)}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function setupUIListeners() {
  // Geocode button
  btnGeocode?.addEventListener('click', geocodeAddress);
  addressInput?.addEventListener('keydown', (e) => { if (e.key === 'Enter') geocodeAddress(); });

  // Geolocate
  document.getElementById('btnGeolocate')?.addEventListener('click', () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        updateCoords(pos.coords.latitude, pos.coords.longitude);
        if (leafletMap) leafletMap.setView([pos.coords.latitude, pos.coords.longitude], 10);
      }, () => {
        showBanner(currentLang === 'tr' ? 'Cihaz konumuna erişilemedi.' : 'Could not access device location.');
      });
    }
  });

  // Tabs
  document.querySelectorAll('.tabs-group .tab-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tabs-group .tab-toggle').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.dataset.tab;
      document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
      const activePane = document.getElementById(targetId);
      if (activePane) activePane.style.display = 'block';
    });
  });

  document.getElementById('btnDownloadReport')?.addEventListener('click', downloadReport);
  document.getElementById('btnPrintReport')?.addEventListener('click', () => { window.print(); });
  btnAnalyze.addEventListener('click', runFullAnalysis);
  btnLang.addEventListener('click', () => { setLanguage(currentLang === 'en' ? 'tr' : 'en'); });
  document.getElementById('btnAddHistoryCrop')?.addEventListener('click', addHistoryCropRow);

  // Coord inputs sync to map
  [latInput, lonInput].forEach(inp => {
    inp.addEventListener('change', () => {
      const lat = parseFloat(latInput.value);
      const lon = parseFloat(lonInput.value);
      if (!isNaN(lat) && !isNaN(lon) && mapMarker) {
        mapMarker.setLatLng([lat, lon]);
        leafletMap.panTo([lat, lon]);
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  initLeaflet();
  await loadCrops();
  initPills();
  setupUIListeners();
  setLanguage('tr'); // Varsayılan Türkçe
});
