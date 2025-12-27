from typing import List, Optional, Any
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


def normalize_certifications(certs: Any) -> Optional[str]:
    """
    Normalise les certifications pour qu'elles soient toujours une string ou None.
    Gère les listes, les strings, les URLs, etc.
    """
    print(f"   🔧 normalize_certifications appelée avec type: {type(certs)}, valeur: {str(certs)[:100] if certs else None}")
    
    if certs is None:
        print(f"   ✅ Retour None (certs est None)")
        return None
    
    # Si c'est déjà une string
    if isinstance(certs, str):
        certs_clean = certs.strip()
        result = certs_clean if certs_clean else None
        print(f"   ✅ Retour string: {result}")
        return result
    
    # Si c'est une liste
    if isinstance(certs, list):
        print(f"   🔧 Traitement d'une liste de {len(certs)} éléments")
        certs_filtered = []
        for c in certs:
            if c is None:
                continue
            c_str = str(c).strip()
            # Ignorer les URLs (commencent par http:// ou https://)
            if c_str and not c_str.startswith('http://') and not c_str.startswith('https://'):
                certs_filtered.append(c_str)
        result = ', '.join(certs_filtered) if certs_filtered else None
        print(f"   ✅ Retour depuis liste: {result}")
        return result
    
    # Autre type, convertir en string
    certs_str = str(certs).strip()
    # Si ça ressemble à une URL, retourner None
    if certs_str.startswith('http://') or certs_str.startswith('https://'):
        print(f"   ✅ Retour None (URL détectée)")
        return None
    result = certs_str if certs_str else None
    print(f"   ✅ Retour depuis autre type: {result}")
    return result


