"""
Routes de démonstration avec données mockées
Utilisables si MongoDB n'est pas disponible
"""
from fastapi import APIRouter, HTTPException
from models.brand import BrandOut
from utils.score_color import get_score_color, get_score_label

router = APIRouter(prefix="/demo", tags=["Demo"])

# Données de démonstration
DEMO_BRANDS = {
    "nike": {
        "brand_name": "nike",
        "logo": "https://logo.clearbit.com/nike.com",
        "website": "https://nike.com",
        "sustainable_materials": 45.0,
        "certifications": "B-Corp, Fair Trade",
        "global_env_impact": 6.5,
        "labor_ethics": 7.2,
        "final_score": 6.8,
        "price_range": 4.0,
        "country_production": "Vietnam, China",
        "unsold_management": "Donation, Recycling"
    },
    "adidas": {
        "brand_name": "adidas",
        "logo": "https://logo.clearbit.com/adidas.com",
        "website": "https://adidas.com",
        "sustainable_materials": 50.0,
        "certifications": "B-Corp",
        "global_env_impact": 7.0,
        "labor_ethics": 6.5,
        "final_score": 6.8,
        "price_range": 4.0,
        "country_production": "Indonesia, Vietnam",
        "unsold_management": "Recycling"
    },
    "patagonia": {
        "brand_name": "patagonia",
        "logo": "https://logo.clearbit.com/patagonia.com",
        "website": "https://patagonia.com",
        "sustainable_materials": 85.0,
        "certifications": "B-Corp, Fair Trade, Organic",
        "global_env_impact": 9.0,
        "labor_ethics": 8.5,
        "final_score": 8.8,
        "price_range": 5.0,
        "country_production": "USA, Fair Trade factories",
        "unsold_management": "Repair, Reuse, Recycle"
    },
    "zara": {
        "brand_name": "zara",
        "logo": "https://logo.clearbit.com/zara.com",
        "website": "https://zara.com",
        "sustainable_materials": 30.0,
        "certifications": None,
        "global_env_impact": 4.5,
        "labor_ethics": 5.0,
        "final_score": 4.8,
        "price_range": 2.0,
        "country_production": "Spain, Morocco, Turkey",
        "unsold_management": "Donation"
    },
    "h&m": {
        "brand_name": "h&m",
        "logo": "https://logo.clearbit.com/hm.com",
        "website": "https://hm.com",
        "sustainable_materials": 35.0,
        "certifications": "B-Corp",
        "global_env_impact": 5.0,
        "labor_ethics": 5.5,
        "final_score": 5.2,
        "price_range": 1.0,
        "country_production": "Bangladesh, China",
        "unsold_management": "Recycling, Donation"
    }
}

@router.get("/brands/name/{brand_name}", response_model=BrandOut)
async def get_demo_brand(brand_name: str) -> BrandOut:
    """
    Retourne des données de démonstration pour une marque
    Utilisable si MongoDB n'est pas disponible
    """
    brand_lower = brand_name.lower()
    
    # Chercher dans les données de démo
    demo_data = None
    for key, data in DEMO_BRANDS.items():
        if key == brand_lower or brand_lower in key or key in brand_lower:
            demo_data = data.copy()
            break
    
    if not demo_data:
        raise HTTPException(status_code=404, detail=f"Brand '{brand_name}' not found in demo data")
    
    # Créer un BrandOut avec les données de démo
    return BrandOut(
        id="demo-123",
        brand_name=demo_data["brand_name"],
        logo=demo_data.get("logo"),
        website=demo_data.get("website"),
        sustainable_materials=demo_data.get("sustainable_materials"),
        certifications=demo_data.get("certifications"),
        global_env_impact=demo_data.get("global_env_impact"),
        labor_ethics=demo_data.get("labor_ethics"),
        final_score=demo_data.get("final_score"),
        score_color=get_score_color(demo_data.get("final_score")),
        score_label=get_score_label(demo_data.get("final_score")),
        price_range=demo_data.get("price_range"),
        country_production=demo_data.get("country_production"),
        unsold_management=demo_data.get("unsold_management"),
    )


