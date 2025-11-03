from pydantic import BaseModel, EmailStr
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password_hash: str
    is_active: bool = True
