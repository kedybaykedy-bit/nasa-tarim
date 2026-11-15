// ============================================================================
// Field Shift — High Performance, Clean & Robust Frontend Logic (v2.0)
// ============================================================================

// --- Translations & Localization ---
const I18N = {
  tr: {
    lang_code: 'EN',
    loc_title: 'Tarla Konumu',
    map_hint: 'Haritaya tıklayarak nokta seçebilirsiniz',
    lbl_lat: 'Enlem (°N)',
    lbl_lon: 'Boylam (°E)',
    date_title: 'Tarih Aralığı',
    lbl_start: 'Başlangıç (Ekim)',
    lbl_end: 'Bitiş (Hasat)',
    pref_title: 'Çiftçi Öncelikleri & Rotasyon',
    lbl_current_crop: 'Şu Anda Ekili Olan Ürün:',
    opt_empty_crop: 'Seçilmedi (Boş tarla / Yeni ekim)',
    lbl_prev_crop: 'Geçen Yıl Ekilen Ürün:',
    opt_prev_none: 'Bilmiyorum / İlk yıl',
    p_water: '💧 Su Tasarrufu',
    p_soil: '🌿 Toprak Sağlığı',
    p_yield: '📈 Kararlı Verim',
    p_resilience: '🛡️ Zorlu Koşul Direnci',
    advanced_title: '⚙️ Gelişmiş Senaryo & Kısıtlar',
    lbl_precip_change: 'Yağış Değişimi Simülasyonu (%)',
    lbl_temp_change: 'Sıcaklık Değişimi Simülasyonu (°C)',
    lbl_irrigation: 'Sulama Durumu',
    opt_irr_any: 'Farketmez / Belirtilmemiş',
    opt_irr_yes: 'Sulama Var',
    opt_irr_no: 'Sulama Yok (Kuru)',
    lbl_market: 'Pazar Hedefi',
    opt_mkt_any: 'Tümü',
    opt_mkt_kislik: 'Kışlık Ürünler',
    opt_mkt_yazlik: 'Yazlık Ürünler',
    opt_mkt_bahar: 'Bahar Ürünleri',
    lbl_field_size: 'Tarla Alanı (decare)',
    btn_run_analysis: 'NASA Verisini Çek & Analiz Et',
    btn_running: 'NASA Verileri Alınıyor...',
    welcome_title: 'NASA POWER Verileriyle Ekin Önerisi Alın',
    welcome_desc: 'Sol panelden tarlanızı haritada seçip tarih aralığını belirleyin, ardından "NASA Verisini Çek & Analiz Et" butonuna basın.',
    m_temp: 'Ort. Sıcaklık',
    m_precip: 'Günlük Yağış',
    m_solar: 'Güneş Enerjisi',
    m_wind: 'Rüzgar Hızı',
    best_match_badge: '⭐ En Yüksek Uyumlu Ekin',
    score_label: '/ 100',
    strategies_heading: '🎯 3 Farklı Rotasyon Stratejisi',
    strategies_sub: 'Hedefinize göre en uygun planı seçin',
    tab_stress: '📅 12 Aylık Stres & Büyüme Takvimi',
    tab_timeline: '📈 Günlük NASA Ölçümleri',
    btn_report: 'Rapor İndir (.txt)',
    leg_temp: 'Sıcaklık Stresi',
    leg_water: 'Su Stresi',
    leg_ndvi: 'NDVI (Bitki Gelişim Tahmini)',
    disclaimer_title: 'Karar Destek Notu:',
    disclaimer_text: 'Bu sistem karar destek amaçlı bir simülasyondur. Saha ekimi öncesi il/ilçe tarım müdürlükleri ve ziraat mühendisleri görüşü esastır.',
    rotation_sequence: '🔄 3 Yıllık Rotasyon Dizisi',
    rotation_year: 'Yıl',
    rotation_role: 'Rol',
    nitrogen_fixer: 'Azot Bağlayıcı',
    cover_crop: 'Örtü Bitkisi',
    main_crop: 'Ana Ürün',
    low_water: 'Düşük Su',
    income_estimate: '💰 Gelir Tahmini',
    field_size_decare: 'Alan (decare)',
    estimated_income: 'Tahmini Brüt Gelir',
    calc_note: 'Verim × Alan × Pazar Fiyatı',
    currency_try: '₺',
  },
  en: {
    lang_code: 'TR',
    loc_title: 'Field Location',
    map_hint: 'Click on the map to set location',
    lbl_lat: 'Latitude (°N)',
    lbl_lon: 'Longitude (°E)',
    date_title: 'Date Range',
    lbl_start: 'Start Date (Planting)',
    lbl_end: 'End Date (Harvest)',
    pref_title: 'Farmer Priorities & Rotation',
    lbl_current_crop: 'Currently Planted Crop:',
    opt_empty_crop: 'None (Fallow / New planting)',
    lbl_prev_crop: 'Crop Planted Last Year:',
    opt_prev_none: "Don't remember / First year",
    p_water: '💧 Water Conservation',
    p_soil: '🌿 Soil Health',
    p_yield: '📈 Stable Yield',
    p_resilience: '🛡️ Hardiness & Resilience',
    advanced_title: '⚙️ Advanced Scenarios & Constraints',
    lbl_precip_change: 'Precipitation Change Sim (%)',
    lbl_temp_change: 'Temperature Change Sim (°C)',
    lbl_irrigation: 'Irrigation Setup',
    opt_irr_any: 'Any / Unspecified',
    opt_irr_yes: 'Irrigated',
    opt_irr_no: 'Rainfed (No Irrigation)',
    lbl_market: 'Market Preference',
    opt_mkt_any: 'All Markets',
    opt_mkt_kislik: 'Winter Crops',
    opt_mkt_yazlik: 'Summer Crops',
    opt_mkt_bahar: 'Spring Crops',
    lbl_field_size: 'Field Size (decare)',
    btn_run_analysis: 'Fetch NASA Data & Analyze',
    btn_running: 'Fetching NASA Climate Data...',
    welcome_title: 'Get Crop Recommendations via NASA POWER Data',
    welcome_desc: 'Select your field on the map, set dates, and click "Fetch NASA Data & Analyze".',
    m_temp: 'Avg. Temp',
    m_precip: 'Daily Rain',
    m_solar: 'Solar Energy',
    m_wind: 'Wind Speed',
    best_match_badge: '⭐ Top Recommended Crop',
    score_label: '/ 100',
    strategies_heading: '🎯 3 Rotation Strategies',
    strategies_sub: 'Choose the best path for your agricultural target',
    tab_stress: '📅 12-Month Stress & Growth Calendar',
    tab_timeline: '📈 Daily NASA Measurements',
    btn_report: 'Download Report (.txt)',
    leg_temp: 'Temp Stress',
    leg_water: 'Water Stress',
    leg_ndvi: 'NDVI (Vegetation Proxy)',
    disclaimer_title: 'Decision Support Note:',
    disclaimer_text: 'This system provides simulation for decision support. Consult local agricultural authorities and agronomists before planting.',
    rotation_sequence: '🔄 3-Year Rotation Sequence',
    rotation_year: 'Year',
    rotation_role: 'Role',
    nitrogen_fixer: 'Nitrogen Fixer',
    cover_crop: 'Cover Crop',
    main_crop: 'Main Crop',
    low_water: 'Low Water',
    income_estimate: '💰 Income Estimate',
    field_size_decare: 'Area (decare)',
    estimated_income: 'Estimated Gross Income',
    calc_note: 'Yield × Area × Market Price',
    currency_try: '₺',
  }
};

