# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json 
import os
import io
from PyPDF2 import PdfReader
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from typing import List, Dict, Any

# Configuration globale pour stocker la liste des marques
BRANDS_TO_SCRAP = None
# Motif de tous les mots-clés critiques. Utilisé pour déterminer si un document est dénonciateur.
CRITICAL_KEYWORDS = r"""(esclavage|servitude|travail forcé|travail obligatoire|modern slavery|
forced labor|exploitation|sous-traitance abusive|travail d'enfants|enfants ouvriers|child labor|
child exploitation|mineurs exploités|salaire vital|salaire décent|living wage|sous-payé|mal payé|
faible rémunération|heures supplémentaires|overtime|temps de travail illégal|
non-respect des horaires|non-respect de la sécurité|conditions dangereuses|sécurité défaillante|Rana Plaza|
accidents de travail|safety violations|droits bafoués|abus|maltraitance|harcèlement|syndicat interdit|rights violated|
abuse|harassment|Manque de transparence|due diligence|chaines d'approvisionnement opaques|lack of transparency|
supply chain risks|Ouïghours|Uighurs|Xinjiang|Israel|Israël|Israeli|Israéliens|Palestiniens|Palestine|Gaza|
sous-remunere|underpaid|debt bondage|human trafficking|abusif|dangereux|non-conformité|
contrefaçon|non-respect des normes|prison labor|salaires impayés|wage theft|sweatshop|atelier de misère|
pauvreté extrême|extreme poverty|droit de s'organiser|liberté d'association|freedom of association|
discrimination|toxic|toxique|produits chimiques nocifs|dangereux pour la santé|violences)"""

def get_brands(): 
    """
    Récupère les marques cibles depuis le fichier JSON.
    """
    global BRANDS_TO_SCRAP
    brands_list = []
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
        
    file_path = "../ressources/jsons/brands.json"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            brands_list = [brand.lower() for category in data["brands_by_category"] for brand in category["brands"]]
            brands_list = [b for b in brands_list if len(b) >= 3 or '&' in b]
            
            # DEBUG: Afficher quelques marques pour vérification
            print(f"DEBUG: Exemples de marques dans la liste: {brands_list[:20]}")
            
            BRANDS_TO_SCRAP = brands_list
            print(f"✅ Nombre total de marques extraites du JSON : {len(BRANDS_TO_SCRAP)}")
            return BRANDS_TO_SCRAP

    except Exception as e:
        print(f"❌ Erreur lors du chargement ou de l'analyse du JSON : {e}")
        return []

def get_text_from_url(url: str, response: requests.Response) -> str:
    """
    V8 : Extrait le texte COMPLET du document sous forme d'une seule chaîne
    en privilégiant l'extraction de blocs pour le HTML pour un texte plus propre.
    """
    content_type = response.headers.get('Content-Type', '').lower()
    full_text = ""
    
    if 'application/pdf' in content_type or url.endswith(".pdf"):
        # Traitement du PDF
        print("— Type de contenu détecté : PDF. Tentative d'extraction du texte.")
        try:
            pdf_file = io.BytesIO(response.content)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            
            return full_text
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du PDF avec PyPDF2 : {e}")
            return ""
    
    else:
        # Traitement du HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Supprime les scripts et styles pour le nettoyage
        for junk in soup(['script', 'style']):
            junk.decompose()
            
        # SÉLECTION DES BALISES DE CONTENU (pour un texte plus pertinent et structuré)
        paragraphes = soup.find_all([
            'p', 'li', 'h3', 'h2', 'h1', 'td', 'th', 'a', 'span', 'strong', 'em', 
            'figcaption', 'blockquote'
        ])
        
        # Concatène les blocs avec des espaces ou sauts de ligne (pour séparer les mots)
        text_blocks = [
            element.get_text(strip=True) 
            for element in paragraphes 
            if len(element.get_text(strip=True)) > 20 # Ignore les très petites chaînes
        ]
        
        return ' '.join(text_blocks)


