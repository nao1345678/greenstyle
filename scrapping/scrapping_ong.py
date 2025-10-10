import requests
from bs4 import BeautifulSoup
import re

MARQUES_CIBLES = [
    "Shein", "Zara", "H&M", "Primark", "Boohoo", 
    "Forever 21", "Fashion Nova", "C&A", "PrettyLittleThing", 
    "Topshop", "Mango", "Uniqlo"
]

def extraire_mentions_critiques(url, marques_cibles):
    """
    Récupère le contenu d'une URL et cherche des mentions de marques cibles
    associées à des mots-clés de critique (droits humains).

    :param url: L'URL de l'article ou du rapport de l'ONG.
    :param marques_cibles: Liste des marques à surveiller.
    :return: Un dictionnaire des marques mentionnées et un extrait de la critique.
    """
    mentions_critiques = {}

    # Mots-clés pour identifier les problèmes de droits humains/sociaux
    mots_cles_critique = r"(travail forcé|exploitation|salaire de subsistance|conditions de travail|Rana Plaza|ouvriers|sous-payé|droits bafoués)"
    
    try:
        # 1. Requête HTTP (avec un User-Agent pour éviter d'être bloqué)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP

        # 2. Analyse du contenu
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cibler le texte principal du corps de l'article (à ajuster selon le site)
        # On cherche souvent dans les balises <p> (paragraphes)
        paragraphes = soup.find_all(['p', 'li', 'h3'])

        for element in paragraphes:
            texte = element.get_text()
            
            # Chercher une marque ET un mot-clé de critique dans le même bloc de texte
            for marque in marques_cibles:
                if marque in texte:
                    # Trouver si un mot-clé de critique est proche de la marque
                    if re.search(mots_cles_critique, texte, re.IGNORECASE):
                        # Stocker la marque et le paragraphe entier comme preuve/contexte
                        mentions_critiques[marque] = texte.strip()
                        
        return mentions_critiques

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion/requête sur {url}: {e}")
        return {}
    except Exception as e:
        print(f"⚠️ Une erreur s'est produite lors de l'analyse : {e}")
        return {}

# --- Utilisation du Script ---

# Ciblez des URL d'ONG ou d'articles de presse reprenant des rapports d'ONG
urls_a_scrapper = [
    "https://www.oxfamfrance.org/agir-oxfam/impact-de-la-mode-consequences-sociales-environnementales/", # Oxfam - Impact de la mode
    "https://www.business-humanrights.org/en/latest-news/fast-fashion-et-seconde-main-un-jeu-de-dupes-r%C3%A9v%C3%A9l%C3%A9-par-des-trackeurs/", # Rapport d'ONG sur H&M, Zara, etc.
    "https://disclose.ngo/fr/article/kiabi-shein-decathlon-la-fast-fashion-encaisse-des-millions-deuros-dargent-public-avec-le-don-de-vetements-invendus", # Enquête Disclose sur les pratiques
    # Ajoutez des URL de la Clean Clothes Campaign ou du Collectif Éthique sur l'étiquette ici si vous en trouvez de pertinentes
]

resultats_finaux = {}

print("🔍 Démarrage du scraping des rapports d'ONG sur la Fast-Fashion...")
print("-" * 50)

for url in urls_a_scrapper:
    print(f"➡️ Traitement de l'URL : {url}")
    resultats_url = extraire_mentions_critiques(url, MARQUES_CIBLES)
    
    if resultats_url:
        for marque, critique in resultats_url.items():
            if marque not in resultats_finaux:
                resultats_finaux[marque] = []
            
            # Limiter le snippet à 150 caractères pour la clarté
            snippet = critique[:150] + "..." if len(critique) > 150 else critique
            resultats_finaux[marque].append({"source": url, "extrait": snippet})
        
        print(f"✅ Marques identifiées dans cette source : {', '.join(resultats_url.keys())}")
    else:
        print("— Aucune mention de marque critique trouvée avec les mots-clés/sélecteurs actuels.")

print("\n" + "=" * 50)
print("🛑 **SYNTHÈSE FINALE : MARQUES CRITIQUÉES POUR LES DROITS HUMAINS** 🛑")
print("=" * 50)

if resultats_finaux:
    for marque, details in resultats_finaux.items():
        print(f"\n### 🚨 {marque.upper()}")
        print(f"Trouvé dans **{len(details)}** rapport(s) ou article(s).")
        for detail in details:
            print(f"> Source : {detail['source']}")
            print(f"> Extrait : \"{detail['extrait']}\"")
else:
    print("Aucune marque de fast-fashion n'a été clairement signalée dans les URL testées avec les mots-clés de critique.")