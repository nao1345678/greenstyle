"""
Système intégré combinant l'authentification et l'IA de recommandation
Point d'entrée principal pour l'application complète
"""

from typing import Optional, List, Dict, Tuple
from authentication_service import AuthenticationService, AuthenticationError
from fashion_ai_api import FashionAI
from user_account_model import UserAccount


class IntegratedFashionSystem:
    """
    Système complet intégrant authentification et recommandations d'IA
    Gère tout le cycle de vie utilisateur avec leurs préférences
    """
    
    def __init__(
        self,
        brands_csv_path: str,
        accounts_dir: str = 'user_accounts',
        preferences_dir: str = 'user_data',
        learning_rate: float = 0.15
    ):
        """
        Args:
            brands_csv_path: Chemin vers le CSV des marques
            accounts_dir: Répertoire pour les comptes utilisateur
            preferences_dir: Répertoire pour les préférences d'IA
            learning_rate: Vitesse d'apprentissage de l'IA
        """
        # Service d'authentification
        self.auth_service = AuthenticationService(accounts_dir=accounts_dir)
        
        # Système d'IA de recommandation
        self.ai_system = FashionAI(
            brands_csv_path=brands_csv_path,
            users_data_dir=preferences_dir,
            learning_rate=learning_rate
        )
    
    # ==================== GESTION DES COMPTES ====================
    
    def register(
        self,
        email: str,
        password: str,
        username: str,
        **profile_data
    ) -> Dict[str, any]:
        """
        Inscrit un nouvel utilisateur et initialise ses préférences d'IA
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            username: Nom d'utilisateur
            **profile_data: Données de profil additionnelles
            
        Returns:
            Informations complètes sur le compte créé avec token de session
        """
        try:
            # Crée le compte utilisateur
            account, session_token = self.auth_service.register_user(
                email=email,
                password=password,
                username=username,
                **profile_data
            )
            
            # Initialise les préférences d'IA pour ce compte
            user_preferences = self.ai_system.create_user(account.user_id)
            
            return {
                'success': True,
                'message': 'Compte créé avec succès',
                'session_token': session_token,
                'user': account.get_full_profile(),
                'ai_learning_confidence': user_preferences.learning_confidence
            }
        
        except AuthenticationError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def login(self, email: str, password: str) -> Dict[str, any]:
        """
        Connecte un utilisateur et charge ses préférences d'IA
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            
        Returns:
            Informations de connexion avec token de session
        """
        try:
            # Authentifie l'utilisateur
            account, session_token = self.auth_service.login(email, password)
            
            # Charge les préférences d'IA (ou les crée si elles n'existent pas)
            user_preferences = self.ai_system.get_or_create_user(account.user_id)
            
            # Obtient le profil d'IA
            ai_profile = self.ai_system.get_user_profile(account.user_id)
            
            return {
                'success': True,
                'message': 'Connexion réussie',
                'session_token': session_token,
                'user': account.get_full_profile(),
                'ai_profile': {
                    'profile_type': ai_profile['profile_type'],
                    'learning_confidence': ai_profile['learning_confidence'],
                    'total_interactions': ai_profile['total_interactions']
                }
            }
        
        except AuthenticationError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def logout(self, session_token: str) -> Dict[str, any]:
        """Déconnecte un utilisateur"""
        success = self.auth_service.logout(session_token)
        return {
            'success': success,
            'message': 'Déconnexion réussie' if success else 'Token invalide'
        }
    
    def verify_and_get_user(self, session_token: str) -> Optional[UserAccount]:
        """
        Vérifie un token de session et retourne le compte utilisateur
        Utilisé pour protéger les endpoints qui nécessitent une authentification
        """
        return self.auth_service.verify_session(session_token)
    
    # ==================== PROFIL UTILISATEUR ====================
    
    def get_complete_profile(self, session_token: str) -> Dict[str, any]:
        """
        Récupère le profil complet (compte + préférences IA)
        
        Args:
            session_token: Token de session
            
        Returns:
            Profil complet ou erreur si non authentifié
        """
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        # Profil utilisateur
        user_profile = account.get_full_profile()
        
        # Profil IA
        ai_profile = self.ai_system.get_user_profile(account.user_id)
        
        return {
            'success': True,
            'user_profile': user_profile,
            'ai_profile': ai_profile
        }
    
    def update_profile(
        self,
        session_token: str,
        **profile_updates
    ) -> Dict[str, any]:
        """Met à jour le profil utilisateur"""
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        try:
            updated_account = self.auth_service.update_profile(
                account.user_id,
                **profile_updates
            )
            
            return {
                'success': True,
                'user': updated_account.get_full_profile()
            }
        
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== INTERACTIONS ET APPRENTISSAGE ====================
    
    def record_brand_interaction(
        self,
        session_token: str,
        brand_name: str,
        interaction_type: str,
        duration_seconds: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Enregistre une interaction avec une marque (avec authentification)
        
        Args:
            session_token: Token de session
            brand_name: Nom de la marque
            interaction_type: Type d'interaction ('like', 'dislike', etc.)
            duration_seconds: Durée de l'interaction
            
        Returns:
            Résultat de l'apprentissage
        """
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        # Enregistre l'interaction dans l'IA
        result = self.ai_system.record_interaction(
            user_id=account.user_id,
            brand_name=brand_name,
            interaction_type=interaction_type,
            duration_seconds=duration_seconds
        )
        
        return result
    
    def record_brand_comparison(
        self,
        session_token: str,
        chosen_brand: str,
        rejected_brand: str
    ) -> Dict[str, any]:
        """Enregistre une comparaison entre deux marques"""
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        result = self.ai_system.record_comparison(
            user_id=account.user_id,
            chosen_brand=chosen_brand,
            rejected_brand=rejected_brand
        )
        
        return result
    
    # ==================== RECOMMANDATIONS ====================
    
    def get_personalized_recommendations(
        self,
        session_token: str,
        n_recommendations: int = 10,
        category: Optional[str] = None,
        min_score: float = 0.5
    ) -> Dict[str, any]:
        """
        Obtient des recommandations personnalisées pour l'utilisateur connecté
        
        Args:
            session_token: Token de session
            n_recommendations: Nombre de recommandations
            category: Filtrer par catégorie
            min_score: Score minimum
            
        Returns:
            Liste de recommandations ou erreur
        """
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        recommendations = self.ai_system.get_recommendations(
            user_id=account.user_id,
            n_recommendations=n_recommendations,
            category=category,
            min_score=min_score
        )
        
        return {
            'success': True,
            'recommendations': recommendations,
            'user_profile_type': self.ai_system.get_user_profile(account.user_id)['profile_type']
        }
    
    def get_similar_brands(
        self,
        session_token: str,
        brand_name: str,
        n_recommendations: int = 5
    ) -> Dict[str, any]:
        """Obtient des marques similaires à une marque donnée"""
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        similar = self.ai_system.get_similar_brands(
            user_id=account.user_id,
            brand_name=brand_name,
            n_recommendations=n_recommendations
        )
        
        return {
            'success': True,
            'similar_brands': similar,
            'reference_brand': brand_name
        }
    
    def explain_brand_recommendation(
        self,
        session_token: str,
        brand_name: str
    ) -> Dict[str, any]:
        """Explique pourquoi une marque est recommandée"""
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        explanation = self.ai_system.explain_recommendation(
            user_id=account.user_id,
            brand_name=brand_name
        )
        
        explanation['success'] = True
        return explanation
    
    # ==================== RECHERCHE ET EXPLORATION ====================
    
    def search_brands(
        self,
        query: str = '',
        category: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, any]:
        """
        Recherche des marques (accessible sans authentification)
        """
        brands = self.ai_system.search_brands(
            query=query,
            category=category,
            limit=limit
        )
        
        return {
            'success': True,
            'brands': brands,
            'count': len(brands)
        }
    
    def get_categories(self) -> Dict[str, any]:
        """Obtient toutes les catégories disponibles"""
        categories = self.ai_system.get_all_categories()
        return {
            'success': True,
            'categories': categories
        }
    
    # ==================== ADMINISTRATION ====================
    
    def get_system_statistics(self) -> Dict[str, any]:
        """Obtient des statistiques complètes sur le système"""
        auth_stats = self.auth_service.get_stats()
        ai_stats = self.ai_system.get_system_stats()
        
        return {
            'authentication': auth_stats,
            'ai_system': ai_stats,
            'total_active_users': auth_stats['active_users'],
            'users_with_ai_preferences': ai_stats['active_users']
        }
    
    def delete_user_account(
        self,
        session_token: str,
        password: str
    ) -> Dict[str, any]:
        """
        Supprime le compte utilisateur et toutes ses données
        (compte + préférences IA)
        """
        account = self.verify_and_get_user(session_token)
        if not account:
            return {'success': False, 'error': 'Non authentifié'}
        
        try:
            # Supprime le compte d'authentification
            auth_deleted = self.auth_service.delete_account(account.user_id, password)
            
            if auth_deleted:
                # Supprime aussi les données d'IA en supprimant le fichier de préférences
                import os
                prefs_file = os.path.join(
                    self.ai_system.users_data_dir,
                    f"{account.user_id}.json"
                )
                if os.path.exists(prefs_file):
                    os.remove(prefs_file)
                
                return {
                    'success': True,
                    'message': 'Compte et données supprimés avec succès'
                }
            else:
                return {
                    'success': False,
                    'error': 'Erreur lors de la suppression'
                }
        
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}

