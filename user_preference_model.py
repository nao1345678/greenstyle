"""
Modèle de préférences utilisateur pour l'apprentissage personnalisé
Apprend les critères importants pour chaque utilisateur
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class UserInteraction:
    """Représente une interaction utilisateur avec une marque"""
    brand_name: str
    timestamp: datetime
    interaction_type: str  # 'view', 'like', 'dislike', 'click', 'save', 'purchase'
    duration_seconds: Optional[float] = None  # Temps passé sur la marque
    brand_features: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'brand_name': self.brand_name,
            'timestamp': self.timestamp.isoformat(),
            'interaction_type': self.interaction_type,
            'duration_seconds': self.duration_seconds,
            'brand_features': self.brand_features
        }


@dataclass
class UserPreferences:
    """
    Stocke et gère les préférences apprises d'un utilisateur
    Chaque critère a un poids qui représente son importance pour l'utilisateur
    """
    user_id: str
    
    # Poids pour chaque critère (0-1, initialement 0.5 = neutre)
    weights: Dict[str, float] = field(default_factory=lambda: {
        'sustainable_materials': 0.5,
        'recycled_materials': 0.5,
        'country_production': 0.5,
        'country_origin': 0.5,
        'supply_chain_transparency': 0.5,
        'global_env_impact': 0.5,
        'labor_ethics': 0.5,
        'certifications': 0.5,
        'unsold_management': 0.5,
        'price_range': 0.5,
    })
    
    # Historique des interactions
    interactions: List[UserInteraction] = field(default_factory=list)
    
    # Statistiques d'apprentissage
    total_interactions: int = 0
    learning_confidence: float = 0.0  # 0-1, augmente avec le nombre d'interactions
    last_update: datetime = field(default_factory=datetime.now)
    
    # Préférences apprises sur les catégories
    preferred_categories: Dict[str, float] = field(default_factory=dict)
    
    # Préférences sur les fourchettes de prix
    preferred_price_ranges: Dict[int, float] = field(default_factory=dict)
    
    def add_interaction(self, interaction: UserInteraction):
        """Ajoute une nouvelle interaction"""
        self.interactions.append(interaction)
        self.total_interactions += 1
        self.last_update = datetime.now()
        
        # La confiance augmente logarithmiquement avec les interactions
        self.learning_confidence = min(1.0, np.log1p(self.total_interactions) / 5)
    
    def get_weight(self, criterion: str) -> float:
        """Récupère le poids d'un critère"""
        return self.weights.get(criterion, 0.5)
    
    def update_weight(self, criterion: str, new_weight: float):
        """Met à jour le poids d'un critère (entre 0 et 1)"""
        self.weights[criterion] = np.clip(new_weight, 0.0, 1.0)
    
    def get_top_criteria(self, n: int = 3) -> List[tuple]:
        """Retourne les n critères les plus importants pour l'utilisateur"""
        sorted_weights = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_weights[:n]
    
    def to_dict(self):
        """Convertit en dictionnaire pour sauvegarde"""
        return {
            'user_id': self.user_id,
            'weights': self.weights,
            'total_interactions': self.total_interactions,
            'learning_confidence': self.learning_confidence,
            'last_update': self.last_update.isoformat(),
            'preferred_categories': self.preferred_categories,
            'preferred_price_ranges': self.preferred_price_ranges,
            'recent_interactions': [i.to_dict() for i in self.interactions[-50:]]  # Garde les 50 dernières
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Charge depuis un dictionnaire"""
        preferences = cls(user_id=data['user_id'])
        preferences.weights = data.get('weights', preferences.weights)
        preferences.total_interactions = data.get('total_interactions', 0)
        preferences.learning_confidence = data.get('learning_confidence', 0.0)
        preferences.preferred_categories = data.get('preferred_categories', {})
        preferences.preferred_price_ranges = data.get('preferred_price_ranges', {})
        
        if 'last_update' in data:
            preferences.last_update = datetime.fromisoformat(data['last_update'])
        
        return preferences
    
    def save_to_file(self, filepath: str):
        """Sauvegarde les préférences dans un fichier JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str):
        """Charge les préférences depuis un fichier JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

