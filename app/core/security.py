from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt

SECRET = "supersecreto"
ALG    = "HS256"
EXP_H  = 2  # token válido 2 h

def hash_pwd(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_pwd(pwd: str, hashed: str) -> bool:
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def create_token(username: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=EXP_H)
    return jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALG)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALG])["sub"]
    except JWTError:
        return None
