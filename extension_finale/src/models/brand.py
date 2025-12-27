"""
Modèle Brand pour Beanie/MongoDB
"""
from typing import Optional
from beanie import Document
from pydantic import Field, BaseModel


class Brand(Document):
    """Modèle de document Brand pour MongoDB via Beanie"""
    
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None
    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: Optional[str] = None  # String, pas de liste
    country_origin: Optional[str] = None
    country_production: Optional[str] = None
    unsold_management: Optional[str] = None
    supply_chain_transparency: Optional[str] = None
    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    planet_badge: Optional[bool] = None
    labor_badge: Optional[bool] = None
    
    class Settings:
        name = "brands"  # Nom de la collection MongoDB


class BrandCreate(BaseModel):
    """Schéma pour créer une marque"""
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None
    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: Optional[str] = None
    country_origin: Optional[str] = None
    country_production: Optional[str] = None
    unsold_management: Optional[str] = None
    supply_chain_transparency: Optional[str] = None
    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    planet_badge: Optional[bool] = None
    labor_badge: Optional[bool] = None


class BrandUpdate(BaseModel):
    """Schéma pour mettre à jour une marque (tous les champs optionnels)"""
    brand_name: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None
    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: Optional[str] = None
    country_origin: Optional[str] = None
    country_production: Optional[str] = None
    unsold_management: Optional[str] = None
    supply_chain_transparency: Optional[str] = None
    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    planet_badge: Optional[bool] = None
    labor_badge: Optional[bool] = None


class BrandOut(BaseModel):
    """Schéma de sortie pour une marque (avec score_color et score_label calculés)"""
    id: str
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None
    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: Optional[str] = None
    country_origin: Optional[str] = None
    country_production: Optional[str] = None
    unsold_management: Optional[str] = None
    supply_chain_transparency: Optional[str] = None
    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None
    score_color: Optional[str] = None
    score_label: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    planet_badge: Optional[bool] = None
    labor_badge: Optional[bool] = None


