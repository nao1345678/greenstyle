"""
Tests fonctionnels pour le service de scraping
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from services.scraper_service import scrape_brand_data


class TestScraperService:
    """Tests pour le service de scraping"""
    
    @pytest.mark.asyncio
    async def test_scrape_brand_with_fallback(self):
        """Test que le scraping utilise les données de fallback pour Veja"""
        data = await scrape_brand_data("veja")
        
        assert data is not None
        assert data["brand_name"] == "veja"
        assert data["sustainable_materials"] == 85.0
        assert "Fair Trade" in data.get("certifications", "")
    
    @pytest.mark.asyncio
    async def test_scrape_brand_unknown(self):
        """Test que le scraping fonctionne pour une marque inconnue"""
        # Mock les scrapers pour éviter les appels réels
        with patch('services.scraper_service.analyze_brand_for_recycled_materials') as mock_recycled, \
             patch('services.scraper_service.find_certifications_for_brand') as mock_certs, \
             patch('services.scraper_service.analyze_unsold_management') as mock_unsold, \
             patch('services.scraper_service.get_production_countries_from_database') as mock_countries:
            
            mock_recycled.return_value = {"percentage": None, "confidence": "low"}
            mock_certs.return_value = {"certifications": [], "confidence": "low"}
            mock_unsold.return_value = {"policy": None, "practices": []}
            mock_countries.return_value = None
            
            data = await scrape_brand_data("marque_inexistante_xyz")
            
            assert data is not None
            assert data["brand_name"] == "marque_inexistante_xyz"
    
    @pytest.mark.asyncio
    async def test_scrape_brand_structure(self):
        """Test que les données scrapées ont la bonne structure"""
        data = await scrape_brand_data("veja")
        
        # Vérifier les champs essentiels
        assert "brand_name" in data
        assert "sustainable_materials" in data
        assert "certifications" in data
        assert "country_production" in data
        assert "country_origin" in data
        assert "unsold_management" in data
        assert "supply_chain_transparency" in data
    
    @pytest.mark.asyncio
    async def test_scrape_brand_with_website(self):
        """Test que le scraping fonctionne avec un site web fourni"""
        data = await scrape_brand_data("veja", website="https://www.veja-store.com")
        
        assert data is not None
        assert data["brand_name"] == "veja"
        if "website" in data:
            assert "veja" in data["website"].lower()
    
    @pytest.mark.asyncio
    async def test_scrape_brand_patagonia(self):
        """Test du scraping pour Patagonia (marque engagée)"""
        data = await scrape_brand_data("patagonia")
        
        assert data is not None
        assert data["brand_name"] == "patagonia"
        assert data["sustainable_materials"] == 90.0
        assert data["sustainable_materials"] >= 80.0  # Score élevé
    
    @pytest.mark.asyncio
    async def test_scrape_brand_nike(self):
        """Test du scraping pour Nike (fast fashion)"""
        data = await scrape_brand_data("nike")
        
        assert data is not None
        assert data["brand_name"] == "nike"
        # Nike devrait avoir un score plus faible
        assert data.get("sustainable_materials", 100) < 50.0

