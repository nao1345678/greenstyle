/**
 * Content script pour détecter les marques sur la page et afficher les scores de durabilité
 * Communique avec l'API FastAPI backend
 */

// Configuration de l'API backend
const API_BASE_URL = 'http://localhost:8000'; // À adapter selon votre configuration

// Base de données enrichie des marques avec alias pour une meilleure détection
const BRANDS_WITH_ALIASES = {
    // Mode & Sportswear
    'nike': ['nike air', 'air jordan', 'jordan', 'nike.com', 'just do it'],
    'adidas': ['adidas originals', 'adidas performance', 'adidas.com', 'adidas yeezy', 'yeezy'],
    'puma': ['puma sport', 'puma.com'],
    'reebok': ['reebok classic', 'reebok.com'],
    'converse': ['converse all star', 'converse.com', 'chuck taylor'],
    'vans': ['vans old skool', 'vans.com'],
    'timberland': ['timberland boots', 'timberland.com'],
    'levis': ['levi\'s', 'levis', 'levis.com', 'levi strauss'],
    'zara': ['zara home', 'zara.com'],
    'h&m': ['h&m home', 'h&m', 'hm.com', 'h&m home'],
    'uniqlo': ['uniqlo japan', 'uniqlo.com'],
    'gap': ['gap kids', 'gap.com'],
    'tommy hilfiger': ['tommy', 'tommyhilfiger.com'],
    'calvin klein': ['ck', 'calvin klein underwear', 'calvinklein.com'],
    'ralph lauren': ['polo ralph lauren', 'ralphlauren.com', 'polo'],
    'lacoste': ['lacoste sport', 'lacoste.com'],
    'the north face': ['north face', 'thenorthface.com', 'tnf'],
    'columbia': ['columbia.com'],
    'salomon': ['salomon.com'],
    'arc\'teryx': ['arcteryx', 'arcteryx.com'],
    
    // Mode durable & éthique
    'patagonia': ['patagonia.com'],
    'veja': ['veja.com'],
    'reformation': ['reformation.com'],
    'everlane': ['everlane.com'],
    'tentree': ['tentree.com'],
    'allbirds': ['allbirds.com'],
    'rothys': ['rothys.com'],
    'mud jeans': ['mudjeans.com'],
    'thought': ['thoughtclothing.com'],
    
    // Streetwear & Luxe
    'supreme': ['supremenewyork.com'],
    'stussy': ['stussy.com'],
    'off-white': ['offwhite.com', 'off white'],
    'a bathing ape': ['bape', 'bape.com'],
    'palace': ['palaceskateboards.com'],
    'kith': ['kith.com'],
    'fear of god': ['fearofgod.com'],
    'gucci': ['gucci.com'],
    'prada': ['prada.com'],
    'versace': ['versace.com'],
    'balenciaga': ['balenciaga.com'],
    'louis vuitton': ['louisvuitton.com', 'lv'],
    'dior': ['dior.com'],
    'chanel': ['chanel.com'],
    'hermes': ['hermes.com'],
    
    // Fast Fashion
    'primark': ['primark.com'],
    'forever 21': ['forever21.com', 'f21'],
    'asos': ['asos.com'],
    'boohoo': ['boohoo.com'],
    'shein': ['shein.com'],
    'zaful': ['zaful.com'],
    'fashion nova': ['fashionnova.com'],
    
    // Mode européenne
    'mango': ['mango.com'],
    'bershka': ['bershka.com'],
    'pull & bear': ['pullandbear.com'],
    'stradivarius': ['stradivarius.com'],
    'cos': ['cos.com'],
    '& other stories': ['stories.com'],
    'aritzia': ['aritzia.com'],
    
    // Accessoires & Chaussures
    'dr martens': ['drmartens.com', 'doc martens'],
    'ugg': ['ugg.com', 'ugg australia', 'ugg boots', 'uggs', 'ugg®'],
    'birkenstock': ['birkenstock.com'],
    'clarks': ['clarks.com'],
    'new balance': ['newbalance.com', 'nb'],
    'asics': ['asics.com'],
    'under armour': ['underarmour.com', 'ua'],
    
    // Mode vintage & seconde main
    'depop': ['depop.com'],
    'vestiaire collective': ['vestiairecollective.com'],
    'the realreal': ['therealreal.com'],
    'grailed': ['grailed.com']
};

// Liste simple pour la recherche rapide
const KNOWN_BRANDS = Object.keys(BRANDS_WITH_ALIASES);

/**
 * Détecte les marques présentes sur la page
 * Recherche dans plusieurs sources pour une meilleure détection sur les sites e-commerce
 */
