from typing import List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from beanie import PydanticObjectId

from models.brand import Brand, BrandCreate, BrandUpdate, BrandOut
from utils.score_color import get_score_color, get_score_label
from services.scraper_service import scrape_brand_data
import sys
import os
# Ajouter le répertoire parent pour importer calcul_score
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CalculScore')))
try:
    from CalculScore.calcul_score import calculate_scores
except ImportError:
    from calcul_score import calculate_scores

router = APIRouter(prefix="/brands", tags=["Brands"])


def to_out(b: Brand) -> BrandOut:
    """Convertit un Brand en BrandOut avec score_color et score_label calculés"""
    return BrandOut(
        id=str(b.id),
        brand_name=b.brand_name,
        logo=b.logo,
        website=b.website,
        category_id=b.category_id,
        price_range=b.price_range,
        sustainable_materials=b.sustainable_materials,
        certifications=b.certifications,
        country_origin=b.country_origin,
        country_production=b.country_production,
        unsold_management=b.unsold_management,
        supply_chain_transparency=b.supply_chain_transparency,
        global_env_impact=b.global_env_impact,
        labor_ethics=b.labor_ethics,
        final_score=b.final_score,
        score_color=get_score_color(b.final_score),
        score_label=get_score_label(b.final_score),
        short_description=b.short_description,
        description=b.description,
        planet_badge=b.planet_badge,
        labor_badge=b.labor_badge,
    )


@router.post("/", response_model=BrandOut)
async def create_brand(payload: BrandCreate) -> BrandOut:
    brand = Brand(**payload.model_dump())
    await brand.insert()
    return to_out(brand)


@router.get("/", response_model=List[BrandOut])
async def list_brands() -> List[BrandOut]:
    brands = await Brand.find_all().to_list()
    return [to_out(b) for b in brands]


@router.get("/{brand_id}", response_model=BrandOut)
async def get_brand(brand_id: PydanticObjectId) -> BrandOut:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return to_out(brand)


@router.put("/{brand_id}", response_model=BrandOut)
async def update_brand(brand_id: PydanticObjectId, data: BrandUpdate) -> BrandOut:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    await brand.set(data.model_dump(exclude_unset=True))
    return to_out(brand)


@router.delete("/{brand_id}")
async def delete_brand(brand_id: PydanticObjectId) -> dict:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    await brand.delete()
    return {"message": "Brand deleted"}


@router.get("/name/{brand_name}", response_model=BrandOut)
async def get_brand_by_name(brand_name: str, auto_scrape: bool = True) -> BrandOut:
    """
    Recherche une marque par son nom (insensible à la casse)
    Utilisé par l'extension Chrome pour obtenir les infos de durabilité
    
    Si la marque n'est pas trouvée et auto_scrape=True, lance automatiquement le scraping
    """
    try:
        # Recherche insensible à la casse
        brand = await Brand.find_one(
            Brand.brand_name == {"$regex": f"^{brand_name}$", "$options": "i"}
        )
        
        if not brand and auto_scrape:
            # Marque non trouvée : lancer le scraping automatique
            print(f"🔍 Marque '{brand_name}' non trouvée, lancement du scraping automatique...")
            scraped_data = await scrape_brand_data(brand_name)
            
            # Calculer les scores
            scores = calculate_scores(scraped_data)
            scraped_data.update(scores)
            
            # Créer et sauvegarder la marque
            brand = Brand(**scraped_data)
            await brand.insert()
            print(f"✅ Marque '{brand_name}' créée avec données scrapées")
        
        if not brand:
            raise HTTPException(status_code=404, detail=f"Brand '{brand_name}' not found")
        
        return to_out(brand)
    except HTTPException:
        raise
    except Exception as e:
        # Si MongoDB n'est pas disponible, retourner 404 au lieu d'une erreur 500
        if "MongoDB" in str(e) or "connection" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Brand '{brand_name}' not found (database unavailable)")
        print(f"❌ Erreur lors de la recherche/scraping de '{brand_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Error processing brand: {str(e)}")


@router.get("/search/{query}", response_model=List[BrandOut])
async def search_brands(query: str, limit: int = 10) -> List[BrandOut]:
    """
    Recherche de marques par nom (recherche partielle)
    """
    brands = await Brand.find(
        Brand.brand_name == {"$regex": query, "$options": "i"}
    ).limit(limit).to_list()
    
    return [to_out(b) for b in brands]


@router.post("/scrape/{brand_name}", response_model=BrandOut)
async def scrape_brand(brand_name: str, website: str = None) -> BrandOut:
    """
    Lance le scraping manuel d'une marque
    """
    try:
        # Vérifier si la marque existe déjà
        existing_brand = await Brand.find_one(
            Brand.brand_name == {"$regex": f"^{brand_name}$", "$options": "i"}
        )
        
        if existing_brand:
            # Mettre à jour avec les nouvelles données scrapées
            scraped_data = await scrape_brand_data(brand_name, website)
            scores = calculate_scores(scraped_data)
            scraped_data.update(scores)
            
            await existing_brand.set(scraped_data)
            return to_out(existing_brand)
        else:
            # Créer une nouvelle marque
            scraped_data = await scrape_brand_data(brand_name, website)
            scores = calculate_scores(scraped_data)
            scraped_data.update(scores)
            
            brand = Brand(**scraped_data)
            await brand.insert()
            return to_out(brand)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping brand: {str(e)}")
