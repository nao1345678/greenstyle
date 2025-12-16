/**
 * Moteur de détection de marques pour extension Chrome
 * Analyse le DOM de la page pour identifier les marques présentes
 */

// Base de données des marques avec alias
const BRANDS_DATABASE = {
    'Mode': {
        'nike': ['nike air', 'air jordan', 'jordan'],
        'adidas': ['adidas originals', 'adidas performance'],
        'puma': ['puma sport'],
        'reebok': ['reebok classic'],
        'converse': ['converse all star'],
        'vans': ['vans old skool'],
        'timberland': ['timberland boots'],
        'levis': ['levi\'s', 'levis'],
        'zara': ['zara home'],
        'h&m': ['h&m home', 'h&m'],
        'uniqlo': ['uniqlo japan'],
        'gap': ['gap kids'],
        'tommy hilfiger': ['tommy'],
        'calvin klein': ['ck', 'calvin klein underwear'],
        'ralph lauren': ['polo ralph lauren'],
        'lacoste': ['lacoste sport'],
        'polo': ['polo ralph lauren'],
        'guess': ['guess jeans'],
        'diesel': ['diesel jeans'],
        'benetton': ['benetton group']
    },
    'Électronique': {
        'apple': ['apple inc', 'iphone', 'macbook', 'ipad', 'mac'],
        'samsung': ['samsung electronics', 'galaxy'],
        'sony': ['sony corporation'],
        'lg': ['lg electronics'],
        'panasonic': ['panasonic corporation'],
        'philips': ['philips lighting'],
        'sharp': ['sharp corporation'],
        'canon': ['canon inc'],
        'nikon': ['nikon corporation'],
        'fujifilm': ['fuji film'],
        'gopro': ['gopro hero'],
        'dji': ['dji drones'],
        'microsoft': ['ms', 'msft'],
        'dell': ['dell technologies'],
        'hp': ['hewlett packard'],
        'lenovo': ['lenovo group'],
        'asus': ['asus computer'],
        'acer': ['acer inc'],
        'toshiba': ['toshiba corporation'],
        'intel': ['intel corporation'],
        'amd': ['advanced micro devices'],
        'nvidia': ['nvidia corporation']
    },
    'Automobile': {
        'bmw': ['bayerische motoren werke'],
        'mercedes': ['mercedes-benz', 'benz'],
        'audi': ['audi ag'],
        'volkswagen': ['vw', 'volkswagen group'],
        'porsche': ['porsche ag'],
        'ferrari': ['ferrari nv'],
        'lamborghini': ['lamborghini automobili'],
        'toyota': ['toyota motor'],
        'honda': ['honda motor'],
        'nissan': ['nissan motor'],
        'mazda': ['mazda motor'],
        'subaru': ['subaru corporation'],
        'ford': ['ford motor'],
        'chevrolet': ['chevrolet motors'],
        'cadillac': ['cadillac motor'],
        'buick': ['buick motor'],
        'chrysler': ['chrysler group'],
        'dodge': ['dodge motor'],
        'jeep': ['jeep brand'],
        'fiat': ['fiat chrysler'],
        'alfa romeo': ['alfa romeo automobiles']
    },
    'Cosmétiques': {
        'loreal': ['l\'oréal', 'loreal paris'],
        'maybelline': ['maybelline new york'],
        'revlon': ['revlon inc'],
        'mac': ['mac cosmetics'],
        'clinique': ['clinique laboratories'],
        'estee lauder': ['estée lauder'],
        'chanel': ['chanel paris'],
        'dior': ['christian dior'],
        'ysl': ['yves saint laurent'],
        'guerlain': ['guerlain paris'],
        'lancome': ['lancôme'],
        'clarins': ['clarins paris'],
        'biotherm': ['biotherm paris']
    },
    'Luxe': {
        'louis vuitton': ['lv', 'louis vuitton malletier'],
        'gucci': ['gucci group'],
        'prada': ['prada spa'],
        'hermes': ['hermès paris'],
        'cartier': ['cartier international'],
        'rolex': ['rolex sa'],
        'omega': ['omega watches'],
        'swatch': ['swatch group'],
        'casio': ['casio computer'],
        'seiko': ['seiko corporation'],
        'citizen': ['citizen watch'],
        'timex': ['timex group'],
        'fossil': ['fossil group']
    }
};