let currentLang = 'tr';
let appState = {
  ort: null,
  raw: null,
  rotationResult: null,
  isAnalyzing: false
};

// --- DOM References ---
const latInput = document.getElementById('latInput');
const lonInput = document.getElementById('lonInput');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const mevcutCropSelect = document.getElementById('mevcutCrop');
const oncekiCropSelect = document.getElementById('oncekiCrop');
const fieldSizeInput = document.getElementById('fieldSize');

const pSu = document.getElementById('p_su');
const pToprak = document.getElementById('p_toprak');
const pKara = document.getElementById('p_kara');
const pGuclu = document.getElementById('p_guclu');

const valPSu = document.getElementById('val_p_su');
const valPToprak = document.getElementById('val_p_toprak');
const valPKara = document.getElementById('val_p_kara');
const valPGuclu = document.getElementById('val_p_guclu');

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

// Metrics
const valTemp = document.getElementById('valTemp');
const valPrecip = document.getElementById('valPrecip');
const valSolar = document.getElementById('valSolar');
const valWind = document.getElementById('valWind');

// Featured Card
const bestCropName = document.getElementById('bestCropName');
const bestCropScore = document.getElementById('bestCropScore');
const bestCropSub = document.getElementById('bestCropSub');

// Strategies Container
const strategiesContainer = document.getElementById('strategiesContainer');
const riskWarningsRow = document.getElementById('riskWarningsRow');