function detectBrandsOnPage() {
    const detectedBrands = new Set();
    
    if (!document.body || !document.body.innerText) {
        console.log('[GreenStyle] ⚠️ Body non disponible pour la détection');
        return [];
    }
    
    const pageText = document.body.innerText.toLowerCase();
    const pageHTML = document.body.innerHTML.toLowerCase();
    
    console.log('[GreenStyle] 📄 Texte de la page analysé:', pageText.length, 'caractères');
    console.log('[GreenStyle] 📄 Extrait du texte:', pageText.substring(0, 200));
    
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
    const metaSelectors = [
        'meta[property="product:brand"]',
        'meta[name="brand"]',
        'meta[property="og:brand"]',
        'meta[itemprop="brand"]'
    ];
    metaSelectors.forEach(selector => {
        const metaBrand = document.querySelector(selector);
        if (metaBrand) {
            const metaValue = (metaBrand.content || metaBrand.getAttribute('content') || '').toLowerCase();
            KNOWN_BRANDS.forEach(brand => {
                const brandLower = brand.toLowerCase();
                const aliases = BRANDS_WITH_ALIASES[brand] || [];
                if (metaValue.includes(brandLower)) {
                    detectedBrands.add(brand);
                }
                aliases.forEach(alias => {
                    if (metaValue.includes(alias.toLowerCase())) {
                        detectedBrands.add(brand);
                    }
                });
            });
        }
    });
    
    // 7. Chercher dans JSON-LD structured data (très utilisé par les sites e-commerce)
    try {
        const jsonLdScripts = document.querySelectorAll('script[type="application/ld+json"]');
        jsonLdScripts.forEach(script => {
            try {
                const data = JSON.parse(script.textContent);
                const searchInJsonLd = (obj) => {
                    if (typeof obj === 'string') {
                        const text = obj.toLowerCase();
                        KNOWN_BRANDS.forEach(brand => {
                            const brandLower = brand.toLowerCase();
                            const aliases = BRANDS_WITH_ALIASES[brand] || [];
                            if (text.includes(brandLower)) {
                                detectedBrands.add(brand);
                            }
                            aliases.forEach(alias => {
                                if (text.includes(alias.toLowerCase())) {
                                    detectedBrands.add(brand);
                                }
                            });
                        });
                    } else if (typeof obj === 'object' && obj !== null) {
                        // Rechercher dans les propriétés spécifiques
                        if (obj.brand || obj.manufacturer || obj.producer) {
                            const brandValue = (obj.brand?.name || obj.brand || obj.manufacturer || obj.producer || '').toLowerCase();
                            KNOWN_BRANDS.forEach(brand => {
                                const brandLower = brand.toLowerCase();
                                const aliases = BRANDS_WITH_ALIASES[brand] || [];
                                if (brandValue.includes(brandLower)) {
                                    detectedBrands.add(brand);
                                }
                                aliases.forEach(alias => {
                                    if (brandValue.includes(alias.toLowerCase())) {
                                        detectedBrands.add(brand);
                                    }
                                });
                            });
                        }
                        // Recherche récursive
                        Object.values(obj).forEach(value => searchInJsonLd(value));
                    }
                };
                searchInJsonLd(data);
            } catch (e) {
                // Ignorer les erreurs de parsing JSON
            }
        });
    } catch (e) {
        // Ignorer les erreurs
    }
    
    // 8. Chercher dans les microdata (itemprop="brand")
    document.querySelectorAll('[itemprop="brand"]').forEach(el => {
        const brandValue = (el.textContent || el.getAttribute('content') || '').toLowerCase();
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            const aliases = BRANDS_WITH_ALIASES[brand] || [];
            if (brandValue.includes(brandLower)) {
                detectedBrands.add(brand);
            }
            aliases.forEach(alias => {
                if (brandValue.includes(alias.toLowerCase())) {
                    detectedBrands.add(brand);
                }
            });
        });
    });
    
    // 9. Chercher dans les titres et descriptions de produits
    const productSelectors = [
        '[class*="product"]',
        '[class*="item"]',
        '[id*="product"]',
        '[id*="item"]'
    ];
    productSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            const text = (el.textContent || '').toLowerCase();
            const title = (el.getAttribute('title') || '').toLowerCase();
            const combined = text + ' ' + title;
            
            KNOWN_BRANDS.forEach(brand => {
                const brandLower = brand.toLowerCase();
                const aliases = BRANDS_WITH_ALIASES[brand] || [];
                if (combined.includes(brandLower)) {
                    detectedBrands.add(brand);
                }
                aliases.forEach(alias => {
                    if (combined.includes(alias.toLowerCase())) {
                        detectedBrands.add(brand);
                    }
                });
            });
        });
    });
    
    // 10. Détection générique de marques depuis les meta tags et attributs (pour marques non listées)
    // Chercher dans les meta tags de marque
    const brandMetaSelectors = [
        'meta[property="product:brand"]',
        'meta[name="brand"]',
        'meta[property="og:brand"]',
        'meta[itemprop="brand"]'
    ];
    brandMetaSelectors.forEach(selector => {
        const meta = document.querySelector(selector);
        if (meta) {
            const brandValue = (meta.content || meta.getAttribute('content') || '').trim();
            if (brandValue && brandValue.length > 1 && brandValue.length < 50) {
                // Normaliser le nom de marque (enlever caractères spéciaux en début/fin)
                const normalizedBrand = brandValue.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
                if (normalizedBrand) {
                    detectedBrands.add(normalizedBrand);
                    console.log(`[GreenStyle] 🔍 Marque détectée depuis meta tag (${selector}): ${normalizedBrand}`);
                }
            }
        }
    });
    
    // Chercher dans les attributs data-brand, data-vendor, etc.
    const brandDataAttributes = ['data-brand', 'data-vendor', 'data-manufacturer', 'data-company'];
    brandDataAttributes.forEach(attr => {
        document.querySelectorAll(`[${attr}]`).forEach(el => {
            const brandValue = (el.getAttribute(attr) || '').trim();
            if (brandValue && brandValue.length > 1 && brandValue.length < 50) {
                const normalizedBrand = brandValue.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
                if (normalizedBrand) {
                    detectedBrands.add(normalizedBrand);
                    console.log(`[GreenStyle] 🔍 Marque détectée depuis ${attr}: ${normalizedBrand}`);
                }
            }
        });
    });
    
    // Chercher dans itemprop="brand"
    document.querySelectorAll('[itemprop="brand"]').forEach(el => {
        const brandValue = (el.textContent || el.getAttribute('content') || '').trim();
        if (brandValue && brandValue.length > 1 && brandValue.length < 50) {
            const normalizedBrand = brandValue.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
            if (normalizedBrand) {
                detectedBrands.add(normalizedBrand);
                console.log(`[GreenStyle] 🔍 Marque détectée depuis itemprop="brand": ${normalizedBrand}`);
            }
        }
    });
    
    // Chercher dans les JSON-LD (structured data) - recherche récursive
    try {
        document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
            try {
                const jsonData = JSON.parse(script.textContent);
                
                // Fonction récursive pour chercher "brand" dans l'objet JSON
                const findBrand = (obj) => {
                    if (!obj || typeof obj !== 'object') return null;
                    
                    // Si c'est un tableau, chercher dans chaque élément
                    if (Array.isArray(obj)) {
                        for (const item of obj) {
                            const result = findBrand(item);
                            if (result) return result;
                        }
                        return null;
                    }
                    
                    // Chercher directement "brand"
                    if (obj.brand) {
                        const brandName = typeof obj.brand === 'string' 
                            ? obj.brand 
                            : (obj.brand.name || obj.brand['@type'] || (obj.brand['@id'] ? obj.brand['@id'].split('/').pop() : null));
                        if (brandName && typeof brandName === 'string') {
                            return brandName.trim();
                        }
                    }
                    
                    // Chercher récursivement dans toutes les propriétés
                    for (const key in obj) {
                        if (obj.hasOwnProperty(key) && typeof obj[key] === 'object') {
                            const result = findBrand(obj[key]);
                            if (result) return result;
                        }
                    }
                    return null;
                };
                
                const brandName = findBrand(jsonData);
                if (brandName) {
                    const normalizedBrand = brandName.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
                    if (normalizedBrand && normalizedBrand.length > 1 && normalizedBrand.length < 50) {
                        detectedBrands.add(normalizedBrand);
                        console.log(`[GreenStyle] 🔍 Marque détectée depuis JSON-LD: ${normalizedBrand}`);
                    }
                }
            } catch (e) {
                // Ignorer les erreurs de parsing JSON
            }
        });
    } catch (e) {
        // Ignorer les erreurs
    }
    
    // Ajouter des logs pour les marques détectées génériquement
    const knownBrandsArray = Array.from(detectedBrands).filter(b => KNOWN_BRANDS.includes(b));
    const genericBrandsArray = Array.from(detectedBrands).filter(b => !KNOWN_BRANDS.includes(b));
    
    if (genericBrandsArray.length > 0) {
        console.log(`[GreenStyle] 🔍 Marques détectées génériquement (non listées): ${genericBrandsArray.join(', ')}`);
    }
    
    console.log(`[GreenStyle] ✅ Détection terminée: ${detectedBrands.size} marque(s) trouvée(s) (${knownBrandsArray.length} connues, ${genericBrandsArray.length} nouvelles)`);
    return Array.from(detectedBrands);
}

