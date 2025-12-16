/**
 * Content script pour détecter les marques sur la page et afficher les scores de durabilité
 * Communique avec l'API FastAPI backend
 */

// Configuration de l'API backend
const API_BASE_URL = 'http://localhost:8000'; // À adapter selon votre configuration

// Base de données des marques avec alias pour une meilleure détection
const BRANDS_WITH_ALIASES = {
    'nike': ['nike air', 'air jordan', 'jordan', 'nike.com'],
    'adidas': ['adidas originals', 'adidas performance', 'adidas.com'],
    'puma': ['puma sport', 'puma.com'],
    'reebok': ['reebok classic', 'reebok.com'],
    'converse': ['converse all star', 'converse.com'],
    'vans': ['vans old skool', 'vans.com'],
    'timberland': ['timberland boots', 'timberland.com'],
    'levis': ['levi\'s', 'levis', 'levis.com'],
    'zara': ['zara home', 'zara.com'],
    'h&m': ['h&m home', 'h&m', 'hm.com'],
    'uniqlo': ['uniqlo japan', 'uniqlo.com'],
    'gap': ['gap kids', 'gap.com'],
    'tommy hilfiger': ['tommy', 'tommyhilfiger.com'],
    'calvin klein': ['ck', 'calvin klein underwear', 'calvinklein.com'],
    'ralph lauren': ['polo ralph lauren', 'ralphlauren.com'],
    'lacoste': ['lacoste sport', 'lacoste.com'],
    'patagonia': ['patagonia.com'],
    'veja': ['veja.com'],
    'reformation': ['reformation.com'],
    'everlane': ['everlane.com'],
    'the north face': ['north face', 'thenorthface.com'],
    'columbia': ['columbia.com'],
    'salomon': ['salomon.com'],
    'arc\'teryx': ['arcteryx', 'arcteryx.com'],
    'supreme': ['supremenewyork.com'],
    'stussy': ['stussy.com'],
    'off-white': ['offwhite.com'],
    'a bathing ape': ['bape', 'bape.com'],
    'palace': ['palaceskateboards.com'],
    'kith': ['kith.com'],
    'fear of god': ['fearofgod.com']
};

// Liste simple pour la recherche rapide
const KNOWN_BRANDS = Object.keys(BRANDS_WITH_ALIASES);

/**
 * Détecte les marques présentes sur la page
 * Recherche dans plusieurs sources pour une meilleure détection sur les sites e-commerce
 */