// Rotation Sequence
const rotationContainer = document.getElementById('rotationContainer');

// Income Estimate
const incomeContainer = document.getElementById('incomeContainer');
const incomeVal = document.getElementById('incomeVal');
const incomeNote = document.getElementById('incomeNote');

// Charts
let stressChartInstance = null;
let timelineChartInstance = null;
let leafletMap = null;
let mapMarker = null;

// --- Helper Functions ---
function showBanner(msg, isSuccess = false) {
  statusBannerText.textContent = msg;
  statusBanner.className = 'status-banner' + (isSuccess ? ' success' : '');
  statusBanner.style.display = 'block';
  setTimeout(() => {
    statusBanner.style.display = 'none';
  }, 5000);
}

function formatDateForAPI(dateStr) {
  return dateStr.replace(/-/g, '');
}

// --- Map Initialization ---
function initLeaflet() {
  const initLat = parseFloat(latInput.value) || 41.0082;
  const initLon = parseFloat(lonInput.value) || 28.9784;

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

  leafletMap.on('click', (e) => {
    updateCoords(e.latlng.lat, e.latlng.lng);
  });

  mapMarker.on('dragend', (e) => {
    const latlng = e.target.getLatLng();
    updateCoords(latlng.lat, latlng.lng);
  });
}

function updateCoords(lat, lon) {
  const roundedLat = parseFloat(lat.toFixed(4));
  const roundedLon = parseFloat(lon.toFixed(4));
  latInput.value = roundedLat;
  lonInput.value = roundedLon;
  if (mapMarker) {
    mapMarker.setLatLng([roundedLat, roundedLon]);
  }
}

// --- Crop Options Loader ---
async function loadCrops() {
  try {
    const res = await fetch('/api/bitkiler');
    if (!res.ok) throw new Error('Bitkiler yüklenemedi');
    const crops = await res.json();

    mevcutCropSelect.innerHTML = `<option value="">${I18N[currentLang].opt_empty_crop}</option>`;
    oncekiCropSelect.innerHTML = `<option value="">${I18N[currentLang].opt_prev_none}</option>`;

    for (const [key, crop] of Object.entries(crops)) {
      const opt1 = document.createElement('option');
      opt1.value = key;
      opt1.textContent = crop.ad;
      mevcutCropSelect.appendChild(opt1);

      const opt2 = document.createElement('option');
      opt2.value = key;
      opt2.textContent = crop.ad;
      oncekiCropSelect.appendChild(opt2);
    }
  } catch (err) {
    console.error(err);
  }
}

// --- Sliders Listeners ---
function initSliders() {
  const sliders = [
    { input: pSu, val: valPSu },
    { input: pToprak, val: valPToprak },
    { input: pKara, val: valPKara },
    { input: pGuclu, val: valPGuclu }
  ];

  sliders.forEach(({ input, val }) => {
    input.addEventListener('input', () => {
      val.textContent = input.value;
      if (appState.ort) {
        debounceRotation();
      }
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

  mevcutCropSelect.addEventListener('change', () => {
    if (appState.ort) debounceRotation();
  });
  oncekiCropSelect.addEventListener('change', () => {
    if (appState.ort) debounceRotation();
  });
  fieldSizeInput.addEventListener('input', () => {
    if (appState.ort && appState.rotationResult) {
      renderIncomeEstimate(appState.rotationResult, fieldSizeInput.value);
    }
  });
  cIrrigation.addEventListener('change', () => {
    if (appState.ort) debounceRotation();
  });
  cMarket.addEventListener('change', () => {
    if (appState.ort) debounceRotation();
  });
}

let debounceTimer = null;
function debounceRotation() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    runRotationCalculation();
  }, 250);
}

// --- Language Switcher ---
function setLanguage(lang) {
  currentLang = lang;
  langText.textContent = I18N[lang].lang_code;
  document.documentElement.lang = lang;

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (I18N[lang][key]) {
      el.textContent = I18N[lang][key];
    }
  });

  if (appState.ort) {
    runRotationCalculation();
  }
}

