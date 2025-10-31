from beanie import Document
from pydantic import BaseModel, field_validator
from typing import Optional


def _to_float_or_none(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None


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
    supply_chain_transparency: Optional[float] = None

    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None

    short_description: Optional[str] = None
    description: Optional[str] = None

    planet_badge: Optional[bool] = False
    labor_badge: Optional[bool] = False

    @field_validator("supply_chain_transparency", mode="before")
    @classmethod
    def _coerce_sct_create(cls, v):
        return _to_float_or_none(v)


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
    supply_chain_transparency: Optional[float] = None

    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None

    short_description: Optional[str] = None
    description: Optional[str] = None

    planet_badge: Optional[bool] = None
    labor_badge: Optional[bool] = None

    @field_validator("supply_chain_transparency", mode="before")
    @classmethod
    def _coerce_sct_update(cls, v):
        return _to_float_or_none(v)


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
    supply_chain_transparency: Optional[float] = None

    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None

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
    supply_chain_transparency: Optional[float] = None

    global_env_impact: Optional[float] = None
    labor_ethics: Optional[float] = None
    final_score: Optional[float] = None

    short_description: Optional[str] = None
    description: Optional[str] = None

    planet_badge: Optional[bool] = False
    labor_badge: Optional[bool] = False

    class Settings:
        name = "brands"

    @field_validator("supply_chain_transparency", mode="before")
    @classmethod
    def _coerce_sct_doc(cls, v):
        return _to_float_or_none(v)