class BrandDetectionEngine {
    constructor() {
        this.brands = this.extractAllBrands();
        this.results = {
            brands: [],
            byCategory: {},
            bySource: {
                text: [],
                links: [],
                images: [],
                attributes: [],
                metadata: []
            },
            statistics: {
                totalFound: 0,
                categoriesFound: 0,
                sourcesAnalyzed: 0
            }
        };
    }

    /**
     * Extrait toutes les marques et alias en un seul array
     */
    extractAllBrands() {
        const allBrands = [];
        for (const category in BRANDS_DATABASE) {
            for (const brand in BRANDS_DATABASE[category]) {
                allBrands.push(brand.toLowerCase());
                BRANDS_DATABASE[category][brand].forEach(alias => {
                    allBrands.push(alias.toLowerCase());
                });
            }
        }
        return [...new Set(allBrands)]; // Supprime les doublons
    }

    /**
     * Trouve la catégorie d'une marque
     */
    findBrandCategory(brandName) {
        const lowerBrand = brandName.toLowerCase();
        for (const category in BRANDS_DATABASE) {
            for (const brand in BRANDS_DATABASE[category]) {
                if (brand.toLowerCase() === lowerBrand) {
                    return category;
                }
                if (BRANDS_DATABASE[category][brand].some(alias => 
                    alias.toLowerCase() === lowerBrand)) {
                    return category;
                }
            }
        }
        return 'Autre';
    }

    /**
     * Normalise le nom de la marque (retourne le nom principal)
     */
    normalizeBrandName(brandName) {
        const lowerBrand = brandName.toLowerCase();
        for (const category in BRANDS_DATABASE) {
            for (const brand in BRANDS_DATABASE[category]) {
                if (brand.toLowerCase() === lowerBrand) {
                    return brand;
                }
                if (BRANDS_DATABASE[category][brand].some(alias => 
                    alias.toLowerCase() === lowerBrand)) {
                    return brand;
                }
            }
        }
        return brandName;
    }

    /**
     * Détecte les marques dans le texte
     */
    detectInText(text) {
        const found = [];
        const lowerText = text.toLowerCase();
        
        this.brands.forEach(brand => {
            if (lowerText.includes(brand)) {
                const normalizedBrand = this.normalizeBrandName(brand);
                if (!found.includes(normalizedBrand)) {
                    found.push(normalizedBrand);
                }
            }
        });
        
        return found;
    }

    /**
     * Détecte les marques dans les liens
     */
    detectInLinks() {
        const found = [];
        const links = document.querySelectorAll('a');
        
        links.forEach(link => {
            const href = link.href.toLowerCase();
            const text = link.textContent.toLowerCase();
            
            this.brands.forEach(brand => {
                if (href.includes(brand) || text.includes(brand)) {
                    const normalizedBrand = this.normalizeBrandName(brand);
                    if (!found.includes(normalizedBrand)) {
                        found.push(normalizedBrand);
                    }
                }
            });
        });
        
        return found;
    }

    /**
     * Détecte les marques dans les images
     */
    detectInImages() {
        const found = [];
        const images = document.querySelectorAll('img');
        
        images.forEach(img => {
            const alt = (img.alt || '').toLowerCase();
            const title = (img.title || '').toLowerCase();
            const src = (img.src || '').toLowerCase();
            
            this.brands.forEach(brand => {
                if (alt.includes(brand) || title.includes(brand) || src.includes(brand)) {
                    const normalizedBrand = this.normalizeBrandName(brand);
                    if (!found.includes(normalizedBrand)) {
                        found.push(normalizedBrand);
                    }
                }
            });
        });
        
        return found;
    }

