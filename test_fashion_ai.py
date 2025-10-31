"""
Tests unitaires simples pour valider le système d'IA
"""

import unittest
import os
import shutil
from user_preference_model import UserPreferences, UserInteraction
from preference_learning_engine import PreferenceLearningEngine
from datetime import datetime


class TestUserPreferenceModel(unittest.TestCase):
    """Tests pour le modèle de préférences utilisateur"""
    
    def setUp(self):
        """Prépare les tests"""
        self.user_id = "test_user"
        self.preferences = UserPreferences(user_id=self.user_id)
    
    def test_user_creation(self):
        """Test la création d'un utilisateur"""
        self.assertEqual(self.preferences.user_id, self.user_id)
        self.assertEqual(self.preferences.total_interactions, 0)
        self.assertEqual(self.preferences.learning_confidence, 0.0)
    
    def test_initial_weights(self):
        """Test que les poids initiaux sont à 0.5"""
        for weight in self.preferences.weights.values():
            self.assertEqual(weight, 0.5)
    
    def test_add_interaction(self):
        """Test l'ajout d'une interaction"""
        interaction = UserInteraction(
            brand_name="TestBrand",
            timestamp=datetime.now(),
            interaction_type="like",
            brand_features={'sustainable_materials': 0.8}
        )
        
        self.preferences.add_interaction(interaction)
        self.assertEqual(self.preferences.total_interactions, 1)
        self.assertGreater(self.preferences.learning_confidence, 0.0)
    
    def test_get_top_criteria(self):
        """Test la récupération des top critères"""
        self.preferences.weights['sustainable_materials'] = 0.9
        self.preferences.weights['price_range'] = 0.2
        
        top_criteria = self.preferences.get_top_criteria(3)
        self.assertEqual(len(top_criteria), 3)
        self.assertEqual(top_criteria[0][0], 'sustainable_materials')
        self.assertEqual(top_criteria[0][1], 0.9)
    
    def test_save_and_load(self):
        """Test la sauvegarde et le chargement"""
        test_dir = "test_user_data"
        os.makedirs(test_dir, exist_ok=True)
        
        try:
            # Sauvegarde
            filepath = os.path.join(test_dir, "test_user.json")
            self.preferences.weights['sustainable_materials'] = 0.8
            self.preferences.total_interactions = 5
            self.preferences.save_to_file(filepath)
            
            # Chargement
            loaded_prefs = UserPreferences.load_from_file(filepath)
            self.assertEqual(loaded_prefs.user_id, self.user_id)
            self.assertEqual(loaded_prefs.weights['sustainable_materials'], 0.8)
            self.assertEqual(loaded_prefs.total_interactions, 5)
        
        finally:
            # Nettoyage
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)


class TestPreferenceLearningEngine(unittest.TestCase):
    """Tests pour le moteur d'apprentissage"""
    
    def setUp(self):
        """Prépare les tests"""
        self.engine = PreferenceLearningEngine(learning_rate=0.1)
        self.preferences = UserPreferences(user_id="test_user")
    
    def test_learn_from_positive_interaction(self):
        """Test l'apprentissage d'une interaction positive"""
        interaction = UserInteraction(
            brand_name="EcoBrand",
            timestamp=datetime.now(),
            interaction_type="like",
            brand_features={'sustainable_materials': 0.9, 'price_range': 0.3}
        )
        
        initial_eco_weight = self.preferences.weights['sustainable_materials']
        
        updated_prefs = self.engine.learn_from_interaction(
            self.preferences,
            interaction
        )
        
        # Le poids du critère avec une valeur élevée devrait augmenter
        self.assertGreater(
            updated_prefs.weights['sustainable_materials'],
            initial_eco_weight
        )
    
    def test_learn_from_negative_interaction(self):
        """Test l'apprentissage d'une interaction négative"""
        interaction = UserInteraction(
            brand_name="CheapBrand",
            timestamp=datetime.now(),
            interaction_type="dislike",
            brand_features={'sustainable_materials': 0.1, 'price_range': 0.9}
        )
        
        initial_eco_weight = self.preferences.weights['sustainable_materials']
        
        updated_prefs = self.engine.learn_from_interaction(
            self.preferences,
            interaction
        )
        
        # Le poids devrait changer après l'interaction négative
        self.assertNotEqual(
            updated_prefs.weights['sustainable_materials'],
            initial_eco_weight
        )
    
    def test_learn_from_comparison(self):
        """Test l'apprentissage par comparaison"""
        chosen_features = {'sustainable_materials': 0.9, 'price_range': 0.5}
        rejected_features = {'sustainable_materials': 0.2, 'price_range': 0.5}
        
        initial_eco_weight = self.preferences.weights['sustainable_materials']
        
        updated_prefs = self.engine.learn_from_comparison(
            self.preferences,
            chosen_features,
            rejected_features
        )
        
        # Le poids de sustainable_materials devrait augmenter
        # car la marque choisie a un meilleur score
        self.assertGreater(
            updated_prefs.weights['sustainable_materials'],
            initial_eco_weight
        )
    
    def test_get_preference_insights(self):
        """Test la génération d'insights"""
        self.preferences.weights['sustainable_materials'] = 0.9
        self.preferences.weights['recycled_materials'] = 0.85
        self.preferences.weights['global_env_impact'] = 0.8
        self.preferences.total_interactions = 10
        
        insights = self.engine.get_preference_insights(self.preferences)
        
        self.assertIn('top_criteria', insights)
        self.assertIn('profile_type', insights)
        self.assertTrue(insights['is_eco_conscious'])
        self.assertEqual(insights['profile_type'], 'Eco-conscient')
    
    def test_signal_strength(self):
        """Test la force du signal pour différents types d'interaction"""
        purchase_strength = self.engine._get_signal_strength('purchase')
        like_strength = self.engine._get_signal_strength('like')
        view_strength = self.engine._get_signal_strength('view')
        
        self.assertGreater(purchase_strength, like_strength)
        self.assertGreater(like_strength, view_strength)
    
    def test_profile_categorization(self):
        """Test la catégorisation des profils"""
        # Profil éco-conscient
        eco_prefs = UserPreferences(user_id="eco_user")
        eco_prefs.weights['sustainable_materials'] = 0.9
        eco_prefs.weights['recycled_materials'] = 0.85
        eco_prefs.weights['global_env_impact'] = 0.8
        
        insights = self.engine.get_preference_insights(eco_prefs)
        self.assertEqual(insights['profile_type'], 'Eco-conscient')
        
        # Profil prix
        price_prefs = UserPreferences(user_id="price_user")
        price_prefs.weights['price_range'] = 0.9
        price_prefs.weights['sustainable_materials'] = 0.3
        
        insights = self.engine.get_preference_insights(price_prefs)
        self.assertEqual(insights['profile_type'], 'Prix')


def run_tests():
    """Lance tous les tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("Lancement des tests unitaires du système d'IA...\n")
    run_tests()

