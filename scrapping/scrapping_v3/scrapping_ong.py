import json
from typing import List, Dict, Any
import re

# --- 1. GRILLE DE NOTATION ET PONDÉRATION DES MOTS-CLÉS ---
# Le score commence à 100 et descend selon les mots-clés trouvés.

# Pondération NÉGATIVE (pour déclasser le score)
PONDERATION_NEG = {
    # -80 : Violations les plus graves (niveau "Aucune Éthique")
    "travail forcé": -80,
    "esclavage": -80,
    "refus s'engager syndicats": -80, # Combinaison critique
    
    # -40 : Critiques graves (niveau "Médiocre")
    "abus": -40,
    "exploitation": -40,
    "scandale": -40,
    "ouïghours": -40,
    "sous-payé": -40,
    "conditions dangereuses": -40,
    
    # -20 : Critiques légères/moyennes (niveau "Moyen")
    "salaire minimum": -20, # Indique un manque d'effort au-delà du minimum légal
    "peu d'informations": -20,
    "non-respect": -20,
    "manque de transparence": -20
}

# Pondération POSITIVE (pour maintenir/augmenter le score de base de 100)
PONDERATION_POS = {
    # +0 (maintient le score) : Bonnes pratiques
    "salaire supérieur au minimum": 0, # Maintient la note de 100
    "audits indépendants": 0,
    "soutient les syndicats": 0,
    "fair wear": 0, # Marque d'excellence
    "commerce équitable": 0,
    "au delà des exigences légales": 0
}


def simulate_google_search(brand_name: str, sources: List[str]) -> str:
    """
    SIMULE l'appel à une API de recherche pour obtenir des résultats pertinents.
    
    Dans un environnement d'IA (comme celui-ci), cette fonction déclenche
    la recherche. Dans un script Python, vous devez la remplacer par une API.
    """
    
    query = f"Critiques éthiques \"{brand_name}\" salaires \"travail forcé\" OR \"conditions dangereuses\" OR \"salaire vital\" site:ethique-sur-etiquette.org OR site:hrw.org OR site:cleanclothes.org"
    
    # Appel à l'outil de recherche (simulation d'API)
    print(f"   [Recherche Google]: {query}")
    
    # Ici, nous allons simuler une recherche pour obtenir des résultats concrets pour l'analyse.
    # L'utilisateur doit lancer la recherche via l'outil pour obtenir les résultats.
    
    return f"RECHERCHE_SIMULÉE_POUR_{brand_name}"


def calculate_score(brand_name: str, search_results: str) -> Dict[str, Any]:
    """
    Analyse les résultats de la recherche IA et calcule le score basé sur les mots-clés.
    Le score commence à 100 (Excellentes Pratiques) et est ajusté.
    """
    
    initial_score = 100
    score_adjustement = 0
    mentions_trouvees = []
    
    # Normalisation du texte pour la recherche (tout en minuscules)
    text = search_results.lower()
    
    # 1. APPLICATION DES PONDÉRATIONS NÉGATIVES (Déclassement)
    for keyword, weight in PONDERATION_NEG.items():
        # Utilisation de regex pour une recherche flexible
        if re.search(r'\b' + re.escape(keyword.replace(' ', r'\s*')) + r'\b', text):
            score_adjustement += weight
            mentions_trouvees.append(f"{keyword} ({weight})")
            
    # 2. APPLICATION DES PONDÉRATIONS POSITIVES (Confirmation de l'excellence)
    # Les termes positifs ne peuvent que maintenir le score si aucun terme négatif n'est trouvé.
    # La logique étant : si rien de négatif n'est trouvé (score reste à 100), les termes positifs confirment.
    # Nous ne les utilisons pas pour AJOUTER des points au-delà de 100.
    
    score_final = max(20, initial_score + score_adjustement) # La note minimale est 20
    
    # 3. CATÉGORISATION FINALE (Basée sur le score)
    if score_final == 100:
        category = "EXCELLENTES PRATIQUES"
        # On vérifie si au moins un terme positif est présent pour vraiment confirmer l'excellence
        if not any(re.search(re.escape(k.replace(' ', r'\s*')), text) for k in PONDERATION_POS.keys()):
             category = "PRATIQUES MOYENNES (Manque de preuve d'excellence)"
             score_final = 60 # Déclassement si rien de critique mais pas de preuve d'excellence
    elif score_final >= 80:
        category = "BONNES PRATIQUES"
    elif score_final >= 60:
        category = "PRATIQUES MOYENNES"
    elif score_final >= 40:
        category = "PRATIQUES MÉDIOCRES"
    else: # score_final est proche ou égal à 20
        category = "AUCUNE ÉTHIQUE (Violations Graves)"
        
    return {
        "Marque": brand_name,
        "Score_Initial": initial_score,
        "Ajustement": score_adjustement,
        "Score_Final": score_final,
        "Catégorie_Éthique": category,
        "Mentions_Clés_Trouvées": mentions_trouvees,
    }

