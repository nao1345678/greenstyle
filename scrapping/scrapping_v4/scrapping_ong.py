import requests
import pandas as pd

API_KEY = "mNm8lpEUIbPzJu5gHu9ieAtt"
METRIC_ID = 5990097  # remplace avec l'ID exact trouvé
LIMIT = 1000

def get_metric_answers(metric_id):
    all_data = []
    offset = 0
    headers = {"User-Agent": "FashionEthicsDataBot/1.0"}

    while True:
        url = "https://wikirate.org/Answers.json"
        params = {
            "metric_id": metric_id,
            "limit": LIMIT,
            "offset": offset,
            "api_key": API_KEY
        }

        print(f"📥 Téléchargement... offset={offset}")
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"⚠️ Erreur {response.status_code}: {response.text[:300]}")
            break

        data = response.json()
        if not data:
            break

        all_data.extend(data)
        if len(data) < LIMIT:
            break

        offset += LIMIT

    return all_data


print("🔍 Récupération des réponses 'Living wage paid?' ...")
answers = get_metric_answers(METRIC_ID)
print(f"✅ {len(answers)} réponses récupérées")

if not answers:
    print("❌ Toujours vide — mauvais ID ? Vérifie la recherche du metric.")
else:
    import json
    print(json.dumps(answers[0], indent=2)[:800])

    df = pd.json_normalize(answers)
    print(df.columns)

    # On garde les colonnes utiles
    cols = [c for c in df.columns if any(k in c for k in ["company", "year", "value", "source"])]
    df = df[cols]
    df.to_csv("living_wage_answers.csv", index=False)
    print("💾 Données enregistrées dans living_wage_answers.csv")
