from CalculScore import calculate_scores

fake_brand = {
    "brand_name": "Test Brand",
    "country_origin": "France",
    "sustainable_materials": 65,
    "certifications": "GOTS, FairTrade, OEKO-TEX",
    "unsold_management": "Don et recyclage",
    "supply_chain_transparency": "Totale",
    "labor_ethics": 0.85
}

scores = calculate_scores(fake_brand)

print(scores)