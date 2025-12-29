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
    'dans', 'sur', 'sous', 'entre', 'depuis', 'jusqu', 'pendant', 'avant', 'après',
    'tous', 'toutes', 'tout', 'autre', 'autres', 'comme', 'tel', 'telle', 'tels',
    'telles', 'chez', 'chez', 'cette', 'ce', 'ces', 'cet', 'son', 'sa', 'ses',
    'leur', 'leurs', 'notre', 'nos', 'votre', 'vos', 'mon', 'ma', 'mes'
]);

// Sélecteurs pour identifier les zones à exclure (filtres, navigation, UI)
const EXCLUDED_SELECTORS = [
    'nav', 'header', 'footer', 'aside', '.sidebar',
    '.filter', '.filtre', '.filters', '.filtres', '.facets',
    '[class*="filter"]', '[class*="filtre"]', '[class*="facet"]',
    '[id*="filter"]', '[id*="filtre"]', '[id*="facet"]',
    '.navigation', '.menu', '.dropdown', '.dropdown-menu',
    '.breadcrumb', '.pagination', '.sort', '.trier',
    'button[class*="filter"]', 'button[class*="facet"]', 'button[class*="dropdown"]',
    'label[for*="filter"]', 'label[for*="facet"]',
    'select', 'option', '.select', '.option',
    '.toolbar', '.toolbar-top', '.toolbar-bottom',
    '.search', '.search-bar', '.search-box',
    '.header', '.header-top', '.header-bottom',
    '.topbar', '.top-bar', '.nav-bar'
];

// Sélecteurs pour identifier les éléments de produit valides
const PRODUCT_SELECTORS = [
    '.productCard', '.product-card', '.product-card-item',
    '.product', '.product-item', '.product-tile', '.product-tile-item',
    '[class*="product-card"]', '[class*="product-tile"]',
    '[data-product-id]', '[data-product-code]', '[data-product-sku]',
    'article.product', 'article[class*="product"]',
    '.item', '.item-card', '[class*="item-card"]',
    '.listing-item', '[class*="listing-item"]',
    '.grid-item', '[class*="grid-item"]'
];

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
    
    // Exclure les mots qui sont des phrases complètes (trop longs ou contiennent plusieurs mots)
    const words = normalized.split(/\s+/);
    if (words.length > 4) return false; // Max 4 mots pour une marque
    
    // Exclure les mots qui contiennent des prépositions/articles communs au début/fin
    if (/^(de|du|des|le|la|les|un|une|et|ou|par|pour|avec|sans)\s/.test(normalized)) return false;
    if (/\s(de|du|des|le|la|les|un|une|et|ou|par|pour|avec|sans)$/.test(normalized)) return false;
    
    // Exclure les mots qui sont des verbes communs
    const commonVerbs = ['acheter', 'vendre', 'voir', 'trouver', 'chercher', 'choisir', 'ajouter', 'panier'];
    if (commonVerbs.includes(normalized)) return false;
    
    return true;
}

/**
 * Vérifie si un élément est dans une zone exclue (filtres, navigation, UI)
 */
function isInExcludedZone(el) {
    if (!el) return true;
    
    // Vérifier les classes/id de l'élément lui-même
    const classList = el.className?.toLowerCase() || '';
    const id = el.id?.toLowerCase() || '';
    const tagName = el.tagName?.toLowerCase() || '';
    
    // Exclure les boutons de filtre/navigation
    if (tagName === 'button' && (
        classList.includes('facet') || 
        classList.includes('filter') || 
        classList.includes('filtre') ||
        classList.includes('dropdown') ||
        classList.includes('toggle') ||
        classList.includes('sort') ||
        classList.includes('trier') ||
        id.includes('facet') ||
        id.includes('filter') ||
        id.includes('filtre') ||
        id.includes('dropdown') ||
        id.includes('sort')
    )) {
        return true;
    }
    
    // Exclure les labels, selects, options
    if (['label', 'select', 'option', 'optgroup'].includes(tagName)) {
        if (id.includes('filter') || id.includes('facet') || id.includes('sort') ||
            classList.includes('filter') || classList.includes('facet') || classList.includes('sort')) {
            return true;
        }
    }
    
    // Vérifier si l'élément est dans une zone exclue (chercher dans les parents)
    for (const selector of EXCLUDED_SELECTORS) {
        try {
            const parent = el.closest(selector);
            if (parent) {
                return true;
            }
        } catch (e) {
            // Ignorer les erreurs de sélecteur invalide
        }
    }
    
    return false;
}

