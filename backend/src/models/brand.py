from beanie import Document
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


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


def _to_list_of_str(v):
    """
    Normalise certifications:
    - None / "" / [] -> []
    - "url" -> ["url"]
    - ["a", "b"] -> ["a", "b"]
    - autres -> [str(v)]
    """
    if v in (None, "", []):
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v if x not in (None, "")]
    return [str(v)]



class BrandCreate(BaseModel):
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None

    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
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

    @field_validator("certifications", mode="before")
    @classmethod
    def _normalize_certs_create(cls, v):
        return _to_list_of_str(v)


class BrandUpdate(BaseModel):
    brand_name: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None

    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: Optional[List[str]] = None
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

    @field_validator("certifications", mode="before")
    @classmethod
    def _normalize_certs_update(cls, v):
        if v is None:
            return None
        return _to_list_of_str(v)


class BrandOut(BaseModel):
    id: str
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None

    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
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

    @field_validator("certifications", mode="before")
    @classmethod
    def _normalize_certs_out(cls, v):
        return _to_list_of_str(v)


class Brand(Document):
    brand_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    category_id: Optional[str] = None

    price_range: Optional[float] = None
    sustainable_materials: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
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

    @field_validator("certifications", mode="before")
    @classmethod
    def _normalize_certs_doc(cls, v):
        return _to_list_of_str(v)
