#!/usr/bin/env python3
"""
Configuration centralisée pour le projet de détection de marques
"""

import os
from pathlib import Path

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CACHE_DIR = PROJECT_ROOT / "cache"

# Créer les répertoires s'ils n'existent pas
for directory in [DATA_DIR, LOGS_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# Configuration du scraper
SCRAPER_CONFIG = {
    "default_delay": 1.0,  # Délai par défaut entre les requêtes
    "timeout": 30,  # Timeout pour les requêtes HTTP
    "max_retries": 3,  # Nombre maximum de tentatives
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
}

# Configuration des marques
BRANDS_CONFIG = {
    "database_file": PROJECT_ROOT / "brands_database.csv",
    "min_brand_length": 2,  # Longueur minimale pour considérer un mot comme marque
    "case_sensitive": False,  # Recherche insensible à la casse
    "fuzzy_match": True,  # Correspondance approximative
    "fuzzy_threshold": 0.8,  # Seuil de similarité pour la correspondance approximative
}

# Configuration du logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "brand_detector.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

# Configuration des tests
TEST_CONFIG = {
    "test_urls": [
        "https://httpbin.org/html",
        "https://example.com",
        "https://httpbin.org/json",
    ],
    "test_brands": [
        "nike", "adidas", "apple", "samsung", "microsoft",
        "google", "amazon", "facebook", "netflix", "spotify"
    ],
    "timeout": 10,  # Timeout pour les tests
}

# Configuration de l'API (si applicable)
API_CONFIG = {
    "base_url": "http://localhost:8000",
    "api_key": os.getenv("BRAND_API_KEY", ""),
    "rate_limit": 100,  # Requêtes par minute
    "timeout": 30,
}

# Configuration de la base de données
DATABASE_CONFIG = {
    "type": "csv",  # ou "sqlite", "postgresql", etc.
    "path": DATA_DIR / "brands.db",
    "backup_enabled": True,
    "backup_interval": 24 * 60 * 60,  # 24 heures en secondes
}

# Configuration des extensions
EXTENSION_CONFIG = {
    "chrome_manifest": PROJECT_ROOT / "brand_detector_extension.ts",
    "firefox_manifest": PROJECT_ROOT / "brand_detector_extension.ts",
    "build_dir": PROJECT_ROOT / "dist",
    "version": "1.0.0",
}

def get_config(section: str = None):
    """Récupère la configuration demandée."""
    if section is None:
        return {
            "scraper": SCRAPER_CONFIG,
            "brands": BRANDS_CONFIG,
            "logging": LOGGING_CONFIG,
            "test": TEST_CONFIG,
            "api": API_CONFIG,
            "database": DATABASE_CONFIG,
            "extension": EXTENSION_CONFIG,
        }
    
    configs = {
        "scraper": SCRAPER_CONFIG,
        "brands": BRANDS_CONFIG,
        "logging": LOGGING_CONFIG,
        "test": TEST_CONFIG,
        "api": API_CONFIG,
        "database": DATABASE_CONFIG,
        "extension": EXTENSION_CONFIG,
    }
    
    return configs.get(section, {})

def validate_config():
    """Valide la configuration."""
    errors = []
    
    # Vérifier que les fichiers de base existent
    if not BRANDS_CONFIG["database_file"].exists():
        errors.append(f"Fichier de base de données introuvable: {BRANDS_CONFIG['database_file']}")
    
    # Vérifier les permissions des répertoires
    for directory in [DATA_DIR, LOGS_DIR, CACHE_DIR]:
        if not os.access(directory, os.W_OK):
            errors.append(f"Pas de permission d'écriture sur: {directory}")
    
    return errors

if __name__ == "__main__":
    # Test de la configuration
    print("🔧 Test de la configuration...")
    errors = validate_config()
    
    if errors:
        print("❌ Erreurs de configuration:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration valide!")
        
    print(f"📁 Répertoire de données: {DATA_DIR}")
    print(f"📝 Répertoire de logs: {LOGS_DIR}")
    print(f"💾 Répertoire de cache: {CACHE_DIR}")
