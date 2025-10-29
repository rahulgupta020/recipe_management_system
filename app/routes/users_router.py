# routes/users_router.py

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.models.user_model import UserModel
from app.auth.auth_bearer import get_db, get_current_user
from app.schemas.user_schema import UserGetSchema, UserUpdateSchema
from app.schemas.user_schema import APIResponse
from typing import Union

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=APIResponse)
def get_all_users(response: Response, db: Session = Depends(get_db)):
    result = db.query(UserModel).all()
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "No users found",
            "data": None
        }
    
    users_data = [UserGetSchema.model_validate(user) for user in result]
    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "Users fetched successfully",
        "data": users_data
    }

@router.get("/{user_id}", response_model=APIResponse)
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }
    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": UserGetSchema.model_validate(result)
    }

@router.put("/{user_id}", response_model=APIResponse)
def update_user(user_id: int, payload: UserUpdateSchema, response: Response, db: Session = Depends(get_db)):
    result = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)

    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "User updated successfully",
        "data": UserGetSchema.model_validate(result)
    }

@router.delete("/{user_id}", response_model=APIResponse)
def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }
    db.delete(result)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "User deleted successfully",
        "data": UserGetSchema.model_validate(result)
    }

@router.get("/me", response_model=APIResponse)
def get_my_profile(
    response: Response,
    current_user: UserModel = Depends(get_current_user)
):
    user_data = UserGetSchema.model_validate(current_user)
    return {
        "status": "success",
        "message": "User profile fetched successfully",
        "data": user_data.dict(),
    }

@router.put("/me", response_model=APIResponse)
def update_my_profile(
    payload: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if payload.username:
        current_user.username = payload.username
    if payload.phone_number:
        current_user.phone_number = payload.phone_number
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    user_data = UserGetSchema.model_validate(current_user)

    return {
        "status": "success",
        "message": "Profile updated successfully",
        "data": user_data.dict(),
    }
