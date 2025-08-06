#!/usr/bin/env python3
"""
Serveur API Flask pour le projet de détection de marques
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import time
from datetime import datetime
from typing import Dict, Any, List
import json

from brand_scraper import BrandScraper
from config import get_config
from utils import setup_logging, save_results_to_json, validate_brand_name

# Configuration
app = Flask(__name__)
CORS(app)  # Permettre les requêtes CORS

# Configuration
config = get_config()
logger = setup_logging("api_server", "INFO")

# Instance globale du scraper
scraper = None

def init_scraper():
    """Initialise le scraper global."""
    global scraper
    try:
        scraper = BrandScraper()
        logger.info("✅ Scraper initialisé avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation du scraper: {e}")
        scraper = None

@app.route('/health', methods=['GET'])
def health_check():
    """Point de terminaison pour vérifier la santé de l'API."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scraper_ready": scraper is not None,
        "version": "1.0.0"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """Analyse une URL pour détecter les marques."""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "URL manquante dans la requête",
                "status": "error"
            }), 400
        
        url = data['url']
        delay = data.get('delay', config['scraper']['default_delay'])
        verbose = data.get('verbose', False)
        
        logger.info(f"🔍 Analyse de l'URL: {url}")
        
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        # Analyser l'URL
        start_time = time.time()
        results = scraper.analyze_page(url, delay=delay, verbose=verbose)
        duration = time.time() - start_time
        
        # Ajouter des métadonnées
        results['api_metadata'] = {
            'request_timestamp': datetime.now().isoformat(),
            'processing_time': duration,
            'url_analyzed': url
        }
        
        logger.info(f"✅ Analyse terminée en {duration:.2f}s - {results.get('total_brands_found', 0)} marques trouvées")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Récupère la liste des marques disponibles."""
    try:
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        brands = list(scraper.brands)
        return jsonify({
            "brands": brands,
            "total_count": len(brands),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des marques: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/brands', methods=['POST'])
def add_brand():
    """Ajoute une nouvelle marque à la base de données."""
    try:
        data = request.get_json()
        
        if not data or 'brand' not in data:
            return jsonify({
                "error": "Nom de marque manquant",
                "status": "error"
            }), 400
        
        brand = data['brand'].strip()
        
        if not validate_brand_name(brand):
            return jsonify({
                "error": "Nom de marque invalide",
                "status": "error"
            }), 400
        
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        # Ajouter la marque
        scraper.brands.add(brand.lower())
        
        logger.info(f"✅ Marque ajoutée: {brand}")
        
        return jsonify({
            "message": f"Marque '{brand}' ajoutée avec succès",
            "brand": brand,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout de marque: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/brands/<brand>', methods=['DELETE'])
def remove_brand(brand):
    """Supprime une marque de la base de données."""
    try:
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        brand_lower = brand.lower()
        
        if brand_lower not in scraper.brands:
            return jsonify({
                "error": f"Marque '{brand}' non trouvée",
                "status": "error"
            }), 404
        
        # Supprimer la marque
        scraper.brands.remove(brand_lower)
        
        logger.info(f"✅ Marque supprimée: {brand}")
        
        return jsonify({
            "message": f"Marque '{brand}' supprimée avec succès",
            "brand": brand,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la suppression de marque: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    """Analyse plusieurs URLs en lot."""
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                "error": "Liste d'URLs manquante",
                "status": "error"
            }), 400
        
        urls = data['urls']
        delay = data.get('delay', config['scraper']['default_delay'])
        
        if not isinstance(urls, list):
            return jsonify({
                "error": "URLs doit être une liste",
                "status": "error"
            }), 400
        
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        logger.info(f"🔍 Analyse en lot de {len(urls)} URLs")
        
        results = []
        start_time = time.time()
        
        for i, url in enumerate(urls):
            try:
                logger.info(f"📊 Progression: {i+1}/{len(urls)} - {url}")
                
                result = scraper.analyze_page(url, delay=delay)
                result['url'] = url
                results.append(result)
                
            except Exception as e:
                logger.error(f"❌ Erreur pour l'URL {url}: {e}")
                results.append({
                    "url": url,
                    "error": str(e),
                    "total_brands_found": 0,
                    "brands": []
                })
        
        duration = time.time() - start_time
        
        # Statistiques globales
        total_brands = sum(r.get('total_brands_found', 0) for r in results)
        successful_analyses = len([r for r in results if 'error' not in r])
        
        batch_result = {
            "batch_metadata": {
                "total_urls": len(urls),
                "successful_analyses": successful_analyses,
                "failed_analyses": len(urls) - successful_analyses,
                "total_brands_found": total_brands,
                "processing_time": duration,
                "timestamp": datetime.now().isoformat()
            },
            "results": results,
            "status": "success"
        }
        
        logger.info(f"✅ Analyse en lot terminée: {successful_analyses}/{len(urls)} réussies")
        
        return jsonify(batch_result)
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse en lot: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques de l'API."""
    try:
        if not scraper:
            return jsonify({
                "error": "Scraper non initialisé",
                "status": "error"
            }), 500
        
        stats = {
            "total_brands": len(scraper.brands),
            "api_uptime": datetime.now().isoformat(),
            "version": "1.0.0",
            "config": {
                "default_delay": config['scraper']['default_delay'],
                "timeout": config['scraper']['timeout'],
                "max_retries": config['scraper']['max_retries']
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des stats: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404."""
    return jsonify({
        "error": "Endpoint non trouvé",
        "status": "error"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500."""
    return jsonify({
        "error": "Erreur interne du serveur",
        "status": "error"
    }), 500

def main():
    """Point d'entrée principal."""
    # Initialiser le scraper
    init_scraper()
    
    if not scraper:
        logger.error("❌ Impossible d'initialiser le scraper. Arrêt du serveur.")
        return
    
    # Configuration du serveur
    host = config.get('api', {}).get('host', '0.0.0.0')
    port = config.get('api', {}).get('port', 5000)
    debug = config.get('api', {}).get('debug', False)
    
    logger.info(f"🚀 Démarrage du serveur API sur {host}:{port}")
    logger.info(f"📊 Mode debug: {debug}")
    
    # Démarrer le serveur
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == "__main__":
    main()
