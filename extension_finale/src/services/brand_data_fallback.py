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
        'labor_ethics': 8.0,
        'description': 'Chaussures durables en laine et eucalyptus',
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
    brand_lower = brand_name.lower().strip()
    return ENGAGED_BRANDS_DATA.get(brand_lower)

