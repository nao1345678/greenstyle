import requests
from bs4 import BeautifulSoup
import re
import json 

brands_to_scrap = []

def get_brands(): 
    """
    Récupère les marques cibles, pour récuperer des informations sur celles-ci. 
    """
    with open("../ressources/jsons/brands.json", "r") as f:
        data = json.load(f)
        categories_list = data["brands_by_category"]

        for category_dict in categories_list:
            brand_list_for_category = category_dict["brands"]

            brands_to_scrap.extend(brand_list_for_category)

    print(f"Nombre total de marques extraites : {len(brands_to_scrap)}")
    print("\nListe des marques :")
    print(brands_to_scrap)

brands_to_scrap = get_brands()


def extract_problematic_terms(url, brands_to_scrap):
    """
    Récupère le contenu d'une URL et cherche des mentions de marques cibles
    associées à des mots-clés de critique (droits humains).

    :param url: L'URL de l'article ou du rapport de l'ONG.
    :param brands_to_scrap: Liste des marques à surveiller.
    :return: Un dictionnaire des marques mentionnées et un extrait de la critique.
    """
    mentions_critiques = {}

    critical_mentions = r"""(
    # FRANCAIS
    esclavage moderne | salaire vital non respecté | ouïghours | non-respect de la sécurité | Rana Plaza | Manque de transparence | 
    heures supplémentaires excessives | non-payées | opacité de la chaîne | travailleurs migrants | abus | abus verbaux | 
    violences physiques et sexuelles | précarité | travail forcé | exploitation | salaire de subsistance | conditions de travail | 
    ouvriers | sous-payé | droits bafoués | esclavage | enfants | mineurs | travail d'enfants |
    
    # ANGLAIS
    modern slavery | living wage not respected | Uighurs | safety violations | Rana Plaza | lack of transparency | 
    excessive overtime | unpaid wages | opacity of the supply chain | migrant workers | abuse | verbal abuse | 
    physical and sexual violence | precariousness | forced labor | exploitation | subsistence wage | working conditions | 
    labor rights | labor standards | labor laws | labor regulations | labor agreements | labor contracts | labor disputes | 
    workers | underpaid | rights violated | slavery | children | minors | child labor)"""

    try:
        # Requête HTTP avec User Agent pour ne pas être bloqué
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 

        # Analyse
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphes = soup.find_all(['p', 'li', 'h3', 'h2', 'h1'])

        for element in paragraphes:
            texte = element.get_text()
            
            # Chercher une marque ET un mot-clé de critique dans le même bloc de texte
            for marque in brands_to_scrap:
                if marque in texte:
                    if re.search(mots_cles_critique, texte, re.IGNORECASE):
                        # Stocker la marque et le paragraphe entier comme preuve/contexte
                        mentions_critiques[marque] = texte.strip()
                        
        return mentions_critiques

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion/requête sur {url}: {e}")
        return {}
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse : {e}")
        return {}

#  EXECUTION DU SCRIPT

# Ciblez des URL d'ONG ou d'articles de presse reprenant des rapports d'ONG
urls_a_scrapper = [
    "https://www.oxfamfrance.org/agir-oxfam/impact-de-la-mode-consequences-sociales-environnementales/", 
    "https://www.business-humanrights.org/en/latest-news/fast-fashion-et-seconde-main-un-jeu-de-dupes-r%C3%A9v%C3%A9l%C3%A9-par-des-trackeurs/",
    "https://disclose.ngo/fr/article/kiabi-shein-decathlon-la-fast-fashion-encaisse-des-millions-deuros-dargent-public-avec-le-don-de-vetements-invendus",
    
    # Ajouts ciblés sur les marques problématiques et les marques au contraire validées
    "http://ethique-sur-etiquette.org/IMG/pdf/rapport_salaire_vital_def.pdf", 
    "https://ethique-sur-etiquette.org/IMG/pdf/rapport_made_in_europe.pdf", 
    "https://www.fashionrevolution.org/fashion-transparency-index-2023/", 
    "https://thefairdude.fr/be-fair/fair-wear-foundation/", 
    "https://www.fairwear.org/", 
    "https://www.publiceye.ch/fr/thematiques/industrie-textile", 
    "https://labourbehindthelabel.org/campaigns/living-wage/", 
    "https://directory.goodonyou.eco",

    # Autres liens pertinents pour le contexte des droits humains
    "https://www.hrw.org/report/2019/12/18/fashions-next-trend/accelerating-supply-chain-transparency-apparel-and-footwear", 
    "https://www.zerowastefrance.org/mobilisation-de-la-coalition-stop-fast-fashion-10-tonnes-de-dechets-textiles-deposes-devant-le-senat-pour-ladoption-de-la-loi-anti-fast-fashion/",
]

resultats_finaux = {}

print("🔍 Démarrage du scraping des rapports d'ONG sur la Fast-Fashion...")
print("-" * 50)

for url in urls_a_scrapper:
    print(f"➡️ Traitement de l'URL : {url}")
    resultats_url = extract_problematic_terms(url, brands_to_scrap)
    
    if resultats_url:
        for marque, critique in resultats_url.items():
            if marque not in resultats_finaux:
                resultats_finaux[marque] = []
            
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