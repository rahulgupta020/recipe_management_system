# # routes/categories_router.py

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.models.category_model import Category
# from app.schemas.category_schema import CategoryCreate, CategoryOut, CategoryUpdate
# from app.db.session import get_db

# router = APIRouter(prefix="/categories", tags=["Categories"])

# @router.post("/", response_model=CategoryOut)
# def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
#     ...

# @router.get("/", response_model=list[CategoryOut])
# def get_all_categories(db: Session = Depends(get_db)):
#     ...

# @router.get("/{category_id}", response_model=CategoryOut)
# def get_category(category_id: int, db: Session = Depends(get_db)):
#     ...

# @router.put("/{category_id}", response_model=CategoryOut)
# def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
#     ...

# @router.delete("/{category_id}")
# def delete_category(category_id: int, db: Session = Depends(get_db)):
#     ...

# @router.get("/search", response_model=list[CategoryOut])
# def search_categories(name: str, db: Session = Depends(get_db)):
#     """
#     Search for categories by name.
#     """
#     return db.query(Category).filter(Category.name.ilike(f"%{name}%")).all()

# @router.get("/count", response_model=int)
# def count_categories(db: Session = Depends(get_db)):
#     """
#     Count the total number of categories.
#     """
#     return db.query(Category).count()

# @router.get("/top", response_model=list[CategoryOut])
# def get_top_categories(limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Get the top categories by the number of recipes.
#     """
#     return db.query(Category).order_by(Category.recipe_count.desc()).limit(limit).all()

# @router.get("/recent", response_model=list[CategoryOut])
# def get_recent_categories(limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Get the most recently created categories.
#     """
#     return db.query(Category).order_by(Category.created_at.desc()).limit(limit).all()

# @router.get("/popular", response_model=list[CategoryOut])
# def get_popular_categories(limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Get the most popular categories based on the number of recipes.
#     """
#     return db.query(Category).order_by(Category.popularity.desc()).limit(limit).all()

# @router.get("/related/{category_id}", response_model=list[CategoryOut])
# def get_related_categories(category_id: int, db: Session = Depends(get_db)):
#     """
#     Get categories related to a specific category.
#     """
#     category = db.query(Category).filter(Category.id == category_id).first()
#     if not category:
#         return []
    
#     # Assuming related categories are determined by some logic, e.g., shared recipes
#     return db.query(Category).filter(Category.id != category_id).all()  

# @router.get("/by-recipe/{recipe_id}", response_model=list[CategoryOut])
# def get_categories_by_recipe(recipe_id: int, db: Session = Depends(get_db)):
#     """
#     Get categories associated with a specific recipe.
#     """
#     # Assuming a many-to-many relationship between recipes and categories
#     return db.query(Category).join(Category.recipes).filter(Recipe.id == recipe_id).all()   

# @router.get("/by-user/{user_id}", response_model=list[CategoryOut])
# def get_categories_by_user(user_id: int, db: Session = Depends(get_db)):
#     """
#     Get categories created by a specific user.
#     """
#     return db.query(Category).filter(Category.created_by == user_id).all()

# @router.get("/by-date", response_model=list[CategoryOut])
# def get_categories_by_date(start_date: str, end_date: str, db: Session = Depends(get_db)):
#     """
#     Get categories created within a specific date range.
#     """
#     return db.query(Category).filter(Category.created_at.between(start_date, end_date)).all()   

# @router.get("/by-popularity", response_model=list[CategoryOut])
# def get_categories_by_popularity(min_popularity: int, db: Session = Depends(get_db)):
#     """
#     Get categories with a minimum popularity score.
#     """
#     return db.query(Category).filter(Category.popularity >= min_popularity).all()

# @router.get("/by-recipe-count", response_model=list[CategoryOut])
# def get_categories_by_recipe_count(min_count: int, db: Session = Depends(get_db)):
#     """
#     Get categories with a minimum number of associated recipes.
#     """
#     return db.query(Category).filter(Category.recipe_count >= min_count).all()  

# @router.get("/by-name", response_model=list[CategoryOut])
# def get_categories_by_name(name: str, db: Session = Depends(get_db)):
#     """
#     Get categories by name.
#     """
#     return db.query(Category).filter(Category.name.ilike(f"%{name}%")).all()    


# @router.get("/by-description", response_model=list[CategoryOut])
# def get_categories_by_description(description: str, db: Session = Depends(get_db)):
#     """
#     Get categories by description.
#     """
#     return db.query(Category).filter(Category.description.ilike(f"%{description}%")).all()  

# @router.get("/by-tags", response_model=list[CategoryOut])
# def get_categories_by_tags(tags: str, db: Session = Depends(get_db)):
#     """
#     Get categories by tags.
#     """
#     tag_list = tags.split(",")
#     return db.query(Category).filter(Category.tags.any(tag.in_(tag_list))).all()

# @router.get("/by-attributes", response_model=list[CategoryOut])
# def get_categories_by_attributes(attributes: str, db: Session = Depends(get_db)):
#     """
#     Get categories by attributes.
#     """
#     attribute_list = attributes.split(",")
#     return db.query(Category).filter(Category.attributes.any(attribute.in_(attribute_list))).all()

# @router.get("/by-ingredients", response_model=list[CategoryOut])
# def get_categories_by_ingredients(ingredients: str, db: Session = Depends(get_db)):
#     """
#     Get categories by ingredients.
#     """
#     ingredient_list = ingredients.split(",")
#     return db.query(Category).filter(Category.ingredients.any(ingredient.in_(ingredient_list))).all()