/**
 * Vérifie si un élément est dans un contexte de produit valide
 */
function isInProductContext(el) {
    if (!el) return false;
    
    // Vérifier si l'élément lui-même est un produit
    for (const selector of PRODUCT_SELECTORS) {
        try {
            if (el.matches && el.matches(selector)) {
                return true;
            }
        } catch (e) {
            // Ignorer les erreurs
        }
    }
    
    // Vérifier si l'élément est dans un élément de produit
    for (const selector of PRODUCT_SELECTORS) {
        try {
            const parent = el.closest(selector);
            if (parent) {
                return true;
            }
        } catch (e) {
            // Ignorer les erreurs
        }
    }
    
    return false;
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
    
    // 1. Chercher dans les éléments de produit seulement (plus précis, évite les faux positifs)
    // Ne pas chercher dans tout le texte de la page, mais seulement dans les contextes de produits
    PRODUCT_SELECTORS.forEach(selector => {
        try {
            document.querySelectorAll(selector).forEach(productEl => {
                // EXCLURE les produits dans les zones exclues (filtres, etc.)
                if (isInExcludedZone(productEl)) {
                    return;
                }
                
                const productText = productEl.textContent?.toLowerCase() || '';
                
                KNOWN_BRANDS.forEach(brand => {
                    const brandLower = brand.toLowerCase();
                    const aliases = BRANDS_WITH_ALIASES[brand] || [];
                    
                    // Utiliser des word boundaries pour éviter les faux positifs
                    const brandRegex = new RegExp(`\\b${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
                    
                    // Recherche du nom principal avec word boundaries
                    if (brandRegex.test(productText)) {
                        detectedBrands.add(brand);
                    }
                    
                    // Recherche des alias avec word boundaries
                    aliases.forEach(alias => {
                        const aliasRegex = new RegExp(`\\b${alias.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
                        if (aliasRegex.test(productText)) {
                            detectedBrands.add(brand);
                        }
                    });
                });
            });
        } catch (e) {
            // Ignorer les erreurs de sélecteur
        }
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
    
    // 5. Chercher dans les classes CSS spécifiques de marque (seulement dans les contextes de produits)
    const brandClassSelectors = [
        '.productCard-brand', '.product-card-brand',
        '[class*="vendor"]', '[class*="manufacturer"]',
        '[class*="product-brand"]', '[class*="item-brand"]'
    ];
    
    brandClassSelectors.forEach(selector => {
        try {
            document.querySelectorAll(selector).forEach(el => {
                // EXCLURE les éléments dans les zones exclues
                if (isInExcludedZone(el)) return;
                
                // Vérifier que l'élément est dans un contexte de produit
                if (!isInProductContext(el)) return;
                
                const classes = el.className.toLowerCase();
                const text = el.textContent?.toLowerCase() || '';
                
                KNOWN_BRANDS.forEach(brand => {
                    const brandLower = brand.toLowerCase();
                    // Chercher dans les classes ET dans le texte (plus sûr)
                    if (classes.includes(brandLower) || text.includes(brandLower)) {
                        detectedBrands.add(brand);
                    }
                });
            });
        } catch (e) {
            // Ignorer les erreurs
        }
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
    
    // 8. Chercher dans les microdata (itemprop="brand") - seulement dans les contextes de produits
    document.querySelectorAll('[itemprop="brand"]').forEach(el => {
        // EXCLURE les éléments dans les zones exclues
        if (isInExcludedZone(el)) return;
        
        // Vérifier que l'élément est dans un contexte de produit
        if (!isInProductContext(el)) return;
        
        const brandValue = (el.textContent || el.getAttribute('content') || '').trim().toLowerCase();
        if (!brandValue || brandValue.length < 2) return;
        
        KNOWN_BRANDS.forEach(brand => {
            const brandLower = brand.toLowerCase();
            const aliases = BRANDS_WITH_ALIASES[brand] || [];
            if (brandValue === brandLower || brandValue.includes(brandLower)) {
                detectedBrands.add(brand);
            }
            aliases.forEach(alias => {
                const aliasLower = alias.toLowerCase();
                if (brandValue === aliasLower || brandValue.includes(aliasLower)) {
                    detectedBrands.add(brand);
                }
            });
        });
    });
    
    // 9. Chercher dans les titres et descriptions de produits (déjà fait dans la section 1, donc on skip)
    
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
    const brandDataAttributes = ['data-brand', 'data-vendor', 'data-manufacturer', 'data-company', 'data-product-brand'];
    brandDataAttributes.forEach(attr => {
        document.querySelectorAll(`[${attr}]`).forEach(el => {
            // EXCLURE les éléments dans les zones exclues
            if (isInExcludedZone(el)) return;
            
            // Vérifier que l'élément est dans un contexte de produit
            if (!isInProductContext(el)) return;
            
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
    
    // Chercher dans itemprop="brand" est déjà fait dans la section 8, donc on skip ici pour éviter les doublons
    
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
                            console.log(`[GreenStyle] ❌ Impossible de récupérer les données pour "${brandName}" (erreur communication)`);
                            resolve(null);
                            return;
                        }
                        
                        if (response?.success && response.data) {
                            // Vérifier que les données sont valides (au moins un score défini)
                            const hasValidScore = response.data.final_score !== null && 
                                                  response.data.final_score !== undefined;
                            if (hasValidScore) {
                                console.log(`[GreenStyle] ✅ Marque "${brandName}" validée (score: ${response.data.final_score.toFixed(1)}/10)`);
                                resolve(response.data);
                            } else {
                                console.log(`[GreenStyle] ⚠️ Marque "${brandName}" retournée par l'API mais sans score valide (ignorée)`);
                                resolve(null);
                            }
                        } else {
                            // Marque non trouvée (404) ou erreur API
                            if (response?.error === '404' || response?.error?.includes('not found')) {
                                console.log(`[GreenStyle] ⚠️ Marque "${brandName}" non trouvée dans la base de données et scraping échoué`);
                                resolve(null);
                            } else if (attempt < retries && response?.error) {
                                // Retry si erreur réseau (500, timeout, etc.)
                                console.log(`[GreenStyle] ⚠️ Erreur API pour "${brandName}" (tentative ${attempt}/${retries}): ${response.error}`);
                                setTimeout(() => attemptRequest(attempt + 1), 1000 * attempt);
                                return;
                            } else {
                                console.log(`[GreenStyle] ❌ Impossible de récupérer les données pour "${brandName}" (erreur: ${response?.error || 'unknown'})`);
                                resolve(null);
                            }
                        }
                    }
                );
            };
            
            attemptRequest(1);
            
            // Timeout de sécurité (10 secondes avec retries)
            setTimeout(() => {
                console.log(`[GreenStyle] ⏱️ Timeout lors de la récupération pour "${brandName}"`);
                resolve(null);
            }, 10000);
        });
    } catch (error) {
        console.error(`[GreenStyle] ❌ Erreur lors de la récupération pour ${brandName}:`, error);
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
    
    // Récupérer les données pour chaque marque (vérification dans la DB + scraping si nécessaire)
    console.log(`[GreenStyle] 🔍 Vérification des ${brands.length} marques détectées dans la base de données...`);
    const brandPromises = brands.map(brand => getBrandSustainability(brand));
    const brandDataList = await Promise.all(brandPromises);
    
    // Filtrer pour ne garder QUE les marques qui ont des données valides (présentes dans la DB ou scrapées avec succès)
    // Une marque sans données = pas une vraie marque ou scraping échoué = on ne l'affiche pas
    const validatedBrandsWithData = brands
        .map((brandName, index) => ({
            name: brandName,
            data: brandDataList[index]
        }))
        .filter(brandItem => {
            // Garder seulement les marques avec des données valides (non-null et avec au moins un score)
            const hasValidData = brandItem.data && (
                brandItem.data.final_score !== null && 
                brandItem.data.final_score !== undefined
            );
            if (!hasValidData) {
                console.log(`[GreenStyle] ⚠️ Marque "${brandItem.name}" non validée (pas dans la DB et scraping échoué), ignorée pour l'affichage`);
            }
            return hasValidData;
        });
    
    // Stocker TOUTES les marques pour le popup (même sans données, pour afficher "non trouvé")
    const brandsWithData = brands.map((brandName, index) => ({
        name: brandName,
        data: brandDataList[index]
    }));
    chrome.storage.local.set({ detectedBrandsData: brandsWithData });
    
    console.log(`[GreenStyle] ✅ Marques validées: ${validatedBrandsWithData.length}/${brands.length} (${brands.length - validatedBrandsWithData.length} ignorées car non trouvées dans la DB)`);
    
    if (validatedBrandsWithData.length === 0) {
        console.log('[GreenStyle] ⚠️ Aucune marque validée trouvée, aucun badge ne sera affiché');
        return;
    }
    
    // Créer une map des marques VALIDÉES vers les éléments de produit
    // Ne chercher dans le DOM QUE pour les marques qui ont été validées
    const brandToElementsMap = new Map();
    
    validatedBrandsWithData.forEach((brandItem) => {
        // Double vérification (normalement déjà filtré, mais sécurité)
        if (!brandItem.data || brandItem.data.final_score === null || brandItem.data.final_score === undefined) {
            return;
        }
        
        const brandName = brandItem.name;
        const brandLower = brandName.toLowerCase();
        const brandRegex = new RegExp(`^${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'i');
        
        // Utiliser les fonctions globales isInExcludedZone et isInProductContext
        
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
                // EXCLURE les éléments dans les zones exclues
                if (isInExcludedZone(brandEl)) {
                    return; // Ignorer cet élément
                }
                
                // Vérifier que l'élément est dans un contexte de produit
                if (!isInProductContext(brandEl)) {
                    return; // Ignorer si pas dans un contexte de produit
                }
                
                const brandText = (brandEl.textContent || '').trim().toLowerCase();
                
                // Vérifier si le texte correspond exactement à la marque (word boundary pour éviter les faux positifs)
                const exactBrandRegex = new RegExp(`^${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$|\\b${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
                if (exactBrandRegex.test(brandText)) {
                    // Trouver le productCard parent
                    let productCard = null;
                    for (const productSelector of PRODUCT_SELECTORS) {
                        try {
                            productCard = brandEl.closest(productSelector);
                            if (productCard) break;
                        } catch (e) {
                            // Ignorer les erreurs
                        }
                    }
                    
                    if (productCard) {
                        // Vérifier aussi que le productCard n'est pas dans une zone exclue
                        if (!isInExcludedZone(productCard)) {
                            if (!brandToElementsMap.has(brandName)) {
                                brandToElementsMap.set(brandName, []);
                            }
                            if (!brandToElementsMap.get(brandName).includes(productCard)) {
                                brandToElementsMap.get(brandName).push(productCard);
                                console.log(`[GreenStyle] ✅ Marque "${brandName}" trouvée dans ${selector}, productCard associé`);
                            }
                        }
                    } else {
                        // Si pas de productCard trouvé avec les sélecteurs, utiliser le parent proche
                        // MAIS seulement si c'est un contexte de produit valide
                        const parent = brandEl.closest('div, article, section, li') || brandEl.parentElement;
                        if (parent && !isInExcludedZone(parent) && isInProductContext(parent)) {
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
        
        // 2. Chercher les marques dans les URLs des liens (seulement dans les contextes de produits)
        document.querySelectorAll('a[href]').forEach(link => {
            // EXCLURE les liens dans les zones exclues
            if (isInExcludedZone(link)) {
                return;
            }
            
            // Vérifier que le lien est dans un contexte de produit
            if (!isInProductContext(link)) {
                return;
            }
            
            const href = link.href.toLowerCase();
            
            // Vérifier si l'URL contient la marque (ex: /p/vestes-diesel/...)
            // Utiliser des word boundaries pour éviter les faux positifs
            const urlPatterns = [
                `/${brandLower}/`,
                `/${brandLower}-`,
                `-${brandLower}/`,
                `-${brandLower}-`,
                `/${brandLower}?`,
                `?brand=${brandLower}`,
                `&brand=${brandLower}`
            ];
            
            // Vérifier avec regex plus strict pour éviter les faux positifs
            const urlBrandRegex = new RegExp(`[/-]${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[/-]|[/-]${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[?&]`, 'i');
            
            if (urlBrandRegex.test(href)) {
                // Trouver l'élément productCard parent
                let productCard = null;
                for (const productSelector of PRODUCT_SELECTORS) {
                    try {
                        productCard = link.closest(productSelector);
                        if (productCard) break;
                    } catch (e) {
                        // Ignorer les erreurs
                    }
                }
                
                if (productCard && !isInExcludedZone(productCard)) {
                    if (!brandToElementsMap.has(brandName)) {
                        brandToElementsMap.set(brandName, []);
                    }
                    if (!brandToElementsMap.get(brandName).includes(productCard)) {
                        brandToElementsMap.get(brandName).push(productCard);
                        console.log(`[GreenStyle] ✅ Marque "${brandName}" trouvée dans URL: ${href.substring(0, 80)}`);
                    }
                }
            }
        });
        
        // 3. Chercher les marques dans le texte visible des productCard (fallback avec word boundaries stricts)
        PRODUCT_SELECTORS.forEach(selector => {
            try {
                document.querySelectorAll(selector).forEach(card => {
                    // EXCLURE les productCard dans les zones exclues
                    if (isInExcludedZone(card)) {
                        return;
                    }
                    
                    // Ignorer si déjà trouvé
                    if (brandToElementsMap.get(brandName)?.includes(card)) return;
                    
                    const text = card.textContent?.toLowerCase() || '';
                    // Utiliser word boundaries pour éviter les faux positifs (ex: "marque" dans "marque")
                    const strictBrandRegex = new RegExp(`\\b${brandLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
                    if (strictBrandRegex.test(text)) {
                        if (!brandToElementsMap.has(brandName)) {
                            brandToElementsMap.set(brandName, []);
                        }
                        if (!brandToElementsMap.get(brandName).includes(card)) {
                            brandToElementsMap.get(brandName).push(card);
                        }
                    }
                });
            } catch (e) {
                // Ignorer les erreurs de sélecteur
            }
        });
    });
    
    // Afficher les badges UNIQUEMENT pour les marques validées (qui ont des données)
    validatedBrandsWithData.forEach((brandItem) => {
        // Double vérification (normalement déjà filtré, mais sécurité)
        if (!brandItem.data || brandItem.data.final_score === null || brandItem.data.final_score === undefined) {
            return;
        }
        
        const brandName = brandItem.name;
        const elements = brandToElementsMap.get(brandName) || [];
        
        // Afficher le badge sur chaque élément de produit trouvé (max 5 par marque)
        elements.slice(0, 5).forEach(el => {
            displayScoreBadge(brandName, brandItem.data, el);
        });
        
        if (elements.length > 0) {
            console.log(`[GreenStyle] ✅ Badge affiché pour ${brandName} (${brandItem.data.final_score.toFixed(1)}/10) sur ${elements.length} élément(s)`);
        } else {
            console.log(`[GreenStyle] ⚠️ Marque "${brandName}" validée mais aucun élément de produit trouvé dans le DOM pour afficher le badge`);
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

