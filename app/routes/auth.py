# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, APIResponse
from app.auth.auth_handler import get_password_hash, verify_password, create_access_token
from app.models.user_model import UserModel
from app.auth.auth_bearer import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()
    if existing_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error",
            "message": "Username or email already registered",
            "data": None
        }

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }

@router.post("/login", response_model=APIResponse)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": "error",
            "message": "Invalid username or password",
            "data": None
        }
    access_token = create_access_token(data={"sub": db_user.username})
    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }
