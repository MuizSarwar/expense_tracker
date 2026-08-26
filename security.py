from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Optional,Annotated

from models import User
from database import get_db





load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")




SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)







#--------------------------------------------------------------------------------------------------------------------
# Authentication Function
#--------------------------------------------------------------------------------------------------------------------

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """
    Returns the User object if credentials are valid, otherwise None.
    HTTP-level error handling belongs in the router, not here.
    """
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None

    if not pwd_context.verify(password, user.hashed_password):
        return None

    return user







#--------------------------------------------------------------------------------------------------------------------
# Function for JWT token creation 
#--------------------------------------------------------------------------------------------------------------------

def create_access_token(username: str, user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)








#--------------------------------------------------------------------------------------------------------------------
# Function for varification JWT token and returning logged in users 
#--------------------------------------------------------------------------------------------------------------------

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user