/**
 * Récupère les informations de durabilité depuis l'API
 * Utilise UNIQUEMENT le background script pour éviter les problèmes CORS
 */
async function getBrandSustainability(brandName, retries = 3) {
    try {
        // Utiliser le background script pour les appels API (obligatoire pour éviter CORS)
        return new Promise((resolve) => {
            const attemptRequest = (attempt) => {
                chrome.runtime.sendMessage(
                    { type: 'BG_GET_BRAND_DATA', brandName },
                    (response) => {
                        if (chrome.runtime.lastError) {
                            console.error(`[GreenStyle] Erreur communication background (tentative ${attempt}/${retries}):`, chrome.runtime.lastError);
                            if (attempt < retries) {
                                // Retry avec délai exponentiel
                                setTimeout(() => attemptRequest(attempt + 1), 1000 * attempt);
                                return;
                            }
                            resolve(null);
                            return;
                        }
                        
                        if (response?.success && response.data) {
                            resolve(response.data);
                        } else {
                            // Marque non trouvée ou erreur API
                            if (attempt < retries && response?.error) {
                                // Retry si erreur réseau
                                setTimeout(() => attemptRequest(attempt + 1), 1000 * attempt);
                                return;
                            }
                            resolve(null);
                        }
                    }
                );
            };
            
            attemptRequest(1);
            
            // Timeout de sécurité (10 secondes avec retries)
            setTimeout(() => {
                resolve(null);
            }, 10000);
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
    console.log('[GreenStyle] Démarrage de la détection de marques...');
    console.log('[GreenStyle] Page URL:', window.location.href);
    console.log('[GreenStyle] Nombre de marques connues:', KNOWN_BRANDS.length);
    
    const brands = detectBrandsOnPage();
    console.log(`[GreenStyle] Marques détectées: ${brands.length > 0 ? brands.join(', ') : 'AUCUNE'}`);
    
    if (brands.length === 0) {
        console.log('[GreenStyle] Aucune marque détectée. Texte de la page (premiers 200 caractères):', document.body.innerText.substring(0, 200));
        // Sauvegarder une liste vide
        chrome.runtime.sendMessage({ type: 'BG_SAVE_DETECTED_BRANDS', brands: [] });
        chrome.storage.local.set({ detectedBrandsData: [] }); // Vider les données si aucune marque
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
    })); // Ne pas filtrer les null ici, le popup gérera l'affichage "non trouvé"
    
    chrome.storage.local.set({ detectedBrandsData: brandsWithData });
    console.log('[GreenStyle] Marques sauvegardées:', brands.length, 'marques');
    
    // Afficher les badges sur les éléments contenant les marques
    brandsWithData.forEach((brandItem) => {
        if (!brandItem.data) return; // Ne pas afficher de badge si pas de données API
        
        const brandName = brandItem.name;
        const brandLower = brandName.toLowerCase();
        
        // Trouver les éléments contenant cette marque
        const elements = Array.from(document.querySelectorAll('*')).filter(el => {
            const text = el.textContent?.toLowerCase() || '';
            // Éléments feuilles ou éléments avec peu d'enfants pour éviter les chevauchements
            return text.includes(brandLower) && (el.children.length === 0 || el.children.length < 3);
        });
        
        // Afficher le badge sur le premier élément trouvé (ou plusieurs si besoin)
        elements.slice(0, 3).forEach(el => {
            displayScoreBadge(brandName, brandItem.data, el);
        });
    });
}

// Démarrer la détection au chargement de la page
console.log('[GreenStyle] ✅ Content script chargé!');
console.log('[GreenStyle] URL:', window.location.href);
console.log('[GreenStyle] État du document:', document.readyState);

if (document.readyState === 'loading') {
    console.log('[GreenStyle] Document en cours de chargement, attente DOMContentLoaded...');
    document.addEventListener('DOMContentLoaded', () => {
        console.log('[GreenStyle] DOMContentLoaded déclenché');
        setTimeout(() => {
            console.log('[GreenStyle] Démarrage de la détection après délai...');
            processDetectedBrands();
        }, 2000); // Attendre 2s pour que la page soit complètement chargée
    });
} else {
    console.log('[GreenStyle] ✅ Document déjà chargé');
    setTimeout(() => {
        console.log('[GreenStyle] Démarrage de la détection après délai...');
        processDetectedBrands();
    }, 2000); // Attendre 2s pour les pages déjà chargées
}

// Réexécuter lors des changements de page (SPA)
let lastUrl = location.href;
new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        console.log('[GreenStyle] 🔄 Changement détecté dans le DOM, nouvelle analyse...');
        setTimeout(processDetectedBrands, 2000); // Attendre 2s après changement d'URL
    }
}).observe(document, { subtree: true, childList: true });

