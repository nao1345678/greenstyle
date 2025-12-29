// Configuration de l'API backend
const API_BASE_URL = 'http://localhost:8000';
const USE_DEMO_MODE = true; // Mode démo si MongoDB non disponible

/**
 * Appelle l'API backend pour récupérer les données d'une marque avec retry logic
 */
async function fetchBrandData(brandName, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout
      
      const response = await fetch(`${API_BASE_URL}/brands/name/${encodeURIComponent(brandName)}`, {
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        if (response.status === 404) {
          console.log(`[GreenStyle Background] ⚠️ Marque "${brandName}" non trouvée (404)`);
          return null; // Marque non trouvée
        }
        
        // Note: Le scraping fonctionne maintenant même sans MongoDB (erreur 503 ne devrait plus arriver)
        // On garde le mode démo en dernier recours si nécessaire
        if (response.status === 503 && USE_DEMO_MODE && attempt >= retries) {
          console.log(`[GreenStyle Background] Tentative mode démo en dernier recours pour ${brandName}`);
          try {
            const demoController = new AbortController();
            const demoTimer = setTimeout(() => demoController.abort(), 5000);
            const demoResponse = await fetch(`${API_BASE_URL}/demo/brands/name/${encodeURIComponent(brandName)}`, {
              signal: demoController.signal,
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              }
            });
            clearTimeout(demoTimer);
            
            if (demoResponse.ok) {
              const demoData = await demoResponse.json();
              console.log(`[GreenStyle Background] ✅ Données démo récupérées pour ${brandName}`);
              return demoData;
            }
          } catch (demoError) {
            console.warn(`[GreenStyle Background] Erreur mode démo pour ${brandName}:`, demoError.message);
          }
        }
        
        // Retry pour les erreurs serveur (5xx)
        if (response.status >= 500 && attempt < retries) {
          console.warn(`[GreenStyle Background] Erreur serveur ${response.status} pour ${brandName}, tentative ${attempt}/${retries}`);
          await new Promise(resolve => setTimeout(resolve, 1000 * attempt)); // Délai exponentiel
          continue;
        }
        
        // Pour les autres erreurs, on retourne null
        const errorText = await response.text().catch(() => 'Unknown error');
        console.warn(`[GreenStyle Background] API erreur ${response.status} pour ${brandName}: ${errorText}`);
        return null;
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      if (error.name === 'AbortError') {
        console.warn(`[GreenStyle Background] Timeout pour ${brandName}, tentative ${attempt}/${retries}`);
      } else {
        console.warn(`[GreenStyle Background] Erreur réseau pour ${brandName}, tentative ${attempt}/${retries}:`, error.message);
      }
      
      // Retry si ce n'est pas la dernière tentative
      if (attempt < retries) {
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt)); // Délai exponentiel
        continue;
      }
      
      return null;
    }
  }
  return null;
}

/**
 * Recherche plusieurs marques via l'API
 */
async function searchBrands(query) {
  try {
    const response = await fetch(`${API_BASE_URL}/brands/search/${encodeURIComponent(query)}?limit=10`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`[GreenStyle Background] Erreur recherche:`, error);
    return [];
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  // Gestion des paramètres
  if (msg?.type === 'BG_GET_SETTINGS') {
    chrome.storage.local.get('settings', (res) => {
      sendResponse({ settings: res?.settings || {} });
    });
    return true;
  }

  // Mise à jour du texte du popup
  if (msg?.type === 'BG_SET_POPUP_TEXT') {
    const text = msg.text || '';
    chrome.storage.local.set({ popupText: text }, () => {
      chrome.runtime.sendMessage({ type: 'POPUP_TEXT_UPDATED', text });
      sendResponse({ ok: true });
    });
    return true;
  }

  // Récupération des données d'une marque depuis l'API
  if (msg?.type === 'BG_GET_BRAND_DATA') {
    fetchBrandData(msg.brandName, 3).then(data => {
      if (data === null) {
        // Marque non trouvée (404) ou scraping échoué
        sendResponse({ success: false, error: '404', data: null });
      } else {
        sendResponse({ success: true, data });
      }
    }).catch(error => {
      console.error(`[GreenStyle Background] Erreur fatale pour ${msg.brandName}:`, error);
      sendResponse({ success: false, error: error.message, data: null });
    });
    return true; // Indique que la réponse sera asynchrone
  }

  // Recherche de marques
  if (msg?.type === 'BG_SEARCH_BRANDS') {
    searchBrands(msg.query).then(brands => {
      sendResponse({ success: true, brands });
    }).catch(error => {
      sendResponse({ success: false, error: error.message, brands: [] });
    });
    return true;
  }

  // Récupération des marques détectées sur la page actuelle
  if (msg?.type === 'BG_GET_DETECTED_BRANDS') {
    chrome.storage.local.get('detectedBrands', (res) => {
      sendResponse({ brands: res?.detectedBrands || [] });
    });
    return true;
  }

  // Sauvegarde des marques détectées
  if (msg?.type === 'BG_SAVE_DETECTED_BRANDS') {
    chrome.storage.local.set({ detectedBrands: msg.brands }, () => {
      sendResponse({ ok: true });
    });
    return true;
  }
});
