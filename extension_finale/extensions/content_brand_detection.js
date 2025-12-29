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
    'diesel': ['diesel.com', 'diesel jeans'],
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

// Mots à exclure (ne sont pas des marques)
const EXCLUDED_WORDS = new Set([
    'marque', 'brand', 'marques', 'brands', 'trier', 'sort', 'recomma', 'recommandé',
    'recommandation', 'filtre', 'filter', 'prix', 'price', 'couleur', 'color',
    'taille', 'size', 'catégorie', 'category', 'résultat', 'result', 'article',
    'product', 'produit', 'mode', 'fashion', 'homme', 'femme', 'enfant', 'home',
    'maison', 'beauté', 'beauty', 'nouveauté', 'nouveautés', 'promotion', 'soldes',
    'accueil', 'home', 'retour', 'back', 'voir', 'see', 'plus', 'more', 'de', 'des',
    'du', 'la', 'le', 'les', 'un', 'une', 'et', 'ou', 'par', 'pour', 'avec', 'sans',
    'dans', 'sur', 'sous', 'entre', 'depuis', 'jusqu', 'pendant', 'avant', 'après'
]);

/**
 * Vérifie si un mot est une marque valide (pas un mot commun)
 */
function isValidBrandName(brandName) {
    if (!brandName || brandName.length < 2) return false;
    const normalized = brandName.toLowerCase().trim();
    
    // Exclure les mots communs
    if (EXCLUDED_WORDS.has(normalized)) return false;
    
    // Exclure les mots trop courts (sauf marques connues)
    if (normalized.length < 3 && !KNOWN_BRANDS.includes(normalized)) return false;
    
    // Exclure les mots qui sont des nombres
    if (/^\d+$/.test(normalized)) return false;
    
    // Exclure les mots qui contiennent seulement des caractères spéciaux
    if (!/[a-z]/.test(normalized)) return false;
    
    return true;
}

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
    
    // 1. Chercher dans le texte visible (avec word boundaries pour éviter les faux positifs)
    KNOWN_BRANDS.forEach(brand => {
        const brandLower = brand.toLowerCase();
        const aliases = BRANDS_WITH_ALIASES[brand] || [];
        
        // Utiliser des word boundaries pour éviter les faux positifs (ex: "marque" dans "marque")
        const brandRegex = new RegExp(`\\b${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
        
        // Recherche du nom principal avec word boundaries
        if (brandRegex.test(pageText)) {
            detectedBrands.add(brand);
        }
        
        // Recherche des alias avec word boundaries
        aliases.forEach(alias => {
            const aliasRegex = new RegExp(`\\b${alias.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
            if (aliasRegex.test(pageText)) {
                detectedBrands.add(brand);
            }
        });
    });
    
    // 2. Chercher dans les liens (href et texte) - IMPORTANT pour détecter les marques dans les URLs
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.href.toLowerCase();
        const text = link.textContent.toLowerCase();
        
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            const aliases = BRANDS_WITH_ALIASES[brand] || [];
            
            // Pour les URLs, chercher la marque dans le chemin (ex: /p/vestes-diesel/ ou /diesel/vestes)
            // Patterns courants: /brand/, /-brand/, /brand-/, /brand/
            const urlPatterns = [
                `/${brandLower}/`,
                `-${brandLower}/`,
                `/${brandLower}-`,
                `/${brandLower}?`,
                `?brand=${brandLower}`,
                `&brand=${brandLower}`
            ];
            
            if (urlPatterns.some(pattern => href.includes(pattern))) {
                detectedBrands.add(brand);
                console.log(`[GreenStyle] 🔍 Marque "${brand}" détectée dans URL: ${href.substring(0, 80)}`);
            }
            
            // Pour le texte, utiliser word boundaries
            const brandRegex = new RegExp(`\\b${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
            if (brandRegex.test(text)) {
                detectedBrands.add(brand);
            }
            
            aliases.forEach(alias => {
                const aliasLower = alias.toLowerCase();
                const aliasUrlPatterns = [
                    `/${aliasLower}/`,
                    `-${aliasLower}/`,
                    `/${aliasLower}-`
                ];
                if (aliasUrlPatterns.some(pattern => href.includes(pattern))) {
                    detectedBrands.add(brand);
                }
                const aliasRegex = new RegExp(`\\b${aliasLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
                if (aliasRegex.test(text)) {
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
    // EXCLURE [class*="brand"] car trop générique et peut matcher les filtres
    // Utiliser seulement les classes spécifiques comme .productCard-brand
    document.querySelectorAll('[class*="vendor"], [class*="manufacturer"]').forEach(el => {
        // Exclure les éléments de filtre/navigation
        const isFilter = el.closest('nav, header, .filter, .filtre, .facet, [class*="filter"], [class*="filtre"], [class*="facet"], button[class*="facet"], button[class*="filter"], button[class*="dropdown"]');
        if (isFilter) return;
        
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
                // Vérifier que c'est une marque valide (pas un mot commun)
                if (normalizedBrand && isValidBrandName(normalizedBrand)) {
                    detectedBrands.add(normalizedBrand);
                    console.log(`[GreenStyle] 🔍 Marque détectée depuis meta tag (${selector}): ${normalizedBrand}`);
                }
            }
        }
    });
    
    // Chercher dans les attributs data-brand, data-vendor, etc. (mais exclure les filtres)
    const brandDataAttributes = ['data-brand', 'data-vendor', 'data-manufacturer', 'data-company'];
    brandDataAttributes.forEach(attr => {
        document.querySelectorAll(`[${attr}]`).forEach(el => {
            // Ignorer les éléments dans les filtres, navigation, ou labels
            const parent = el.closest('label, .filter, .filtre, [class*="filter"], [class*="filtre"], nav, header, .navigation, select, option');
            if (parent) {
                return; // Ignorer cet élément
            }
            
            const brandValue = (el.getAttribute(attr) || '').trim();
            if (brandValue && brandValue.length > 1 && brandValue.length < 50) {
                const normalizedBrand = brandValue.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
                // Vérifier que c'est une marque valide (pas un mot commun)
                if (normalizedBrand && isValidBrandName(normalizedBrand)) {
                    detectedBrands.add(normalizedBrand);
                    console.log(`[GreenStyle] 🔍 Marque détectée depuis ${attr}: ${normalizedBrand}`);
                }
            }
        });
    });
    
    // Chercher dans itemprop="brand" (mais exclure les éléments de filtre/navigation)
    document.querySelectorAll('[itemprop="brand"]').forEach(el => {
        // Ignorer les éléments dans les filtres, navigation, ou labels
        const parent = el.closest('label, .filter, .filtre, [class*="filter"], [class*="filtre"], nav, header, .navigation');
        if (parent) {
            return; // Ignorer cet élément
        }
        
        const brandValue = (el.textContent || el.getAttribute('content') || '').trim();
        if (brandValue && brandValue.length > 1 && brandValue.length < 50) {
            const normalizedBrand = brandValue.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, '').toLowerCase();
            // Vérifier que c'est une marque valide (pas un mot commun)
            if (normalizedBrand && isValidBrandName(normalizedBrand)) {
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
                    // Vérifier que c'est une marque valide (pas un mot commun)
                    if (normalizedBrand && normalizedBrand.length > 1 && normalizedBrand.length < 50 && isValidBrandName(normalizedBrand)) {
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
    
    // Filtrer les marques détectées pour exclure les mots communs
    const filteredBrands = Array.from(detectedBrands).filter(brand => {
        // Garder les marques connues
        if (KNOWN_BRANDS.includes(brand)) return true;
        // Filtrer les marques génériques avec isValidBrandName
        return isValidBrandName(brand);
    });
    
    // Ajouter des logs pour les marques détectées génériquement
    const knownBrandsArray = filteredBrands.filter(b => KNOWN_BRANDS.includes(b));
    const genericBrandsArray = filteredBrands.filter(b => !KNOWN_BRANDS.includes(b));
    
    if (genericBrandsArray.length > 0) {
        console.log(`[GreenStyle] 🔍 Marques détectées génériquement (non listées): ${genericBrandsArray.join(', ')}`);
    }
    
    console.log(`[GreenStyle] ✅ Détection terminée: ${filteredBrands.length} marque(s) trouvée(s) (${knownBrandsArray.length} connues, ${genericBrandsArray.length} nouvelles)`);
    return filteredBrands;
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
    
    // Créer une map des marques détectées vers les éléments de produit
    const brandToElementsMap = new Map();
    
    brandsWithData.forEach((brandItem) => {
        if (!brandItem.data) return;
        
        const brandName = brandItem.name;
        const brandLower = brandName.toLowerCase();
        const brandRegex = new RegExp(`^${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'i');
        
        // Fonction pour vérifier si un élément est dans une zone de filtre/navigation
        const isInFilterOrNavigation = (el) => {
            // Vérifier les classes/id de l'élément
            const classList = el.className?.toLowerCase() || '';
            const id = el.id?.toLowerCase() || '';
            const tagName = el.tagName?.toLowerCase() || '';
            
            // Exclure les boutons de filtre
            if (tagName === 'button' && (
                classList.includes('facet') || 
                classList.includes('filter') || 
                classList.includes('filtre') ||
                classList.includes('dropdown') ||
                classList.includes('toggle') ||
                id.includes('facet') ||
                id.includes('filter') ||
                id.includes('filtre') ||
                id.includes('dropdown')
            )) {
                return true;
            }
            
            // Vérifier si l'élément est dans une zone de filtre/navigation
            const parent = el.closest('nav, header, .filter, .filtre, .facet, [class*="filter"], [class*="filtre"], [class*="facet"], [id*="filter"], [id*="filtre"], [id*="facet"], .navigation, .sidebar, .filters, .facets');
            return parent !== null;
        };
        
        // 1. PRIORITÉ: Chercher dans les éléments spécifiques de marque (ex: .productCard-brand)
        // EXCLURE [class*="brand"] car cela peut matcher des éléments de filtre comme "facet-brand" ou "filter-brand"
        const brandSelectors = [
            '.productCard-brand',
            '.product-card-brand',
            // '[class*="brand"]', // EXCLU car trop générique et peut matcher les filtres
            '[class*="vendor"]',
            '[class*="manufacturer"]',
            '[data-brand]',
            '[itemprop="brand"]'
        ];
        
        brandSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(brandEl => {
                // EXCLURE les éléments de filtre/navigation
                if (isInFilterOrNavigation(brandEl)) {
                    return; // Ignorer cet élément
                }
                
                const brandText = (brandEl.textContent || '').trim().toLowerCase();
                
                // Vérifier si le texte correspond exactement à la marque
                if (brandRegex.test(brandText)) {
                    // Trouver le productCard parent
                    const productCard = brandEl.closest('.productCard, .product-card, [class*="product"], [class*="item"], article, [data-product-id]');
                    if (productCard) {
                        // Vérifier aussi que le productCard n'est pas dans une zone de filtre
                        if (!isInFilterOrNavigation(productCard)) {
                            if (!brandToElementsMap.has(brandName)) {
                                brandToElementsMap.set(brandName, []);
                            }
                            if (!brandToElementsMap.get(brandName).includes(productCard)) {
                                brandToElementsMap.get(brandName).push(productCard);
                                console.log(`[GreenStyle] ✅ Marque "${brandName}" trouvée dans ${selector}, productCard associé`);
                            }
                        }
                    } else {
                        // Si pas de productCard, utiliser l'élément brand lui-même ou son parent proche
                        // MAIS seulement si ce n'est pas dans une zone de filtre
                        const parent = brandEl.closest('div, article, section') || brandEl.parentElement;
                        if (parent && !isInFilterOrNavigation(parent)) {
                            if (!brandToElementsMap.has(brandName)) {
                                brandToElementsMap.set(brandName, []);
                            }
                            if (!brandToElementsMap.get(brandName).includes(parent)) {
                                brandToElementsMap.get(brandName).push(parent);
                            }
                        }
                    }
                }
            });
        });
        
        // Fonction pour vérifier si un élément est dans une zone de filtre/navigation
        const isInFilterOrNavigation = (el) => {
            const classList = el.className?.toLowerCase() || '';
            const id = el.id?.toLowerCase() || '';
            const tagName = el.tagName?.toLowerCase() || '';
            
            if (tagName === 'button' && (
                classList.includes('facet') || 
                classList.includes('filter') || 
                classList.includes('filtre') ||
                classList.includes('dropdown') ||
                classList.includes('toggle') ||
                id.includes('facet') ||
                id.includes('filter') ||
                id.includes('filtre') ||
                id.includes('dropdown')
            )) {
                return true;
            }
            
            const parent = el.closest('nav, header, .filter, .filtre, .facet, [class*="filter"], [class*="filtre"], [class*="facet"], [id*="filter"], [id*="filtre"], [id*="facet"], .navigation, .sidebar, .filters, .facets');
            return parent !== null;
        };
        
        // 2. Chercher les marques dans les URLs des liens
        document.querySelectorAll('a[href]').forEach(link => {
            // EXCLURE les liens dans les filtres
            if (isInFilterOrNavigation(link)) {
                return;
            }
            
            const href = link.href.toLowerCase();
            
            // Vérifier si l'URL contient la marque (ex: /p/vestes-diesel/...)
            const urlPatterns = [
                `/${brandLower}/`,
                `-${brandLower}/`,
                `/${brandLower}-`,
                `/${brandLower}?`
            ];
            
            if (urlPatterns.some(pattern => href.includes(pattern))) {
                // Trouver l'élément productCard parent
                const productCard = link.closest('.productCard, .product-card, [class*="product"], [class*="item"], article, [data-product-id]');
                if (productCard && !isInFilterOrNavigation(productCard)) {
                    if (!brandToElementsMap.has(brandName)) {
                        brandToElementsMap.set(brandName, []);
                    }
                    if (!brandToElementsMap.get(brandName).includes(productCard)) {
                        brandToElementsMap.get(brandName).push(productCard);
                    }
                }
            }
        });
        
        // 3. Chercher les marques dans le texte visible des productCard (fallback)
        document.querySelectorAll('.productCard, .product-card, [class*="product"], [class*="item"], article').forEach(card => {
            // EXCLURE les productCard dans les filtres
            if (isInFilterOrNavigation(card)) {
                return;
            }
            
            // Ignorer si déjà trouvé
            if (brandToElementsMap.get(brandName)?.includes(card)) return;
            
            const text = card.textContent?.toLowerCase() || '';
            if (brandRegex.test(text)) {
                if (!brandToElementsMap.has(brandName)) {
                    brandToElementsMap.set(brandName, []);
                }
                if (!brandToElementsMap.get(brandName).includes(card)) {
                    brandToElementsMap.get(brandName).push(card);
                }
            }
        });
    });
    
    // 3. Afficher les badges sur les éléments trouvés
    brandsWithData.forEach((brandItem) => {
        if (!brandItem.data) return;
        
        const brandName = brandItem.name;
        const elements = brandToElementsMap.get(brandName) || [];
        
        // Afficher le badge sur chaque élément de produit trouvé (max 5 par marque)
        elements.slice(0, 5).forEach(el => {
            displayScoreBadge(brandName, brandItem.data, el);
        });
        
        if (elements.length > 0) {
            console.log(`[GreenStyle] ✅ Badge affiché pour ${brandName} sur ${elements.length} élément(s)`);
        }
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

