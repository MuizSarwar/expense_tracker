from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserRegister
from security import pwd_context, authenticate_user, create_access_token

from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Authentication"])







#--------------------------------------------------------------------------------------------------------------------
# dependency
#--------------------------------------------------------------------------------------------------------------------

db_dependency = Annotated[Session, Depends(get_db)]






#--------------------------------------------------------------------------------------------------------------------
# Authentication Endpoints
#--------------------------------------------------------------------------------------------------------------------

#------------------------>
# User Registration
#------------------------>
@router.post('/register', status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRegister, db: db_dependency):

    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    
    # Create user
    user_model = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=pwd_context.hash(user_data.password)
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)  

    return JSONResponse(status_code=201, content={"message": "New user created successfully"})






#------------------------>
# User Login
#------------------------>
@router.post('/login')
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(user.username, user.id)
    return {"access_token": token, "token_type": "bearer"}