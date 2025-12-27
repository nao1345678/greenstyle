(function () {
  // Attendre que le DOM soit chargé
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    const loadingEl = document.getElementById('loading');
    const noBrandsEl = document.getElementById('no-brands');
    const brandsListEl = document.getElementById('brands-list');
    const currentPageInfoEl = document.getElementById('current-page-info');
    
    if (!loadingEl || !noBrandsEl || !brandsListEl) {
      console.error('[GreenStyle Popup] Éléments DOM non trouvés');
      return;
    }
    
    console.log('[GreenStyle Popup] Initialisation réussie');

    /**
     * Génère les étoiles (pleines ou vides) basées sur le score
     */
    function renderStars(score) {
      if (score === null || score === undefined) return '☆☆☆☆☆';
      const fullStars = Math.round(score / 2); // Score sur 10, donc /2 pour avoir sur 5
      let starsHtml = "";
      for (let i = 1; i <= 5; i++) {
        starsHtml += i <= fullStars ? "★" : "☆";
      }
      return starsHtml;
    }

    /**
     * Affiche le prix avec des symboles $
     */
    function renderPrice(priceRange) {
      if (!priceRange) return '';
      const value = Math.round(priceRange);
      let html = "";
      for (let i = 1; i <= 5; i++) {
        const color = i <= value ? "#000" : "#ccc";
        html += `<span style="color: ${color}">$</span>`;
      }
      return html;
    }

    /**
     * Met à jour une jauge (work ou planet)
     */
    function updateGauge(element, value) {
      if (!element || value === null || value === undefined) return;
      const percentage = (value / 10) * 100; // Score sur 10
      element.style.width = `${Math.min(percentage, 100)}%`;
      
      if (value <= 2) element.style.backgroundColor = "#ff7e7e";
      else if (value <= 4) element.style.backgroundColor = "#ffb800";
      else if (value <= 7) element.style.backgroundColor = "#ffeb3b";
      else element.style.backgroundColor = "#4CAF50";
    }

    /**
     * Affiche une marque dans une carte principale
     */
    function displayBrand(brand) {
      const brandData = brand.data;
      const brandName = brand.name || 'Marque inconnue';
      
      // Créer la carte principale
      const mainCard = document.createElement('div');
      mainCard.className = 'main-card';
      
      // Si pas de données, afficher un message simple
      if (!brandData) {
        mainCard.innerHTML = `
          <div class="header">
            <div class="brand-identity">
              <h1 id="brand-name">${brandName.toLowerCase()}</h1>
              <div class="price-container"></div>
            </div>
            <div class="score-container">
              <div class="score-value">N/A</div>
              <div class="stars">☆☆☆☆☆</div>
            </div>
          </div>
          <div style="text-align: center; padding: 20px; color: #666;">
            <p>Marque détectée mais non trouvée dans la base de données</p>
          </div>
        `;
        brandsListEl.appendChild(mainCard);
        return;
      }

      const score = brandData.final_score || 0;
      const laborScore = brandData.labor_ethics || 0;
      const planetScore = brandData.global_env_impact || 0;
      
      // Construire le HTML de la carte
      mainCard.innerHTML = `
        <div class="header">
          <div class="brand-identity">
            ${brandData.logo ? `<img id="brand-logo" src="${brandData.logo}" alt="${brandName}">` : ''}
            <h1 id="brand-name">${brandName.toLowerCase()}</h1>
            <div class="price-container">${renderPrice(brandData.price_range)}</div>
          </div>
          <div class="score-container">
            <div class="score-value">${score.toFixed(1)}</div>
            <div class="stars">${renderStars(score)}</div>
          </div>
        </div>

        <div class="stats-section">
          <div class="gauge-row">
            <span class="gauge-label">work</span>
            <div class="gauge-bg">
              <div id="labor-gauge-${brandName.replace(/\s+/g, '-')}" class="gauge-fill work-color"></div>
            </div>
          </div>
          <div class="gauge-row">
            <span class="gauge-label">planet</span>
            <div class="gauge-bg">
              <div id="planet-gauge-${brandName.replace(/\s+/g, '-')}" class="gauge-fill planet-color"></div>
            </div>
          </div>
        </div>

        ${brandData.sustainable_materials || brandData.certifications ? `
        <div class="alternatives-box">
          <div class="alt-title">
            <span class="bulb-icon">ℹ️</span> Informations :
          </div>
          <div class="alt-list">
            ${brandData.sustainable_materials ? `
              <div class="alt-row">
                <div class="alt-name">Matières durables</div>
                <div class="alt-dots"></div>
                <div class="alt-price">${brandData.sustainable_materials}%</div>
              </div>
            ` : ''}
            ${brandData.certifications ? `
              <div class="alt-row">
                <div class="alt-name">Certifications</div>
                <div class="alt-dots"></div>
                <div class="alt-price">${brandData.certifications}</div>
              </div>
            ` : ''}
          </div>
        </div>
        ` : ''}
      `;
      
      brandsListEl.appendChild(mainCard);
      
      // Mettre à jour les jauges après l'insertion
      setTimeout(() => {
        const laborGauge = document.getElementById(`labor-gauge-${brandName.replace(/\s+/g, '-')}`);
        const planetGauge = document.getElementById(`planet-gauge-${brandName.replace(/\s+/g, '-')}`);
        if (laborGauge) updateGauge(laborGauge, laborScore);
        if (planetGauge) updateGauge(planetGauge, planetScore);
      }, 50);
    }

    /**
     * Charge et affiche les marques détectées
     */
    function loadDetectedBrands() {
      console.log('[GreenStyle Popup] Chargement des marques détectées...');
      chrome.storage.local.get(['detectedBrands', 'detectedBrandsData'], (res) => {
        loadingEl.style.display = 'none';
        brandsListEl.innerHTML = '';
        
        const brands = res.detectedBrands || [];
        const brandsData = res.detectedBrandsData || [];
        console.log('[GreenStyle Popup] Marques brutes:', brands);
        console.log('[GreenStyle Popup] Données de marques:', brandsData);

        if (brands.length === 0) {
          noBrandsEl.style.display = 'block';
          return;
        } else {
          noBrandsEl.style.display = 'none';
        }

        // Créer un dictionnaire pour un accès rapide aux données
        const dataMap = new Map(brandsData.map(b => [b.name.toLowerCase(), b.data]));

        brands.forEach(brandName => {
          const brandData = dataMap.get(brandName.toLowerCase());
          displayBrand({ name: brandName, data: brandData });
        });
        console.log('[GreenStyle Popup] Marques affichées.');
      });
    }

    // Écouter les changements de stockage pour mettre à jour en temps réel
    chrome.storage.onChanged.addListener((changes, area) => {
      if (area === 'local' && (changes.detectedBrands || changes.detectedBrandsData)) {
        console.log('[GreenStyle Popup] Changement de storage détecté, rechargement...');
        brandsListEl.innerHTML = '';
        loadingEl.style.display = 'block';
        noBrandsEl.style.display = 'none';
        setTimeout(loadDetectedBrands, 100);
      }
    });

    /**
     * Affiche l'URL de la page actuelle
     */
    function displayCurrentPage() {
      const currentUrlEl = document.getElementById('current-url');
      if (!currentUrlEl) return;
      
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0] && tabs[0].url) {
          const url = tabs[0].url;
          try {
            const urlObj = new URL(url);
            const domain = urlObj.hostname.replace('www.', '');
            currentUrlEl.textContent = domain;
            currentUrlEl.title = url;
            if (currentPageInfoEl) currentPageInfoEl.style.display = 'block';
          } catch (e) {
            if (url && typeof url === 'string') {
              currentUrlEl.textContent = url.length > 40 ? url.substring(0, 40) + '...' : url;
              currentUrlEl.title = url;
              if (currentPageInfoEl) currentPageInfoEl.style.display = 'block';
            }
          }
        }
      });
    }

    // Afficher la page actuelle
    displayCurrentPage();

    // Recharger quand on change d'onglet
    chrome.tabs.onActivated.addListener(() => {
      console.log('[GreenStyle Popup] Onglet changé, rechargement...');
      displayCurrentPage();
      brandsListEl.innerHTML = '';
      loadingEl.style.display = 'block';
      noBrandsEl.style.display = 'none';
      setTimeout(loadDetectedBrands, 500);
    });

    // Recharger quand l'URL change dans l'onglet actif
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.active) {
        console.log('[GreenStyle Popup] URL de l\'onglet actif mise à jour, rechargement...');
        displayCurrentPage();
        brandsListEl.innerHTML = '';
        loadingEl.style.display = 'block';
        noBrandsEl.style.display = 'none';
        setTimeout(loadDetectedBrands, 1000);
      }
    });

    // Charger au démarrage
    loadDetectedBrands();
  }
})();
