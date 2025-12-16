// Configuration de l'API backend
const API_BASE_URL = 'http://localhost:8000';

/**
 * Appelle l'API backend pour récupérer les données d'une marque
 */
async function fetchBrandData(brandName) {
  try {
    const response = await fetch(`${API_BASE_URL}/brands/name/${encodeURIComponent(brandName)}`);
    if (!response.ok) {
      if (response.status === 404) {
        return null; // Marque non trouvée
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`[GreenStyle Background] Erreur API pour ${brandName}:`, error);
    return null;
  }
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
    fetchBrandData(msg.brandName).then(data => {
      sendResponse({ success: true, data });
    }).catch(error => {
      sendResponse({ success: false, error: error.message });
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