    /**
     * Détecte les marques dans les attributs data
     */
    detectInAttributes() {
        const found = [];
        const dataSelectors = [
            '[data-brand]',
            '[data-vendor]',
            '[data-manufacturer]',
            '[data-company]',
            '[data-maker]'
        ];
        
        dataSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                const value = el.dataset.brand || 
                            el.dataset.vendor || 
                            el.dataset.manufacturer ||
                            el.dataset.company ||
                            el.dataset.maker;
                
                if (value) {
                    this.brands.forEach(brand => {
                        if (value.toLowerCase().includes(brand)) {
                            const normalizedBrand = this.normalizeBrandName(brand);
                            if (!found.includes(normalizedBrand)) {
                                found.push(normalizedBrand);
                            }
                        }
                    });
                }
            });
        });
        
        return found;
    }

    /**
     * Détecte les marques dans les métadonnées
     */
    detectInMetadata() {
        const found = [];
        const metaTags = document.querySelectorAll('meta');
        
        metaTags.forEach(meta => {
            const content = (meta.content || '').toLowerCase();
            const name = (meta.name || '').toLowerCase();
            const property = (meta.getAttribute('property') || '').toLowerCase();
            
            this.brands.forEach(brand => {
                if (content.includes(brand) || name.includes(brand) || property.includes(brand)) {
                    const normalizedBrand = this.normalizeBrandName(brand);
                    if (!found.includes(normalizedBrand)) {
                        found.push(normalizedBrand);
                    }
                }
            });
        });
        
        return found;
    }

    /**
     * Détecte les marques dans les classes CSS
     */
    detectInClasses() {
        const found = [];
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(el => {
            const classes = (el.className || '').toLowerCase();
            
            this.brands.forEach(brand => {
                if (classes.includes(brand) || classes.includes(`brand-${brand}`)) {
                    const normalizedBrand = this.normalizeBrandName(brand);
                    if (!found.includes(normalizedBrand)) {
                        found.push(normalizedBrand);
                    }
                }
            });
        });
        
        return found;
    }

    /**
     * Analyse complète de la page
     */
    analyzePage() {
        // Reset results
        this.results = {
            brands: [],
            byCategory: {},
            bySource: {
                text: [],
                links: [],
                images: [],
                attributes: [],
                metadata: [],
                classes: []
            },
            statistics: {
                totalFound: 0,
                categoriesFound: 0,
                sourcesAnalyzed: 0
            }
        };

        // 1. Analyse du texte principal
        const pageText = document.body.innerText || '';
        this.results.bySource.text = this.detectInText(pageText);

        // 2. Analyse des liens
        this.results.bySource.links = this.detectInLinks();

        // 3. Analyse des images
        this.results.bySource.images = this.detectInImages();

        // 4. Analyse des attributs data
        this.results.bySource.attributes = this.detectInAttributes();

        // 5. Analyse des métadonnées
        this.results.bySource.metadata = this.detectInMetadata();

        // 6. Analyse des classes CSS
        this.results.bySource.classes = this.detectInClasses();

        // Combiner tous les résultats
        const allFound = [
            ...this.results.bySource.text,
            ...this.results.bySource.links,
            ...this.results.bySource.images,
            ...this.results.bySource.attributes,
            ...this.results.bySource.metadata,
            ...this.results.bySource.classes
        ];

        // Supprimer les doublons et organiser par catégorie
        this.results.brands = [...new Set(allFound)];
        this.results.statistics.totalFound = this.results.brands.length;

        // Organiser par catégorie
        this.results.brands.forEach(brand => {
            const category = this.findBrandCategory(brand);
            if (!this.results.byCategory[category]) {
                this.results.byCategory[category] = [];
            }
            if (!this.results.byCategory[category].includes(brand)) {
                this.results.byCategory[category].push(brand);
            }
        });

        this.results.statistics.categoriesFound = Object.keys(this.results.byCategory).length;
        this.results.statistics.sourcesAnalyzed = Object.keys(this.results.bySource).length;

        return this.results;
    }

    /**
     * Affiche les résultats dans la console
     */
    logResults() {
        console.log('🔍 RÉSULTATS DE DÉTECTION DE MARQUES');
        console.log('=' .repeat(50));
        console.log(`📊 Marques trouvées: ${this.results.statistics.totalFound}`);
        console.log(`📁 Catégories: ${this.results.statistics.categoriesFound}`);
        
        if (this.results.brands.length > 0) {
            console.log('\n🏷️ Marques par catégorie:');
            for (const category in this.results.byCategory) {
                console.log(`  📂 ${category}:`);
                this.results.byCategory[category].forEach(brand => {
                    console.log(`    • ${brand}`);
                });
            }
            
            console.log('\n📋 Détail par source:');
            for (const source in this.results.bySource) {
                if (this.results.bySource[source].length > 0) {
                    console.log(`  ${source}: ${this.results.bySource[source].join(', ')}`);
                }
            }
        } else {
            console.log('\n❌ Aucune marque détectée sur cette page.');
        }
    }
}

// Fonction d'utilisation simple
function detectBrandsOnPage() {
    const engine = new BrandDetectionEngine();
    const results = engine.analyzePage();
    engine.logResults();
    return results;
}

// Export pour utilisation dans une extension
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BrandDetectionEngine, detectBrandsOnPage };
} 