"""
Base de données de fallback pour les marques engagées connues
Utilisée quand le scraping automatique ne trouve pas de données
"""
from typing import Dict, Optional

# Base de données de marques engagées avec données réelles
ENGAGED_BRANDS_DATA = {
    'veja': {
        'brand_name': 'veja',
        'sustainable_materials': 85.0,  # Caoutchouc naturel, coton bio, cuir écologique
        'certifications': 'Fair Trade, Organic Cotton, B-Corp',
        'country_production': 'Brazil',
        'country_origin': 'France',
        'unsold_management': 'Recyclage, Réparation',
        'supply_chain_transparency': 'Totale',
        'labor_ethics': 85,  # Bonnes conditions de travail au Brésil (sur 100)
        'description': 'Marque française de baskets éthiques produites au Brésil avec des matières durables',
    },
    'patagonia': {
        'brand_name': 'patagonia',
        'sustainable_materials': 90.0,
        'certifications': 'Fair Trade Certified, B-Corp, Organic',
        'country_production': 'USA, Fair Trade factories',
        'country_origin': 'USA',
        'unsold_management': 'Réparation, Réutilisation, Recyclage',
        'supply_chain_transparency': 'Très élevée',
        'labor_ethics': 90,  # (sur 100)
        'description': 'Leader en vêtements d\'extérieur durables et éthiques',
    },
    'reformation': {
        'brand_name': 'reformation',
        'sustainable_materials': 75.0,
        'certifications': 'B-Corp, Carbon Neutral',
        'country_production': 'USA, Local production',
        'country_origin': 'USA',
        'unsold_management': 'Réutilisation, Recyclage',
        'supply_chain_transparency': 'Élevée',
        'labor_ethics': 8.0,
        'description': 'Marque de mode durable avec production locale',
    },
    'everlane': {
        'brand_name': 'everlane',
        'sustainable_materials': 60.0,
        'certifications': 'B-Corp',
        'country_production': 'USA, Ethical factories',
        'country_origin': 'USA',
        'unsold_management': 'Donation, Recyclage',
        'supply_chain_transparency': 'Élevée',
        'labor_ethics': 75,  # (sur 100)
        'description': 'Marque transparente avec chaîne d\'approvisionnement éthique',
    },
    'allbirds': {
        'brand_name': 'allbirds',
        'sustainable_materials': 80.0,
        'certifications': 'B-Corp, Carbon Neutral',
        'country_production': 'New Zealand, USA',
        'country_origin': 'USA',
        'unsold_management': 'Réutilisation, Recyclage',
        'supply_chain_transparency': 'Élevée',
        'labor_ethics': 80,  # (sur 100)
        'description': 'Chaussures durables en laine et eucalyptus',
    },
    # Marques de fast fashion (scores faibles mais réalistes)
    'nike': {
        'brand_name': 'nike',
        'sustainable_materials': 25.0,  # Quelques initiatives mais limitées
        'certifications': 'Nike Grind, Move to Zero',
        'country_production': 'Vietnam, China, Indonesia',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage partiel, Donation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 55,  # Problèmes documentés dans la chaîne d'approvisionnement
        'description': 'Marque de sportswear avec initiatives durabilité limitées',
    },
    'adidas': {
        'brand_name': 'adidas',
        'sustainable_materials': 30.0,  # Parley Ocean Plastic, Primegreen
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Vietnam, China, Cambodia',
        'country_origin': 'Germany',
        'unsold_management': 'Recyclage, Donation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 60,  # Améliorations mais problèmes persistants
        'description': 'Marque de sportswear avec programmes durabilité',
    },
    'zara': {
        'brand_name': 'zara',
        'sustainable_materials': 20.0,  # Collection Join Life mais limitée
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Spain, Portugal, Morocco, Turkey, Bangladesh',
        'country_origin': 'Spain',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Faible',
        'labor_ethics': 45,  # Fast fashion, conditions de travail problématiques
        'description': 'Fast fashion avec initiatives durabilité limitées',
    },
    'h&m': {
        'brand_name': 'h&m',
        'sustainable_materials': 35.0,  # Conscious Collection
        'certifications': 'Better Cotton Initiative, GOTS',
        'country_production': 'Bangladesh, China, Turkey, India',
        'country_origin': 'Sweden',
        'unsold_management': 'Recyclage, Donation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 50,  # Améliorations mais modèle fast fashion
        'description': 'Fast fashion avec programmes durabilité',
    },
    'puma': {
        'brand_name': 'puma',
        'sustainable_materials': 28.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Vietnam, China, Indonesia',
        'country_origin': 'Germany',
        'unsold_management': 'Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 58,
        'description': 'Marque de sportswear',
    },
    'uniqlo': {
        'brand_name': 'uniqlo',
        'sustainable_materials': 22.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'China, Vietnam, Bangladesh',
        'country_origin': 'Japan',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 52,
        'description': 'Fast fashion japonaise',
    },
    'calvin klein': {
        'brand_name': 'calvin klein',
        'sustainable_materials': 15.0,
        'certifications': None,
        'country_production': 'China, Vietnam, Turkey',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Faible',
        'labor_ethics': 48,
        'description': 'Marque de mode premium',
    },
    'the north face': {
        'brand_name': 'the north face',
        'sustainable_materials': 40.0,  # The North Face Renewed
        'certifications': 'Bluesign, Responsible Down Standard',
        'country_production': 'Vietnam, China, Bangladesh',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage, Réparation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 65,  # Meilleur que fast fashion
        'description': 'Marque d\'équipement outdoor avec initiatives durabilité',
    },
    'ugg': {
        'brand_name': 'ugg',
        'sustainable_materials': 10.0,  # Peu d'initiatives
        'certifications': None,
        'country_production': 'China',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage limité',
        'supply_chain_transparency': 'Faible',
        'labor_ethics': 42,  # Production en Chine, transparence limitée
        'description': 'Marque de chaussures en laine',
    },
    'diesel': {
        'brand_name': 'diesel',
        'sustainable_materials': 18.0,  # Quelques initiatives mais limitées
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Italy, Turkey, China',
        'country_origin': 'Italy',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 55,  # Mix de production (Italie + pays à risque)
        'description': 'Marque de denim et mode italienne',
    },
    'mango': {
        'brand_name': 'mango',
        'sustainable_materials': 28.0,  # Committed Collection
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Spain, Portugal, Morocco, Turkey, Bangladesh',
        'country_origin': 'Spain',
        'unsold_management': 'Recyclage, Donation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 52,  # Fast fashion avec quelques améliorations
        'description': 'Fast fashion espagnole avec initiatives durabilité',
    },
    'bershka': {
        'brand_name': 'bershka',
        'sustainable_materials': 15.0,  # Très limité
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Spain, Portugal, Morocco, Bangladesh',
        'country_origin': 'Spain',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Faible',
        'labor_ethics': 48,  # Fast fashion, transparence limitée
        'description': 'Fast fashion du groupe Inditex',
    },
    'pull & bear': {
        'brand_name': 'pull & bear',
        'sustainable_materials': 20.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Spain, Portugal, Morocco, Turkey',
        'country_origin': 'Spain',
        'unsold_management': 'Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 50,
        'description': 'Fast fashion du groupe Inditex',
    },
    'stradivarius': {
        'brand_name': 'stradivarius',
        'sustainable_materials': 18.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Spain, Portugal, Morocco, Turkey',
        'country_origin': 'Spain',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 50,
        'description': 'Fast fashion du groupe Inditex',
    },
    'cos': {
        'brand_name': 'cos',
        'sustainable_materials': 45.0,  # Meilleur que les autres marques H&M
        'certifications': 'Better Cotton Initiative, GOTS',
        'country_production': 'Europe, Turkey',
        'country_origin': 'Sweden',
        'unsold_management': 'Recyclage, Réutilisation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 62,  # Meilleur que H&M standard
        'description': 'Marque premium du groupe H&M avec meilleures pratiques',
    },
    '& other stories': {
        'brand_name': '& other stories',
        'sustainable_materials': 40.0,
        'certifications': 'Better Cotton Initiative, GOTS',
        'country_production': 'Europe, Turkey',
        'country_origin': 'Sweden',
        'unsold_management': 'Recyclage, Donation',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 60,
        'description': 'Marque premium du groupe H&M',
    },
    'new balance': {
        'brand_name': 'new balance',
        'sustainable_materials': 35.0,  # Quelques initiatives
        'certifications': 'Better Cotton Initiative',
        'country_production': 'USA, UK, China, Vietnam',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 58,
        'description': 'Marque de chaussures de sport',
    },
    'asics': {
        'brand_name': 'asics',
        'sustainable_materials': 32.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'Japan, China, Vietnam',
        'country_origin': 'Japan',
        'unsold_management': 'Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 60,
        'description': 'Marque de chaussures de sport japonaise',
    },
    'under armour': {
        'brand_name': 'under armour',
        'sustainable_materials': 25.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'USA, China, Vietnam',
        'country_origin': 'USA',
        'unsold_management': 'Recyclage partiel',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 56,
        'description': 'Marque de sportswear',
    },
    'dr martens': {
        'brand_name': 'dr martens',
        'sustainable_materials': 22.0,
        'certifications': 'Leather Working Group',
        'country_production': 'UK, Thailand, China',
        'country_origin': 'UK',
        'unsold_management': 'Réparation, Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 62,  # Bonne réputation pour la durabilité
        'description': 'Marque de chaussures durables',
    },
    'birkenstock': {
        'brand_name': 'birkenstock',
        'sustainable_materials': 30.0,
        'certifications': 'Leather Working Group',
        'country_production': 'Germany, Portugal',
        'country_origin': 'Germany',
        'unsold_management': 'Réparation, Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 68,  # Production européenne, bonne qualité
        'description': 'Marque de sandales durables',
    },
    'clarks': {
        'brand_name': 'clarks',
        'sustainable_materials': 28.0,
        'certifications': 'Better Cotton Initiative',
        'country_production': 'UK, India, Vietnam, China',
        'country_origin': 'UK',
        'unsold_management': 'Recyclage',
        'supply_chain_transparency': 'Modérée',
        'labor_ethics': 58,
        'description': 'Marque de chaussures britannique',
    },
}


def get_fallback_brand_data(brand_name: str) -> Optional[Dict]:
    """
    Retourne les données de fallback pour une marque engagée connue
    
    Args:
        brand_name: Nom de la marque (insensible à la casse)
    
    Returns:
        Dictionnaire avec les données ou None si non trouvée
    """
    # Normaliser le nom : minuscules, supprimer espaces, caractères spéciaux
    import re
    brand_normalized = re.sub(r'[^a-z0-9]', '', brand_name.lower().strip())
    
    # Chercher d'abord avec le nom exact (avec caractères spéciaux)
    brand_lower = brand_name.lower().strip()
    if brand_lower in ENGAGED_BRANDS_DATA:
        return ENGAGED_BRANDS_DATA.get(brand_lower)
    
    # Chercher avec le nom normalisé (sans caractères spéciaux)
    for key in ENGAGED_BRANDS_DATA.keys():
        key_normalized = re.sub(r'[^a-z0-9]', '', key.lower().strip())
        if brand_normalized == key_normalized:
            return ENGAGED_BRANDS_DATA.get(key)
    
    return None

