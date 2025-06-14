# # routes/recipes.py

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.models.recipe_model import Recipe
# from app.schemas.recipe_schema import RecipeCreate, RecipeOut, RecipeUpdate
# from app.db.session import get_db

# router = APIRouter(prefix="/recipes", tags=["Recipes"])

# @router.post("/", response_model=RecipeOut)
# def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
#     ...

# @router.get("/", response_model=list[RecipeOut])
# def get_all_recipes(db: Session = Depends(get_db)):
#     ...

# @router.get("/{recipe_id}", response_model=RecipeOut)
# def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
#     ...

# @router.put("/{recipe_id}", response_model=RecipeOut)
# def update_recipe(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
#     ...

# @router.delete("/{recipe_id}")
# def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
#     ...
