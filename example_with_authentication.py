"""
Exemple d'utilisation du système intégré avec authentification
Démontre le cycle complet: inscription, connexion, interactions, recommandations
"""

from integrated_fashion_system import IntegratedFashionSystem
import json


def print_section(title: str):
    """Affiche un titre de section"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def print_json(data: dict):
    """Affiche un dictionnaire en JSON formaté"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """Démonstration complète du système intégré"""
    
    # ==================== INITIALISATION ====================
    print_section("1. INITIALISATION DU SYSTÈME INTÉGRÉ")
    
    system = IntegratedFashionSystem(
        brands_csv_path='brands_database_with_recycled_materials.csv',
        accounts_dir='user_accounts',
        preferences_dir='user_data',
        learning_rate=0.15
    )
    
    print("Système initialisé avec:")
    print("- Authentification des utilisateurs")
    print("- IA d'apprentissage des préférences")
    print("- Moteur de recommandation personnalisé")
    
    # ==================== INSCRIPTION ====================
    print_section("2. INSCRIPTION D'UN NOUVEL UTILISATEUR")
    
    print("Marie s'inscrit sur la plateforme...\n")
    
    registration_result = system.register(
        email="marie@example.com",
        password="SecurePass123",
        username="marie_eco",
        first_name="Marie",
        last_name="Dupont",
        age=28,
        country="France",
        data_sharing_consent=True
    )
    
    if registration_result['success']:
        print("Inscription réussie!")
        print(f"Nom d'utilisateur: {registration_result['user']['username']}")
        print(f"Email: {registration_result['user']['email']}")
        marie_token = registration_result['session_token']
        print(f"Token de session: {marie_token[:20]}...")
    else:
        print(f"Erreur: {registration_result['error']}")
        return
    
    # ==================== PROFIL INITIAL ====================
    print_section("3. PROFIL INITIAL DE MARIE")
    
    profile = system.get_complete_profile(marie_token)
    if profile['success']:
        print(f"Profil utilisateur:")
        print(f"  Username: {profile['user_profile']['username']}")
        print(f"  Email: {profile['user_profile']['email']}")
        print(f"  Pays: {profile['user_profile']['country']}")
        
        print(f"\nProfil IA:")
        print(f"  Type: {profile['ai_profile']['profile_type']}")
        print(f"  Confiance d'apprentissage: {profile['ai_profile']['learning_confidence']:.1%}")
        print(f"  Interactions: {profile['ai_profile']['total_interactions']}")
    
    # ==================== INTERACTIONS ====================
    print_section("4. MARIE EXPLORE DES MARQUES")
    
    print("Marie découvre et interagit avec différentes marques...\n")
    
    # Marie aime les marques écologiques
    interactions = [
        ("Patagonia", "like", 60.0),
        ("Veja", "save", 45.0),
        ("Reformation", "like", 90.0),
        ("Ekyog", "like", 30.0),
        ("Supreme", "dislike", 5.0),  # Pas assez écologique
        ("Nike", "dislike", 10.0)
    ]
    
    for brand, action, duration in interactions:
        result = system.record_brand_interaction(
            session_token=marie_token,
            brand_name=brand,
            interaction_type=action,
            duration_seconds=duration
        )
        
        if result.get('success'):
            emoji = "❤️" if action == "like" else "💾" if action == "save" else "👎"
            print(f"{emoji} {action.upper()}: {brand}")
            print(f"   Confiance: {result['learning_confidence']:.1%}")
            print(f"   Profil: {result['insights']['profile_type']}")
    
    # ==================== COMPARAISON ====================
    print_section("5. MARIE COMPARE DES MARQUES")
    
    print("Marie hésite entre deux marques et fait un choix...\n")
    
    comparison_result = system.record_brand_comparison(
        session_token=marie_token,
        chosen_brand="Patagonia",
        rejected_brand="The North Face"
    )
    
    if comparison_result.get('success'):
        print(f"Choix: Patagonia vs The North Face")
        print(f"Profil après comparaison: {comparison_result['insights']['profile_type']}")
        print(f"\nCritères importants pour Marie:")
        for criterion in comparison_result['insights']['top_criteria'][:3]:
            print(f"  - {criterion['criterion'].replace('_', ' ').title()}: {criterion['weight']:.3f}")
    
    # ==================== PROFIL APPRIS ====================
    print_section("6. PROFIL APPRIS DE MARIE")
    
    profile = system.get_complete_profile(marie_token)
    if profile['success']:
        ai_profile = profile['ai_profile']
        
        print(f"Type de profil: {ai_profile['profile_type']}")
        print(f"Confiance: {ai_profile['learning_confidence']:.1%}")
        print(f"Interactions: {ai_profile['total_interactions']}")
        
        print(f"\nTop 5 critères pour Marie:")
        for i, criterion in enumerate(ai_profile['top_criteria'][:5], 1):
            print(f"  {i}. {criterion['criterion'].replace('_', ' ').title()}: {criterion['weight']:.3f}")
        
        print(f"\nCaractéristiques:")
        chars = ai_profile['characteristics']
        print(f"  Eco-consciente: {'Oui' if chars['eco_conscious'] else 'Non'}")
        print(f"  Sensible au prix: {'Oui' if chars['price_sensitive'] else 'Non'}")
        print(f"  Valorise la transparence: {'Oui' if chars['values_transparency'] else 'Non'}")
        print(f"  Valorise l'éthique: {'Oui' if chars['values_ethics'] else 'Non'}")
    
    # ==================== RECOMMANDATIONS ====================
    print_section("7. RECOMMANDATIONS PERSONNALISÉES POUR MARIE")
    
    recs_result = system.get_personalized_recommendations(
        session_token=marie_token,
        n_recommendations=10,
        min_score=0.5
    )
    
    if recs_result['success']:
        print(f"Profil: {recs_result['user_profile_type']}\n")
        print("Top 10 marques recommandées:\n")
        
        for i, rec in enumerate(recs_result['recommendations'], 1):
            print(f"{i}. {rec['brand_name']} ({rec['category']})")
            print(f"   Score: {rec['score']:.3f}")
            if rec['match_reasons']:
                print(f"   Raisons: {', '.join(rec['match_reasons'][:2])}")
            print()
    
    # ==================== RECOMMANDATIONS PAR CATÉGORIE ====================
    print_section("8. RECOMMANDATIONS PAR CATÉGORIE")
    
    print("Meilleures marques de sportswear pour Marie:\n")
    
    sportswear_recs = system.get_personalized_recommendations(
        session_token=marie_token,
        n_recommendations=5,
        category="sportswear",
        min_score=0.4
    )
    
    if sportswear_recs['success']:
        for i, rec in enumerate(sportswear_recs['recommendations'], 1):
            print(f"{i}. {rec['brand_name']} - Score: {rec['score']:.3f}")
    
    # ==================== MARQUES SIMILAIRES ====================
    print_section("9. MARQUES SIMILAIRES")
    
    print("Marques similaires à Patagonia (que Marie aime):\n")
    
    similar_result = system.get_similar_brands(
        session_token=marie_token,
        brand_name="Patagonia",
        n_recommendations=5
    )
    
    if similar_result['success']:
        for i, rec in enumerate(similar_result['similar_brands'], 1):
            print(f"{i}. {rec['brand_name']} - Score: {rec['score']:.3f}")
    
    # ==================== EXPLICATION ====================
    print_section("10. EXPLICATION D'UNE RECOMMANDATION")
    
    print("Pourquoi Veja est recommandé à Marie?\n")
    
    explanation = system.explain_brand_recommendation(
        session_token=marie_token,
        brand_name="Veja"
    )
    
    if explanation.get('success'):
        print(f"Marque: {explanation['brand_name']}")
        print(f"Score: {explanation['overall_score']:.3f}")
        print(f"Évaluation: {explanation['recommendation']}\n")
        
        print("Analyse détaillée (top 3 critères):")
        for analysis in explanation['detailed_analysis'][:3]:
            print(f"\n  {analysis['criterion']}:")
            print(f"    Importance pour Marie: {analysis['user_importance']:.3f}")
            print(f"    Valeur de la marque: {analysis['brand_value']:.3f}")
            print(f"    Évaluation: {analysis['evaluation']}")
    
    # ==================== DEUXIÈME UTILISATEUR ====================
    print_section("11. NOUVEAU PROFIL UTILISATEUR DIFFÉRENT")
    
    print("Thomas s'inscrit avec des préférences différentes...\n")
    
    thomas_reg = system.register(
        email="thomas@example.com",
        password="SecurePass456",
        username="thomas_street",
        first_name="Thomas",
        age=24,
        country="France"
    )
    
    if thomas_reg['success']:
        thomas_token = thomas_reg['session_token']
        print(f"Thomas inscrit: {thomas_reg['user']['username']}")
        
        # Thomas aime le streetwear et est sensible au prix
        print("\nThomas explore le streetwear...\n")
        
        thomas_interactions = [
            ("Supreme", "like"),
            ("Stussy", "save"),
            ("Off-White", "like"),
            ("Palace", "like"),
            ("Patagonia", "dislike"),  # Trop cher et pas son style
        ]
        
        for brand, action in thomas_interactions:
            system.record_brand_interaction(
                session_token=thomas_token,
                brand_name=brand,
                interaction_type=action
            )
            emoji = "❤️" if action == "like" else "💾" if action == "save" else "👎"
            print(f"{emoji} {action.upper()}: {brand}")
        
        # Profil de Thomas
        thomas_profile = system.get_complete_profile(thomas_token)
        if thomas_profile['success']:
            print(f"\nProfil de Thomas: {thomas_profile['ai_profile']['profile_type']}")
            
            print("\nTop 3 critères pour Thomas:")
            for criterion in thomas_profile['ai_profile']['top_criteria'][:3]:
                print(f"  - {criterion['criterion'].replace('_', ' ').title()}: {criterion['weight']:.3f}")
        
        # Recommandations pour Thomas
        thomas_recs = system.get_personalized_recommendations(
            session_token=thomas_token,
            n_recommendations=5,
            min_score=0.4
        )
        
        if thomas_recs['success']:
            print(f"\nTop 5 recommandations pour Thomas:\n")
            for i, rec in enumerate(thomas_recs['recommendations'], 1):
                print(f"{i}. {rec['brand_name']} ({rec['category']}) - Score: {rec['score']:.3f}")
    
    # ==================== COMPARAISON DES PROFILS ====================
    print_section("12. COMPARAISON MARIE VS THOMAS")
    
    marie_profile = system.get_complete_profile(marie_token)
    thomas_profile = system.get_complete_profile(thomas_token)
    
    if marie_profile['success'] and thomas_profile['success']:
        print(f"{'Critère':<35} {'Marie':<12} {'Thomas':<12}")
        print("-" * 60)
        
        for criterion in ['sustainable_materials', 'price_range', 'labor_ethics', 'recycled_materials']:
            marie_weight = marie_profile['ai_profile']['all_weights'].get(criterion, 0.5)
            thomas_weight = thomas_profile['ai_profile']['all_weights'].get(criterion, 0.5)
            criterion_name = criterion.replace('_', ' ').title()
            print(f"{criterion_name:<35} {marie_weight:<12.3f} {thomas_weight:<12.3f}")
        
        print(f"\nProfil Marie: {marie_profile['ai_profile']['profile_type']}")
        print(f"Profil Thomas: {thomas_profile['ai_profile']['profile_type']}")
    
    # ==================== DÉCONNEXION ====================
    print_section("13. DÉCONNEXION")
    
    marie_logout = system.logout(marie_token)
    thomas_logout = system.logout(thomas_token)
    
    print(f"Marie: {marie_logout['message']}")
    print(f"Thomas: {thomas_logout['message']}")
    
    # ==================== RECONNEXION ====================
    print_section("14. RECONNEXION DE MARIE")
    
    print("Marie se reconnecte plus tard...\n")
    
    marie_login = system.login(
        email="marie@example.com",
        password="SecurePass123"
    )
    
    if marie_login['success']:
        print("Connexion réussie!")
        print(f"Profil: {marie_login['ai_profile']['profile_type']}")
        print(f"Confiance: {marie_login['ai_profile']['learning_confidence']:.1%}")
        print(f"Interactions totales: {marie_login['ai_profile']['total_interactions']}")
        print("\nLes préférences de Marie ont été conservées et rechargées!")
    
    # ==================== STATISTIQUES ====================
    print_section("15. STATISTIQUES DU SYSTÈME")
    
    stats = system.get_system_statistics()
    
    print("Authentification:")
    print(f"  Total utilisateurs: {stats['authentication']['total_users']}")
    print(f"  Utilisateurs actifs: {stats['authentication']['active_users']}")
    print(f"  Sessions actives: {stats['authentication']['active_sessions']}")
    
    print("\nSystème IA:")
    print(f"  Total marques: {stats['ai_system']['total_brands']}")
    print(f"  Catégories: {len(stats['ai_system']['categories'])}")
    print(f"  Utilisateurs avec préférences: {stats['users_with_ai_preferences']}")
    
    print_section("DÉMONSTRATION TERMINÉE")
    
    print("Le système complet est maintenant opérationnel avec:")
    print("- Gestion des comptes utilisateur sécurisée")
    print("- Authentification par email/mot de passe")
    print("- Apprentissage automatique des préférences")
    print("- Recommandations personnalisées par IA")
    print("- Persistance des données utilisateur")
    print("\nLes utilisateurs peuvent créer un compte, interagir avec des marques,")
    print("et recevoir des recommandations adaptées à leurs goûts uniques!")


if __name__ == "__main__":
    main()

