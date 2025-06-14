from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.models.user_model import UserModel, UserRole
from sqlalchemy.orm import Session
from app.auth.auth_bearer import get_db
from app.auth.auth_handler import create_access_token 

import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/auth", tags=["social-auth"])

# OAuth setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid email profile"}
)

# http://localhost:8000/auth/google/login
@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            resp = await oauth.google.get("userinfo", token=token)
            user_info = resp.json()

    except Exception as e:
        print(f"Error during Google OAuth callback: {e}")
        raise HTTPException(status_code=400, detail="Failed to login with Google")

    # Check or create user
    user = db.query(UserModel).filter(UserModel.email == user_info['email']).first()
    if not user:
        user = UserModel(
            username=user_info['name'],
            email=user_info['email'],
            role=UserRole.REGULAR,
            is_active=True,
            password_hash="social_login"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.email, "user_id": user.user_id})
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.user_id,
            "username": user.username,
            "email": user.email
        }
    }
