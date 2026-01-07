"""
Tests d'intégration pour l'API complète
"""
import pytest
from httpx import AsyncClient

from models.brand import Brand


class TestAPIIntegration:
    """Tests d'intégration pour le flux complet de l'API"""
    
    @pytest.mark.asyncio
    async def test_complete_brand_workflow(self, client: AsyncClient):
        """Test du workflow complet : création, récupération, mise à jour, suppression"""
        # 1. Créer une marque
        brand_data = {
            "brand_name": "test_integration",
            "sustainable_materials": 75.0,
            "certifications": "B-Corp",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage",
            "supply_chain_transparency": "Élevée",
            "labor_ethics": 80.0
        }
        
        create_response = await client.post("/brands/", json=brand_data)
        assert create_response.status_code == 200
        created_brand = create_response.json()
        brand_id = created_brand["id"]
        
        # 2. Récupérer la marque par ID
        get_response = await client.get(f"/brands/{brand_id}")
        assert get_response.status_code == 200
        retrieved_brand = get_response.json()
        assert retrieved_brand["brand_name"] == brand_data["brand_name"]
        
        # 3. Récupérer la marque par nom
        get_by_name_response = await client.get(f"/brands/name/{brand_data['brand_name']}")
        assert get_by_name_response.status_code == 200
        assert get_by_name_response.json()["brand_name"] == brand_data["brand_name"]
        
        # 4. Mettre à jour la marque
        update_data = {"sustainable_materials": 85.0}
        update_response = await client.put(f"/brands/{brand_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["sustainable_materials"] == 85.0
        
        # 5. Rechercher la marque
        search_response = await client.get(f"/brands/search/test")
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) > 0
        
        # 6. Supprimer la marque
        delete_response = await client.delete(f"/brands/{brand_id}")
        assert delete_response.status_code == 200
        
        # 7. Vérifier que la marque n'existe plus
        get_after_delete = await client.get(f"/brands/{brand_id}")
        assert get_after_delete.status_code == 404
    
    @pytest.mark.asyncio
    async def test_brand_scoring_integration(self, client: AsyncClient):
        """Test que le calcul de score est intégré dans le workflow"""
        brand_data = {
            "brand_name": "test_scoring",
            "sustainable_materials": 90.0,
            "certifications": "B-Corp, Fair Trade, GOTS",
            "country_origin": "France",
            "country_production": "France",
            "unsold_management": "Recyclage, Réparation",
            "supply_chain_transparency": "Totale",
            "labor_ethics": 90.0
        }
        
        response = await client.post("/brands/", json=brand_data)
        assert response.status_code == 200
        data = response.json()
        
        # Vérifier que les scores sont calculés
        assert data["final_score"] is not None
        assert data["global_env_impact"] is not None
        assert data["labor_ethics"] is not None
        
        # Vérifier que les scores sont cohérents (marque engagée = score élevé)
        assert data["final_score"] >= 8.0
        assert data["score_color"] == "green"
        assert data["score_label"] == "Excellent"
    
    @pytest.mark.asyncio
    async def test_multiple_brands_operations(self, client: AsyncClient):
        """Test des opérations sur plusieurs marques"""
        brands = [
            {
                "brand_name": f"test_brand_{i}",
                "sustainable_materials": 50.0 + i * 5,
                "certifications": "B-Corp",
                "country_origin": "France",
                "country_production": "France",
                "unsold_management": "Recyclage",
                "supply_chain_transparency": "Élevée",
                "labor_ethics": 70.0
            }
            for i in range(3)
        ]
        
        created_ids = []
        
        # Créer plusieurs marques
        for brand_data in brands:
            response = await client.post("/brands/", json=brand_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])
        
        # Lister toutes les marques
        list_response = await client.get("/brands/")
        assert list_response.status_code == 200
        all_brands = list_response.json()
        assert len(all_brands) >= len(brands)
        
        # Rechercher une marque
        search_response = await client.get("/brands/search/test_brand")
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) >= len(brands)
        
        # Nettoyer : supprimer les marques créées
        for brand_id in created_ids:
            await client.delete(f"/brands/{brand_id}")