def extract_problematic_terms(url: str, brands_list: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """
    V8 : Logique Document Critique Global / Maximum Recall.
    """
    critical_mentions = {}
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Encoding': 'identity'
        }
        response = requests.get(url, headers=headers, timeout=20) 
        response.raise_for_status() 

        # Étape 1 : Obtenir le texte COMPLET
        full_document_text = get_text_from_url(url, response)
        
        if not full_document_text:
            print("— Contenu non lisible ou vide.")
            return {}
            
        normalized_full_text = full_document_text.lower()

        # DEBUG pour l'article des 83 marques
        if "83-marques-esclave-ouighour" in url:
            print(f"DEBUG: Longueur du texte extrait: {len(full_document_text)}")
            print(f"DEBUG: Échantillon du texte: {full_document_text[:500]}...")
            
            # Test manuel sur quelques marques connues
            test_brands = ["nike", "adidas", "zara", "h&m", "gap", "uniqlo", "puma"]
            print("DEBUG: Test de présence de marques connues:")
            for brand in test_brands:
                if brand in normalized_full_text:
                    print(f"  ✅ {brand} TROUVÉ")
                else:
                    print(f"  ❌ {brand} NON TROUVÉ")

        # Étape 2 : Vérification du Marqueur de Dénonciation (sur le document entier)
        match_critique_global = re.search(CRITICAL_KEYWORDS, normalized_full_text, re.IGNORECASE)
        
        if not match_critique_global:
            print("— Document non jugé critique (aucun mot-clé majeur trouvé).")
            return {}
        
        # Mot-clé critique qui a validé le document comme "dénonciateur"
        mot_cle_de_critique_global = match_critique_global.group(1).strip()
        print(f"📍 Mot-clé critique détecté: '{mot_cle_de_critique_global}'")
        
        # Étape 3 : Extraction avec normalisation TRÈS flexible
        marques_trouvees = 0
        for marque in brands_list:
            # Nettoyer la marque (supprimer parenthèses et annotations)
            marque_clean = re.sub(r'\s*\([^)]*\)', '', marque).strip()
            
            # NOUVELLE APPROCHE : Recherche très flexible
            found = False
            
            # 1. Recherche simple dans le texte normalisé
            if marque_clean.lower() in normalized_full_text:
                found = True
            
            # 2. Recherche sans espaces
            elif marque_clean.replace(' ', '').lower() in normalized_full_text.replace(' ', ''):
                found = True
            
            # 3. Recherche avec variations communes pour &
            elif '&' in marque_clean:
                variants = [
                    marque_clean.replace('&', 'and'),
                    marque_clean.replace('&', ' and '),
                    marque_clean.replace('&', ''),
                    marque_clean.replace('&', ' ')
                ]
                for variant in variants:
                    if variant.lower() in normalized_full_text:
                        found = True
                        break
            
            # 4. Recherche par mots (pour les marques composées)
            elif ' ' in marque_clean:
                words = marque_clean.lower().split()
                if all(word in normalized_full_text for word in words):
                    found = True
            
            if found:
                marques_trouvees += 1
                if marque not in critical_mentions:
                    critical_mentions[marque] = []
                
                # Trouver la première occurrence de la marque pour un extrait contextuel
                first_brand_match = re.search(re.escape(marque_clean), full_document_text, re.IGNORECASE)
                if not first_brand_match:
                    # Recherche plus flexible pour l'extrait
                    first_brand_match = re.search(marque_clean.lower(), normalized_full_text)
                
                context_excerpt = "Marque citée dans le document dénonciateur."
                if first_brand_match:
                    start_index = first_brand_match.start()
                    context_start = max(0, start_index - 150)
                    context_end = min(len(full_document_text), start_index + 150)
                    context_excerpt = full_document_text[context_start:context_end].strip()

                mention = {
                    "source": url, 
                    "extrait": context_excerpt, 
                    "mot_cle": f"Cité dans un document critiquant {mot_cle_de_critique_global}" 
                }
                
                critical_mentions[marque].append(mention)
        
        # Debug pour l'article des 83 marques
        if "83-marques-esclave-ouighour" in url:
            print(f"DEBUG: {marques_trouvees} marques trouvées dans l'article des 83 marques")
                
        print(f"✅ {len(critical_mentions)} marques identifiées dans cette source DÉNONCIATRICE.")
        return critical_mentions

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion/requête sur {url}: {e}")
        return {}
    except Exception as e:
        print(f"❌ Une erreur s'est produite lors de l'analyse : {e}")
        return {}