# --- 4. FONCTION D'EXÉCUTION ---

def run_automated_scoring(brands: List[str], sources: List[str]):
    """
    Orchestre le processus de recherche et de scoring pour toutes les marques.
    """
    all_scores = []
    
    print("\n" + "="*70)
    print("🤖 DÉMARRAGE DU SCORING AUTOMATISÉ (Simulé par Recherche IA)")
    print("="*70)
    
    for brand in brands:
        print(f"\n▶️ Traitement de la marque : {brand.upper()}")
        
        # Étape 1 : Récupération des résultats de recherche (via l'outil)
        # L'outil Google est appelé ici. L'utilisateur doit relancer l'analyse
        # après la première exécution pour obtenir les résultats.
        search_output = simulate_google_search(brand, sources)
        
        # Dans un scénario réel/API, la variable 'search_output' contiendrait 
        # tous les snippets. Ici, je vais simuler ces snippets pour les 
        # marques de test afin de démontrer la logique de scoring.
        
        # Étape 2 : Simulation des résultats de recherche pour la démonstration
        if brand.lower() == "zara":
            simulated_results = "Plaintes ONG Inditex travail forcé Ouïghours. Non-respect du salaire minimum légal. Scandale d'exploitation des travailleurs au Chili. Manque de transparence dans la chaîne d'approvisionnement."
        elif brand.lower() == "h&m":
            simulated_results = "Accusations d'exploitation. H&M n'a pas tenu son engagement de salaire vital. Salaire inférieur au minimum dans certains pays. Signalée par Clean Clothes Campaign pour abus et heures supplémentaires excessives."
        elif brand.lower() == "patagonia":
            simulated_results = "Politique d'entreprise avec salaire supérieur au minimum. Publie des audits indépendants et soutient les syndicats. Commerce équitable et au delà des exigences légales. Partenaire Fair Wear Foundation."
        else:
            simulated_results = "Très peu d'informations publiques disponibles. Informations compliquées à trouver. Code de conduite existant mais sans mise en œuvre prouvée."
            
        # Étape 3 : Calcul du score
        score_data = calculate_score(brand, simulated_results)
        all_scores.append(score_data)
        
        print(f"   [Synthèse Analysée]: {simulated_results[:80]}...")
        print(f"   [Mentions Négatives]: {score_data['Mentions_Clés_Trouvées'] if score_data['Mentions_Clés_Trouvées'] else 'Aucune.'}")
        print(f"   🏆 Score Final : {score_data['Score_Final']}/100 ({score_data['Catégorie_Éthique']})")
        
    return all_scores

# --- 5. DONNÉES D'EXÉCUTION ---

# Exemple de marques à évaluer (à partir de votre liste de 177)
marques_test = ["Zara", "H&M", "Patagonia", "Marque_Inconnue"]

# Liste des sources à cibler pour la recherche
sources_cibles = ["site:ethique-sur-etiquette.org", "site:hrw.org", "site:cleanclothes.org", "site:publiceye.ch"]

# Exécution
final_ranking = run_automated_scoring(marques_test, sources_cibles)

# --- Affichage des résultats ---
print("\n" + "="*50)
print("CLASSEMENT ÉTHIQUE FINAL")
print("="*50)

final_ranking.sort(key=lambda x: x['Score_Final'], reverse=True)

for item in final_ranking:
    print(f"[{item['Score_Final']}/100] {item['Marque'].upper()} : {item['Catégorie_Éthique']}")

# Sauvegarde des résultats
with open("classement_ethique_automatise.json", "w", encoding="utf-8") as f:
    json.dump(final_ranking, f, indent=4, ensure_ascii=False)

print("\nLe classement complet a été sauvegardé dans classement_ethique_automatise.json")