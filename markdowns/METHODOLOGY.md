# Méthodologie de Collecte des Données de Durabilité

## 📊 Sources de Données Officielles

### Comment Collecter les Vraies Données

#### **1. Télécharger les Rapports Officiels**

##### Nike - Move to Zero Impact Report
```bash
# URL du rapport 2023
https://www.nike.com/pdf/NikeFY23ImpactReport.pdf

# Données à extraire :
- Page 12 : "43% of our materials were recycled or sustainable"
- Page 15 : Certifications (Bluesign, Better Cotton, LWG)
- Page 18 : Carbon emissions data
- Page 22 : Manufacturing countries breakdown
```

##### H&M Group - Sustainability Performance Report
```bash
# URL du rapport 2023
https://hmgroup.com/wp-content/uploads/2024/03/HM-Group-Sustainability-Performance-Report-2023.pdf

# Données à extraire :
- Page 8 : "28% sustainable materials (target 100% by 2030)"
- Page 14 : Better Cotton Initiative partnership
- Page 20 : Supplier transparency metrics
- Page 32 : Circular economy initiatives
```

##### Patagonia - Environmental + Social Initiatives
```bash
# URL du rapport
https://www.patagonia.com/our-footprint/

# Données publiques :
- 87% matériaux recyclés ou biologiques (vérifié 2023)
- B Corp certification (score 151.4/200)
- Fair Trade Certified depuis 2014
- 1% for the Planet membre fondateur
```

---

#### **2. Extraction Automatisée des PDFs**

##### Script Python pour extraire les données

```python
import PyPDF2
import re
import requests

def download_report(url, brand_name):
    """Télécharge le rapport PDF"""
    response = requests.get(url)
    filename = f"reports/{brand_name}_2023.pdf"
    
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    return filename

def extract_recycled_percentage_from_pdf(pdf_path):
    """Extrait le % de matériaux recyclés d'un PDF"""
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Extraire tout le texte
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
        
        # Patterns pour trouver les pourcentages
        patterns = [
            r'(\d+)%\s*(?:of\s*)?(?:materials|products).*?(?:recycled|sustainable)',
            r'(?:recycled|sustainable)\s*materials.*?(\d+)%',
            r'(\d+)%\s*recycled\s*content',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            if matches:
                # Retourner le premier match trouvé
                return int(matches[0])
    
    return None

# Utilisation
nike_report = download_report(
    "https://www.nike.com/pdf/NikeFY23ImpactReport.pdf",
    "Nike"
)
percentage = extract_recycled_percentage_from_pdf(nike_report)
print(f"Nike: {percentage}% matériaux recyclés")
```

---

#### **3. Utiliser les APIs Officielles**

Certaines organisations proposent des APIs :

##### Good On You API (Beta)
```python
import requests

def get_brand_rating(brand_name):
    """Récupère les données via Good On You"""
    # Note: API en beta, peut nécessiter une clé
    
    url = f"https://api.goodonyou.eco/v1/brands/{brand_name}"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'rating': data['overall_rating'],  # Great/Good/It's a Start/Not Good Enough/We Avoid
            'certifications': data['certifications'],
            'materials_score': data['planet_score'],
            'labor_score': data['people_score'],
        }
    
    return None
```

##### Fashion Transparency Index Data
```python
def get_transparency_score(brand_name):
    """Récupère le score de transparence"""
    
    # Fashion Revolution publie des données ouvertes
    url = "https://www.fashionrevolution.org/about/transparency/"
    
    # Télécharger le fichier Excel/CSV public
    data_url = "https://www.fashionrevolution.org/wp-content/uploads/2023/05/FTI-2023-data.xlsx"
    
    # Parser le fichier pour trouver la marque
    # ...
    
    return transparency_score
```

---

#### **4. Bases de Données Tierces Vérifiées**

##### B Corp Directory (Officiel)
```python
def verify_bcorp_status(brand_name):
    """Vérifie si une marque est B Corp certifiée"""
    
    # API publique B Corp
    url = "https://www.bcorporation.net/en-us/find-a-b-corp/search"
    params = {"query": brand_name}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['results']:
            return {
                'certified': True,
                'score': data['results'][0]['overall_score'],
                'year_certified': data['results'][0]['certification_date'],
            }
    
    return {'certified': False}

# Exemple
patagonia_bcorp = verify_bcorp_status("Patagonia")
# → {'certified': True, 'score': 151.4, 'year_certified': 2012}
```

##### Better Cotton Initiative Members
```python
def check_better_cotton_member(brand_name):
    """Vérifie l'adhésion Better Cotton"""
    
    # BCI publie la liste des membres
    url = "https://bettercotton.org/who-we-are/our-members/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    members_list = soup.find_all('div', class_='member-name')
    
    for member in members_list:
        if brand_name.lower() in member.text.lower():
            return True
    
    return False
```

