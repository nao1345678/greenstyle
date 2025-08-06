/**
 * Détecteur de marques auto-apprenant pour extension Chrome
 * Version TypeScript avec types stricts
 */

interface BrandResult {
    brand: string;
    confidence: 'high' | 'medium' | 'low';
    source: 'known' | 'discovered' | 'candidate';
    context?: string;
    position?: number;
}

interface AnalysisResults {
    knownBrands: BrandResult[];
    discoveredBrands: BrandResult[];
    newCandidates: string[];
    newlyDiscovered: Array<{ brand: string; confidence: number }>;
    stats: {
        totalKnown: number;
        totalDiscovered: number;
        textLength: number;
        newBrandsFound: number;
    };
}

interface BrandPattern {
    pattern: RegExp;
    name: string;
    weight: number;
}

class ChromeBrandDetector {
    private knownBrands: Set<string>;
    private discoveredBrands: Set<string>;
    private brandPatterns: BrandPattern[];
    private brandIndicators: string[];
    private confidenceThreshold: number = 0.5;

    constructor() {
        // Base de données initiale
        this.knownBrands = new Set([
            'nike', 'adidas', 'apple', 'samsung', 'sony', 'zara', 'h&m', 'uniqlo',
            'bmw', 'mercedes', 'gucci', 'louis vuitton', 'chanel', 'dior',
            'coca-cola', 'pepsi', 'nestle', 'danone', 'microsoft', 'dell', 'hp',
            'lenovo', 'asus', 'acer', 'canon', 'nikon', 'fujifilm', 'gopro',
            'wilson', 'head', 'babolat', 'yonex', 'prince', 'dunlop'
        ]);

        this.discoveredBrands = new Set();

        // Patterns de détection avec poids
        this.brandPatterns = [
            { pattern: /marque\s*:\s*(\w+)/gi, name: 'marque_label', weight: 0.9 },
            { pattern: /fabricant\s*:\s*(\w+)/gi, name: 'fabricant_label', weight: 0.9 },
            { pattern: /brand\s*:\s*(\w+)/gi, name: 'brand_label', weight: 0.9 },
            { pattern: /manufacturer\s*:\s*(\w+)/gi, name: 'manufacturer_label', weight: 0.9 },
            { pattern: /by\s+(\w+)/gi, name: 'by_prefix', weight: 0.8 },
            { pattern: /©\s*(\w+)/gi, name: 'copyright', weight: 0.7 },
            { pattern: /™\s*(\w+)/gi, name: 'trademark', weight: 0.7 },
            { pattern: /propriétaire\s*:\s*(\w+)/gi, name: 'proprietaire_label', weight: 0.8 },
            { pattern: /distributeur\s*:\s*(\w+)/gi, name: 'distributeur_label', weight: 0.6 }
        ];

        this.brandIndicators = [
            'marque', 'fabricant', 'brand', 'manufacturer', 'propriétaire',
            'distributeur', 'éditeur', 'créateur', 'designer', 'producteur'
        ];

        this.loadSavedBrands();
    }

    /**
     * Charge les marques sauvegardées depuis le storage Chrome
     */
    private async loadSavedBrands(): Promise<void> {
        try {
            const result = await chrome.storage.local.get(['discoveredBrands']);
            if (result.discoveredBrands) {
                this.discoveredBrands = new Set(result.discoveredBrands);
                console.log(`📚 Chargé ${result.discoveredBrands.length} marques découvertes`);
            }
        } catch (error) {
            console.warn('Erreur lors du chargement des marques:', error);
        }
    }

    /**
     * Sauvegarde les marques découvertes dans le storage Chrome
     */
    private async saveDiscoveredBrands(): Promise<void> {
        try {
            const brands = Array.from(this.discoveredBrands);
            await chrome.storage.local.set({ discoveredBrands: brands });
            console.log(`💾 Sauvegardé ${brands.length} marques découvertes`);
        } catch (error) {
            console.warn('Erreur lors de la sauvegarde:', error);
        }
    }

    /**
     * Détecte les marques connues dans le texte
     */
    private detectKnownBrands(text: string): BrandResult[] {
        const found: BrandResult[] = [];
        const lowerText = text.toLowerCase();

        // Cherche les marques connues
        for (const brand of this.knownBrands) {
            const index = lowerText.indexOf(brand.toLowerCase());
            if (index !== -1) {
                found.push({
                    brand,
                    confidence: 'high',
                    source: 'known',
                    position: index,
                    context: this.extractContext(text, index, brand.length)
                });
            }
        }

        // Cherche les marques découvertes
        for (const brand of this.discoveredBrands) {
            const index = lowerText.indexOf(brand.toLowerCase());
            if (index !== -1) {
                found.push({
                    brand,
                    confidence: 'medium',
                    source: 'discovered',
                    position: index,
                    context: this.extractContext(text, index, brand.length)
                });
            }
        }

        return found;
    }

    /**
     * Extrait le contexte autour d'une marque trouvée
     */
    private extractContext(text: string, position: number, brandLength: number): string {
        const start = Math.max(0, position - 50);
        const end = Math.min(text.length, position + brandLength + 50);
        return text.substring(start, end).trim();
    }

