from beanie import Document
from pydantic import BaseModel
from typing import Optional


class BrandCreate(BaseModel):
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

    planet_badge: Optional[bool] = False
    labor_badge: Optional[bool] = False


class BrandUpdate(BaseModel):
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
    score_color: Optional[str] = None  # Couleur calculée à partir du score
    score_label: Optional[str] = None  # Label textuel du score

    short_description: Optional[str] = None
    description: Optional[str] = None

    planet_badge: Optional[bool] = False
    labor_badge: Optional[bool] = False


class Brand(Document):
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

    planet_badge: Optional[bool] = False
    labor_badge: Optional[bool] = False

    class Settings:
        name = "brands"
