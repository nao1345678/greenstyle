from beanie import Document
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- INPUT SCHEMA (JSON body) ----
class UserCreate(BaseModel):
    username: str
    firstname: str
    email: EmailStr
    password: str

    def hash_password(self):
        self.password = pwd_context.hash(self.password)

# ---- DOCUMENT stored in DB ----
class User(Document):
    username: str
    firstname: str
    email: EmailStr
    password: str

    class Settings:
        name = "users"  # matches Mongo collection

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