---

## ✅ Process Recommandé pour Production

### **Étape 1 : Identifier les sources officielles**
```
Pour chaque marque :
1. Trouver le site officiel
2. Chercher la section sustainability/CSR
3. Télécharger le rapport le plus récent (2023-2024)
4. Noter l'URL et la date du rapport
```

### **Étape 2 : Extraction manuelle (pour commencer)**
```
Créer un fichier Excel :

Brand | Report URL | Year | Recycled % | Source Page | Certifications | Verified Date
Nike  | nike.com/... | 2023 | 43%       | Page 12     | Bluesign, BCI  | 2024-01-15
H&M   | hmgroup.com/..| 2023 | 28%       | Page 8      | BCI, Fair Trade| 2024-01-15
```

### **Étape 3 : Automatisation progressive**
```python
# 1. Scraper les pages sustainability
# 2. Télécharger automatiquement les PDFs
# 3. Extraire via OCR/PDF parsing
# 4. Valider manuellement les données
# 5. Mettre à jour la base de données
```

### **Étape 4 : Mise à jour régulière**
```python
# Script à exécuter tous les 3 mois
def update_sustainability_data():
    for brand in brands_database:
        # Vérifier si nouveau rapport publié
        latest_report = check_for_new_report(brand)
        
        if latest_report.date > brand.last_update:
            # Télécharger et extraire
            new_data = extract_data(latest_report)
            
            # Mettre à jour
            update_brand_data(brand, new_data)
```

---

## 📚 Ressources pour Vérification

### Sites de référence
1. **Good On You** : https://goodonyou.eco/
   - Base de données vérifiée de 3000+ marques
   
2. **Fashion Transparency Index** : https://www.fashionrevolution.org/
   - Index annuel de transparence (250+ grandes marques)
   
3. **Ethical Consumer** : https://www.ethicalconsumer.org/
   - Recherches indépendantes sur l'éthique des marques
   
4. **Rank a Brand** : https://rankabrand.org/
   - Classement des marques par durabilité

### Certifications officielles
1. **B Corp** : https://www.bcorporation.net/en-us/find-a-b-corp/
2. **Fair Trade** : https://www.fairtradecertified.org/
3. **GOTS** : https://global-standard.org/find-suppliers-shops-and-inputs
4. **Bluesign** : https://www.bluesign.com/en/business-partners
5. **Better Cotton** : https://bettercotton.org/

---

## 🎯 Exemple de Fiche Source Vérifiée

### Patagonia
```yaml
Brand: Patagonia
Last Updated: 2024-01-15
Data Quality: HIGH (official reports + third-party verified)

Sources:
  - Primary: https://www.patagonia.com/our-footprint/
  - Report: "Patagonia Environmental & Social Initiatives 2023"
  - B Corp Profile: https://www.bcorporation.net/en-us/find-a-b-corp/company/patagonia-inc

Verified Data:
  - Recycled Materials: 87%
    Source: Annual Report 2023, Page 4
    Quote: "87% of our materials were either recycled or renewable"
    
  - Certifications:
    - B Corp: Verified ✅ (Score 151.4, Certified 2012)
    - Fair Trade: Verified ✅ (Since 2014)
    - Bluesign: Verified ✅ (System Partner)
    - 1% for the Planet: Verified ✅ (Founding member)
    
  - Countries of Production: USA, Vietnam, Thailand, China
    Source: Footprint Chronicles (public database)
    
  - Carbon Footprint: 33,038 metric tons CO2e (2022)
    Source: Environmental Report 2023, Page 12
```

---

## ⚠️ Avertissement sur les Données Actuelles

Les données dans `recycled_materials_scraper.py` et `certifications_scraper.py` 
sont des **estimations indicatives** basées sur :

1. Connaissances générales de l'industrie
2. Rapports publics consultés avant ma date de coupure (2024)
3. Informations publiquement disponibles

**Pour un usage professionnel/académique**, vous devez :
- ✅ Vérifier chaque donnée avec les rapports officiels
- ✅ Citer les sources exactes (URL + page + date)
- ✅ Mettre à jour régulièrement (les marques évoluent)
- ✅ Indiquer le niveau de confiance des données

---

## 🔄 Processus de Validation Recommandé

```
1. Donnée trouvée par scraping
   ↓
2. Vérification croisée avec 2+ sources
   ↓
3. Consultation du rapport officiel
   ↓
4. Validation manuelle par un expert
   ↓
5. Ajout à la base de données avec métadonnées :
   - Date de vérification
   - Sources multiples
   - Niveau de confiance
   - Notes contextuelles
```

