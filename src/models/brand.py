from beanie import Document
from pydantic import BaseModel
from typing import Optional

# ---- INPUT SCHEMA (JSON body) ----
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


# ---- DOCUMENT stored in DB ----
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
        name = "brands"  # match Mongo collection
