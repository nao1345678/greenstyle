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
    
    if (!loadingEl || !noBrandsEl || !brandsListEl) {
      console.error('[GreenStyle Popup] Éléments DOM non trouvés');
      return;
    }

  /**
   * Récupère le score et retourne la classe CSS correspondante
   */
  function getScoreClass(score) {
    if (score === null || score === undefined) return 'poor';
    if (score >= 7) return 'excellent';
    if (score >= 4) return 'good';
    return 'poor';
  }

  /**
   * Formate un score pour l'affichage
   */
  function formatScore(score) {
    if (score === null || score === undefined) return 'N/A';
    return score.toFixed(1);
  }

  /**
   * Affiche une marque dans la liste
   */
  function displayBrand(brand) {
    const brandData = brand.data;
    if (!brandData) return;

    const score = brandData.final_score;
    const scoreClass = getScoreClass(score);
    const scoreColor = brandData.score_color || '#808080';
    const scoreLabel = brandData.score_label || 'Non évalué';

    const brandItem = document.createElement('div');
    brandItem.className = `brand-item ${scoreClass}`;
    
    brandItem.innerHTML = `
      <div class="brand-header">
        <span class="brand-name">${brand.name}</span>
        <span class="brand-score ${scoreClass}" style="background: ${scoreColor}">
          ${formatScore(score)}/10
        </span>
      </div>
      <div class="brand-label">${scoreLabel}</div>
      <div class="brand-details">
        ${brandData.sustainable_materials ? `
          <div class="detail-item">
            <span>♻️</span>
            <span>${brandData.sustainable_materials}% matières durables</span>
          </div>
        ` : ''}
        ${brandData.certifications ? `
          <div class="detail-item">
            <span>🏆</span>
            <span>${brandData.certifications}</span>
          </div>
        ` : ''}
        ${brandData.planet_badge ? `
          <span class="badge planet">🌍 Planète</span>
        ` : ''}
        ${brandData.labor_badge ? `
          <span class="badge labor">👥 Travail</span>
        ` : ''}
      </div>
    `;

    brandsListEl.appendChild(brandItem);
  }

  /**
   * Charge et affiche les marques détectées
   */
  function loadDetectedBrands() {
    chrome.storage.local.get(['detectedBrands', 'detectedBrandsData'], (res) => {
      loadingEl.style.display = 'none';
      
      const brands = res.detectedBrands || [];
      const brandsData = res.detectedBrandsData || [];

      if (brands.length === 0) {
        noBrandsEl.style.display = 'block';
        return;
      }

      // Si on a des données complètes, les utiliser
      if (brandsData.length > 0) {
        brandsData.forEach(brand => displayBrand(brand));
      } else {
        // Sinon, récupérer les données via le background
        brands.forEach(brandName => {
          chrome.runtime.sendMessage(
            { type: 'BG_GET_BRAND_DATA', brandName },
            (response) => {
              if (response?.success && response.data) {
                displayBrand({ name: brandName, data: response.data });
              }
            }
          );
        });
      }
    });
  }

  // Écouter les changements de stockage pour mettre à jour en temps réel
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === 'local' && (changes.detectedBrands || changes.detectedBrandsData)) {
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
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        const url = tabs[0].url;
        // Afficher le nom de domaine principal
        try {
          const urlObj = new URL(url);
          const domain = urlObj.hostname.replace('www.', '');
          currentUrlEl.textContent = domain;
          currentUrlEl.title = url;
        } catch (e) {
          currentUrlEl.textContent = url.length > 40 ? url.substring(0, 40) + '...' : url;
          currentUrlEl.title = url;
        }
      }
    });
  }
  
  // Afficher la page actuelle
  displayCurrentPage();
  
  // Recharger quand on change d'onglet
  chrome.tabs.onActivated.addListener(() => {
    displayCurrentPage();
    brandsListEl.innerHTML = '';
    loadingEl.style.display = 'block';
    noBrandsEl.style.display = 'none';
    setTimeout(loadDetectedBrands, 500);
  });
  
  // Recharger quand l'URL change dans l'onglet actif
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.active) {
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