def to_out(b: Brand) -> BrandOut:
    """Convertit un Brand en BrandOut avec score_color et score_label calculés"""
    # Normaliser les certifications (peuvent être une liste dans MongoDB)
    certifications = normalize_certifications(b.certifications)
    
    return BrandOut(
        id=str(b.id),
        brand_name=b.brand_name,
        logo=b.logo,
        website=b.website,
        category_id=b.category_id,
        price_range=b.price_range,
        sustainable_materials=b.sustainable_materials,
        certifications=certifications,
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


@router.get("/fix-certifications", response_model=dict)
async def fix_all_certifications() -> dict:
    """
    Endpoint temporaire pour corriger toutes les certifications dans MongoDB
    Convertit les listes de certifications en strings
    """
    try:
        collection = Brand.get_motor_collection()
        
        # Trouver tous les documents avec des certifications en liste
        cursor = collection.find({"certifications": {"$exists": True, "$ne": None, "$type": "array"}})
        
        fixed_count = 0
        skipped_count = 0
        error_count = 0
        
        async for doc in cursor:
            try:
                certs = doc.get('certifications')
                
                # Normaliser les certifications
                certs_normalized = normalize_certifications(certs)
                
                # Mettre à jour le document
                await collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"certifications": certs_normalized}}
                )
                
                brand_name = doc.get('brand_name', 'Unknown')
                print(f"  ✅ Corrigé: {brand_name}")
                fixed_count += 1
                
            except Exception as e:
                error_count += 1
                brand_name = doc.get('brand_name', 'Unknown')
                print(f"  ❌ Erreur pour {brand_name}: {e}")
        
        return {
            "message": "Correction terminée",
            "fixed": fixed_count,
            "errors": error_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fixing certifications: {str(e)}")


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
    Fonctionne même si MongoDB n'est pas disponible (retourne les données scrapées sans les sauvegarder)
    """
    brand = None
    try:
        # Essayer de se connecter à MongoDB via Beanie
        mongo_available = False
        try:
            # Tester si Beanie est initialisé en cherchant une marque inexistante
            await Brand.find_one(Brand.brand_name == "___test_connection___")
            mongo_available = True
        except Exception as e:
            print(f"⚠️  MongoDB non disponible: {e}")
            print("📊 Mode sans MongoDB activé - scraping et calcul de scores sans sauvegarde")
        
        # Si MongoDB est disponible, chercher la marque dans la base
        existing_brand = None
        if mongo_available:
            try:
                # Recherche insensible à la casse avec Beanie
                existing_brand = await Brand.find_one(
                    Brand.brand_name == {"$regex": f"^{brand_name}$", "$options": "i"}
                )
            except Exception as e:
                print(f"⚠️  Erreur lors de la recherche MongoDB: {e}")
                mongo_available = False
        
        # Si la marque existe dans MongoDB, la retourner
        if existing_brand:
            return to_out(existing_brand)
            
        # Si la marque n'est pas trouvée dans MongoDB (ou MongoDB indisponible), scraper et calculer
        if not existing_brand and auto_scrape:
            # Marque non trouvée : lancer le scraping automatique
            print(f"🔍 Marque '{brand_name}' non trouvée, lancement du scraping automatique...")
            scraped_data = await scrape_brand_data(brand_name)
            
            # Normaliser les certifications AVANT le calcul des scores
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            # Calculer les scores
            print(f"📊 Calcul des scores pour '{brand_name}'...")
            scores = calculate_scores(scraped_data.copy())
            if scores and isinstance(scores, dict):
                scraped_data.update(scores)
                print(f"✅ Scores calculés pour '{brand_name}': final_score={scraped_data.get('final_score')}, labor={scraped_data.get('labor_ethics')}, planet={scraped_data.get('global_env_impact')}")
            
            # Normaliser à nouveau après le calcul des scores (au cas où calculate_scores aurait modifié)
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            # S'assurer que sustainable_materials est un float ou None
            if 'sustainable_materials' in scraped_data:
                try:
                    if scraped_data['sustainable_materials'] is not None:
                        scraped_data['sustainable_materials'] = float(scraped_data['sustainable_materials'])
                except (ValueError, TypeError):
                    scraped_data['sustainable_materials'] = None
            
            # Protection ULTIME : normaliser les certifications une dernière fois
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            # Debug: afficher les données finales
            print(f"   📋 Données finales pour '{brand_name}': certifications type={type(scraped_data.get('certifications'))}, value={str(scraped_data.get('certifications'))[:50] if scraped_data.get('certifications') else None}")
            
            # Sauvegarder dans MongoDB si disponible, sinon retourner directement les données
            if mongo_available:
                try:
                    brand = Brand(**scraped_data)
                    await brand.insert()
                    print(f"✅ Marque '{brand_name}' sauvegardée dans MongoDB (score: {scraped_data.get('final_score', 'N/A')})")
                except Exception as e:
                    print(f"⚠️  Erreur lors de la sauvegarde dans MongoDB: {e}")
                    print("📊 Retour des données sans sauvegarde")
                    # Continuer pour retourner les données quand même
            else:
                print(f"📊 Marque '{brand_name}' scrapée et scores calculés (sans sauvegarde MongoDB)")
            
            # Créer un BrandOut directement depuis les données scrapées (avec ou sans MongoDB)
            return BrandOut(
                id=scraped_data.get('id', f"scraped-{brand_name}"),
                brand_name=scraped_data.get('brand_name', brand_name),
                logo=scraped_data.get('logo'),
                website=scraped_data.get('website'),
                category_id=scraped_data.get('category_id'),
                price_range=scraped_data.get('price_range'),
                sustainable_materials=scraped_data.get('sustainable_materials'),
                certifications=scraped_data.get('certifications'),
                country_origin=scraped_data.get('country_origin'),
                country_production=scraped_data.get('country_production'),
                unsold_management=scraped_data.get('unsold_management'),
                supply_chain_transparency=scraped_data.get('supply_chain_transparency'),
                global_env_impact=scraped_data.get('global_env_impact'),
                labor_ethics=scraped_data.get('labor_ethics'),
                final_score=scraped_data.get('final_score'),
                score_color=get_score_color(scraped_data.get('final_score')),
                score_label=get_score_label(scraped_data.get('final_score')),
                short_description=scraped_data.get('short_description'),
                description=scraped_data.get('description'),
                planet_badge=scraped_data.get('planet_badge', False),
                labor_badge=scraped_data.get('labor_badge', False),
            )
        
        # Si on n'a pas trouvé la marque et qu'on ne scrappe pas, retourner 404
        if not raw_doc and not auto_scrape:
            raise HTTPException(status_code=404, detail=f"Brand '{brand_name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la recherche/scraping de '{brand_name}': {e}")
        import traceback
        traceback.print_exc()
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
            
            # Normaliser les certifications
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            scores = calculate_scores(scraped_data)
            scraped_data.update(scores)
            
            # Normaliser à nouveau après le calcul des scores
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            await existing_brand.set(scraped_data)
            return to_out(existing_brand)
        else:
            # Créer une nouvelle marque
            scraped_data = await scrape_brand_data(brand_name, website)
            
            # Normaliser les certifications
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            scores = calculate_scores(scraped_data)
            scraped_data.update(scores)
            
            # Normaliser à nouveau après le calcul des scores
            scraped_data['certifications'] = normalize_certifications(scraped_data.get('certifications'))
            
            brand = Brand(**scraped_data)
            await brand.insert()
            return to_out(brand)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping brand: {str(e)}")
