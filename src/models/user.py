from beanie import Document
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    firstname: str
    email: EmailStr
    password: str

    def hash_password(self):
        self.password = pwd_context.hash(self.password)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    def hash_password(self):
        if self.password:
            self.password = pwd_context.hash(self.password)


# 👉 Schéma de sortie sans password
class UserOut(BaseModel):
    id: str
    username: str
    firstname: str
    email: EmailStr


class User(Document):
    username: str
    firstname: str
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
