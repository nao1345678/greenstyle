/**
 * Détecteur de marques auto-apprenant simplifié
 * Version sans notation - juste détection et apprentissage
 */

class SimpleBrandDetector {
    constructor() {
        // Base de données initiale (marques connues)
        this.knownBrands = new Set([
            'nike', 'adidas', 'apple', 'samsung', 'sony', 'zara', 'h&m', 'uniqlo',
            'bmw', 'mercedes', 'gucci', 'louis vuitton', 'chanel', 'dior',
            'coca-cola', 'pepsi', 'nestle', 'danone', 'microsoft', 'dell', 'hp',
            'lenovo', 'asus', 'acer', 'canon', 'nikon', 'fujifilm', 'gopro',
            'wilson', 'head', 'babolat', 'yonex', 'prince', 'dunlop'
        ]);
        
        // Marques découvertes (nouvelles)
        this.discoveredBrands = new Set();
        
        // Patterns pour identifier de potentielles marques
        this.brandPatterns = [
            /marque\s*:\s*(\w+)/gi,
            /fabricant\s*:\s*(\w+)/gi,
            /brand\s*:\s*(\w+)/gi,
            /manufacturer\s*:\s*(\w+)/gi,
            /by\s+(\w+)/gi,
            /©\s*(\w+)/gi,
            /™\s*(\w+)/gi,
            /propriétaire\s*:\s*(\w+)/gi,
            /distributeur\s*:\s*(\w+)/gi
        ];
        
        // Mots-clés qui indiquent qu'un terme pourrait être une marque
        this.brandIndicators = [
            'marque', 'fabricant', 'brand', 'manufacturer', 'propriétaire',
            'distributeur', 'éditeur', 'créateur', 'designer'
        ];
        
        // Charger les marques sauvegardées
        this.loadSavedBrands();
    }
    
    /**
     * Charge les marques sauvegardées depuis le localStorage
     */
    loadSavedBrands() {
        try {
            const saved = localStorage.getItem('discoveredBrands');
            if (saved) {
                const brands = JSON.parse(saved);
                this.discoveredBrands = new Set(brands);
                console.log(`📚 Chargé ${brands.length} marques découvertes`);
            }
        } catch (error) {
            console.warn('Erreur lors du chargement des marques:', error);
        }
    }
    
    /**
     * Sauvegarde les marques découvertes dans le localStorage
     */
    saveDiscoveredBrands() {
        try {
            const brands = Array.from(this.discoveredBrands);
            localStorage.setItem('discoveredBrands', JSON.stringify(brands));
            console.log(`💾 Sauvegardé ${brands.length} marques découvertes`);
        } catch (error) {
            console.warn('Erreur lors de la sauvegarde:', error);
        }
    }
    
    /**
     * Détecte les marques connues dans le texte
     */
    detectKnownBrands(text) {
        const found = [];
        const lowerText = text.toLowerCase();
        
        // Cherche les marques connues
        for (const brand of this.knownBrands) {
            if (lowerText.includes(brand.toLowerCase())) {
                found.push({ brand, source: 'known' });
            }
        }
        
        // Cherche les marques découvertes
        for (const brand of this.discoveredBrands) {
            if (lowerText.includes(brand.toLowerCase())) {
                found.push({ brand, source: 'discovered' });
            }
        }
        
        return found;
    }
    
    /**
     * Découvre de nouvelles marques potentielles
     */
    discoverNewBrands(text) {
        const candidates = new Set();
        
        // 1. Cherche dans les patterns structurés
        this.brandPatterns.forEach(pattern => {
            const matches = text.match(pattern);
            if (matches) {
                matches.forEach(match => {
                    const brand = match.replace(/^.*?:\s*/, '').trim();
                    if (this.isValidBrandCandidate(brand)) {
                        candidates.add(brand.toLowerCase());
                    }
                });
            }
        });
        
        // 2. Cherche des mots proches des indicateurs de marque
        const words = text.split(/\s+/);
        words.forEach((word, index) => {
            this.brandIndicators.forEach(indicator => {
                if (word.toLowerCase().includes(indicator)) {
                    // Regarde les mots suivants
                    for (let i = 1; i <= 3; i++) {
                        const nextWord = words[index + i];
                        if (nextWord && this.isValidBrandCandidate(nextWord)) {
                            candidates.add(nextWord.toLowerCase());
                        }
                    }
                }
            });
        });
        
        // 3. Cherche des mots avec des caractéristiques de marques
        words.forEach(word => {
            if (this.isValidBrandCandidate(word)) {
                candidates.add(word.toLowerCase());
            }
        });
        
        return Array.from(candidates);
    }
    
