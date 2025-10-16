#!/usr/bin/env python3
"""
Machine Learning Sustainability Scorer
Véritable IA qui APPREND à prédire le score de durabilité des marques de mode
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class SustainabilityMLScorer:
    """
    Modèle de Machine Learning pour prédire le score de durabilité
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.trained = False
        
    def extract_features(self, df):
        """
        Extrait les features (caractéristiques) du DataFrame
        C'est ici qu'on transforme les données brutes en features numériques
        """
        features = pd.DataFrame()
        
        # Feature 1: Pourcentage de matériaux recyclés (numérique)
        features['recycled_percentage'] = pd.to_numeric(
            df['sustainable_materials'].fillna(0), 
            errors='coerce'
        ).fillna(0)
        
        # Feature 2: Nombre de certifications
        features['num_certifications'] = df['certifications'].apply(
            lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() else 0
        )
        
        # Feature 3: A des certifications premium (B Corp, Fair Trade, etc.)
        premium_certs = ['B Corp', 'Fair Trade', 'GOTS', 'Cradle to Cradle']
        features['has_premium_cert'] = df['certifications'].apply(
            lambda x: 1 if any(cert in str(x) for cert in premium_certs) else 0
        )
        
        # Feature 4: Nombre de pays de production (moins = mieux généralement)
        features['num_production_countries'] = df['country_production'].apply(
            lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() else 0
        )
        
        # Feature 5: Production locale (pays origine = pays production)
        features['local_production'] = (
            df['country_origin'].fillna('') == df['country_production'].fillna('')
        ).astype(int)
        
        # Feature 6: A une politique de gestion des invendus
        features['has_unsold_policy'] = df['unsold_management'].apply(
            lambda x: 1 if pd.notna(x) and str(x).strip() and str(x) != 'Not disclosed' else 0
        )
        
        # Feature 7: Politique positive invendus (donation, recycling, no destruction)
        positive_keywords = ['donate', 'recycl', 'no destruction', 'repair', 'resale', 'circular']
        features['positive_unsold_policy'] = df['unsold_management'].apply(
            lambda x: sum(1 for keyword in positive_keywords if keyword in str(x).lower())
        )
        
        # Feature 8: Transparence supply chain (oui/non)
        features['supply_chain_transparency'] = df['supply_chain_transparency'].apply(
            lambda x: 1 if pd.notna(x) and str(x).strip() and str(x).lower() not in ['no', 'unknown'] else 0
        )
        
        # Feature 9: Prix (encoder en catégories)
        price_mapping = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
        features['price_category'] = df['price_range'].map(price_mapping).fillna(3)
        
        # Feature 10: Catégorie de marque (encoder)
        if 'category' in df.columns:
            if 'category' not in self.label_encoders:
                self.label_encoders['category'] = LabelEncoder()
                features['category_encoded'] = self.label_encoders['category'].fit_transform(
                    df['category'].fillna('unknown')
                )
            else:
                # Pour les nouvelles données, utiliser l'encoder existant
                try:
                    features['category_encoded'] = self.label_encoders['category'].transform(
                        df['category'].fillna('unknown')
                    )
                except ValueError:
                    # Si nouvelle catégorie inconnue, mettre 0
                    features['category_encoded'] = 0
        
        # Feature 11: Badges planète et travail
        features['has_planet_badge'] = df['planet_badge'].apply(
            lambda x: 1 if pd.notna(x) and str(x).strip() and str(x) != "['']" else 0
        )
        
        features['has_labor_badge'] = df['labor_badge'].apply(
            lambda x: 1 if pd.notna(x) and str(x).strip() and str(x) != "['']" else 0
        )
        
        # Feature 12: Score impact environnemental global (si disponible)
        features['global_env_impact'] = pd.to_numeric(
            df['global_env_impact'].fillna(0), 
            errors='coerce'
        ).fillna(0)
        
        # Feature 13: Score éthique travail (si disponible)
        features['labor_ethics'] = pd.to_numeric(
            df['labor_ethics'].fillna(0), 
            errors='coerce'
        ).fillna(0)
        
        self.feature_names = features.columns.tolist()
        
        return features
    
    def prepare_training_data(self, csv_file):
        """
        Prépare les données d'entraînement
        """
        print("\n📊 Chargement des données...")
        df = pd.read_csv(csv_file)
        
        print(f"   Total: {len(df)} marques")
        
        # Filtrer les marques qui ont un score final
        df_with_scores = df[df['final_score'].notna() & (df['final_score'] != '')]
        print(f"   Avec scores: {len(df_with_scores)} marques")
        
        if len(df_with_scores) < 10:
            print("\n⚠️  Pas assez de données avec scores pour l'entraînement!")
            print("   Génération de scores synthétiques basés sur les features...")
            
            # Générer des scores synthétiques pour l'entraînement initial
            df_with_scores = self._generate_synthetic_scores(df)
        
        # Extraire les features
        X = self.extract_features(df_with_scores)
        
        # Target : score final
        y = pd.to_numeric(df_with_scores['final_score'], errors='coerce').fillna(5.0)
        
        print(f"\n✅ Features extraites: {X.shape[1]} features")
        print(f"   {X.shape[0]} exemples d'entraînement")
        
        return X, y, df_with_scores
    
    def _generate_synthetic_scores(self, df):
        """
        Génère des scores synthétiques basés sur les features disponibles
        Pour l'entraînement initial quand pas de scores manuels
        """
        print("\n🎲 Génération de scores synthétiques...")
        
        df = df.copy()
        
        # Calculer un score basé sur des règles
        scores = []
        for idx, row in df.iterrows():
            score = 5.0  # Score de base
            
            # Bonus matériaux recyclés
            recycled = pd.to_numeric(row['sustainable_materials'], errors='coerce')
            if pd.notna(recycled):
                score += min(recycled / 20, 3.0)  # Max +3 points
            
            # Bonus certifications
            certs = str(row['certifications'])
            if pd.notna(certs) and certs.strip():
                num_certs = len(certs.split(','))
                score += min(num_certs * 0.5, 2.0)  # Max +2 points
            
            # Bonus politique invendus
            unsold = str(row['unsold_management']).lower()
            if 'no destruction' in unsold or 'donate' in unsold or 'recycl' in unsold:
                score += 1.0
            
            # Malus fast fashion
            if row['category'] in ['fast_fashion', 'ultra_fast_fashion']:
                score -= 2.0
            
            # Bonus marques durables
            if row['category'] in ['sustainable', 'ethical', 'eco']:
                score += 2.0
            
            # Normaliser entre 0 et 10
            score = max(0, min(10, score))
            
            scores.append(score)
        
        df['final_score'] = scores
        
        print(f"   Scores générés : min={min(scores):.1f}, max={max(scores):.1f}, moyenne={np.mean(scores):.1f}")
        
        return df
    
    def train(self, csv_file, test_size=0.2):
        """
        ENTRAÎNE le modèle de Machine Learning
        C'est ici que l'IA APPREND !
        """
        print("\n" + "="*70)
        print("🤖 ENTRAÎNEMENT DU MODÈLE DE MACHINE LEARNING")
        print("="*70)
        
        # Préparer les données
        X, y, df = self.prepare_training_data(csv_file)
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"\n📚 Split des données:")
        print(f"   Training set: {len(X_train)} exemples")
        print(f"   Test set: {len(X_test)} exemples")
        
        # Normaliser les features
        print("\n⚙️  Normalisation des features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entraîner plusieurs modèles et choisir le meilleur
        print("\n🎓 Entraînement des modèles...")
        
        models = {
            'Random Forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        best_score = -np.inf
        best_model_name = None
        
        for name, model in models.items():
            print(f"\n   Entraînement {name}...")
            model.fit(X_train_scaled, y_train)
            
            # Prédictions
            y_pred_train = model.predict(X_train_scaled)
            y_pred_test = model.predict(X_test_scaled)
            
            # Métriques
            train_r2 = r2_score(y_train, y_pred_train)
            test_r2 = r2_score(y_test, y_pred_test)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
            
            print(f"      R² train: {train_r2:.3f}")
            print(f"      R² test: {test_r2:.3f}")
            print(f"      MAE test: {test_mae:.3f}")
            print(f"      RMSE test: {test_rmse:.3f}")
            
            if test_r2 > best_score:
                best_score = test_r2
                best_model_name = name
                self.model = model
        
        print(f"\n🏆 Meilleur modèle: {best_model_name} (R²={best_score:.3f})")
        
        # Feature importance
        self._display_feature_importance()
        
        # Validation croisée
        print("\n🔄 Validation croisée (5-fold)...")
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='r2', n_jobs=-1
        )
        print(f"   Scores CV: {cv_scores}")
        print(f"   Moyenne CV: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        self.trained = True
        
        print("\n✅ Modèle entraîné avec succès!")
        
        return {
            'model_name': best_model_name,
            'r2_score': best_score,
            'mae': test_mae,
            'rmse': test_rmse,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def _display_feature_importance(self):
        """
        Affiche l'importance des features (ce que le modèle a appris)
        """
        if hasattr(self.model, 'feature_importances_'):
            print("\n📊 Importance des features (ce que le modèle a appris):")
            importances = self.model.feature_importances_
            
            feature_importance = sorted(
                zip(self.feature_names, importances),
                key=lambda x: x[1],
                reverse=True
            )
            
            print("\n   Top 10 features les plus importantes:")
            for i, (feature, importance) in enumerate(feature_importance[:10], 1):
                bar = '█' * int(importance * 50)
                print(f"   {i:2d}. {feature:30s} {bar} {importance:.3f}")
    
    def predict(self, brand_data):
        """
        Prédit le score de durabilité pour une nouvelle marque
        """
        if not self.trained:
            raise ValueError("Le modèle doit être entraîné avant de prédire!")
        
        # Extraire les features
        if isinstance(brand_data, dict):
            brand_df = pd.DataFrame([brand_data])
        else:
            brand_df = brand_data
        
        X = self.extract_features(brand_df)
        X_scaled = self.scaler.transform(X)
        
        # Prédiction
        predictions = self.model.predict(X_scaled)
        
        # Clip entre 0 et 10
        predictions = np.clip(predictions, 0, 10)
        
        return predictions
    
    def predict_all_brands(self, csv_file, output_file):
        """
        Prédit les scores pour toutes les marques du CSV
        """
        print("\n" + "="*70)
        print("🔮 PRÉDICTION DES SCORES POUR TOUTES LES MARQUES")
        print("="*70 + "\n")
        
        df = pd.read_csv(csv_file)
        
        print(f"📊 {len(df)} marques à scorer\n")
        
        # Prédire
        predictions = self.predict(df)
        
        # Ajouter au DataFrame
        df['ml_predicted_score'] = predictions
        df['ml_predicted_score'] = df['ml_predicted_score'].round(1)
        
        # Si pas de final_score, utiliser la prédiction
        df['final_score'] = df.apply(
            lambda row: row['final_score'] if pd.notna(row['final_score']) and str(row['final_score']).strip() 
            else row['ml_predicted_score'],
            axis=1
        )
        
        # Sauvegarder
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✅ Scores prédits et sauvegardés dans: {output_file}\n")
        
        # Statistiques
        print("📊 STATISTIQUES DES SCORES PRÉDITS")
        print("-" * 70)
        print(f"   Min:     {predictions.min():.1f}")
        print(f"   Max:     {predictions.max():.1f}")
        print(f"   Moyenne: {predictions.mean():.1f}")
        print(f"   Médiane: {np.median(predictions):.1f}")
        print(f"   Écart-type: {predictions.std():.1f}")
        
        # Distribution
        print("\n📈 Distribution des scores:")
        bins = [0, 2, 4, 6, 8, 10]
        labels = ['0-2 (Très mauvais)', '2-4 (Mauvais)', '4-6 (Moyen)', '6-8 (Bon)', '8-10 (Excellent)']
        
        for i in range(len(bins)-1):
            count = sum((predictions >= bins[i]) & (predictions < bins[i+1]))
            percentage = count / len(predictions) * 100
            bar = '█' * int(percentage / 2)
            print(f"   {labels[i]:20s} {bar} {count:3d} marques ({percentage:.1f}%)")
        
        # Top 10
        top_10 = df.nlargest(10, 'ml_predicted_score')[['brand', 'ml_predicted_score', 'category']]
        print("\n🏆 TOP 10 MARQUES LES PLUS DURABLES (selon le modèle ML):")
        print("-" * 70)
        for i, row in top_10.iterrows():
            print(f"   {row.name+1:2d}. {row['brand']:30s} {row['ml_predicted_score']:.1f}/10  ({row['category']})")
        
        return df
    
    def save_model(self, filepath='sustainability_ml_model.pkl'):
        """
        Sauvegarde le modèle entraîné
        """
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'trained': self.trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\n💾 Modèle sauvegardé: {filepath}")
    
    def load_model(self, filepath='sustainability_ml_model.pkl'):
        """
        Charge un modèle pré-entraîné
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Modèle non trouvé: {filepath}")
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_names = model_data['feature_names']
        self.trained = model_data['trained']
        
        print(f"\n📂 Modèle chargé: {filepath}")
    
    def explain_prediction(self, brand_data):
        """
        Explique pourquoi le modèle a donné ce score
        """
        if not self.trained:
            raise ValueError("Le modèle doit être entraîné!")
        
        # Prédire
        score = self.predict(brand_data)[0]
        
        # Extraire features
        if isinstance(brand_data, dict):
            brand_df = pd.DataFrame([brand_data])
        else:
            brand_df = brand_data
        
        X = self.extract_features(brand_df)
        
        # Importance des features pour cette prédiction
        print(f"\n🔍 EXPLICATION DE LA PRÉDICTION")
        print("="*70)
        print(f"Score prédit: {score:.1f}/10\n")
        
        if hasattr(self.model, 'feature_importances_'):
            print("Facteurs contributifs:")
            
            importances = self.model.feature_importances_
            feature_values = X.iloc[0]
            
            contributions = []
            for feature, importance, value in zip(self.feature_names, importances, feature_values):
                contribution = importance * value
                contributions.append((feature, importance, value, contribution))
            
            # Trier par contribution
            contributions.sort(key=lambda x: abs(x[3]), reverse=True)
            
            for feature, importance, value, contribution in contributions[:10]:
                symbol = "📈" if contribution > 0 else "📉"
                print(f"   {symbol} {feature:30s} = {value:6.2f} (importance: {importance:.3f})")


if __name__ == "__main__":
    # Créer et entraîner le modèle
    scorer = SustainabilityMLScorer()
    
    input_file = "brands_database_with_production_countries.csv"
    output_file = "brands_database_with_ml_scores.csv"
    model_file = "sustainability_ml_model.pkl"
    
    print("\n🚀 Système de Machine Learning pour scorer la durabilité")
    print("="*70)
    
    # Entraîner
    metrics = scorer.train(input_file)
    
    # Sauvegarder le modèle
    scorer.save_model(model_file)
    
    # Prédire pour toutes les marques
    df_with_scores = scorer.predict_all_brands(input_file, output_file)
    
    print("\n" + "="*70)
    print("✅ TERMINÉ!")
    print("="*70)
    print(f"\n📁 Fichiers créés:")
    print(f"   - {output_file} (CSV avec scores ML)")
    print(f"   - {model_file} (Modèle entraîné)")
    print(f"\n💡 Le modèle peut maintenant prédire le score de n'importe quelle marque!")

