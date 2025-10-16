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

# Configuration
BRANDS_TO_SCRAP = None

def get_brands(): 
    """
    Récupère les marques cibles depuis le fichier JSON.
    (La logique est inchangée et est bonne pour la préparation)
    """
    global BRANDS_TO_SCRAP
    brands_list = []
    
    # Chemin présumé du JSON
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
        
    file_path = os.path.join(base_dir, "../ressources/jsons/brands.json")
    
    if not os.path.exists(file_path):
        print(f"Erreur: Le fichier brands.json n'a pas été trouvé à l'emplacement: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            brands_list = [brand.lower() for category in data["brands_by_category"] for brand in category["brands"]]
            brands_list = [b for b in brands_list if len(b) >= 3 or '&' in b]
            
    except Exception as e:
        print(f"Erreur lors du chargement ou de l'analyse du JSON : {e}")
        return []

    BRANDS_TO_SCRAP = brands_list
    print(f"Nombre total de marques extraites : {len(BRANDS_TO_SCRAP)}")
    print("\nListe des marques (extrait, en minuscules) :")
    print(BRANDS_TO_SCRAP[:5] + ["..."] + BRANDS_TO_SCRAP[-5:]) 
    
    return BRANDS_TO_SCRAP


def get_text_from_url(url, response):
    """
    Extrait le texte d'une réponse HTTP, qu'il s'agisse de HTML ou de PDF.
    (La logique d'extraction est inchangée)
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
                # Ajout d'un espace pour faciliter la recherche de bornes de mots
                full_text += page.extract_text() + " "
            
            # Retourne le texte complet dans une liste pour une analyse globale/par ligne
            return full_text.split('\n')
        except Exception as e:
            print(f"Erreur lors de la lecture du PDF avec PyPDF2 : {e}")
            return []
    
    else:
        # Traitement du HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # SÉLECTION LARGE : On cible toutes les balises de contenu
        paragraphes = soup.find_all([
            'p', 'li', 'h3', 'h2', 'h1', 'td', 'th', 
            'a', 'span', 'strong', 'em', 'figcaption', 'blockquote'
        ])
        
        # Retourne une liste de blocs de texte
        return [
            element.get_text(strip=True) 
            for element in paragraphes 
            if len(element.get_text(strip=True)) > 20
        ]


def extract_problematic_terms(url, brands_list):
    """
    Récupère le contenu d'une URL et cherche des mentions de marques cibles
    associées à des mots-clés de critique DANS LE MÊME BLOC OU À PROXIMITÉ (100 caractères).
    """
    critical_mentions = {}
    
    # Motif de capture pour identifier quel mot critique a matché
    # REMARQUE : Ces mots-clés sont sensibles à la casse pour capturer la version originale.
    critical_keywords_pattern = r"(esclavage moderne|salaire vital|ouïghours|non-respect de la sécurité|Rana Plaza|Manque de transparence|heures supplémentaires|abus|travail forcé|exploitation|sous-payé|droits bafoués|travail d'enfants|modern slavery|living wage|Uighurs|safety violations|lack of transparency|excessive overtime|forced labor|exploitation|underpaid|rights violated|child labor)"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Encoding': 'identity'
        }
        response = requests.get(url, headers=headers, timeout=20) 
        response.raise_for_status() 

        text_blocks = get_text_from_url(url, response)
        
        # 1. Joindre tous les blocs de texte pour former le texte complet du document (nécessaire pour la recherche de proximité)
        full_document_text = ' '.join(text_blocks)
        normalized_full_text = full_document_text.lower()
        
        # 2. Chercher les occurrences de chaque marque dans le document complet
        for marque in brands_list:
            
            # Recherche de toutes les positions de la marque
            # (Note: la marque est en minuscules dans brands_list)
            # La regex est plus simple ici car on cherche dans le texte continu
            for match in re.finditer(re.escape(marque), normalized_full_text):
                start_index = match.start()
                end_index = match.end()
                
                # Définir la fenêtre de recherche de proximité (100 caractères avant/après)
                # On utilise le texte COMPLET (full_document_text)
                
                # La fenêtre de recherche inclut 10000 caractères avant le début et après la fin de la marque
                search_window_start = max(0, start_index - 10000)
                search_window_end = min(len(full_document_text), end_index + 10000)
                
                proximity_window = full_document_text[search_window_start:search_window_end]
                
                # 3. Chercher un mot-clé de critique dans la fenêtre de proximité (case-insensitive)
                match_critique = re.search(critical_keywords_pattern, proximity_window, re.IGNORECASE)
                
                if match_critique:
                    # Succès : Marque et mot-clé critique sont proches.
                    
                    # Récupérer le mot-clé exact et l'extrait pertinent
                    mot_cle_de_critique = match_critique.group(1).strip()
                    
                    if marque not in critical_mentions:
                        critical_mentions[marque] = []
                    
                    # Définir l'extrait comme la fenêtre de proximité pour le contexte
                    mention = {
                        "source": url, 
                        "extrait": proximity_window.strip(), # L'extrait est la fenêtre de 200+ caractères
                        "mot_cle": mot_cle_de_critique
                    }
                    
                    # Ajout de la mention si unique
                    if mention not in critical_mentions[marque]:
                        critical_mentions[marque].append(mention)
                        
        return critical_mentions

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion/requête sur {url}: {e}")
        return {}
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse : {e}")
        return {}

def save_results_to_json(resultats_finaux, filename="resultats_scraping_ong.json"):
    """
    Sauvegarde les résultats finaux en format JSON.
    """
    try:
        # Préparer les données avec métadonnées
        data = {
            "metadata": {
                "date_generation": datetime.now().isoformat(),
                "nombre_marques_trouvees": len(resultats_finaux),
                "nombre_total_mentions": sum(len(details) for details in resultats_finaux.values())
            },
            "resultats": resultats_finaux
        }
        
        # Sauvegarder dans le répertoire du script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Résultats sauvegardés en JSON : {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde JSON : {e}")
        return None

def save_results_to_pdf(resultats_finaux, filename="rapport_scraping_ong.pdf"):
    """
    Génère un rapport PDF des résultats finaux.
    """
    try:
        # Installer reportlab si nécessaire : pip install reportlab
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            spaceAfter=30,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
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
                # Nom de la marque
                story.append(Paragraph(f"🚨 {marque.upper()}", heading_style))
                story.append(Paragraph(f"Trouvé dans {len(details)} mention(s) critique(s).", styles['Normal']))
                
                for i, detail in enumerate(details, 1):
                    story.append(Paragraph(f"<b>Mention {i}:</b>", styles['Normal']))
                    story.append(Paragraph(f"• <b>Mot-clé critique :</b> {detail['mot_cle'].strip()}", styles['Normal']))
                    story.append(Paragraph(f"• <b>Source :</b> {detail['source']}", styles['Normal']))
                    
                    # Limiter l'extrait pour le PDF
                    extrait_limite = detail['extrait'][:800] + "..." if len(detail['extrait']) > 800 else detail['extrait']
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
        return None
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        return None

#  EXECUTION DU SCRIPT (inchangée)

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
    "https://www.fairwear.org/", 
    "https://www.publiceye.ch/fr/thematiques/industrie-textile", 
    "https://labourbehindthelabel.org/campaigns/living-wage/", 
    "https://directory.goodonyou.eco",
    "https://www.aspi.org.au/report/uyghurs-sale",
    "https://www.hrw.org/report/2019/12/18/fashions-next-trend/accelerating-supply-chain-transparency-apparel-and-footwear", 
    "https://www.zerowastefrance.org/mobilisation-de-la-coalition-stop-fast-fashion-10-tonnes-de-dechets-textiles-deposes-devant-le-senat-pour-ladoption-de-la-loi-anti-fast-fashion/",
]

resultats_finaux = {}

print("\n" + "🔍 Démarrage du scraping des rapports d'ONG (V4 : Recherche par Proximité 20000 caractères)...")
print("-" * 50)

for url in urls_a_scrapper:
    print(f"➡️ Traitement de l'URL : {url}")
    resultats_url = extract_problematic_terms(url, BRANDS_TO_SCRAP)
    
    # Fusionner les résultats dans la synthèse finale
    if resultats_url:
        for marque, details in resultats_url.items():
            if marque not in resultats_finaux:
                resultats_finaux[marque] = []
            
            resultats_finaux[marque].extend(details) 
        
        print(f"✅ Marques identifiées dans cette source : {', '.join(resultats_url.keys())}")
    else:
        print("— Aucune mention de marque critique trouvée à proximité (20000 caractères).")

print("\n" + "=" * 50)
print("🛑 **SYNTHÈSE FINALE : MARQUES CRITIQUÉES POUR LES DROITS HUMAINS** 🛑")
print("=" * 50)

if resultats_finaux:
    for marque, details in resultats_finaux.items():
        print(f"\n### 🚨 {marque.upper()}")
        print(f"Trouvé dans **{len(details)}** mention(s) critique(s).")
        for detail in details:
            print(f"> **Mot-clé critique :** {detail['mot_cle'].strip()}")
            print(f"> Source : {detail['source']}")
            print(f"> **Extrait (Proximité de la mention) :**")
            # Mise en évidence de la marque et du mot-clé
            extracted_text = detail['extrait']
            
            # Mettre la marque en gras
            marque_display = marque.upper()
            extracted_text = re.sub(re.escape(marque), f'**{marque_display}**', extracted_text, flags=re.IGNORECASE)
            
            # Mettre le mot-clé en gras
            extracted_text = extracted_text.replace(detail['mot_cle'], f"**{detail['mot_cle']}**")
            
            print(f"   {extracted_text[:500]}...")
            print("-" * 30)
            
    # Génération des fichiers de sortie
    print("\n" + "=" * 50)
    print("📄 GÉNÉRATION DES RAPPORTS")
    print("=" * 50)
    
    # Sauvegarder en JSON
    json_file = save_results_to_json(resultats_finaux)
    
    # Sauvegarder en PDF
    pdf_file = save_results_to_pdf(resultats_finaux)
    
    if json_file or pdf_file:
        print(f"\n✅ Rapports générés avec succès dans le répertoire du script.")
        
else:
    print("Aucune marque n'a été clairement signalée dans les URL testées avec un mot-clé de critique à proximité.")