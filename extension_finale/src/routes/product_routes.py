from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId

from models.product import Product, ProductCreate, ProductUpdate, ProductOut
from models.brand import Brand

router = APIRouter(prefix="/products", tags=["Products"])

async def to_out(p: Product) -> ProductOut:
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None
    if p.brand is not None:
        b = await p.brand.fetch() if hasattr(p.brand, "fetch") else p.brand
        if b:
            brand_id = str(b.id)
            brand_name = b.brand_name
    return ProductOut(id=str(p.id), name=p.name, brand_id=brand_id, brand_name=brand_name)

@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductCreate) -> ProductOut:
    prod = await Product.from_create(payload)
    if payload.brand_id and prod.brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    await prod.insert()
    return await to_out(prod)

@router.get("/", response_model=List[ProductOut])
async def list_products(brand_id: Optional[str] = Query(default=None)) -> List[ProductOut]:
    # filtre optionnel par marque
    if brand_id:
        brand = await Brand.get(brand_id)
        if not brand:
            # on peut retourner [] plutôt que 404, à toi de voir
            raise HTTPException(status_code=404, detail="Brand not found")
        products = await Product.find(Product.brand.id == brand.id).to_list()
    else:
        products = await Product.find_all().to_list()

    out: List[ProductOut] = []
    for p in products:
        out.append(await to_out(p))
    return out

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: PydanticObjectId) -> ProductOut:
    prod = await Product.get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return await to_out(prod)

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: PydanticObjectId, data: ProductUpdate) -> ProductOut:
    prod = await Product.get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = {}
    if data.name is not None:
        updates["name"] = data.name

    # si brand_id a été fourni (même si null), on met à jour l’association
    if "brand_id" in data.model_fields_set:
        if data.brand_id:
            brand = await Brand.get(data.brand_id)
            if not brand:
                raise HTTPException(status_code=404, detail="Brand not found")
            updates["brand"] = brand
        else:
            updates["brand"] = None

    if updates:
        await prod.set(updates)

    return await to_out(prod)

@router.delete("/{product_id}")
async def delete_product(product_id: PydanticObjectId) -> dict:
    prod = await Product.get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    await prod.delete()
    return {"message": "Product deleted"}
