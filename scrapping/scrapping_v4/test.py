import requests
import pandas as pd

API_KEY = "mNm8lpEUIbPzJu5gHu9ieAtt"

url = "https://wikirate.org/Metrics.json"
headers = {"User-Agent": "FashionEthicsDataBot/1.0"}

params = {
    "filter": "Living wage paid",
    "limit": 100,
    "api_key": API_KEY
}

print("🔍 Recherche des métriques contenant 'Living wage paid'...")
response = requests.get(url, headers=headers, params=params)
print("Status:", response.status_code)

if response.status_code != 200:
    print("⚠️ Erreur:", response.text[:500])
else:
    data = response.json()
    print(f"✅ {len(data)} metrics trouvés.")

    # On crée un DataFrame
    df = pd.json_normalize(data)

    # Afficher les colonnes disponibles pour debug
    print("\n📋 Colonnes disponibles dans la réponse :")
    print(list(df.columns))

    # On affiche les 5 premières lignes pour inspection
    print("\n📊 Exemple de lignes :")
    print(df.head(5))

    # On garde les colonnes utiles si elles existent
    cols_to_keep = [c for c in ["id", "name", "designer", "topic", "title", "url"] if c in df.columns]
    df_filtered = df[cols_to_keep] if cols_to_keep else df

    # Enregistre en CSV
    df_filtered.to_csv("metrics_living_wage_results.csv", index=False)
    print("💾 Résultats enregistrés dans 'metrics_living_wage_results.csv'")