// --- Main Analysis & API Execution ---
async function runFullAnalysis() {
  const lat = parseFloat(latInput.value);
  const lon = parseFloat(lonInput.value);
  const start = formatDateForAPI(startDateInput.value);
  const end = formatDateForAPI(endDateInput.value);
  const fieldSize = parseFloat(fieldSizeInput.value) || 0;

  if (isNaN(lat) || isNaN(lon)) {
    showBanner('Lütfen geçerli enlem ve boylam girin.');
    return;
  }

  if (!start || !end || start >= end) {
    showBanner('Bitiş tarihi başlangıç tarihinden sonra olmalıdır.');
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
    if (!res.ok || data.error) {
      throw new Error(data.error || 'NASA POWER verisi alınamadı.');
    }

    appState.ort = data.ortalama;
    appState.raw = data.raw;

    valTemp.textContent = appState.ort.sıcaklık_C;
    valPrecip.textContent = appState.ort.yağış_mm_gun;
    valSolar.textContent = appState.ort.güneş_MJ_m2_gun;
    valWind.textContent = appState.ort.rüzgar_m_s;

    welcomePlaceholder.style.display = 'none';
    analysisContent.style.display = 'block';

    renderTimelineChart(appState.raw);

    await runRotationCalculation(fieldSize);

    showBanner('NASA iklim verileri başarıyla işlendi!', true);
  } catch (err) {
    showBanner(`Hata: ${err.message}`);
  } finally {
    btnAnalyze.disabled = false;
    btnAnalyze.querySelector('.btn-spinner').style.display = 'none';
    btnAnalyze.querySelector('.btn-label').textContent = I18N[currentLang].btn_run_analysis;
  }
}

async function runRotationCalculation(fieldSize = null) {
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

  const fieldSizeVal = fieldSize !== null ? fieldSize : (parseFloat(fieldSizeInput.value) || 0);

  const payload = {
    ortalama: appState.ort,
    oncelikler,
    mevcut: mevcutCropSelect.value || null,
    onceki: oncekiCropSelect.value || null,
    scenario,
    constraints,
    lang: currentLang,
    field_size_decare: fieldSizeVal
  };

  try {
    const res = await fetch('/api/rotasyon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Rotasyon hesaplanamadı.');
    }

    appState.rotationResult = data;
    renderResultsUI(data);
    renderRotationSequence(data);
    renderIncomeEstimate(data, fieldSizeVal);
  } catch (err) {
    console.error(err);
  }
}

