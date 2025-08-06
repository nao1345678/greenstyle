/**
 * Moteur de détection de marques auto-apprenant
 * Construit sa propre base de données en découvrant de nouvelles marques
 */

class LearningBrandDetector {
    constructor() {
        // Base de données initiale (marques connues)
        this.knownBrands = new Set([
            'nike', 'adidas', 'apple', 'samsung', 'sony', 'zara', 'h&m', 'uniqlo',
            'bmw', 'mercedes', 'gucci', 'louis vuitton', 'chanel', 'dior',
            'coca-cola', 'pepsi', 'nestle', 'danone', 'microsoft', 'dell', 'hp'
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
            /™\s*(\w+)/gi
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
                found.push({ brand, confidence: 'high', source: 'known' });
            }
        }
        
        // Cherche les marques découvertes
        for (const brand of this.discoveredBrands) {
            if (lowerText.includes(brand.toLowerCase())) {
                found.push({ brand, confidence: 'medium', source: 'discovered' });
            }
        }
        
        return found;
    }
    
    /**
     * Découvre de nouvelles marques potentielles
     */
    discoverNewBrands(text) {
        const candidates = new Set();
        const lowerText = text.toLowerCase();
        
        // 1. Cherche dans les patterns structurés
        this.brandPatterns.forEach(pattern => {
            const matches = text.match(pattern);
            if (matches) {
                matches.forEach(match => {
                    const brand = match.replace(/^.*?:\s*/, '').trim();
                    if (brand.length > 2 && brand.length < 50) {
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
                        if (nextWord && this.isPotentialBrand(nextWord)) {
                            candidates.add(nextWord.toLowerCase());
                        }
                    }
                }
            });
        });
        
        // 3. Cherche des mots avec des caractéristiques de marques
        words.forEach(word => {
            if (this.isPotentialBrand(word)) {
                candidates.add(word.toLowerCase());
            }
        });
        
        return Array.from(candidates);
    }
    
    /**
     * Détermine si un mot pourrait être une marque
     */
    isPotentialBrand(word) {
        const cleanWord = word.replace(/[^\w]/g, '').toLowerCase();
        
        // Critères pour une marque potentielle
        const criteria = [
            cleanWord.length >= 2 && cleanWord.length <= 20, // Taille raisonnable
            /^[a-zA-Z]+$/.test(cleanWord), // Seulement des lettres
            !this.isCommonWord(cleanWord), // Pas un mot commun
            this.hasBrandCharacteristics(cleanWord) // Caractéristiques de marque
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
            'product', 'item', 'goods', 'article', 'piece', 'model', 'version'
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
     * Valide et ajoute de nouvelles marques à la base de données
     */
    validateAndAddBrands(candidates, context) {
        const newBrands = [];
        
        candidates.forEach(candidate => {
            // Vérifie si ce n'est pas déjà connu
            if (!this.knownBrands.has(candidate) && !this.discoveredBrands.has(candidate)) {
                
                // Validation basée sur le contexte
                const confidence = this.calculateConfidence(candidate, context);
                
                if (confidence > 0.5) { // Seuil de confiance
                    this.discoveredBrands.add(candidate);
                    newBrands.push({ brand: candidate, confidence });
                    
                    console.log(`🎯 Nouvelle marque découverte: ${candidate} (confiance: ${confidence.toFixed(2)})`);
                }
            }
        });
        
        // Sauvegarde les nouvelles découvertes
        if (newBrands.length > 0) {
            this.saveDiscoveredBrands();
        }
        
        return newBrands;
    }
    
    /**
     * Calcule la confiance qu'un candidat est vraiment une marque
     */
    calculateConfidence(candidate, context) {
        let score = 0;
        
        // Score basé sur la fréquence d'apparition
        const frequency = (context.match(new RegExp(candidate, 'gi')) || []).length;
        score += Math.min(frequency * 0.2, 0.4);
        
        // Score basé sur le contexte (proximité avec des mots-clés)
        const brandKeywords = ['marque', 'fabricant', 'brand', 'manufacturer', 'propriétaire'];
        const hasBrandContext = brandKeywords.some(keyword => 
            context.toLowerCase().includes(keyword) && 
            context.toLowerCase().includes(candidate)
        );
        if (hasBrandContext) score += 0.3;
        
        // Score basé sur les caractéristiques du nom
        if (/^[A-Z]/.test(candidate)) score += 0.1; // Commence par majuscule
        if (candidate.length >= 3) score += 0.1; // Taille minimale
        if (candidate.length <= 15) score += 0.1; // Taille maximale
        
        return Math.min(score, 1.0);
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
        
        // Valide et ajoute les nouvelles marques
        results.newlyDiscovered = this.validateAndAddBrands(results.newCandidates, text);
        
        return results;
    }
    
    /**
     * Affiche un rapport d'analyse
     */
    generateReport(results) {
        console.log('\n🔍 RAPPORT D\'ANALYSE DES MARQUES');
        console.log('=' .repeat(50));
        
        console.log(`📊 Statistiques:`);
        console.log(`  - Marques connues: ${results.stats.totalKnown}`);
        console.log(`  - Marques découvertes: ${results.stats.totalDiscovered}`);
        console.log(`  - Texte analysé: ${results.stats.textLength} caractères`);
        
        if (results.knownBrands.length > 0) {
            console.log(`\n🏷️  Marques connues trouvées (${results.knownBrands.length}):`);
            results.knownBrands.forEach(({ brand, confidence, source }) => {
                console.log(`  • ${brand} (${confidence}, ${source})`);
            });
        }
        
        if (results.newlyDiscovered.length > 0) {
            console.log(`\n🎯 Nouvelles marques découvertes (${results.newlyDiscovered.length}):`);
            results.newlyDiscovered.forEach(({ brand, confidence }) => {
                console.log(`  • ${brand} (confiance: ${confidence.toFixed(2)})`);
            });
        }
        
        if (results.newCandidates.length > 0) {
            console.log(`\n🔍 Candidats analysés (${results.newCandidates.length}):`);
            results.newCandidates.forEach(candidate => {
                console.log(`  • ${candidate}`);
            });
        }
        
        console.log('\n✅ Analyse terminée!');
    }
}

// Utilisation
const detector = new LearningBrandDetector();

// Analyser la page actuelle
const results = detector.analyzePage();
detector.generateReport(results);

// Exporter pour utilisation dans une extension
window.BrandDetector = LearningBrandDetector; 