/**
 * Content script pour détecter les marques sur la page et afficher les scores de durabilité
 * Communique avec l'API FastAPI backend
 */

// Configuration de l'API backend
const API_BASE_URL = 'http://localhost:8000'; // À adapter selon votre configuration

// Base de données simple des marques (pour la détection initiale)
const KNOWN_BRANDS = [
    'nike', 'adidas', 'puma', 'reebok', 'converse', 'vans', 'timberland',
    'levis', 'zara', 'h&m', 'uniqlo', 'gap', 'tommy hilfiger', 'calvin klein',
    'ralph lauren', 'lacoste', 'patagonia', 'veja', 'reformation', 'everlane',
    'the north face', 'columbia', 'salomon', 'arc\'teryx', 'supreme', 'stussy',
    'off-white', 'a bathing ape', 'palace', 'kith', 'fear of god'
];

/**
 * Détecte les marques présentes sur la page
 */
function detectBrandsOnPage() {
    const detectedBrands = new Set();
    const pageText = document.body.innerText.toLowerCase();
    
    // Chercher les marques dans le texte
    KNOWN_BRANDS.forEach(brand => {
        const brandLower = brand.toLowerCase();
        // Recherche simple dans le texte
        if (pageText.includes(brandLower)) {
            detectedBrands.add(brand);
        }
    });
    
    // Chercher aussi dans les liens
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.href.toLowerCase();
        const text = link.textContent.toLowerCase();
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            if (href.includes(brandLower) || text.includes(brandLower)) {
                detectedBrands.add(brand);
            }
        });
    });
    
    return Array.from(detectedBrands);
}

/**
 * Récupère les informations de durabilité depuis l'API
 */
async function getBrandSustainability(brandName) {
    try {
        const response = await fetch(`${API_BASE_URL}/brands/name/${encodeURIComponent(brandName)}`);
        if (!response.ok) {
            if (response.status === 404) {
                return null; // Marque non trouvée dans la base
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`[GreenStyle] Erreur lors de la récupération pour ${brandName}:`, error);
        return null;
    }
}

/**
 * Affiche un badge de score sur la page
 */
function displayScoreBadge(brandName, brandData, element) {
    // Supprimer les badges existants pour cette marque
    const existingBadge = element.querySelector('.greenstyle-badge');
    if (existingBadge) {
        existingBadge.remove();
    }
    
    const score = brandData.final_score;
    const color = brandData.score_color || '#808080';
    const label = brandData.score_label || 'Non évalué';
    
    // Créer le badge
    const badge = document.createElement('div');
    badge.className = 'greenstyle-badge';
    badge.style.cssText = `
        position: absolute;
        top: 5px;
        right: 5px;
        background: ${color};
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        z-index: 10000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        pointer-events: none;
    `;
    badge.textContent = score !== null ? `${score.toFixed(1)}/10` : 'N/A';
    badge.title = `${brandName}: ${label} (${score !== null ? score.toFixed(1) : 'N/A'}/10)`;
    
    // Positionner le badge
    const position = window.getComputedStyle(element);
    if (position.position === 'static') {
        element.style.position = 'relative';
    }
    
    element.appendChild(badge);
}

/**
 * Traite toutes les marques détectées
 */
async function processDetectedBrands() {
    const brands = detectBrandsOnPage();
    console.log(`[GreenStyle] Marques détectées: ${brands.join(', ')}`);
    
    if (brands.length === 0) {
        return;
    }
    
    // Récupérer les données pour chaque marque
    const brandPromises = brands.map(brand => getBrandSustainability(brand));
    const brandDataList = await Promise.all(brandPromises);
    
    // Afficher les badges sur les éléments contenant les marques
    brandDataList.forEach((brandData, index) => {
        if (!brandData) return; // Marque non trouvée
        
        const brandName = brands[index];
        const brandLower = brandName.toLowerCase();
        
        // Trouver les éléments contenant cette marque
        const elements = Array.from(document.querySelectorAll('*')).filter(el => {
            const text = el.textContent?.toLowerCase() || '';
            return text.includes(brandLower) && el.children.length === 0; // Éléments feuilles seulement
        });
        
        // Afficher le badge sur le premier élément trouvé (ou plusieurs si besoin)
        elements.slice(0, 3).forEach(el => {
            displayScoreBadge(brandName, brandData, el);
        });
    });
}

// Démarrer la détection au chargement de la page
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(processDetectedBrands, 1000); // Attendre 1s pour que la page soit complètement chargée
    });
} else {
    setTimeout(processDetectedBrands, 1000);
}

// Réexécuter lors des changements de page (SPA)
let lastUrl = location.href;
new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        setTimeout(processDetectedBrands, 1000);
    }
}).observe(document, { subtree: true, childList: true });