// --- Render Results UI ---
function renderResultsUI(data) {
  riskWarningsRow.innerHTML = '';
  if (data.risk_uyarilari && data.risk_uyarilari.length > 0) {
    riskWarningsRow.style.display = 'flex';
    data.risk_uyarilari.forEach((risk) => {
      const box = document.createElement('div');
      box.className = 'risk-alert-box';
      box.innerHTML = `<span>⚠️</span> <span>${risk.mesaj}</span>`;
      riskWarningsRow.appendChild(box);
    });
  } else {
    riskWarningsRow.style.display = 'none';
  }

  if (data.en_iyi_bitki) {
    bestCropName.textContent = data.en_iyi_bitki.bitki;
    bestCropScore.textContent = data.en_iyi_bitki.skor;
    const grup = data.en_iyi_bitki.grup ? ` • ${data.en_iyi_bitki.grup.toUpperCase()}` : '';
    bestCropSub.textContent = (currentLang === 'tr' ? 'İklim şartları ve çiftçi önceliklerine göre en yüksek puanı alan ekin' : 'Highest scoring crop considering climate conditions and priorities') + grup;
  }

  strategiesContainer.innerHTML = '';
  if (data.stratejiler) {
    const pillClasses = ['pill-soil', 'pill-water', 'pill-yield'];
    data.stratejiler.forEach((strat, idx) => {
      const card = document.createElement('div');
      card.className = 'strategy-card';
      const pillClass = pillClasses[idx % pillClasses.length];

      card.innerHTML = `
        <span class="strategy-badge-pill ${pillClass}">Strateji #${idx + 1}</span>
        <h4 class="strategy-name">${strat.ad}</h4>
        <div class="strategy-crop-highlight">
          <span>${strat.bitki}</span>
          <span class="strategy-crop-score">${strat.skor} / 100</span>
        </div>
        <p class="strategy-body-text">${strat.neden}</p>
        <ul class="strategy-list">
          <li><strong>${currentLang === 'tr' ? 'Kanıt:' : 'Evidence:'}</strong> ${strat.kanit || '--'}</li>
          <li><strong>${currentLang === 'tr' ? 'Faydalar:' : 'Benefits:'}</strong> ${(strat.faydalar || []).join(', ')}</li>
          <li><strong>${currentLang === 'tr' ? 'Riskler:' : 'Risks:'}</strong> ${(strat.riskler || []).join(', ')}</li>
        </ul>
      `;
      strategiesContainer.appendChild(card);
    });
  }

  if (data.stres_takvimi) {
    renderStressChart(data.stres_takvimi);
  }
}

// --- Render Rotation Sequence (3-year) ---
function renderRotationSequence(data) {
  rotationContainer.innerHTML = '';
  if (!data.rotasyon_dizisi) return;

  const roleLabels = {
    'main_crop': currentLang === 'tr' ? 'Ana Ürün' : 'Main Crop',
    'nitrogen_fixer': currentLang === 'tr' ? 'Azot Bağlayıcı' : 'Nitrogen Fixer',
    'cover_crop': currentLang === 'tr' ? 'Örtü Bitkisi' : 'Cover Crop',
    'low_water': currentLang === 'tr' ? 'Düşük Su' : 'Low Water'
  };

  const heading = document.createElement('h3');
  heading.className = 'section-heading-title';
  heading.textContent = I18N[currentLang].rotation_sequence;
  rotationContainer.appendChild(heading);

  data.rotasyon_dizisi.forEach((step) => {
    const card = document.createElement('div');
    card.className = 'rotation-step-card';
    const roleLabel = roleLabels[step.rol] || step.rol;
    card.innerHTML = `
      <div class="rotation-step-header">
        <span class="rotation-year-badge">${I18N[currentLang].rotation_year} ${step.yil}</span>
        <span class="rotation-role-badge">${roleLabel}</span>
      </div>
      <div class="rotation-step-crop">${step.bitki}</div>
      <div class="rotation-step-info">
        <span>${step.grup.toUpperCase()}</span>
        <span>Skor: ${step.skor}/100</span>
      </div>
    `;
    rotationContainer.appendChild(card);
  });
}

// --- Render Income Estimate ---
function renderIncomeEstimate(data, fieldSize) {
  incomeContainer.innerHTML = '';
  if (!data.gelir_tahmini) {
    const note = document.createElement('p');
    note.className = 'income-note';
    note.textContent = currentLang === 'tr'
      ? 'Gelir tahmini için lütfen tarla alanı (decare) girin.'
      : 'Please enter field size (decare) for income estimate.';
    incomeContainer.appendChild(note);
    return;
  }

  const g = data.gelir_tahmini;
  const currency = I18N[currentLang].currency_try;

  const card = document.createElement('div');
  card.className = 'income-card';
  card.innerHTML = `
    <div class="income-header">
      <span class="income-title">${I18N[currentLang].estimated_income}</span>
      <span class="income-crop">${g.bitki}</span>
    </div>
    <div class="income-value">${currency} ${g.brüt_gelir_try.toLocaleString('tr-TR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}</div>
    <div class="income-breakdown">
      <span>${I18N[currentLang].field_size_decare}: ${g.alan_decare} decare</span>
      <span>Verim: ${g.verim_kg_decare} kg/decare</span>
      <span>Fiyat: ${currency} ${g.fiyat_try_kg}/kg</span>
    </div>
    <div class="income-note">${I18N[currentLang].calc_note}</div>
  `;
  incomeContainer.appendChild(card);
}