    /**
     * Valide si un candidat peut être une marque
     */
    isValidBrandCandidate(word) {
        const cleanWord = word.replace(/[^\w]/g, '').toLowerCase();
        
        // Critères simples pour une marque potentielle
        const criteria = [
            cleanWord.length >= 2 && cleanWord.length <= 20, // Taille raisonnable
            /^[a-zA-Z]+$/.test(cleanWord), // Seulement des lettres
            !this.isCommonWord(cleanWord), // Pas un mot commun
            this.hasBrandCharacteristics(word) // Caractéristiques de marque
        ];
        
        return criteria.every(criterion => criterion);
    }
    
    /**
     * Vérifie si c'est un mot commun (pas une marque)
     */
    isCommonWord(word) {
        const commonWords = [
            'le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'mais', 'donc',
            'avec', 'sans', 'pour', 'par', 'sur', 'sous', 'dans', 'de', 'du',
            'the', 'and', 'or', 'but', 'with', 'without', 'for', 'by', 'in', 'on',
            'product', 'item', 'goods', 'article', 'piece', 'model', 'version',
            'new', 'old', 'big', 'small', 'good', 'bad', 'best', 'worst'
        ];
        return commonWords.includes(word.toLowerCase());
    }
    
    /**
     * Vérifie les caractéristiques typiques d'une marque
     */
    hasBrandCharacteristics(word) {
        // Commence par une majuscule (dans le texte original)
        const startsWithCapital = /^[A-Z]/.test(word);
        
        // Contient des caractéristiques de marque
        const hasBrandFeatures = /[A-Z]/.test(word) || // CamelCase
                                word.includes('-') || // Kebab-case
                                word.includes('_') || // Snake_case
                                /^[A-Z]{2,}$/.test(word); // Acronymes
        
        return startsWithCapital || hasBrandFeatures;
    }
    
    /**
     * Ajoute de nouvelles marques à la base de données
     */
    addNewBrands(candidates) {
        const newBrands = [];
        
        candidates.forEach(candidate => {
            // Vérifie si ce n'est pas déjà connu
            if (!this.knownBrands.has(candidate) && !this.discoveredBrands.has(candidate)) {
                this.discoveredBrands.add(candidate);
                newBrands.push(candidate);
                console.log(`🎯 Nouvelle marque découverte: ${candidate}`);
            }
        });
        
        // Sauvegarde les nouvelles découvertes
        if (newBrands.length > 0) {
            this.saveDiscoveredBrands();
        }
        
        return newBrands;
    }
    
    /**
     * Analyse complète d'une page et apprend de nouvelles marques
     */
    analyzePage() {
        const text = document.body.innerText || '';
        
        const results = {
            knownBrands: this.detectKnownBrands(text),
            newCandidates: this.discoverNewBrands(text),
            newlyDiscovered: [],
            stats: {
                totalKnown: this.knownBrands.size,
                totalDiscovered: this.discoveredBrands.size,
                textLength: text.length
            }
        };
        
        // Ajoute les nouvelles marques
        results.newlyDiscovered = this.addNewBrands(results.newCandidates);
        
        return results;
    }
    
    /**
     * Affiche un rapport d'analyse simplifié
     */
    generateReport(results) {
        console.log('\n🔍 RAPPORT D\'ANALYSE DES MARQUES');
        console.log('=' .repeat(50));
        
        console.log(`📊 Statistiques:`);
        console.log(`  - Marques connues: ${results.stats.totalKnown}`);
        console.log(`  - Marques découvertes: ${results.stats.totalDiscovered}`);
        console.log(`  - Texte analysé: ${results.stats.textLength} caractères`);
        
        if (results.knownBrands.length > 0) {
            console.log(`\n🏷️  Marques trouvées (${results.knownBrands.length}):`);
            results.knownBrands.forEach(({ brand, source }) => {
                console.log(`  • ${brand} (${source})`);
            });
        }
        
        if (results.newlyDiscovered.length > 0) {
            console.log(`\n🎯 Nouvelles marques découvertes (${results.newlyDiscovered.length}):`);
            results.newlyDiscovered.forEach(brand => {
                console.log(`  • ${brand}`);
            });
        }
        
        if (results.knownBrands.length === 0 && results.newlyDiscovered.length === 0) {
            console.log('\n❌ Aucune marque trouvée sur cette page.');
        }
        
        console.log('\n✅ Analyse terminée!');
    }
    
    /**
     * Retourne les statistiques de la base de données
     */
    getStats() {
        return {
            known: this.knownBrands.size,
            discovered: this.discoveredBrands.size,
            total: this.knownBrands.size + this.discoveredBrands.size
        };
    }
    
    /**
     * Efface toutes les marques découvertes
     */
    clearDiscoveredBrands() {
        this.discoveredBrands.clear();
        this.saveDiscoveredBrands();
        console.log('🗑️ Toutes les marques découvertes ont été effacées');
    }
}

// Utilisation
const detector = new SimpleBrandDetector();

// Analyser la page actuelle
const results = detector.analyzePage();
detector.generateReport(results);

// Exporter pour utilisation dans une extension
window.SimpleBrandDetector = SimpleBrandDetector; 