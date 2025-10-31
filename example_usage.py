"""
Exemple d'utilisation du système d'IA de recommandation de mode
Démontre comment le système apprend les préférences de l'utilisateur
"""

from fashion_ai_api import FashionAI
import json


def print_section(title: str):
    """Affiche un titre de section"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def main():
    """Démontre l'utilisation complète du système"""
    
    # ========== Initialisation ==========
    print_section("1. INITIALISATION DU SYSTÈME")
    
    # Crée l'instance de l'IA
    ai = FashionAI(
        brands_csv_path='brands_database_with_recycled_materials.csv',
        users_data_dir='user_data',
        learning_rate=0.15
    )
    
    # Affiche les stats du système
    stats = ai.get_system_stats()
    print(f"Nombre de marques: {stats['total_brands']}")
    print(f"Catégories disponibles: {', '.join(stats['categories'][:5])}...")
    
    # ========== Création d'un utilisateur ==========
    print_section("2. CRÉATION D'UN UTILISATEUR")
    
    user_id = "alice_2025"
    user_prefs = ai.create_user(user_id)
    print(f"Utilisateur créé: {user_id}")
    print(f"Confiance d'apprentissage initiale: {user_prefs.learning_confidence}")
    
    # ========== Premières interactions ==========
    print_section("3. APPRENTISSAGE - PREMIÈRES INTERACTIONS")
    
    print("Alice explore des marques et interagit avec elles...\n")
    
    # Alice aime Patagonia (marque très écologique)
    result = ai.record_interaction(
        user_id=user_id,
        brand_name="Patagonia",
        interaction_type="like",
        duration_seconds=45.0
    )
    print(f"Interaction 1: LIKE Patagonia")
    print(f"  Confiance: {result['learning_confidence']:.3f}")
    print(f"  Profil: {result['insights']['profile_type']}")
    
    # Alice sauvegarde Veja (marque éthique et écologique)
    result = ai.record_interaction(
        user_id=user_id,
        brand_name="Veja",
        interaction_type="save",
        duration_seconds=60.0
    )
    print(f"\nInteraction 2: SAVE Veja")
    print(f"  Confiance: {result['learning_confidence']:.3f}")
    print(f"  Profil: {result['insights']['profile_type']}")
    
    # Alice n'aime pas Supreme (marque streetwear sans focus écologique)
    result = ai.record_interaction(
        user_id=user_id,
        brand_name="Supreme",
        interaction_type="dislike",
        duration_seconds=5.0
    )
    print(f"\nInteraction 3: DISLIKE Supreme")
    print(f"  Confiance: {result['learning_confidence']:.3f}")
    print(f"  Profil: {result['insights']['profile_type']}")
    
    # Alice aime Reformation (marque durable)
    result = ai.record_interaction(
        user_id=user_id,
        brand_name="Reformation",
        interaction_type="like",
        duration_seconds=90.0
    )
    print(f"\nInteraction 4: LIKE Reformation")
    print(f"  Confiance: {result['learning_confidence']:.3f}")
    print(f"  Profil: {result['insights']['profile_type']}")
    
    # ========== Comparaison directe ==========
    print_section("4. APPRENTISSAGE PAR COMPARAISON")
    
    print("Alice compare deux marques et choisit...\n")
    
    result = ai.record_comparison(
        user_id=user_id,
        chosen_brand="Patagonia",
        rejected_brand="Nike"
    )
    print(f"Comparaison: Patagonia vs Nike")
    print(f"  Choix: Patagonia")
    print(f"  Profil après comparaison: {result['insights']['profile_type']}")
    
    # ========== Profil utilisateur ==========
    print_section("5. PROFIL UTILISATEUR APPRIS")
    
    profile = ai.get_user_profile(user_id)
    print(f"Profil de {user_id}:")
    print(f"  Type: {profile['profile_type']}")
    print(f"  Confiance: {profile['learning_confidence']:.1%}")
    print(f"  Total interactions: {profile['total_interactions']}")
    
    print(f"\nTop 3 critères importants pour Alice:")
    for i, criterion in enumerate(profile['top_criteria'], 1):
        print(f"  {i}. {criterion['criterion'].replace('_', ' ').title()}: {criterion['weight']:.3f}")
    
    print(f"\nCaractéristiques:")
    for key, value in profile['characteristics'].items():
        status = "Oui" if value else "Non"
        print(f"  {key.replace('_', ' ').title()}: {status}")
    
    # ========== Recommandations personnalisées ==========
    print_section("6. RECOMMANDATIONS PERSONNALISÉES")
    
    recommendations = ai.get_recommendations(
        user_id=user_id,
        n_recommendations=10,
        min_score=0.5
    )
    
    print(f"Top 10 recommandations pour Alice:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['brand_name']} ({rec['category']})")
        print(f"   Score: {rec['score']:.3f}")
        print(f"   Raisons: {', '.join(rec['match_reasons'][:2]) if rec['match_reasons'] else 'Bon match général'}")
        print()
    
    # ========== Recommandations par catégorie ==========
    print_section("7. RECOMMANDATIONS PAR CATÉGORIE")
    
    print("Meilleures marques de sportswear pour Alice:\n")
    sportswear_recs = ai.get_recommendations(
        user_id=user_id,
        n_recommendations=5,
        category="sportswear",
        min_score=0.4
    )
    
    for i, rec in enumerate(sportswear_recs, 1):
        print(f"{i}. {rec['brand_name']} - Score: {rec['score']:.3f}")
    
    # ========== Marques similaires ==========
    print_section("8. MARQUES SIMILAIRES")
    
    print("Marques similaires à Patagonia (qu'Alice aime):\n")
    similar = ai.get_similar_brands(
        user_id=user_id,
        brand_name="Patagonia",
        n_recommendations=5
    )
    
    for i, rec in enumerate(similar, 1):
        print(f"{i}. {rec['brand_name']} - Score: {rec['score']:.3f}")
    
    # ========== Explication détaillée ==========
    print_section("9. EXPLICATION D'UNE RECOMMANDATION")
    
    print("Pourquoi Veja est recommandé à Alice?\n")
    explanation = ai.explain_recommendation(
        user_id=user_id,
        brand_name="Veja"
    )
    
    print(f"Marque: {explanation['brand_name']}")
    print(f"Score global: {explanation['overall_score']:.3f}")
    print(f"Évaluation: {explanation['recommendation']}\n")
    
    print("Analyse détaillée:")
    for analysis in explanation['detailed_analysis'][:5]:
        print(f"\n  {analysis['criterion']}:")
        print(f"    Importance pour Alice: {analysis['user_importance']:.3f}")
        print(f"    Valeur de la marque: {analysis['brand_value']:.3f}")
        print(f"    Match: {analysis['evaluation']}")
    
    # ========== Nouveau scénario utilisateur ==========
    print_section("10. NOUVEAU UTILISATEUR - PROFIL DIFFÉRENT")
    
    user2_id = "bob_2025"
    ai.create_user(user2_id)
    print(f"Nouvel utilisateur: {user2_id}")
    print("Bob est sensible au prix et aime le streetwear...\n")
    
    # Bob interagit différemment
    ai.record_interaction(user2_id, "Supreme", "like", 30.0)
    ai.record_interaction(user2_id, "Stussy", "save", 45.0)
    ai.record_interaction(user2_id, "Off-White", "like", 20.0)
    ai.record_interaction(user2_id, "Patagonia", "dislike", 5.0)  # Trop cher pour Bob
    
    profile2 = ai.get_user_profile(user2_id)
    print(f"Profil de Bob: {profile2['profile_type']}")
    
    print(f"\nTop 3 critères pour Bob:")
    for i, criterion in enumerate(profile2['top_criteria'], 1):
        print(f"  {i}. {criterion['criterion'].replace('_', ' ').title()}: {criterion['weight']:.3f}")
    
    # Recommandations pour Bob
    bob_recs = ai.get_recommendations(
        user_id=user2_id,
        n_recommendations=5,
        min_score=0.4
    )
    
    print(f"\nTop 5 recommandations pour Bob:\n")
    for i, rec in enumerate(bob_recs, 1):
        print(f"{i}. {rec['brand_name']} ({rec['category']}) - Score: {rec['score']:.3f}")
    
    # ========== Comparaison des profils ==========
    print_section("11. COMPARAISON DES PROFILS")
    
    print("Alice vs Bob - Poids des critères:\n")
    print(f"{'Critère':<30} {'Alice':<10} {'Bob':<10}")
    print("-" * 50)
    
    for criterion in ['sustainable_materials', 'price_range', 'labor_ethics', 'country_production']:
        alice_weight = profile['all_weights'].get(criterion, 0.5)
        bob_weight = profile2['all_weights'].get(criterion, 0.5)
        criterion_name = criterion.replace('_', ' ').title()
        print(f"{criterion_name:<30} {alice_weight:<10.3f} {bob_weight:<10.3f}")
    
    # ========== Sauvegarde ==========
    print_section("12. SAUVEGARDE DES DONNÉES")
    
    ai.save_user(user_id)
    ai.save_user(user2_id)
    print(f"Données sauvegardées pour {user_id} et {user2_id}")
    print(f"Fichiers: user_data/{user_id}.json et user_data/{user2_id}.json")
    
    print_section("DÉMONSTRATION TERMINÉE")
    print("Le système a appris les préférences des utilisateurs et peut maintenant")
    print("faire des recommandations personnalisées basées sur leurs goûts uniques.")
    print("\nLes données sont persistées et peuvent être rechargées à tout moment.")


if __name__ == "__main__":
    main()
