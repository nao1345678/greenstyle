"""
Tests unitaires pour calcul_score.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

try:
    from CalculScore.calcul_score import calculate_scores
except ImportError:
    from calcul_score import calculate_scores


class TestCalculateScores:
    """Tests pour la fonction calculate_scores"""
    
    def test_marque_excellente_veja(self):
        """Test du calcul de score pour Veja (marque engagée)"""
        brand_data = {
            "brand_name": "veja",
            "sustainable_materials": 85.0,
            "certifications": "Fair Trade, Organic Cotton, B-Corp",
            "country_origin": "France",
            "country_production": "Brazil",
            "unsold_management": "Recyclage, Réparation",
            "supply_chain_transparency": "Totale",
            "labor_ethics": 85.0
        }
        
        scores = calculate_scores(brand_data)
        
        assert scores is not None
        assert "final_score" in scores
        assert "global_env_impact" in scores
        assert "labor_ethics" in scores
        
        # Veja devrait avoir un score élevé
        assert scores["final_score"] >= 8.0
        assert scores["global_env_impact"] >= 8.0
        assert scores["labor_ethics"] >= 8.0
    
    def test_marque_fast_fashion_nike(self):
        """Test du calcul de score pour Nike (fast fashion)"""
        brand_data = {
            "brand_name": "nike",
            "sustainable_materials": 25.0,
            "certifications": "Nike Grind, Move to Zero",
            "country_origin": "USA",
            "country_production": "Vietnam, China, Indonesia",
            "unsold_management": "Recyclage partiel, Donation",
            "supply_chain_transparency": "Modérée",
            "labor_ethics": 55.0
        }
        
        scores = calculate_scores(brand_data)
        
        assert scores is not None
        assert "final_score" in scores
        
        # Nike devrait avoir un score plus faible
        assert scores["final_score"] < 7.0
    
    def test_production_france(self):
        """Test que la production en France donne un bonus"""
        brand_data = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        scores = calculate_scores(brand_data)
        assert scores["global_env_impact"] >= 7.0
    
    def test_production_chine(self):
        """Test que la production en Chine donne un score plus faible"""
        brand_data = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "USA",
            "country_production": "China",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Modérée",
            "labor_ethics": 60.0
        }
        
        scores = calculate_scores(brand_data)
        # Le score environnemental devrait être plus faible à cause de la Chine
        assert scores["global_env_impact"] < 7.0
    
    def test_materiaux_durables_elevés(self):
        """Test que des matériaux durables élevés augmentent le score"""
        brand_data_high = {
            "brand_name": "test",
            "sustainable_materials": 90.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        brand_data_low = {
            "brand_name": "test",
            "sustainable_materials": 10.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        scores_high = calculate_scores(brand_data_high)
        scores_low = calculate_scores(brand_data_low)
        
        assert scores_high["global_env_impact"] > scores_low["global_env_impact"]
    
    def test_certifications_multiples(self):
        """Test que plusieurs certifications augmentent le score"""
        brand_data_many = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp, Fair Trade, GOTS",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        brand_data_few = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        scores_many = calculate_scores(brand_data_many)
        scores_few = calculate_scores(brand_data_few)
        
        assert scores_many["global_env_impact"] > scores_few["global_env_impact"]
    
    def test_donnees_manquantes(self):
        """Test que le calcul fonctionne avec des données manquantes"""
        brand_data = {
            "brand_name": "test",
            "sustainable_materials": None,
            "certifications": None,
            "country_origin": None,
            "country_production": None,
            "unsold_management": None,
            "supply_chain_transparency": None,
            "labor_ethics": None
        }
        
        scores = calculate_scores(brand_data)
        
        assert scores is not None
        assert "final_score" in scores
        # Le score devrait être faible mais calculable
        assert scores["final_score"] >= 0
    
    def test_labor_ethics_numerique(self):
        """Test que labor_ethics numérique est correctement traité"""
        brand_data = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 85.0  # Sur 100
        }
        
        scores = calculate_scores(brand_data)
        
        # labor_ethics devrait être converti sur 10
        assert scores["labor_ethics"] <= 10.0
        assert scores["labor_ethics"] >= 0.0
    
    def test_scores_finaux_limites(self):
        """Test que les scores finaux sont dans les bonnes limites"""
        brand_data = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 75.0
        }
        
        scores = calculate_scores(brand_data)
        
        assert 0 <= scores["final_score"] <= 10
        assert 0 <= scores["global_env_impact"] <= 10
        assert 0 <= scores["labor_ethics"] <= 10
    
    def test_transparence_totale(self):
        """Test que la transparence totale augmente le score"""
        brand_data_high = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Totale",
            "labor_ethics": 75.0
        }
        
        brand_data_low = {
            "brand_name": "test",
            "sustainable_materials": 50.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Faible",
            "labor_ethics": 75.0
        }
        
        scores_high = calculate_scores(brand_data_high)
        scores_low = calculate_scores(brand_data_low)
        
        assert scores_high["global_env_impact"] > scores_low["global_env_impact"]

