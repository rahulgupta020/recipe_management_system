# main.py

from fastapi import FastAPI
from app.routes import auth, users_router, recipes_router, categories_router
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

from app.routes.social_auth_router import router as social_auth_router
app.include_router(social_auth_router)

app.include_router(auth.router)
app.include_router(users_router.router)
# app.include_router(recipes_router.router)
# app.include_router(categories_router.router)