def save_results_to_json(resultats_finaux: Dict[str, List[Dict[str, str]]], filename: str = "resultats_scraping_ong.json") -> str:
    """ Sauvegarde les résultats finaux en format JSON. """
    filepath = filename 
    try:
        data = {
            "metadata": {
                "date_generation": datetime.now().isoformat(),
                "nombre_marques_trouvees": len(resultats_finaux),
                "nombre_total_mentions": sum(len(details) for details in resultats_finaux.values())
            },
            "resultats": resultats_finaux
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Résultats sauvegardés en JSON : {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde JSON : {e}")
        return ""

def save_results_to_pdf(resultats_finaux: Dict[str, List[Dict[str, str]]], filename: str = "rapport_scraping_ong.pdf") -> str:
    """ Génère un rapport PDF des résultats finaux. """
    
    filepath = filename
    
    try:
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Title'], fontSize=16, spaceAfter=30, leading=20
        )
        heading_style = ParagraphStyle(
            'CustomHeading', parent=styles['Heading2'], fontSize=14, spaceAfter=12
        )
        
        story = []
        
        # Titre du rapport
        story.append(Paragraph("🛑 RAPPORT : MARQUES CRITIQUÉES POUR LES DROITS HUMAINS 🛑", title_style))
        story.append(Paragraph(f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Résumé
        story.append(Paragraph("📊 RÉSUMÉ EXÉCUTIF", heading_style))
        story.append(Paragraph(f"• Nombre de marques identifiées : {len(resultats_finaux)}", styles['Normal']))
        total_mentions = sum(len(details) for details in resultats_finaux.values())
        story.append(Paragraph(f"• Nombre total de mentions critiques : {total_mentions}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        if resultats_finaux:
            story.append(Paragraph("📋 DÉTAILS PAR MARQUE", heading_style))
            
            for marque, details in resultats_finaux.items():
                story.append(Paragraph(f"🚨 {marque.upper()}", heading_style))
                story.append(Paragraph(f"Trouvé dans {len(details)} mention(s) critique(s).", styles['Normal']))
                
                for i, detail in enumerate(details, 1):
                    story.append(Paragraph(f"<br/><b>Mention {i}:</b>", styles['Normal']))
                    story.append(Paragraph(f"• <b>Motif de critique :</b> {detail['mot_cle'].strip()}", styles['Normal']))
                    story.append(Paragraph(f"• <b>Source :</b> <font color='blue'>{detail['source']}</font>", styles['Normal']))
                    
                    # Préparation de l'extrait
                    extracted_text = detail['extrait']
                    
                    # Mise en évidence (HTML pour ReportLab)
                    marque_display = marque.upper()
                    # Mettre la marque en gras
                    extracted_text = re.sub(re.escape(marque), f'<b>{marque_display}</b>', extracted_text, flags=re.IGNORECASE)
                    
                    # Limiter l'extrait pour le PDF
                    extrait_limite = extracted_text[:1200] + "..." if len(extracted_text) > 1200 else extracted_text
                    
                    story.append(Paragraph(f"• <b>Extrait :</b> {extrait_limite}", styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
                
                story.append(Spacer(1, 0.2*inch))
        else:
            story.append(Paragraph("Aucune marque n'a été clairement signalée dans les sources analysées.", styles['Normal']))
        
        # Construire le PDF
        doc.build(story)
        print(f"✅ Rapport PDF généré : {filepath}")
        return filepath
        
    except ImportError:
        print("❌ Pour générer un PDF, installez reportlab : pip install reportlab")
        return ""
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        return ""

# ==============================================================================
# EXECUTION DU SCRIPT
# ==============================================================================

# --- Initialisation des marques ---
get_brands()

if not BRANDS_TO_SCRAP:
    exit()

urls_a_scrapper = [
   "https://www.oxfamfrance.org/agir-oxfam/impact-de-la-mode-consequences-sociales-environnementales/", 
    "https://www.business-humanrights.org/en/latest-news/fast-fashion-et-seconde-main-un-jeu-de-dupes-r%C3%A9v%C3%A9l%C3%A9-par-des-trackeurs/",
    "https://disclose.ngo/fr/article/kiabi-shein-decathlon-la-fast-fashion-encaisse-des-millions-deuros-dargent-public-avec-le-don-de-vetements-invendus",
    
    # URLs PDF ciblées pour l'analyse
    "http://ethique-sur-etiquette.org/IMG/pdf/rapport_salaire_vital_def.pdf", 
    "https://ethique-sur-etiquette.org/IMG/pdf/rapport_made_in_europe.pdf", 
    "https://www.oxfamfrance.org/app/uploads/2022/03/Fast-Fashion-Impacts-alternatives-et-moyens-dagir.pdf",
    "https://www.librinfo74.fr/wp-content/uploads/2015/03/produits-à-boycotter.pdf",
    
    "https://www.fashionrevolution.org/fashion-transparency-index-2023/", 
    "https://thefairdude.fr/be-fair/fair-wear-foundation/", 
    "https://www.publiceye.ch/fr/thematiques/industrie-textile", 
    "https://labourbehindthelabel.org/campaigns/living-wage/", 
    "https://www.capital.fr/entreprises-marches/shein-epingle-pour-pollution-et-esclavage-moderne-1489612",
    "https://fr.fashionnetwork.com/news/Une-ong-pointe-ces-marques-qui-alimentent-l-esclavage-moderne-,296014.html",
    "https://adaptationmagazine.com/entendre/83-marques-esclave-ouighour", # La cible principale pour la liste des 83 marques
    "https://www.hrw.org/report/2019/12/18/fashions-next-trend/accelerating-supply-chain-transparency-apparel-and-footwear", 
    "https://www.zerowastefrance.org/mobilisation-de-la-coalition-stop-fast-fashion-10-tonnes-de-dechets-textiles-deposes-devant-le-senat-pour-ladoption-de-la-loi-anti-fast-fashion/",
]

resultats_finaux = {}

print("\n" + "🔍 Démarrage du scraping des rapports d'ONG (V8 : Maximum Recall)...")
print("-" * 50)

for url in urls_a_scrapper:
    print(f"➡️ Traitement de l'URL : {url}")
    resultats_url = extract_problematic_terms(url, BRANDS_TO_SCRAP)
    
    # Fusionner les résultats dans la synthèse finale
    if resultats_url:
        for marque, details in resultats_url.items():
            if marque not in resultats_finaux:
                resultats_finaux[marque] = []
            
            # Nous n'ajoutons que la première mention par URL, car la critique est globale au document
            if not any(d['source'] == url for d in resultats_finaux[marque]):
                 resultats_finaux[marque].extend(details)
        
        print(f"✅ {len(resultats_url)} marques identifiées dans cette source DÉNONCIATRICE.")
    else:
        print("— Document non pertinent (pas assez de mots-clés critiques trouvés) ou aucune de vos marques citée.")

print("\n" + "=" * 50)
print(f"🛑 SYNTHÈSE FINALE : {len(resultats_finaux)} MARQUES CRITIQUÉES 🛑")
print("=" * 50)

if resultats_finaux:
    for marque, details in resultats_finaux.items():
        # Affichage synthétique final
        sources_uniques = set([d['source'] for d in details])
        print(f"### 🚨 {marque.upper()} : Trouvé dans {len(details)} mention(s) / {len(sources_uniques)} source(s) différente(s).")
        
    # Génération des fichiers de sortie
    print("\n" + "=" * 50)
    print("📄 GÉNÉRATION DES RAPPORTS")
    print("=" * 50)
    
    # Sauvegarder en JSON
    save_results_to_json(resultats_finaux)
    
    # Sauvegarder en PDF
    save_results_to_pdf(resultats_finaux)
    
else:
    print("Aucune marque n'a été clairement signalée dans les URL testées.")
