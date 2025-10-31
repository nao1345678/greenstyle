"""
Service d'authentification pour gérer l'inscription, la connexion et les sessions
"""

import secrets
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
from user_account_model import UserAccount, UserAccountManager, PasswordHasher


class AuthenticationError(Exception):
    """Exception levée lors d'erreurs d'authentification"""
    pass


class SessionToken:
    """Représente un token de session utilisateur"""
    
    def __init__(self, user_id: str, token: str, expires_at: datetime):
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
    
    def is_valid(self) -> bool:
        """Vérifie si le token est toujours valide"""
        return datetime.now() < self.expires_at


class AuthenticationService:
    """
    Service complet d'authentification et de gestion des utilisateurs
    """
    
    def __init__(self, accounts_dir: str = 'user_accounts'):
        """
        Args:
            accounts_dir: Répertoire pour stocker les comptes
        """
        self.account_manager = UserAccountManager(accounts_dir)
        self.password_hasher = PasswordHasher()
        
        # Stockage en mémoire des sessions (dans une vraie app, utiliser Redis ou DB)
        self.active_sessions: Dict[str, SessionToken] = {}
    
    def register_user(
        self,
        email: str,
        password: str,
        username: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        country: Optional[str] = None,
        data_sharing_consent: bool = False,
        marketing_consent: bool = False
    ) -> Tuple[UserAccount, str]:
        """
        Inscrit un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair
            username: Nom d'utilisateur
            ... autres paramètres optionnels
            
        Returns:
            (UserAccount, session_token) - Le compte créé et un token de session
            
        Raises:
            AuthenticationError: Si l'inscription échoue
        """
        # Validations
        if not self._is_valid_email(email):
            raise AuthenticationError("Email invalide")
        
        if self.account_manager.email_exists(email):
            raise AuthenticationError("Cet email est déjà utilisé")
        
        if not self._is_valid_password(password):
            raise AuthenticationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule et un chiffre"
            )
        
        if not username or len(username) < 3:
            raise AuthenticationError("Le nom d'utilisateur doit contenir au moins 3 caractères")
        
        # Génère un ID unique
        user_id = self._generate_user_id()
        
        # Hash le mot de passe
        salt = self.password_hasher.generate_salt()
        password_hash = self.password_hasher.hash_password(password, salt)
        
        # Crée le compte
        account = UserAccount(
            user_id=user_id,
            email=email.lower(),
            username=username,
            password_hash=password_hash,
            salt=salt,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            country=country,
            data_sharing_consent=data_sharing_consent,
            marketing_consent=marketing_consent
        )
        
        # Sauvegarde le compte
        self.account_manager.save_account(account)
        
        # Crée une session automatiquement
        session_token = self._create_session(user_id)
        
        return account, session_token
    
    def login(self, email: str, password: str) -> Tuple[UserAccount, str]:
        """
        Connecte un utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair
            
        Returns:
            (UserAccount, session_token) - Le compte et un token de session
            
        Raises:
            AuthenticationError: Si la connexion échoue
        """
        # Charge le compte
        account = self.account_manager.load_account_by_email(email)
        
        if not account:
            raise AuthenticationError("Email ou mot de passe incorrect")
        
        # Vérifie que le compte est actif
        if not account.is_active:
            raise AuthenticationError("Ce compte a été désactivé")
        
        # Vérifie le mot de passe
        if not self.password_hasher.verify_password(password, account.salt, account.password_hash):
            raise AuthenticationError("Email ou mot de passe incorrect")
        
        # Met à jour la dernière connexion
        account.update_last_login()
        self.account_manager.save_account(account)
        
        # Crée une session
        session_token = self._create_session(account.user_id)
        
        return account, session_token
    
    def logout(self, session_token: str) -> bool:
        """
        Déconnecte un utilisateur (invalide le token)
        
        Args:
            session_token: Token de session à invalider
            
        Returns:
            True si le logout a réussi
        """
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False
    
    def verify_session(self, session_token: str) -> Optional[UserAccount]:
        """
        Vérifie qu'un token de session est valide et retourne le compte associé
        
        Args:
            session_token: Token à vérifier
            
        Returns:
            UserAccount si valide, None sinon
        """
        if session_token not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_token]
        
        # Vérifie l'expiration
        if not session.is_valid():
            del self.active_sessions[session_token]
            return None
        
        # Charge et retourne le compte
        return self.account_manager.load_account_by_id(session.user_id)
    
    def get_user_by_id(self, user_id: str) -> Optional[UserAccount]:
        """Récupère un compte par son ID"""
        return self.account_manager.load_account_by_id(user_id)
    
    def update_profile(
        self,
        user_id: str,
        **kwargs
    ) -> UserAccount:
        """
        Met à jour le profil d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            **kwargs: Champs à mettre à jour (username, first_name, last_name, etc.)
            
        Returns:
            Compte mis à jour
            
        Raises:
            AuthenticationError: Si l'utilisateur n'existe pas
        """
        account = self.account_manager.load_account_by_id(user_id)
        if not account:
            raise AuthenticationError("Utilisateur non trouvé")
        
        # Met à jour les champs autorisés
        allowed_fields = [
            'username', 'first_name', 'last_name', 'age', 
            'gender', 'country', 'data_sharing_consent', 'marketing_consent'
        ]
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(account, field, value)
        
        self.account_manager.save_account(account)
        return account
    
    def change_password(
        self,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        Change le mot de passe d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            old_password: Ancien mot de passe
            new_password: Nouveau mot de passe
            
        Returns:
            True si le changement a réussi
            
        Raises:
            AuthenticationError: Si l'ancien mot de passe est incorrect
        """
        account = self.account_manager.load_account_by_id(user_id)
        if not account:
            raise AuthenticationError("Utilisateur non trouvé")
        
        # Vérifie l'ancien mot de passe
        if not self.password_hasher.verify_password(old_password, account.salt, account.password_hash):
            raise AuthenticationError("Ancien mot de passe incorrect")
        
        # Valide le nouveau mot de passe
        if not self._is_valid_password(new_password):
            raise AuthenticationError(
                "Le nouveau mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule et un chiffre"
            )
        
        # Hash le nouveau mot de passe
        new_salt = self.password_hasher.generate_salt()
        new_hash = self.password_hasher.hash_password(new_password, new_salt)
        
        account.salt = new_salt
        account.password_hash = new_hash
        
        self.account_manager.save_account(account)
        return True
    
    def delete_account(self, user_id: str, password: str) -> bool:
        """
        Supprime un compte utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            password: Mot de passe pour confirmation
            
        Returns:
            True si la suppression a réussi
            
        Raises:
            AuthenticationError: Si le mot de passe est incorrect
        """
        account = self.account_manager.load_account_by_id(user_id)
        if not account:
            raise AuthenticationError("Utilisateur non trouvé")
        
        # Vérifie le mot de passe
        if not self.password_hasher.verify_password(password, account.salt, account.password_hash):
            raise AuthenticationError("Mot de passe incorrect")
        
        # Invalide toutes les sessions de cet utilisateur
        tokens_to_remove = [
            token for token, session in self.active_sessions.items()
            if session.user_id == user_id
        ]
        for token in tokens_to_remove:
            del self.active_sessions[token]
        
        # Supprime le compte
        return self.account_manager.delete_account(user_id)
    
    def _create_session(self, user_id: str, duration_hours: int = 24) -> str:
        """Crée un token de session pour un utilisateur"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=duration_hours)
        
        session = SessionToken(user_id, token, expires_at)
        self.active_sessions[token] = session
        
        return token
    
    def _generate_user_id(self) -> str:
        """Génère un ID utilisateur unique"""
        return f"user_{secrets.token_urlsafe(16)}"
    
    def _is_valid_email(self, email: str) -> bool:
        """Valide un email (validation simple)"""
        return '@' in email and '.' in email.split('@')[1]
    
    def _is_valid_password(self, password: str) -> bool:
        """
        Valide un mot de passe
        Doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre
        """
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_upper and has_lower and has_digit
    
    def get_stats(self) -> Dict:
        """Obtient des statistiques sur le système d'authentification"""
        all_accounts = self.account_manager.list_all_accounts()
        active_sessions = [s for s in self.active_sessions.values() if s.is_valid()]
        
        return {
            'total_users': len(all_accounts),
            'active_users': len([a for a in all_accounts if a.is_active]),
            'verified_users': len([a for a in all_accounts if a.is_verified]),
            'active_sessions': len(active_sessions),
            'users_with_data_consent': len([a for a in all_accounts if a.data_sharing_consent])
        }

