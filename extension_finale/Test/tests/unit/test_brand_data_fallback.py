"""
Tests unitaires pour brand_data_fallback.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from services.brand_data_fallback import get_fallback_brand_data, ENGAGED_BRANDS_DATA


class TestGetFallbackBrandData:
    """Tests pour la fonction get_fallback_brand_data"""
    
    def test_marque_connue_veja(self):
        """Test que Veja retourne des données"""
        data = get_fallback_brand_data("veja")
        assert data is not None
        assert data["brand_name"] == "veja"
        assert data["sustainable_materials"] == 85.0
        assert "Fair Trade" in data["certifications"]
    
    def test_marque_connue_patagonia(self):
        """Test que Patagonia retourne des données"""
        data = get_fallback_brand_data("patagonia")
        assert data is not None
        assert data["brand_name"] == "patagonia"
        assert data["sustainable_materials"] == 90.0
    
    def test_marque_connue_insensible_casse(self):
        """Test que la recherche est insensible à la casse"""
        data1 = get_fallback_brand_data("VEJA")
        data2 = get_fallback_brand_data("Veja")
        data3 = get_fallback_brand_data("veja")
        
        assert data1 is not None
        assert data2 is not None
        assert data3 is not None
        assert data1["brand_name"] == data2["brand_name"] == data3["brand_name"]
    
    def test_marque_avec_espaces(self):
        """Test que les espaces sont gérés"""
        data = get_fallback_brand_data("the north face")
        assert data is not None
        assert data["brand_name"] == "the north face"
    
    def test_marque_avec_caracteres_speciaux(self):
        """Test que les caractères spéciaux sont gérés"""
        data = get_fallback_brand_data("h&m")
        assert data is not None
        assert data["brand_name"] == "h&m"
    
    def test_marque_inexistante(self):
        """Test qu'une marque inconnue retourne None"""
        data = get_fallback_brand_data("marque_inexistante_xyz")
        assert data is None
    
    def test_marque_vide(self):
        """Test qu'une chaîne vide retourne None"""
        data = get_fallback_brand_data("")
        assert data is None
    
    def test_marque_nike(self):
        """Test que Nike retourne des données (fast fashion)"""
        data = get_fallback_brand_data("nike")
        assert data is not None
        assert data["brand_name"] == "nike"
        assert data["sustainable_materials"] == 25.0  # Score faible
    
    def test_marque_zara(self):
        """Test que Zara retourne des données (fast fashion)"""
        data = get_fallback_brand_data("zara")
        assert data is not None
        assert data["brand_name"] == "zara"
        assert data["sustainable_materials"] == 20.0  # Score faible
    
    def test_structure_donnees(self):
        """Test que les données retournées ont la bonne structure"""
        data = get_fallback_brand_data("veja")
        assert data is not None
        
        # Vérifier que tous les champs attendus sont présents
        required_fields = [
            "brand_name", "sustainable_materials", "certifications",
            "country_production", "country_origin", "unsold_management",
            "supply_chain_transparency", "labor_ethics", "description"
        ]
        
        for field in required_fields:
            assert field in data, f"Le champ {field} est manquant"
    
    def test_valeurs_numeriques(self):
        """Test que les valeurs numériques sont correctes"""
        data = get_fallback_brand_data("veja")
        assert isinstance(data["sustainable_materials"], (int, float))
        assert isinstance(data["labor_ethics"], (int, float))
        assert 0 <= data["sustainable_materials"] <= 100
        assert 0 <= data["labor_ethics"] <= 100

