from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json, os
from .core.security import hash_pwd, verify_pwd, create_token

USERS_FILE = os.path.join(os.path.dirname(__file__), "models", "users.json")
router = APIRouter(prefix="/auth", tags=["Auth"])

class UserIn(BaseModel):
    username: str
    password: str

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    return json.load(open(USERS_FILE))

def save_users(users):
    json.dump(users, open(USERS_FILE, "w"), indent=2)

@router.post("/register")
def register(data: UserIn):
    users = load_users()
    if any(u["username"] == data.username for u in users):
        raise HTTPException(400, "Usuario ya existe")
    users.append({"username": data.username, "password": hash_pwd(data.password)})
    save_users(users)
    return {"msg": "Usuario creado"}

@router.post("/login")
def login(data: UserIn):
    users = load_users()
    user = next((u for u in users if u["username"] == data.username), None)
    if not user or not verify_pwd(data.password, user["password"]):
        raise HTTPException(400, "Credenciales inválidas")
    token = create_token(data.username)
    return {"token": token}