function detectBrandsOnPage() {
    const detectedBrands = new Set();
    const pageText = document.body.innerText.toLowerCase();
    const pageHTML = document.body.innerHTML.toLowerCase();
    
    // 1. Chercher dans le texte visible
    KNOWN_BRANDS.forEach(brand => {
        const brandLower = brand.toLowerCase();
        const aliases = BRANDS_WITH_ALIASES[brand] || [];
        
        // Recherche du nom principal
        if (pageText.includes(brandLower)) {
            detectedBrands.add(brand);
        }
        
        // Recherche des alias
        aliases.forEach(alias => {
            if (pageText.includes(alias.toLowerCase())) {
                detectedBrands.add(brand);
            }
        });
    });
    
    // 2. Chercher dans les liens (href et texte)
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.href.toLowerCase();
        const text = link.textContent.toLowerCase();
        
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            const aliases = BRANDS_WITH_ALIASES[brand] || [];
            
            if (href.includes(brandLower) || text.includes(brandLower)) {
                detectedBrands.add(brand);
            }
            
            aliases.forEach(alias => {
                if (href.includes(alias.toLowerCase()) || text.includes(alias.toLowerCase())) {
                    detectedBrands.add(brand);
                }
            });
        });
    });
    
    // 3. Chercher dans les attributs data-* (très utilisé sur les sites e-commerce)
    const dataSelectors = [
        '[data-brand]', '[data-vendor]', '[data-manufacturer]', 
        '[data-company]', '[data-maker]', '[data-product-brand]'
    ];
    
    dataSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            const value = (el.dataset.brand || el.dataset.vendor || 
                          el.dataset.manufacturer || el.dataset.company || 
                          el.dataset.maker || el.dataset.productBrand || '').toLowerCase();
            
            if (value) {
                KNOWN_BRANDS.forEach(brand => {
                    const brandLower = brand.toLowerCase();
                    const aliases = BRANDS_WITH_ALIASES[brand] || [];
                    
                    if (value.includes(brandLower)) {
                        detectedBrands.add(brand);
                    }
                    
                    aliases.forEach(alias => {
                        if (value.includes(alias.toLowerCase())) {
                            detectedBrands.add(brand);
                        }
                    });
                });
            }
        });
    });
    
    // 4. Chercher dans les images (attributs alt et title)
    document.querySelectorAll('img').forEach(img => {
        const alt = (img.alt || '').toLowerCase();
        const title = (img.title || '').toLowerCase();
        const src = (img.src || '').toLowerCase();
        
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            const aliases = BRANDS_WITH_ALIASES[brand] || [];
            
            if (alt.includes(brandLower) || title.includes(brandLower) || src.includes(brandLower)) {
                detectedBrands.add(brand);
            }
            
            aliases.forEach(alias => {
                if (alt.includes(alias.toLowerCase()) || title.includes(alias.toLowerCase()) || 
                    src.includes(alias.toLowerCase())) {
                    detectedBrands.add(brand);
                }
            });
        });
    });
    
    // 5. Chercher dans les classes CSS (souvent utilisées pour les marques)
    document.querySelectorAll('[class*="brand"], [class*="vendor"], [class*="manufacturer"]').forEach(el => {
        const classes = el.className.toLowerCase();
        
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            if (classes.includes(brandLower)) {
                detectedBrands.add(brand);
            }
        });
    });
    
    // 6. Chercher dans les métadonnées (meta tags)
    const metaBrand = document.querySelector('meta[property="product:brand"]') || 
                     document.querySelector('meta[name="brand"]');
    if (metaBrand) {
        const metaValue = (metaBrand.content || metaBrand.getAttribute('content') || '').toLowerCase();
        KNOWN_BRANDS.forEach(brand => {
            if (metaValue.includes(brand.toLowerCase())) {
                detectedBrands.add(brand);
            }
        });
    }
    
    return Array.from(detectedBrands);
}

/**
 * Récupère les informations de durabilité depuis l'API
 * Utilise UNIQUEMENT le background script pour éviter les problèmes CORS
 */
async function getBrandSustainability(brandName) {
    try {
        // Utiliser le background script pour les appels API (obligatoire pour éviter CORS)
        return new Promise((resolve) => {
            chrome.runtime.sendMessage(
                { type: 'BG_GET_BRAND_DATA', brandName },
                (response) => {
                    if (chrome.runtime.lastError) {
                        console.error(`[GreenStyle] Erreur communication background:`, chrome.runtime.lastError);
                        resolve(null);
                        return;
                    }
                    
                    if (response?.success && response.data) {
                        resolve(response.data);
                    } else {
                        // Marque non trouvée ou erreur API
                        resolve(null);
                    }
                }
            );
            
            // Timeout de sécurité (5 secondes)
            setTimeout(() => {
                resolve(null);
            }, 5000);
        });
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
        // Sauvegarder une liste vide
        chrome.runtime.sendMessage({ type: 'BG_SAVE_DETECTED_BRANDS', brands: [] });
        return;
    }
    
    // Sauvegarder les marques détectées pour le popup
    chrome.runtime.sendMessage({ type: 'BG_SAVE_DETECTED_BRANDS', brands });
    
    // Récupérer les données pour chaque marque
    const brandPromises = brands.map(brand => getBrandSustainability(brand));
    const brandDataList = await Promise.all(brandPromises);
    
    // Stocker les données complètes pour le popup
    const brandsWithData = brands.map((brandName, index) => ({
        name: brandName,
        data: brandDataList[index]
    })).filter(b => b.data !== null); // Filtrer les marques non trouvées
    
    chrome.storage.local.set({ detectedBrandsData: brandsWithData });
    
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

