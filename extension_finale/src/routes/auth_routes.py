from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from models.user import User, UserOut
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=UserOut)
async def login(payload: LoginRequest) -> UserOut:
    """Authentifie un utilisateur avec email et mot de passe"""
    # Chercher l'utilisateur par email
    user = await User.find_one(User.email == payload.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Vérifier le mot de passe
    if not user.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Retourner les informations de l'utilisateur (sans le mot de passe)
    return UserOut(id=str(user.id), username=user.username, firstname=user.firstname, email=user.email)


@router.get("/me", response_model=Optional[UserOut])
async def get_current_user(user_id: Optional[str] = None) -> Optional[UserOut]:
    """Récupère les informations de l'utilisateur connecté (pour vérification)"""
    if not user_id:
        return None
    
    try:
        from beanie import PydanticObjectId
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            return None
        return UserOut(id=str(user.id), username=user.username, firstname=user.firstname, email=user.email)
    except Exception:
        return None