    /**
     * Découvre de nouvelles marques potentielles
     */
    private discoverNewBrands(text: string): string[] {
        const candidates = new Set<string>();

        // 1. Cherche dans les patterns structurés
        this.brandPatterns.forEach(({ pattern, weight }) => {
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
    private isValidBrandCandidate(word: string): boolean {
        const cleanWord = word.replace(/[^\w]/g, '').toLowerCase();
        
        const criteria = [
            cleanWord.length >= 2 && cleanWord.length <= 20,
            /^[a-zA-Z]+$/.test(cleanWord),
            !this.isCommonWord(cleanWord),
            this.hasBrandCharacteristics(word)
        ];
        
        return criteria.every(criterion => criterion);
    }

    /**
     * Vérifie si c'est un mot commun
     */
    private isCommonWord(word: string): boolean {
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
    private hasBrandCharacteristics(word: string): boolean {
        const startsWithCapital = /^[A-Z]/.test(word);
        const hasBrandFeatures = /[A-Z]/.test(word) || 
                                word.includes('-') || 
                                word.includes('_') || 
                                /^[A-Z]{2,}$/.test(word);
        
        return startsWithCapital || hasBrandFeatures;
    }

    /**
     * Calcule la confiance qu'un candidat est vraiment une marque
     */
    private calculateConfidence(candidate: string, context: string): number {
        let score = 0;
        
        // Score basé sur la fréquence d'apparition
        const frequency = (context.match(new RegExp(candidate, 'gi')) || []).length;
        score += Math.min(frequency * 0.2, 0.4);
        
        // Score basé sur le contexte
        const brandKeywords = ['marque', 'fabricant', 'brand', 'manufacturer', 'propriétaire'];
        const hasBrandContext = brandKeywords.some(keyword => 
            context.toLowerCase().includes(keyword) && 
            context.toLowerCase().includes(candidate)
        );
        if (hasBrandContext) score += 0.3;
        
        // Score basé sur les caractéristiques du nom
        if (/^[A-Z]/.test(candidate)) score += 0.1;
        if (candidate.length >= 3) score += 0.1;
        if (candidate.length <= 15) score += 0.1;
        
        return Math.min(score, 1.0);
    }

    /**
     * Valide et ajoute de nouvelles marques
     */
    private async validateAndAddBrands(candidates: string[], context: string): Promise<Array<{ brand: string; confidence: number }>> {
        const newBrands: Array<{ brand: string; confidence: number }> = [];
        
        for (const candidate of candidates) {
            if (!this.knownBrands.has(candidate) && !this.discoveredBrands.has(candidate)) {
                const confidence = this.calculateConfidence(candidate, context);
                
                if (confidence > this.confidenceThreshold) {
                    this.discoveredBrands.add(candidate);
                    newBrands.push({ brand: candidate, confidence });
                    
                    console.log(`🎯 Nouvelle marque découverte: ${candidate} (confiance: ${confidence.toFixed(2)})`);
                }
            }
        }
        
        if (newBrands.length > 0) {
            await this.saveDiscoveredBrands();
        }
        
        return newBrands;
    }

    /**
     * Analyse complète d'une page
     */
    public async analyzePage(): Promise<AnalysisResults> {
        const text = document.body.innerText || '';
        
        const knownBrands = this.detectKnownBrands(text);
        const newCandidates = this.discoverNewBrands(text);
        const newlyDiscovered = await this.validateAndAddBrands(newCandidates, text);
        
        return {
            knownBrands,
            discoveredBrands: knownBrands.filter(b => b.source === 'discovered'),
            newCandidates,
            newlyDiscovered,
            stats: {
                totalKnown: this.knownBrands.size,
                totalDiscovered: this.discoveredBrands.size,
                textLength: text.length,
                newBrandsFound: newlyDiscovered.length
            }
        };
    }

    /**
     * Génère un rapport d'analyse
     */
    public generateReport(results: AnalysisResults): void {
        console.log('\n🔍 RAPPORT D\'ANALYSE DES MARQUES (Extension Chrome)');
        console.log('=' .repeat(60));
        
        console.log(`📊 Statistiques:`);
        console.log(`  - Marques connues: ${results.stats.totalKnown}`);
        console.log(`  - Marques découvertes: ${results.stats.totalDiscovered}`);
        console.log(`  - Texte analysé: ${results.stats.textLength} caractères`);
        console.log(`  - Nouvelles marques trouvées: ${results.stats.newBrandsFound}`);
        
        if (results.knownBrands.length > 0) {
            console.log(`\n🏷️  Marques trouvées (${results.knownBrands.length}):`);
            results.knownBrands.forEach(({ brand, confidence, source, context }) => {
                console.log(`  • ${brand} (${confidence}, ${source})`);
                if (context) {
                    console.log(`    Contexte: "${context}"`);
                }
            });
        }
        
        if (results.newlyDiscovered.length > 0) {
            console.log(`\n🎯 Nouvelles marques découvertes (${results.newlyDiscovered.length}):`);
            results.newlyDiscovered.forEach(({ brand, confidence }) => {
                console.log(`  • ${brand} (confiance: ${confidence.toFixed(2)})`);
            });
        }
        
        console.log('\n✅ Analyse terminée!');
    }

    /**
     * Retourne les statistiques de la base de données
     */
    public getStats(): { known: number; discovered: number; total: number } {
        return {
            known: this.knownBrands.size,
            discovered: this.discoveredBrands.size,
            total: this.knownBrands.size + this.discoveredBrands.size
        };
    }
}

// Export pour utilisation dans l'extension
export { ChromeBrandDetector, type AnalysisResults, type BrandResult }; 