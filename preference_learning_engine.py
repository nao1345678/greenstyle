"""
Moteur d'apprentissage des préférences utilisateur
Analyse les interactions pour déduire les critères importants
"""

import numpy as np
from typing import Dict, List, Tuple
from user_preference_model import UserPreferences, UserInteraction
from datetime import datetime


class PreferenceLearningEngine:
    """
    Moteur d'apprentissage qui analyse les interactions utilisateur
    pour identifier les critères qui influencent leurs choix
    """
    
    def __init__(self, learning_rate: float = 0.1):
        """
        Args:
            learning_rate: Vitesse d'apprentissage (0-1), contrôle la rapidité d'adaptation
        """
        self.learning_rate = learning_rate
        self.positive_interaction_types = {'like', 'save', 'purchase', 'click'}
        self.negative_interaction_types = {'dislike', 'skip'}
        
    def learn_from_interaction(
        self, 
        preferences: UserPreferences, 
        interaction: UserInteraction
    ) -> UserPreferences:
        """
        Met à jour les préférences basé sur une nouvelle interaction
        
        Args:
            preferences: Préférences actuelles de l'utilisateur
            interaction: Nouvelle interaction à analyser
            
        Returns:
            Préférences mises à jour
        """
        # Ajoute l'interaction à l'historique
        preferences.add_interaction(interaction)
        
        # Détermine si l'interaction est positive ou négative
        is_positive = interaction.interaction_type in self.positive_interaction_types
        is_negative = interaction.interaction_type in self.negative_interaction_types
        
        if not (is_positive or is_negative):
            return preferences  # Interaction neutre, pas d'apprentissage
        
        # Force du signal basée sur le type d'interaction
        signal_strength = self._get_signal_strength(interaction.interaction_type)
        
        # Met à jour les poids pour chaque critère présent dans la marque
        for criterion, value in interaction.brand_features.items():
            if criterion in preferences.weights:
                current_weight = preferences.weights[criterion]
                
                # Si la valeur du critère est élevée et l'interaction positive,
                # augmente le poids de ce critère
                if is_positive and value > 0.5:
                    adjustment = self.learning_rate * signal_strength * (value - 0.5)
                    new_weight = current_weight + adjustment
                
                # Si la valeur est faible et l'interaction négative,
                # diminue le poids de ce critère
                elif is_negative and value < 0.5:
                    adjustment = self.learning_rate * signal_strength * (0.5 - value)
                    new_weight = current_weight - adjustment
                
                # Si l'interaction est négative et la valeur élevée,
                # ça indique que ce critère n'est pas important pour l'utilisateur
                elif is_negative and value > 0.5:
                    adjustment = self.learning_rate * signal_strength * 0.5
                    new_weight = current_weight - adjustment
                
                else:
                    new_weight = current_weight
                
                preferences.update_weight(criterion, new_weight)
        
        return preferences
    
    def learn_from_comparison(
        self,
        preferences: UserPreferences,
        chosen_brand_features: Dict[str, float],
        rejected_brand_features: Dict[str, float]
    ) -> UserPreferences:
        """
        Apprend en comparant une marque choisie vs une marque rejetée
        C'est la méthode la plus informative pour l'apprentissage
        
        Args:
            preferences: Préférences actuelles
            chosen_brand_features: Caractéristiques de la marque choisie
            rejected_brand_features: Caractéristiques de la marque rejetée
        """
        # Pour chaque critère, si la marque choisie a une meilleure valeur,
        # augmente le poids de ce critère
        all_criteria = set(chosen_brand_features.keys()) | set(rejected_brand_features.keys())
        
        for criterion in all_criteria:
            if criterion not in preferences.weights:
                continue
                
            chosen_value = chosen_brand_features.get(criterion, 0.5)
            rejected_value = rejected_brand_features.get(criterion, 0.5)
            
            # Différence entre les deux marques pour ce critère
            difference = chosen_value - rejected_value
            
            if abs(difference) > 0.1:  # Seuil de significativité
                current_weight = preferences.weights[criterion]
                # Si la marque choisie est meilleure sur ce critère, augmente son importance
                adjustment = self.learning_rate * difference
                new_weight = current_weight + adjustment
                preferences.update_weight(criterion, new_weight)
        
        return preferences
    
    def learn_from_batch(
        self,
        preferences: UserPreferences,
        interactions: List[UserInteraction]
    ) -> UserPreferences:
        """
        Apprend d'un lot d'interactions (plus efficace)
        """
        for interaction in interactions:
            preferences = self.learn_from_interaction(preferences, interaction)
        
        # Normalisation des poids après traitement du lot
        preferences = self._normalize_weights(preferences)
        
        return preferences
    
    def _get_signal_strength(self, interaction_type: str) -> float:
        """
        Retourne la force du signal d'apprentissage selon le type d'interaction
        Purchase > Save > Like > Click > View
        """
        strength_map = {
            'purchase': 1.0,
            'save': 0.8,
            'like': 0.6,
            'click': 0.4,
            'view': 0.2,
            'dislike': 0.7,
            'skip': 0.3
        }
        return strength_map.get(interaction_type, 0.3)
    
    def _normalize_weights(self, preferences: UserPreferences) -> UserPreferences:
        """
        Normalise les poids pour éviter qu'ils ne dérivent trop
        Garde la somme des poids proche de len(weights) * 0.5
        """
        weights_array = np.array(list(preferences.weights.values()))
        
        # Si les poids dérivent trop de 0.5, on les ramène doucement
        mean_weight = np.mean(weights_array)
        if abs(mean_weight - 0.5) > 0.2:
            adjustment = (0.5 - mean_weight) * 0.1
            for criterion in preferences.weights:
                preferences.weights[criterion] += adjustment
                preferences.weights[criterion] = np.clip(preferences.weights[criterion], 0.0, 1.0)
        
        return preferences
    
    def get_preference_insights(self, preferences: UserPreferences) -> Dict[str, any]:
        """
        Génère des insights sur les préférences de l'utilisateur
        """
        top_criteria = preferences.get_top_criteria(3)
        
        # Identifie les critères les moins importants
        bottom_criteria = sorted(preferences.weights.items(), key=lambda x: x[1])[:3]
        
        # Catégorise l'utilisateur
        profile_type = self._categorize_user_profile(preferences)
        
        return {
            'top_criteria': [{'criterion': c, 'weight': w} for c, w in top_criteria],
            'bottom_criteria': [{'criterion': c, 'weight': w} for c, w in bottom_criteria],
            'profile_type': profile_type,
            'learning_confidence': preferences.learning_confidence,
            'total_interactions': preferences.total_interactions,
            'is_eco_conscious': preferences.weights.get('sustainable_materials', 0.5) > 0.7,
            'is_price_sensitive': preferences.weights.get('price_range', 0.5) > 0.7,
            'values_transparency': preferences.weights.get('supply_chain_transparency', 0.5) > 0.7,
            'values_ethics': preferences.weights.get('labor_ethics', 0.5) > 0.7
        }
    
    def _categorize_user_profile(self, preferences: UserPreferences) -> str:
        """
        Catégorise l'utilisateur en profil type
        """
        weights = preferences.weights
        
        # Profil éco-responsable
        eco_score = (
            weights.get('sustainable_materials', 0.5) +
            weights.get('recycled_materials', 0.5) +
            weights.get('global_env_impact', 0.5)
        ) / 3
        
        # Profil éthique
        ethics_score = (
            weights.get('labor_ethics', 0.5) +
            weights.get('supply_chain_transparency', 0.5)
        ) / 2
        
        # Profil local/origine
        origin_score = (
            weights.get('country_production', 0.5) +
            weights.get('country_origin', 0.5)
        ) / 2
        
        # Profil prix
        price_score = weights.get('price_range', 0.5)
        
        # Détermine le profil dominant
        scores = {
            'Eco-conscient': eco_score,
            'Ethique': ethics_score,
            'Local': origin_score,
            'Prix': price_score
        }
        
        if max(scores.values()) < 0.6:
            return 'Equilibré'
        
        return max(scores.items(), key=lambda x: x[1])[0]

