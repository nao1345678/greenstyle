"""
Tests fonctionnels pour les routes de marques
"""
import pytest
from httpx import AsyncClient
from beanie import PydanticObjectId

from models.brand import Brand


class TestBrandRoutes:
    """Tests pour les routes /brands"""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test de l'endpoint racine"""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "GreenStyle API"
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, client: AsyncClient):
        """Test de l'endpoint de santé"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_list_brands_empty(self, client: AsyncClient):
        """Test de la liste des marques (vide)"""
        response = await client.get("/brands/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_create_brand(self, client: AsyncClient, sample_brand_data):
        """Test de création d'une marque"""
        response = await client.post("/brands/", json=sample_brand_data)
        assert response.status_code == 200
        data = response.json()
        assert data["brand_name"] == sample_brand_data["brand_name"]
        assert "id" in data
        assert "score_color" in data
        assert "score_label" in data
    
    @pytest.mark.asyncio
    async def test_get_brand_by_name(self, client: AsyncClient, sample_brand_data_veja):
        """Test de récupération d'une marque par nom"""
        # Créer d'abord la marque
        create_response = await client.post("/brands/", json=sample_brand_data_veja)
        assert create_response.status_code == 200
        
        # Récupérer par nom
        response = await client.get(f"/brands/name/{sample_brand_data_veja['brand_name']}")
        assert response.status_code == 200
        data = response.json()
        assert data["brand_name"].lower() == sample_brand_data_veja["brand_name"].lower()
    
    @pytest.mark.asyncio
    async def test_get_brand_by_name_not_found(self, client: AsyncClient):
        """Test de récupération d'une marque inexistante"""
        response = await client.get("/brands/name/marque_inexistante_xyz", params={"auto_scrape": False})
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_brand_by_name_auto_scrape(self, client: AsyncClient):
        """Test de récupération avec auto-scraping"""
        # Tester avec une marque connue (Veja) qui devrait être scrapée
        response = await client.get("/brands/name/veja", params={"auto_scrape": True})
        # Peut retourner 200 (si scraping réussi) ou 500 (si erreur)
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "brand_name" in data
            assert "final_score" in data
    
    @pytest.mark.asyncio
    async def test_update_brand(self, client: AsyncClient, sample_brand_data):
        """Test de mise à jour d'une marque"""
        # Créer la marque
        create_response = await client.post("/brands/", json=sample_brand_data)
        assert create_response.status_code == 200
        brand_id = create_response.json()["id"]
        
        # Mettre à jour
        update_data = {"sustainable_materials": 90.0}
        response = await client.put(f"/brands/{brand_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["sustainable_materials"] == 90.0
    
    @pytest.mark.asyncio
    async def test_delete_brand(self, client: AsyncClient, sample_brand_data):
        """Test de suppression d'une marque"""
        # Créer la marque
        create_response = await client.post("/brands/", json=sample_brand_data)
        assert create_response.status_code == 200
        brand_id = create_response.json()["id"]
        
        # Supprimer
        response = await client.delete(f"/brands/{brand_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Vérifier qu'elle n'existe plus
        get_response = await client.get(f"/brands/{brand_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_search_brands(self, client: AsyncClient, sample_brand_data):
        """Test de recherche de marques"""
        # Créer une marque
        await client.post("/brands/", json=sample_brand_data)
        
        # Rechercher
        response = await client.get(f"/brands/search/{sample_brand_data['brand_name'][:4]}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_brand_score_calculation(self, client: AsyncClient, sample_brand_data):
        """Test que les scores sont calculés lors de la création"""
        response = await client.post("/brands/", json=sample_brand_data)
        assert response.status_code == 200
        data = response.json()
        
        # Vérifier que les scores sont présents
        assert "final_score" in data
        assert "global_env_impact" in data
        assert "labor_ethics" in data
        assert "score_color" in data
        assert "score_label" in data
        
        # Vérifier que les scores sont dans les bonnes limites
        if data["final_score"] is not None:
            assert 0 <= data["final_score"] <= 10
    
    @pytest.mark.asyncio
    async def test_brand_score_color_mapping(self, client: AsyncClient):
        """Test que les couleurs de score sont correctement mappées"""
        # Test avec une marque à score élevé
        high_score_data = {
            "brand_name": "test_high",
            "sustainable_materials": 90.0,
            "certifications": "B-Corp, Fair Trade",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Totale",
            "labor_ethics": 90.0
        }
        
        response = await client.post("/brands/", json=high_score_data)
        assert response.status_code == 200
        data = response.json()
        
        if data["final_score"] and data["final_score"] >= 8:
            assert data["score_color"] == "green"
            assert data["score_label"] == "Excellent"

