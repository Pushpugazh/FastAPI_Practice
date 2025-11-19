from datetime import datetime, timedelta
# from http.client import HTTPException

from fastapi import Depends, HTTPException
from fastapi.openapi.utils import status_code_ranges
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
SECRET_KEY = "erchiaphfqbmnbvaqphjkaf"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(expires_delta)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = payload.get("userName")
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")
        return {"username": user}

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
