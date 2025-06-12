# models/category_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="category", cascade="all, delete-orphan")
