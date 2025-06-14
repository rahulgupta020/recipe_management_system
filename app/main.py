# main.py

from fastapi import FastAPI
from app.routes import auth, users_router, recipes_router, categories_router

app = FastAPI()

app.include_router(auth.router)
app.include_router(users_router.router)
# app.include_router(recipes_router.router)
# app.include_router(categories_router.router)



# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import text
# from app.db.session import SessionLocal

# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def home():
#     return {"message": "Welcome to Home page"}

# @app.get("/dummy/")
# def dummy_fun(db: Session = Depends(get_db)):
#     result = db.execute(text("SELECT * FROM dummy;"))
#     rows = result.fetchall()
#     return [dict(row._mapping) for row in rows]