"""
API principale pour interagir avec le système d'IA de recommandation de mode
Gère les utilisateurs, l'apprentissage et les recommandations
"""

import pandas as pd
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from user_preference_model import UserPreferences, UserInteraction
from preference_learning_engine import PreferenceLearningEngine
from recommendation_engine import RecommendationEngine, BrandRecommendation


class FashionAI:
    """
    API principale du système d'IA de recommandation de marques de mode
    """
    
    def __init__(
        self, 
        brands_csv_path: str,
        users_data_dir: str = 'user_data',
        learning_rate: float = 0.1
    ):
        """
        Args:
            brands_csv_path: Chemin vers le CSV des marques
            users_data_dir: Répertoire pour stocker les données utilisateurs
            learning_rate: Vitesse d'apprentissage du système
        """
        # Charge les données des marques
        self.brands_df = pd.read_csv(brands_csv_path)
        
        # Initialise les moteurs
        self.learning_engine = PreferenceLearningEngine(learning_rate=learning_rate)
        self.recommendation_engine = RecommendationEngine(self.brands_df)
        
        # Gestion des utilisateurs
        self.users_data_dir = Path(users_data_dir)
        self.users_data_dir.mkdir(exist_ok=True)
        self.active_users: Dict[str, UserPreferences] = {}
    
    # ====================== Gestion des utilisateurs ======================
    
    def create_user(self, user_id: str) -> UserPreferences:
        """Crée un nouvel utilisateur"""
        if user_id in self.active_users:
            return self.active_users[user_id]
        
        preferences = UserPreferences(user_id=user_id)
        self.active_users[user_id] = preferences
        return preferences
    
    def load_user(self, user_id: str) -> Optional[UserPreferences]:
        """Charge un utilisateur existant"""
        if user_id in self.active_users:
            return self.active_users[user_id]
        
        user_file = self.users_data_dir / f"{user_id}.json"
        if user_file.exists():
            preferences = UserPreferences.load_from_file(str(user_file))
            self.active_users[user_id] = preferences
            return preferences
        
        return None
    
    def save_user(self, user_id: str):
        """Sauvegarde les données d'un utilisateur"""
        if user_id not in self.active_users:
            return
        
        user_file = self.users_data_dir / f"{user_id}.json"
        self.active_users[user_id].save_to_file(str(user_file))
    
    def get_or_create_user(self, user_id: str) -> UserPreferences:
        """Récupère ou crée un utilisateur"""
        user = self.load_user(user_id)
        if user is None:
            user = self.create_user(user_id)
        return user
    
    # ====================== Enregistrement des interactions ======================
    
    def record_interaction(
        self,
        user_id: str,
        brand_name: str,
        interaction_type: str,
        duration_seconds: Optional[float] = None,
        auto_save: bool = True
    ) -> Dict[str, any]:
        """
        Enregistre une interaction utilisateur et met à jour les préférences
        
        Args:
            user_id: Identifiant de l'utilisateur
            brand_name: Nom de la marque
            interaction_type: Type d'interaction ('like', 'dislike', 'click', 'save', 'purchase', etc.)
            duration_seconds: Durée de l'interaction (optionnel)
            auto_save: Sauvegarder automatiquement après l'interaction
            
        Returns:
            Résultat de l'apprentissage et nouvelles préférences
        """
        user_prefs = self.get_or_create_user(user_id)
        
        # Récupère les features de la marque
        brand_data = self.brands_df[self.brands_df['brand'] == brand_name]
        if brand_data.empty:
            return {'error': f'Marque {brand_name} non trouvée'}
        
        brand_features = self.recommendation_engine.get_brand_features(brand_data.iloc[0])
        
        # Crée l'interaction
        interaction = UserInteraction(
            brand_name=brand_name,
            timestamp=datetime.now(),
            interaction_type=interaction_type,
            duration_seconds=duration_seconds,
            brand_features=brand_features
        )
        
        # Apprend de l'interaction
        user_prefs = self.learning_engine.learn_from_interaction(user_prefs, interaction)
        self.active_users[user_id] = user_prefs
        
        if auto_save:
            self.save_user(user_id)
        
        # Retourne les insights mis à jour
        insights = self.learning_engine.get_preference_insights(user_prefs)
        
        return {
            'success': True,
            'user_id': user_id,
            'brand_name': brand_name,
            'interaction_type': interaction_type,
            'learning_confidence': user_prefs.learning_confidence,
            'insights': insights
        }
    
    def record_comparison(
        self,
        user_id: str,
        chosen_brand: str,
        rejected_brand: str,
        auto_save: bool = True
    ) -> Dict[str, any]:
        """
        Enregistre une comparaison entre deux marques (très informatif pour l'apprentissage)
        
        Args:
            user_id: Identifiant de l'utilisateur
            chosen_brand: Marque choisie
            rejected_brand: Marque rejetée
        """
        user_prefs = self.get_or_create_user(user_id)
        
        # Récupère les features des deux marques
        chosen_data = self.brands_df[self.brands_df['brand'] == chosen_brand]
        rejected_data = self.brands_df[self.brands_df['brand'] == rejected_brand]
        
        if chosen_data.empty or rejected_data.empty:
            return {'error': 'Une ou les deux marques non trouvées'}
        
        chosen_features = self.recommendation_engine.get_brand_features(chosen_data.iloc[0])
        rejected_features = self.recommendation_engine.get_brand_features(rejected_data.iloc[0])
        
        # Apprend de la comparaison
        user_prefs = self.learning_engine.learn_from_comparison(
            user_prefs,
            chosen_features,
            rejected_features
        )
        self.active_users[user_id] = user_prefs
        
        if auto_save:
            self.save_user(user_id)
        
        insights = self.learning_engine.get_preference_insights(user_prefs)
        
        return {
            'success': True,
            'user_id': user_id,
            'chosen_brand': chosen_brand,
            'rejected_brand': rejected_brand,
            'insights': insights
        }
    
    # ====================== Recommandations ======================
    
    def get_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10,
        category: Optional[str] = None,
        min_score: float = 0.5
    ) -> List[Dict[str, any]]:
        """
        Obtient des recommandations personnalisées pour un utilisateur
        
        Args:
            user_id: Identifiant de l'utilisateur
            n_recommendations: Nombre de recommandations
            category: Filtrer par catégorie (optionnel)
            min_score: Score minimum
            
        Returns:
            Liste de recommandations avec détails
        """
        user_prefs = self.get_or_create_user(user_id)
        
        recommendations = self.recommendation_engine.recommend_brands(
            user_preferences=user_prefs,
            n_recommendations=n_recommendations,
            category=category,
            min_score=min_score
        )
        
        # Convertit en format dictionnaire
        return [
            {
                'brand_name': rec.brand_name,
                'category': rec.category,
                'score': round(rec.score, 3),
                'match_reasons': rec.match_reasons,
                'price_range': rec.price_range,
                'website': rec.website
            }
            for rec in recommendations
        ]
    
    def get_similar_brands(
        self,
        user_id: str,
        brand_name: str,
        n_recommendations: int = 5
    ) -> List[Dict[str, any]]:
        """
        Recommande des marques similaires à une marque donnée
        """
        user_prefs = self.get_or_create_user(user_id)
        
        recommendations = self.recommendation_engine.recommend_similar_brands(
            brand_name=brand_name,
            user_preferences=user_prefs,
            n_recommendations=n_recommendations
        )
        
        return [
            {
                'brand_name': rec.brand_name,
                'category': rec.category,
                'score': round(rec.score, 3),
                'match_reasons': rec.match_reasons,
                'price_range': rec.price_range,
                'website': rec.website
            }
            for rec in recommendations
        ]
    
    def explain_recommendation(
        self,
        user_id: str,
        brand_name: str
    ) -> Dict[str, any]:
        """
        Explique pourquoi une marque est (ou n'est pas) recommandée
        """
        user_prefs = self.get_or_create_user(user_id)
        
        explanation = self.recommendation_engine.explain_recommendation(
            brand_name=brand_name,
            user_preferences=user_prefs
        )
        
        return explanation
    
    # ====================== Analyse des préférences ======================
    
    def get_user_profile(self, user_id: str) -> Dict[str, any]:
        """
        Obtient le profil complet d'un utilisateur
        """
        user_prefs = self.get_or_create_user(user_id)
        insights = self.learning_engine.get_preference_insights(user_prefs)
        
        return {
            'user_id': user_id,
            'total_interactions': user_prefs.total_interactions,
            'learning_confidence': round(user_prefs.learning_confidence, 3),
            'profile_type': insights['profile_type'],
            'top_criteria': insights['top_criteria'],
            'bottom_criteria': insights['bottom_criteria'],
            'characteristics': {
                'eco_conscious': insights['is_eco_conscious'],
                'price_sensitive': insights['is_price_sensitive'],
                'values_transparency': insights['values_transparency'],
                'values_ethics': insights['values_ethics']
            },
            'all_weights': {k: round(v, 3) for k, v in user_prefs.weights.items()},
            'last_update': user_prefs.last_update.isoformat()
        }
    
    def get_all_categories(self) -> List[str]:
        """Retourne toutes les catégories disponibles"""
        return sorted(self.brands_df['category'].dropna().unique().tolist())
    
    def search_brands(
        self,
        query: str = '',
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, any]]:
        """
        Recherche des marques par nom ou catégorie
        """
        df = self.brands_df
        
        if category:
            df = df[df['category'] == category]
        
        if query:
            df = df[df['brand'].str.contains(query, case=False, na=False)]
        
        df = df.head(limit)
        
        return [
            {
                'brand': row.get('brand'),
                'category': row.get('category'),
                'price_range': row.get('price_range'),
                'website': row.get('website'),
                'final_score': row.get('final_score')
            }
            for _, row in df.iterrows()
        ]
    
    # ====================== Statistiques ======================
    
    def get_system_stats(self) -> Dict[str, any]:
        """Obtient des statistiques sur le système"""
        return {
            'total_brands': len(self.brands_df),
            'categories': self.get_all_categories(),
            'active_users': len(self.active_users),
            'saved_users': len(list(self.users_data_dir.glob('*.json')))
        }

