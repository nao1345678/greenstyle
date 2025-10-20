import pandas as pd

# 🔹 URLs publiques vers les données CSV sur WikiRate (aucune authentification requise)
URL_LIVING_WAGE = "https://wikirate.org/Companies.csv?metric_name=Living%20wage%20paid%3F&project=Fashion%20Checker"
URL_TRANSPARENCY = "https://wikirate.org/Companies.csv?metric_name=Publishing%20supplier%20list%3F&project=Fashion%20Checker"

# -------------------------------------------------------------
# Étape 1 — Télécharger les datasets
# -------------------------------------------------------------
print("📥 Téléchargement des données...")

df_living = pd.read_csv(URL_LIVING_WAGE)
df_transparency = pd.read_csv(URL_TRANSPARENCY)

print(f"Living wage : {len(df_living)} lignes")
print(f"Transparency : {len(df_transparency)} lignes")

# -------------------------------------------------------------
# Étape 2 — Nettoyage des colonnes principales
# -------------------------------------------------------------
def clean_df(df, metric_name):
    # On garde uniquement les colonnes pertinentes si elles existent
    cols_to_keep = [col for col in df.columns if col.lower() in ["company", "company_name", "value", "year"]]
    df = df[cols_to_keep].copy()
    # Harmoniser le nom de la colonne marque
    if "company" in df.columns:
        df.rename(columns={"company": "brand"}, inplace=True)
    elif "company_name" in df.columns:
        df.rename(columns={"company_name": "brand"}, inplace=True)
    # Ajouter le nom du metric (utile si fusion)
    df.rename(columns={"value": metric_name, "year": f"year_{metric_name}"}, inplace=True)
    # Supprimer doublons
    df.drop_duplicates(subset=["brand"], keep="last", inplace=True)
    return df

df_living_clean = clean_df(df_living, "living_wage_paid")
df_transp_clean = clean_df(df_transparency, "publishes_supplier_list")

# -------------------------------------------------------------
# Étape 3 — Fusion des deux datasets sur le nom de la marque
# -------------------------------------------------------------
df_merged = pd.merge(df_living_clean, df_transp_clean, on="brand", how="outer")

# -------------------------------------------------------------
# Étape 4 — Nettoyage final et export
# -------------------------------------------------------------
df_merged.sort_values(by="brand", inplace=True)
df_merged.reset_index(drop=True, inplace=True)

# Sauvegarde du fichier propre
df_merged.to_csv("fashion_checker_clean.csv", index=False)

print("\n✅ Données consolidées enregistrées : fashion_checker_clean.csv")
print(df_merged.head(10))
