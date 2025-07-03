# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, APIResponse, VerifyOtpRequest, ResendOtpRequest, ResetPasswordRequest, ConfirmResetPassword
from app.auth.auth_handler import get_password_hash, verify_password, create_access_token
from app.models.user_model import UserModel
from app.auth.auth_bearer import get_db
from app.utils.email_service import email_service
from fastapi import Body
from datetime import datetime, timedelta, timezone
from app.config import OTP_EXPIRY_MINUTES
from sqlalchemy import or_
import random

router = APIRouter(prefix="/auth", tags=["auth"])

def generate_otp():
    return str(random.randint(100000, 999999))

def is_otp_expired(otp_created_at):
    """Check if OTP has expired"""
    if not otp_created_at:
        return True
    
    # Get current time in UTC
    current_time = datetime.now(timezone.utc)
    
    # Ensure otp_created_at is timezone-aware
    if otp_created_at.tzinfo is None:
        # If stored datetime is naive, assume it's UTC
        otp_created_at = otp_created_at.replace(tzinfo=timezone.utc)
    
    expiry_time = otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES)
    return current_time > expiry_time


@router.post("/register", response_model=APIResponse)
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

    otp = generate_otp()
    otp_created_at = datetime.now()

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        is_active=False,
        otp=otp,
        otp_created_at= otp_created_at
    )

    try:
        # Save user to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Send OTP email using email service
        email_sent = email_service.send_otp_email(
            to_email=user.email,
            otp=otp,
            username=user.username
        )
        
        if email_sent:
            response.status_code = status.HTTP_202_ACCEPTED
            return {
                "status": "success",
                "message": f"OTP sent to your email. Valid for {OTP_EXPIRY_MINUTES} minutes.",
                "data": {
                    "user_id": new_user.user_id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "otp_expires_in_minutes": OTP_EXPIRY_MINUTES
                }
            }
        else:
            # Email failed, but user is created
            response.status_code = status.HTTP_201_CREATED
            return {
                "status": "warning",
                "message": f"User created but email failed to send. Your OTP is: {otp}",
                "data": {
                    "user_id": new_user.user_id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "otp": otp,
                    "otp_expires_in_minutes": OTP_EXPIRY_MINUTES
                }
            }
            
    except Exception as e:
        # Rollback if something goes wrong
        db.rollback()
        print(f"Registration error: {e}")
        
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Registration failed. Please try again.",
            "data": None
        }


@router.post("/verify-otp", response_model=APIResponse)
def verify_otp(payload: VerifyOtpRequest, response: Response, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == payload.user_id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }

    # Check if OTP exists
    if not user.otp:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error",
            "message": "No OTP found. Please request a new OTP.",
            "data": None
        }
    
    # Check if OTP has expired
    if is_otp_expired(user.otp_created_at):
        # Clear expired OTP
        user.otp = None
        user.otp_created_at = None
        db.commit()

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error",
            "message": "OTP has expired. Please request a new OTP.",
            "data": None
        }
    
    # Verify OTP
    if user.otp != payload.otp:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": "error",
            "message": "Invalid OTP",
            "data": None
        }

    # OTP is valid, activate user and clear OTP
    user.is_active = True
    user.otp = None
    user.otp_created_at = None
    db.commit()
    
    # # ✅ Send welcome email directly here
    # email_service.send_welcome_email(
    #     to_email=user.email,
    #     username=user.username
    # )

    # Using background_tasks
    background_tasks.add_task(
        email_service.send_welcome_email,
        to_email=user.email,
        username=user.username
    )


    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "Email verified successfully. You are now registered!",
        "data": {
            "user_id": user.user_id,
            "username": user.username
        }
    }

@router.post("/resend-otp", response_model=APIResponse)
def resend_otp(payload: ResendOtpRequest, response: Response, db: Session = Depends(get_db)):
    """
    Resend OTP to user email
    """
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }
    
    if user.is_active:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error", 
            "message": "Account is already verified",
            "data": None
        }
    
    # Generate new OTP
    new_otp = generate_otp()
    user.otp = new_otp
    user.otp_created_at = datetime.now()
    db.commit()
    
    # Send email using email service
    email_sent = email_service.send_otp_email(
        to_email=user.email,
        otp=new_otp,
        username=user.username
    )
    
    if email_sent:
        response.status_code = status.HTTP_200_OK
        return {
            "status": "success",
            "message": f"New OTP sent to your email. Valid for {OTP_EXPIRY_MINUTES} minutes.",
            "data": {
                "otp_expires_in_minutes": OTP_EXPIRY_MINUTES
            }
        }
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Failed to send email. Please try again.",
            "data": None
        }

@router.post("/reset-password/request", response_model=APIResponse)
def reset_password_request(payload: ResetPasswordRequest, response: Response, background_tasks:BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found with this email",
            "data": None
        }

    # Generate new OTP
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = datetime.now()
    db.commit()

    background_tasks.add_task(
        email_service.send_otp_email,
        to_email=user.email,
        otp=otp,
        username=user.username
    )

    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": f"Reset OTP sent to your email. Valid for {OTP_EXPIRY_MINUTES} minutes.",
        "data": None
    }

@router.post("/reset-password/confirm", response_model=APIResponse)
def confirm_reset_password(payload: ConfirmResetPassword, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "message": "User not found",
            "data": None
        }

    # Validate OTP
    if not user.otp or user.otp != payload.otp:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": "error",
            "message": "Invalid OTP",
            "data": None
        }

    if is_otp_expired(user.otp_created_at):
        user.otp = None
        user.otp_created_at = None
        db.commit()

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error",
            "message": "OTP has expired. Please request a new one.",
            "data": None
        }

    # Set new password and clear OTP
    user.password_hash = get_password_hash(payload.new_password)
    user.otp = None
    user.otp_created_at = None
    db.commit()

    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "Password has been reset successfully",
        "data": None
    }

@router.post("/login", response_model=APIResponse)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(
        or_(
            UserModel.username == user.username,
            UserModel.email == user.username  # using username field for both
        )
    ).first()

    if not db_user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": "error",
            "message": "Invalid username or password",
            "data": None
        }

    if not verify_password(user.password, db_user.password_hash):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "status": "error",
            "message": "Invalid username or password",
            "data": None
        }

    if not db_user.is_active:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "status": "error",
            "message": "Please verify your email before logging in",
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

@router.post("/logout", response_model=APIResponse)
def logout(response: Response): 
    response.status_code = status.HTTP_200_OK
    return {
        "status": "success",
        "message": "Logout successful",
        "data": None
    }