"""
Moteur de recommandation personnalisé
Suggère des marques en fonction des préférences apprises de l'utilisateur
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from user_preference_model import UserPreferences
from dataclasses import dataclass


@dataclass
class BrandRecommendation:
    """Représente une recommandation de marque avec son score"""
    brand_name: str
    category: str
    score: float
    match_reasons: List[str]  # Pourquoi cette marque est recommandée
    features: Dict[str, float]
    price_range: Optional[int] = None
    website: Optional[str] = None


class RecommendationEngine:
    """
    Moteur de recommandation qui personnalise les suggestions
    selon les préférences apprises de chaque utilisateur
    """
    
    def __init__(self, brands_df: pd.DataFrame):
        """
        Args:
            brands_df: DataFrame contenant les données des marques
        """
        self.brands_df = brands_df
        self._preprocess_brands()
    
    def _preprocess_brands(self):
        """Prétraite les données des marques pour la recommandation"""
        # Normalise les scores (0-100) vers (0-1)
        score_columns = [
            'sustainable_materials', 'country_production', 'country_origin',
            'unsold_management', 'supply_chain_transparency', 'global_env_impact',
            'labor_ethics', 'recycled_materials_note'
        ]
        
        for col in score_columns:
            if col in self.brands_df.columns:
                # Remplit les valeurs manquantes avec 0
                self.brands_df[col] = pd.to_numeric(self.brands_df[col], errors='coerce').fillna(0)
                # Normalise entre 0 et 1
                max_val = self.brands_df[col].max()
                if max_val > 0:
                    self.brands_df[col] = self.brands_df[col] / max_val
        
        # Normalise price_range (supposé entre 1-5)
        if 'price_range' in self.brands_df.columns:
            self.brands_df['price_range'] = pd.to_numeric(
                self.brands_df['price_range'], 
                errors='coerce'
            ).fillna(3)
            self.brands_df['price_range_norm'] = self.brands_df['price_range'] / 5
    
    def get_brand_features(self, brand_row: pd.Series) -> Dict[str, float]:
        """Extrait les features d'une marque pour le calcul de score"""
        features = {
            'sustainable_materials': brand_row.get('sustainable_materials', 0),
            'recycled_materials': brand_row.get('recycled_materials_note', 0),
            'country_production': self._score_country_production(brand_row.get('country_production', '')),
            'country_origin': self._score_country_origin(brand_row.get('country_origin', '')),
            'supply_chain_transparency': brand_row.get('supply_chain_transparency', 0),
            'global_env_impact': brand_row.get('global_env_impact', 0),
            'labor_ethics': brand_row.get('labor_ethics', 0),
            'certifications': self._score_certifications(brand_row.get('certifications', '')),
            'unsold_management': brand_row.get('unsold_management', 0),
            'price_range': brand_row.get('price_range_norm', 0.5),
        }
        return features
    
    def _score_country_production(self, country_str: str) -> float:
        """Score basé sur les pays de production (pays européens = meilleur score)"""
        if pd.isna(country_str) or country_str == '':
            return 0.5
        
        european_countries = [
            'France', 'Italy', 'Spain', 'Portugal', 'Germany', 'UK', 
            'Belgium', 'Netherlands', 'Switzerland', 'Austria'
        ]
        
        countries = str(country_str).split(',')
        european_count = sum(1 for c in countries if any(eu in c for eu in european_countries))
        
        if len(countries) == 0:
            return 0.5
        
        return min(1.0, european_count / len(countries) + 0.2)
    
    def _score_country_origin(self, country_str: str) -> float:
        """Score basé sur le pays d'origine"""
        if pd.isna(country_str) or country_str == '':
            return 0.5
        
        # Bonus pour les marques européennes
        european_countries = [
            'France', 'Italy', 'Spain', 'Portugal', 'Germany', 'UK',
            'Belgium', 'Netherlands', 'Switzerland', 'Austria'
        ]
        
        if any(eu in str(country_str) for eu in european_countries):
            return 0.8
        
        return 0.5
    
    def _score_certifications(self, cert_str: str) -> float:
        """Score basé sur les certifications"""
        if pd.isna(cert_str) or cert_str == '':
            return 0.3
        
        certifications = str(cert_str).split(',')
        # Plus de certifications = meilleur score
        return min(1.0, len(certifications) * 0.25 + 0.3)
    
    def calculate_personalized_score(
        self,
        brand_features: Dict[str, float],
        user_preferences: UserPreferences
    ) -> Tuple[float, List[str]]:
        """
        Calcule un score personnalisé pour une marque
        
        Returns:
            (score, reasons) - Score entre 0-1 et liste des raisons du match
        """
        score = 0.0
        reasons = []
        
        # Pour chaque critère, multiplie la valeur de la marque par le poids de l'utilisateur
        for criterion, brand_value in brand_features.items():
            user_weight = user_preferences.get_weight(criterion)
            contribution = brand_value * user_weight
            score += contribution
            
            # Si ce critère contribue significativement au score
            if contribution > 0.6 and brand_value > 0.7:
                criterion_name = criterion.replace('_', ' ').title()
                reasons.append(f"Excellent {criterion_name}")
        
        # Normalise le score
        score = score / len(brand_features)
        
        return score, reasons
    
    def recommend_brands(
        self,
        user_preferences: UserPreferences,
        n_recommendations: int = 10,
        category: Optional[str] = None,
        min_score: float = 0.5
    ) -> List[BrandRecommendation]:
        """
        Génère des recommandations personnalisées
        
        Args:
            user_preferences: Préférences de l'utilisateur
            n_recommendations: Nombre de recommandations à retourner
            category: Filtrer par catégorie (optionnel)
            min_score: Score minimum pour être recommandé
            
        Returns:
            Liste de recommandations triées par score
        """
        recommendations = []
        
        # Filtre par catégorie si spécifié
        df = self.brands_df
        if category:
            df = df[df['category'] == category]
        
        # Calcule le score pour chaque marque
        for idx, brand_row in df.iterrows():
            brand_features = self.get_brand_features(brand_row)
            score, reasons = self.calculate_personalized_score(
                brand_features, 
                user_preferences
            )
            
            if score >= min_score:
                recommendation = BrandRecommendation(
                    brand_name=brand_row.get('brand', 'Unknown'),
                    category=brand_row.get('category', 'Unknown'),
                    score=score,
                    match_reasons=reasons,
                    features=brand_features,
                    price_range=brand_row.get('price_range'),
                    website=brand_row.get('website')
                )
                recommendations.append(recommendation)
        
        # Trie par score décroissant
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return recommendations[:n_recommendations]
    
    def recommend_similar_brands(
        self,
        brand_name: str,
        user_preferences: UserPreferences,
        n_recommendations: int = 5
    ) -> List[BrandRecommendation]:
        """
        Recommande des marques similaires à une marque donnée,
        en tenant compte des préférences utilisateur
        """
        # Trouve la marque de référence
        brand_row = self.brands_df[self.brands_df['brand'] == brand_name]
        
        if brand_row.empty:
            return []
        
        brand_row = brand_row.iloc[0]
        reference_features = self.get_brand_features(brand_row)
        reference_category = brand_row.get('category')
        
        recommendations = []
        
        # Cherche dans la même catégorie
        same_category = self.brands_df[
            (self.brands_df['category'] == reference_category) &
            (self.brands_df['brand'] != brand_name)
        ]
        
        for idx, other_brand in same_category.iterrows():
            other_features = self.get_brand_features(other_brand)
            
            # Calcule la similarité entre les marques
            similarity = self._calculate_similarity(reference_features, other_features)
            
            # Ajuste avec les préférences utilisateur
            personalized_score, reasons = self.calculate_personalized_score(
                other_features,
                user_preferences
            )
            
            # Score combiné: similarité + préférences
            combined_score = (similarity * 0.6) + (personalized_score * 0.4)
            
            recommendation = BrandRecommendation(
                brand_name=other_brand.get('brand', 'Unknown'),
                category=other_brand.get('category', 'Unknown'),
                score=combined_score,
                match_reasons=reasons + [f"Similaire à {brand_name}"],
                features=other_features,
                price_range=other_brand.get('price_range'),
                website=other_brand.get('website')
            )
            recommendations.append(recommendation)
        
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:n_recommendations]
    
    def _calculate_similarity(
        self,
        features1: Dict[str, float],
        features2: Dict[str, float]
    ) -> float:
        """Calcule la similarité cosinus entre deux ensembles de features"""
        common_keys = set(features1.keys()) & set(features2.keys())
        
        if not common_keys:
            return 0.0
        
        vec1 = np.array([features1[k] for k in common_keys])
        vec2 = np.array([features2[k] for k in common_keys])
        
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return np.dot(vec1, vec2) / (norm1 * norm2)
    
    def explain_recommendation(
        self,
        brand_name: str,
        user_preferences: UserPreferences
    ) -> Dict[str, any]:
        """
        Explique pourquoi une marque est recommandée (ou non) à un utilisateur
        """
        brand_row = self.brands_df[self.brands_df['brand'] == brand_name]
        
        if brand_row.empty:
            return {'error': 'Marque non trouvée'}
        
        brand_row = brand_row.iloc[0]
        brand_features = self.get_brand_features(brand_row)
        score, reasons = self.calculate_personalized_score(brand_features, user_preferences)
        
        # Analyse détaillée par critère
        criteria_analysis = []
        top_user_criteria = user_preferences.get_top_criteria(5)
        
        for criterion, user_weight in top_user_criteria:
            brand_value = brand_features.get(criterion, 0)
            match_score = brand_value * user_weight
            
            criteria_analysis.append({
                'criterion': criterion.replace('_', ' ').title(),
                'user_importance': user_weight,
                'brand_value': brand_value,
                'match_score': match_score,
                'evaluation': self._evaluate_match(match_score)
            })
        
        return {
            'brand_name': brand_name,
            'overall_score': score,
            'recommendation': 'Fortement recommandé' if score > 0.7 else 'Recommandé' if score > 0.5 else 'Moyennement compatible',
            'match_reasons': reasons,
            'detailed_analysis': criteria_analysis,
            'user_profile': user_preferences.get_top_criteria(3)
        }
    
    def _evaluate_match(self, match_score: float) -> str:
        """Évalue la qualité d'un match pour un critère"""
        if match_score > 0.7:
            return 'Excellent match'
        elif match_score > 0.5:
            return 'Bon match'
        elif match_score > 0.3:
            return 'Match moyen'
        else:
            return 'Faible match'

