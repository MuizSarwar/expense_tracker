from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Optional

from models import User

load_dotenv()




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