// --- Chart Rendering ---
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
      labels: labels,
      datasets: [
        {
          label: currentLang === 'tr' ? 'Sıcaklık Stresi (%)' : 'Temp Stress (%)',
          data: tempStress,
          borderColor: '#f97316',
          backgroundColor: 'rgba(249, 115, 22, 0.08)',
          fill: true,
          tension: 0.35,
          pointRadius: 4
        },
        {
          label: currentLang === 'tr' ? 'Su Stresi (%)' : 'Water Stress (%)',
          data: waterStress,
          borderColor: '#0284c7',
          backgroundColor: 'rgba(2, 132, 199, 0.08)',
          fill: true,
          tension: 0.35,
          pointRadius: 4
        },
        {
          label: currentLang === 'tr' ? 'Bitki Gelişimi (NDVI Proxy)' : 'NDVI Vegetation Proxy',
          data: ndvi,
          borderColor: '#16a34a',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          tension: 0.35,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: { color: '#f1f5f9' },
          ticks: { font: { family: 'Plus Jakarta Sans', size: 11 } }
        },
        x: {
          grid: { display: false },
          ticks: { font: { family: 'Plus Jakarta Sans', size: 11 } }
        }
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
      labels: labels,
      datasets: [
        {
          label: currentLang === 'tr' ? 'Sıcaklık (°C)' : 'Temperature (°C)',
          data: t2mData,
          borderColor: '#ea580c',
          backgroundColor: 'rgba(234, 88, 12, 0.05)',
          tension: 0.2,
          yAxisID: 'y'
        },
        {
          label: currentLang === 'tr' ? 'Yağış (mm/gün)' : 'Rain (mm/day)',
          data: precData,
          borderColor: '#0284c7',
          backgroundColor: 'rgba(2, 132, 199, 0.15)',
          tension: 0.2,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { type: 'linear', position: 'left', grid: { color: '#f1f5f9' } },
        y1: { type: 'linear', position: 'right', grid: { display: false } },
        x: { grid: { display: false } }
      }
    }
  });
}

