#!/usr/bin/env python3
"""
AI Master Orchestrator - Intelligence Artificielle Complète
Gère TOUS les scrappings et apprend à optimiser la collecte de données
"""

import pandas as pd
import numpy as np
import csv
import time
import pickle
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Import des scrapers existants
import sys
sys.path.append(os.path.dirname(__file__))

class AIBrandIntelligence:
    """
    Intelligence Artificielle Maîtresse pour la collecte et l'analyse de données de durabilité
    
    Cette IA:
    1. APPREND quelle source de données est la plus fiable pour chaque type d'info
    2. DÉCIDE intelligemment quelle stratégie de scraping utiliser
    3. PRÉDIT les scores de durabilité
    4. S'AMÉLIORE avec chaque nouvelle donnée collectée
    """
    
    def __init__(self):
        # Modèles ML pour différentes tâches
        self.source_selector_model = None  # Choix de la meilleure source
        self.scorer_model = None  # Prédiction des scores
        self.quality_predictor_model = None  # Prédiction de la qualité des données
        
        # Scalers
        self.scaler = StandardScaler()
        
        # Historique d'apprentissage
        self.learning_history = {
            'sources_tried': [],
            'sources_success': {},
            'scraping_times': {},
            'data_quality': {}
        }
        
        # Configuration des scrapers
        self.scrapers_config = {
            'recycled_materials': {
                'sources': ['database', 'website', 'good_on_you', 'reports'],
                'priority': ['database', 'reports', 'website', 'good_on_you'],
                'success_rate': {},
                'avg_time': {}
            },
            'certifications': {
                'sources': ['database', 'bcorp', 'fairtrade', 'good_on_you', 'fashion_revolution', 'website'],
                'priority': ['database', 'bcorp', 'fairtrade', 'good_on_you', 'fashion_revolution', 'website'],
                'success_rate': {},
                'avg_time': {}
            },
            'unsold_management': {
                'sources': ['database', 'good_on_you', 'fashion_revolution', 'website'],
                'priority': ['database', 'good_on_you', 'fashion_revolution', 'website'],
                'success_rate': {},
                'avg_time': {}
            },
            'supply_chain': {
                'sources': ['database', 'website', 'fashion_revolution'],
                'priority': ['database', 'fashion_revolution', 'website'],
                'success_rate': {},
                'avg_time': {}
            }
        }
        
        self.trained = False
        
    def learn_from_scraping_history(self, history_file='scraping_history.pkl'):
        """
        APPRENTISSAGE : Apprend de l'historique des scrappings précédents
        Le modèle apprend quelles sources sont les plus fiables
        """
        if os.path.exists(history_file):
            print("\n📚 Chargement de l'historique d'apprentissage...")
            with open(history_file, 'rb') as f:
                self.learning_history = pickle.load(f)
            
            # Mettre à jour les taux de succès
            for data_type, config in self.scrapers_config.items():
                for source in config['sources']:
                    key = f"{data_type}_{source}"
                    if key in self.learning_history['sources_success']:
                        success_data = self.learning_history['sources_success'][key]
                        if success_data['total'] > 0:
                            config['success_rate'][source] = success_data['success'] / success_data['total']
                        else:
                            config['success_rate'][source] = 0.5  # Valeur neutre
            
            print(f"   ✅ {len(self.learning_history['sources_tried'])} entrées historiques chargées")
        else:
            print("\n🆕 Première exécution - Pas d'historique d'apprentissage")
    
    def intelligent_source_selection(self, data_type, brand_name, brand_info):
        """
        INTELLIGENCE : Sélectionne la meilleure source basée sur l'apprentissage
        """
        if data_type not in self.scrapers_config:
            return self.scrapers_config[data_type]['priority']
        
        config = self.scrapers_config[data_type]
        
        # Si pas de données d'apprentissage, utiliser l'ordre par défaut
        if not config['success_rate']:
            return config['priority']
        
        # Sinon, trier par taux de succès
        sources_with_scores = []
        for source in config['sources']:
            success_rate = config['success_rate'].get(source, 0.5)
            avg_time = config['avg_time'].get(source, 5.0)
            
            # Score = succès pondéré par vitesse
            # On privilégie les sources rapides ET fiables
            score = success_rate * (1 / (avg_time + 0.1))
            
            sources_with_scores.append((source, score, success_rate))
        
        # Trier par score décroissant
        sources_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        optimized_order = [s[0] for s in sources_with_scores]
        
        return optimized_order
    
    def scrape_recycled_materials(self, brand_name, website):
        """
        Scraping intelligent des matières recyclées
        """
        from recycled_materials_scraper import analyze_brand_for_recycled_materials
        
        print(f"\n♻️  Matières recyclées pour {brand_name}")
        print("-" * 70)
        
        sources_order = self.intelligent_source_selection('recycled_materials', brand_name, {'website': website})
        
        for source in sources_order:
            start_time = time.time()
            
            try:
                if source == 'database' or source == 'reports':
                    # Utiliser le scraper existant (qui a une base de données)
                    result = analyze_brand_for_recycled_materials(brand_name, website)
                    
                    if result['percentage']:
                        elapsed = time.time() - start_time
                        self._record_success('recycled_materials', source, True, elapsed)
                        print(f"   ✅ {source}: {result['percentage']}% (confiance: {result['confidence']})")
                        return result
                    else:
                        self._record_success('recycled_materials', source, False, time.time() - start_time)
                        
            except Exception as e:
                print(f"   ⚠️ Erreur {source}: {e}")
                self._record_success('recycled_materials', source, False, time.time() - start_time)
        
        print(f"   ❌ Aucune donnée trouvée")
        return {'percentage': None, 'source': None, 'confidence': 'low'}
    
    def scrape_certifications(self, brand_name, website):
        """
        Scraping intelligent des certifications
        """
        from certifications_scraper import find_certifications_for_brand
        
        print(f"\n🏆 Certifications pour {brand_name}")
        print("-" * 70)
        
        sources_order = self.intelligent_source_selection('certifications', brand_name, {'website': website})
        
        start_time = time.time()
        result = find_certifications_for_brand(brand_name, website)
        elapsed = time.time() - start_time
        
        if result['certifications']:
            self._record_success('certifications', 'mixed', True, elapsed)
            print(f"   ✅ Trouvé: {len(result['certifications'])} certification(s)")
            return result
        else:
            self._record_success('certifications', 'mixed', False, elapsed)
            print(f"   ❌ Aucune certification trouvée")
            return result
    
    def scrape_unsold_management(self, brand_name, website):
        """
        Scraping intelligent de la gestion des invendus
        """
        from unsold_management_scraper import analyze_unsold_management
        
        print(f"\n♻️  Gestion invendus pour {brand_name}")
        print("-" * 70)
        
        sources_order = self.intelligent_source_selection('unsold_management', brand_name, {'website': website})
        
        start_time = time.time()
        result = analyze_unsold_management(brand_name, website)
        elapsed = time.time() - start_time
        
        if result['policy'] or result['practices']:
            self._record_success('unsold_management', 'mixed', True, elapsed)
            print(f"   ✅ Politique: {result['policy'][:60] if result['policy'] else 'N/A'}")
            return result
        else:
            self._record_success('unsold_management', 'mixed', False, elapsed)
            print(f"   ❌ Aucune information trouvée")
            return result
    
    def _record_success(self, data_type, source, success, time_taken):
        """
        Enregistre le résultat pour l'apprentissage futur
        """
        key = f"{data_type}_{source}"
        
        # Enregistrer dans l'historique
        self.learning_history['sources_tried'].append({
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'source': source,
            'success': success,
            'time': time_taken
        })
        
        # Mettre à jour les statistiques
        if key not in self.learning_history['sources_success']:
            self.learning_history['sources_success'][key] = {'success': 0, 'total': 0}
        
        self.learning_history['sources_success'][key]['total'] += 1
        if success:
            self.learning_history['sources_success'][key]['success'] += 1
        
        # Mettre à jour les temps moyens
        if key not in self.learning_history['scraping_times']:
            self.learning_history['scraping_times'][key] = []
        
        self.learning_history['scraping_times'][key].append(time_taken)
        
        # Mettre à jour la config
        if data_type in self.scrapers_config:
            config = self.scrapers_config[data_type]
            stats = self.learning_history['sources_success'][key]
            config['success_rate'][source] = stats['success'] / stats['total']
            config['avg_time'][source] = np.mean(self.learning_history['scraping_times'][key])
    
    def process_brand_complete(self, brand_data):
        """
        Traitement COMPLET d'une marque : tous les scrappings orchestrés par l'IA
        """
        brand_name = brand_data['brand']
        website = brand_data.get('website', '')
        
        print("\n" + "="*70)
        print(f"🤖 TRAITEMENT COMPLET IA : {brand_name}")
        print("="*70)
        
        results = {
            'brand': brand_name,
            'recycled_materials': None,
            'certifications': None,
            'unsold_management': None,
            'ml_score': None
        }
        
        # 1. Matières recyclées
        if not brand_data.get('sustainable_materials'):
            recycled_result = self.scrape_recycled_materials(brand_name, website)
            results['recycled_materials'] = recycled_result['percentage']
            brand_data['sustainable_materials'] = recycled_result['percentage'] or ''
            time.sleep(1)
        else:
            print(f"\n♻️  Matières recyclées: ✓ Déjà rempli ({brand_data['sustainable_materials']}%)")
        
        # 2. Certifications
        if not brand_data.get('certifications'):
            cert_result = self.scrape_certifications(brand_name, website)
            results['certifications'] = cert_result['certifications']
            brand_data['certifications'] = ', '.join(cert_result['certifications']) if cert_result['certifications'] else ''
            time.sleep(1)
        else:
            print(f"\n🏆 Certifications: ✓ Déjà rempli ({brand_data['certifications']})")
        
        # 3. Gestion des invendus
        if not brand_data.get('unsold_management'):
            unsold_result = self.scrape_unsold_management(brand_name, website)
            results['unsold_management'] = unsold_result['policy']
            brand_data['unsold_management'] = unsold_result['policy'] or ''
            time.sleep(1)
        else:
            print(f"\n♻️  Gestion invendus: ✓ Déjà rempli")
        
        return results
    
    def train_ml_scorer(self, csv_file):
        """
        Entraîne le modèle ML pour scorer la durabilité
        """
        from ml_sustainability_scorer import SustainabilityMLScorer
        
        print("\n" + "="*70)
        print("🎓 ENTRAÎNEMENT DU MODÈLE ML DE SCORING")
        print("="*70)
        
        scorer = SustainabilityMLScorer()
        metrics = scorer.train(csv_file)
        
        self.scorer_model = scorer
        self.trained = True
        
        return scorer, metrics
    
    def process_all_brands(self, csv_file, output_file, max_brands=None):
        """
        Traite TOUTES les marques avec l'IA orchestratrice
        """
        print("\n" + "="*70)
        print("🚀 INTELLIGENCE ARTIFICIELLE MASTER - TRAITEMENT COMPLET")
        print("="*70)
        
        # Charger l'historique d'apprentissage
        self.learn_from_scraping_history()
        
        # Lire le CSV
        df = pd.read_csv(csv_file)
        
        if max_brands:
            df = df.head(max_brands)
            print(f"\n⚠️  Mode test: Traitement de {max_brands} marques seulement")
        
        print(f"\n📊 Total: {len(df)} marques à traiter")
        
        # Statistiques
        stats = {
            'total': len(df),
            'recycled_found': 0,
            'certs_found': 0,
            'unsold_found': 0,
            'already_complete': 0,
            'start_time': time.time()
        }
        
        # Traiter chaque marque
        updated_brands = []
        
        for i, (idx, brand) in enumerate(df.iterrows(), 1):
            print(f"\n{'='*70}")
            print(f"[{i}/{len(df)}] 🏷️  {brand['brand']}")
            print('='*70)
            
            # Vérifier si déjà complet
            is_complete = all([
                brand.get('sustainable_materials'),
                brand.get('certifications'),
                brand.get('unsold_management')
            ])
            
            if is_complete:
                print("✅ Marque complète (toutes les données présentes)")
                stats['already_complete'] += 1
                updated_brands.append(brand.to_dict())
                continue
            
            # Traiter la marque
            results = self.process_brand_complete(brand.to_dict())
            
            # Mettre à jour les stats
            if results['recycled_materials']:
                stats['recycled_found'] += 1
            if results['certifications']:
                stats['certs_found'] += 1
            if results['unsold_management']:
                stats['unsold_found'] += 1
            
            # Mettre à jour le DataFrame
            if results['recycled_materials']:
                brand['sustainable_materials'] = results['recycled_materials']
            if results['certifications']:
                brand['certifications'] = ', '.join(results['certifications'])
            if results['unsold_management']:
                brand['unsold_management'] = results['unsold_management']
            
            updated_brands.append(brand.to_dict())
            
            # Pause entre les marques
            time.sleep(2)
        
        # Créer DataFrame mis à jour
        df_updated = pd.DataFrame(updated_brands)
        
        # Entraîner le modèle ML et prédire les scores
        print("\n" + "="*70)
        print("🎓 PHASE 2: ENTRAÎNEMENT ML ET PRÉDICTION DES SCORES")
        print("="*70)
        
        scorer, metrics = self.train_ml_scorer(output_file if os.path.exists(output_file) else csv_file)
        
        # Prédire les scores
        predictions = scorer.predict(df_updated)
        df_updated['ml_predicted_score'] = predictions.round(1)
        
        # Si pas de final_score, utiliser la prédiction
        df_updated['final_score'] = df_updated.apply(
            lambda row: row['final_score'] if pd.notna(row['final_score']) and str(row['final_score']).strip() 
            else row['ml_predicted_score'],
            axis=1
        )
        
        # Sauvegarder
        df_updated.to_csv(output_file, index=False, encoding='utf-8')
        
        # Sauvegarder l'historique d'apprentissage
        with open('scraping_history.pkl', 'wb') as f:
            pickle.dump(self.learning_history, f)
        
        # Sauvegarder le modèle ML
        scorer.save_model('sustainability_ml_model.pkl')
        
        # Afficher les statistiques finales
        elapsed = time.time() - stats['start_time']
        
        print("\n" + "="*70)
        print("📊 STATISTIQUES FINALES")
        print("="*70)
        print(f"\n⏱️  Temps total: {elapsed/60:.1f} minutes ({elapsed:.0f} secondes)")
        print(f"\n📈 Données collectées:")
        print(f"   • Matières recyclées: {stats['recycled_found']}/{stats['total']-stats['already_complete']}")
        print(f"   • Certifications: {stats['certs_found']}/{stats['total']-stats['already_complete']}")
        print(f"   • Gestion invendus: {stats['unsold_found']}/{stats['total']-stats['already_complete']}")
        print(f"   • Marques déjà complètes: {stats['already_complete']}")
        
        print(f"\n🤖 Apprentissage de l'IA:")
        print(f"   • Tentatives de scraping: {len(self.learning_history['sources_tried'])}")
        print(f"   • Sources évaluées: {len(self.learning_history['sources_success'])}")
        
        print(f"\n📊 Scores ML:")
        print(f"   • R² score: {metrics['r2_score']:.3f}")
        print(f"   • MAE: {metrics['mae']:.3f}")
        print(f"   • Validation croisée: {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
        
        print(f"\n📁 Fichiers créés:")
        print(f"   • {output_file} (CSV avec toutes les données)")
        print(f"   • sustainability_ml_model.pkl (Modèle ML entraîné)")
        print(f"   • scraping_history.pkl (Historique d'apprentissage)")
        
        # Top 10 marques
        top_10 = df_updated.nlargest(10, 'final_score')[['brand', 'final_score', 'category']]
        print(f"\n🏆 TOP 10 MARQUES LES PLUS DURABLES:")
        print("-" * 70)
        for i, (idx, row) in enumerate(top_10.iterrows(), 1):
            print(f"   {i:2d}. {row['brand']:30s} {row['final_score']:.1f}/10  ({row['category']})")
        
        print("\n" + "="*70)
        print("✅ TRAITEMENT COMPLET TERMINÉ!")
        print("="*70)
        
        return df_updated


if __name__ == "__main__":
    # Créer l'IA maîtresse
    ai = AIBrandIntelligence()
    
    input_file = "brands_database_with_production_countries.csv"
    output_file = "brands_database_complete_with_ai.csv"
    
    # Mode test (5 marques) ou complet ?
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("\n🧪 MODE TEST: Traitement de 5 marques seulement\n")
        df_complete = ai.process_all_brands(input_file, output_file, max_brands=5)
    else:
        print("\n🚀 MODE COMPLET: Traitement de toutes les marques\n")
        print("⚠️  Cela peut prendre plusieurs heures!")
        print("💡 Pour tester d'abord, lancez: python3 ai_master_orchestrator.py --test\n")
        
        response = input("Continuer? (y/n): ")
        if response.lower() == 'y':
            df_complete = ai.process_all_brands(input_file, output_file)
        else:
            print("\n❌ Annulé")

