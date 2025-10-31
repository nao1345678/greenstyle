"""
Modèle de compte utilisateur pour l'authentification et la gestion des profils
Lie les comptes utilisateur aux préférences d'IA
"""

import hashlib
import secrets
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path


@dataclass
class UserAccount:
    """
    Représente un compte utilisateur avec authentification
    """
    user_id: str  # Identifiant unique généré automatiquement
    email: str  # Email pour la connexion
    username: str  # Nom d'affichage
    password_hash: str  # Hash du mot de passe (jamais le mot de passe en clair)
    salt: str  # Salt pour le hachage
    
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    # Informations de profil optionnelles
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    
    # Paramètres de confidentialité
    data_sharing_consent: bool = False
    marketing_consent: bool = False
    
    # Métadonnées
    is_active: bool = True
    is_verified: bool = False
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire pour sauvegarde"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'country': self.country,
            'data_sharing_consent': self.data_sharing_consent,
            'marketing_consent': self.marketing_consent,
            'is_active': self.is_active,
            'is_verified': self.is_verified
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Charge depuis un dictionnaire"""
        account = cls(
            user_id=data['user_id'],
            email=data['email'],
            username=data['username'],
            password_hash=data['password_hash'],
            salt=data['salt']
        )
        
        if 'created_at' in data:
            account.created_at = datetime.fromisoformat(data['created_at'])
        if 'last_login' in data and data['last_login']:
            account.last_login = datetime.fromisoformat(data['last_login'])
        
        account.first_name = data.get('first_name')
        account.last_name = data.get('last_name')
        account.age = data.get('age')
        account.gender = data.get('gender')
        account.country = data.get('country')
        account.data_sharing_consent = data.get('data_sharing_consent', False)
        account.marketing_consent = data.get('marketing_consent', False)
        account.is_active = data.get('is_active', True)
        account.is_verified = data.get('is_verified', False)
        
        return account
    
    def update_last_login(self):
        """Met à jour la date de dernière connexion"""
        self.last_login = datetime.now()
    
    def get_public_profile(self) -> Dict:
        """Retourne les informations publiques du profil (sans données sensibles)"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'created_at': self.created_at.isoformat(),
            'is_verified': self.is_verified
        }
    
    def get_full_profile(self) -> Dict:
        """Retourne le profil complet (pour l'utilisateur lui-même)"""
        profile = self.get_public_profile()
        profile.update({
            'email': self.email,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'country': self.country,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'data_sharing_consent': self.data_sharing_consent,
            'marketing_consent': self.marketing_consent
        })
        return profile


class PasswordHasher:
    """
    Gère le hachage sécurisé des mots de passe
    """
    
    @staticmethod
    def generate_salt() -> str:
        """Génère un salt aléatoire"""
        return secrets.token_hex(32)
    
    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """
        Hash un mot de passe avec un salt
        Utilise SHA-256 avec plusieurs itérations pour la sécurité
        """
        # Combine le mot de passe et le salt
        salted_password = (password + salt).encode('utf-8')
        
        # Hash avec plusieurs itérations pour ralentir les attaques
        hashed = salted_password
        for _ in range(10000):
            hashed = hashlib.sha256(hashed).digest()
        
        return hashed.hex()
    
    @staticmethod
    def verify_password(password: str, salt: str, password_hash: str) -> bool:
        """Vérifie qu'un mot de passe correspond au hash"""
        computed_hash = PasswordHasher.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, password_hash)


class UserAccountManager:
    """
    Gère les comptes utilisateurs (stockage, récupération)
    """
    
    def __init__(self, accounts_dir: str = 'user_accounts'):
        """
        Args:
            accounts_dir: Répertoire pour stocker les comptes
        """
        self.accounts_dir = Path(accounts_dir)
        self.accounts_dir.mkdir(exist_ok=True)
        
        # Index email -> user_id pour recherche rapide
        self.email_index_file = self.accounts_dir / '_email_index.json'
        self.email_index = self._load_email_index()
    
    def _load_email_index(self) -> Dict[str, str]:
        """Charge l'index email -> user_id"""
        if self.email_index_file.exists():
            with open(self.email_index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_email_index(self):
        """Sauvegarde l'index email -> user_id"""
        with open(self.email_index_file, 'w') as f:
            json.dump(self.email_index, f, indent=2)
    
    def save_account(self, account: UserAccount):
        """Sauvegarde un compte utilisateur"""
        account_file = self.accounts_dir / f"{account.user_id}.json"
        with open(account_file, 'w') as f:
            json.dump(account.to_dict(), f, indent=2)
        
        # Met à jour l'index email
        self.email_index[account.email.lower()] = account.user_id
        self._save_email_index()
    
    def load_account_by_id(self, user_id: str) -> Optional[UserAccount]:
        """Charge un compte par son ID"""
        account_file = self.accounts_dir / f"{user_id}.json"
        if not account_file.exists():
            return None
        
        with open(account_file, 'r') as f:
            data = json.load(f)
        
        return UserAccount.from_dict(data)
    
    def load_account_by_email(self, email: str) -> Optional[UserAccount]:
        """Charge un compte par email"""
        email_lower = email.lower()
        if email_lower not in self.email_index:
            return None
        
        user_id = self.email_index[email_lower]
        return self.load_account_by_id(user_id)
    
    def email_exists(self, email: str) -> bool:
        """Vérifie si un email est déjà utilisé"""
        return email.lower() in self.email_index
    
    def delete_account(self, user_id: str) -> bool:
        """Supprime un compte"""
        account = self.load_account_by_id(user_id)
        if not account:
            return False
        
        # Supprime le fichier
        account_file = self.accounts_dir / f"{user_id}.json"
        if account_file.exists():
            account_file.unlink()
        
        # Met à jour l'index
        if account.email.lower() in self.email_index:
            del self.email_index[account.email.lower()]
            self._save_email_index()
        
        return True
    
    def list_all_accounts(self) -> list:
        """Liste tous les comptes (pour administration)"""
        accounts = []
        for account_file in self.accounts_dir.glob('*.json'):
            if account_file.name != '_email_index.json':
                with open(account_file, 'r') as f:
                    data = json.load(f)
                    accounts.append(UserAccount.from_dict(data))
        return accounts