// --- Download Report Function ---
function downloadReport() {
  if (!appState.ort || !appState.rotationResult) {
    showBanner('Lütfen önce analizi tamamlayın.');
    return;
  }

  const ort = appState.ort;
  const res = appState.rotationResult;
  const lines = [
    '=====================================================',
    '  FIELD SHIFT — NASA SPACE APPS KARAR DESTEK RAPORU  ',
    '=====================================================',
    `Tarih: ${new Date().toLocaleString()}`,
    `Konum: Enlem ${latInput.value}°N, Boylam ${lonInput.value}°E`,
    `Dönem: ${startDateInput.value} -> ${endDateInput.value}`,
    `Tarla Alanı: ${fieldSizeInput.value || 0} decare`,
    '',
    '1. NASA POWER İKLİM GÖZLEMLERİ (GÜNLÜK ORTALAMA)',
    '-----------------------------------------------------',
    `- Ortalama Sıcaklık: ${ort.sıcaklık_C} °C`,
    `- Günlük Yağış: ${ort.yağış_mm_gun} mm/gün`,
    `- Güneş Radyasyonu: ${ort.güneş_MJ_m2_gun} MJ/m²/gün`,
    `- Rüzgar Hızı: ${ort.rüzgar_m_s} m/s`,
    '',
    '2. ÖNERİLEN ROTASYON STRATEJİLERİ',
    '-----------------------------------------------------'
  ];

  (res.stratejiler || []).forEach((strat, i) => {
    lines.push(`Strateji ${i + 1}: ${strat.ad}`);
    lines.push(`  Önerilen Ürün : ${strat.bitki} (Skor: ${strat.skor}/100)`);
    lines.push(`  Gerekçe       : ${strat.neden}`);
    lines.push(`  Kanıt         : ${strat.kanit}`);
    lines.push(`  Faydalar      : ${(strat.faydalar || []).join(', ')}`);
    lines.push(`  Riskler       : ${(strat.riskler || []).join(', ')}`);
    lines.push('');
  });

  if (res.rotasyon_dizisi && res.rotasyon_dizisi.length) {
    lines.push('3. 3 YILLIK ROTASYON DİZİSİ');
    lines.push('-----------------------------------------------------');
    res.rotasyon_dizisi.forEach(step => {
      lines.push(`  Yıl ${step.yil}: ${step.bitki} (${step.rol}, Skor: ${step.skor}/100)`);
    });
    lines.push('');
  }

  if (res.gelir_tahmini) {
    const g = res.gelir_tahmini;
    lines.push('4. GELİR TAHMİNİ');
    lines.push('-----------------------------------------------------');
    lines.push(`  Ürün: ${g.bitki}`);
    lines.push(`  Alan: ${g.alan_decare} decare`);
    lines.push(`  Verim: ${g.verim_kg_decare} kg/decare`);
    lines.push(`  Fiyat: ₺${g.fiyat_try_kg}/kg`);
    lines.push(`  Tahmini Brüt Gelir: ₺${g.brüt_gelir_try.toLocaleString('tr-TR', { minimumFractionDigits: 0 })}`);
    lines.push('');
  }

  if (res.risk_uyarilari && res.risk_uyarilari.length) {
    lines.push('5. TESPİT EDİLEN RİSKLER & UYARILAR');
    lines.push('-----------------------------------------------------');
    res.risk_uyarilari.forEach(r => lines.push(`- ${r.mesaj}`));
    lines.push('');
  }

  lines.push('Veri Kaynağı: NASA POWER Daily API (power.larc.nasa.gov)');
  lines.push('Uyarı: Bu rapor karar destek amaçlıdır.');

  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `field_shift_rapor_${formatDateForAPI(startDateInput.value)}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// --- Setup City Preset Pills & Chart Tabs ---
function setupUIListeners() {
  document.querySelectorAll('#cityPills .pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lat = parseFloat(btn.dataset.lat);
      const lon = parseFloat(btn.dataset.lon);
      updateCoords(lat, lon);
      if (leafletMap) leafletMap.setView([lat, lon], 9);
    });
  });

  document.getElementById('btnGeolocate')?.addEventListener('click', () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        updateCoords(pos.coords.latitude, pos.coords.longitude);
        if (leafletMap) leafletMap.setView([pos.coords.latitude, pos.coords.longitude], 10);
      }, () => {
        showBanner('Konumunuza ulaşılamadı.');
      });
    }
  });

  document.getElementById('btnLastYear')?.addEventListener('click', () => {
    startDateInput.value = '2024-01-01';
    endDateInput.value = '2024-12-31';
  });

  document.getElementById('btnSeasonSummer')?.addEventListener('click', () => {
    startDateInput.value = '2024-06-01';
    endDateInput.value = '2024-09-30';
  });

  document.querySelectorAll('.chart-tabs .tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.chart-tabs .tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.dataset.tab;
      document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
      const activePane = document.getElementById(targetId);
      if (activePane) activePane.style.display = 'block';
    });
  });

  document.getElementById('btnDownloadReport')?.addEventListener('click', downloadReport);
  btnAnalyze.addEventListener('click', () => runFullAnalysis());
  btnLang.addEventListener('click', () => {
    setLanguage(currentLang === 'tr' ? 'en' : 'tr');
  });

  latInput.addEventListener('change', () => {
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);
    if (!isNaN(lat) && !isNaN(lon) && mapMarker) {
      mapMarker.setLatLng([lat, lon]);
      leafletMap.panTo([lat, lon]);
    }
  });
  lonInput.addEventListener('change', () => {
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);
    if (!isNaN(lat) && !isNaN(lon) && mapMarker) {
      mapMarker.setLatLng([lat, lon]);
      leafletMap.panTo([lat, lon]);
    }
  });
}

// --- Initialize App ---
document.addEventListener('DOMContentLoaded', async () => {
  initLeaflet();
  await loadCrops();
  initSliders();
  setupUIListeners();
});
