# app/utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
from app.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_ENABLED

class EmailService:
    """
    Email service for sending various types of emails
    """
    
    def __init__(self):
        self.sender_email = EMAIL_SENDER
        self.sender_password = EMAIL_PASSWORD
        self.enabled = EMAIL_ENABLED
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Private method to send email using Gmail SMTP
        """
        if not self.enabled:
            print(f"Email disabled. Would send to {to_email}: {subject}")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP configuration
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Enable security
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.sender_email, to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_otp_email(self, to_email: str, otp: str, username: str) -> bool:
        """
        Send OTP verification email
        """
        subject = "Verify Your Account - Recipe Management System"
        
        body = f"""
Hi {username},

Welcome to Recipe Management System!

Your verification OTP is: {otp}

Please enter this OTP to complete your registration.

This OTP will expire in 10 minutes for security reasons.

If you didn't create this account, please ignore this email.

Best regards,
Recipe Management Team
        """
        
        return self._send_email(to_email, subject, body.strip())
    
    def send_password_reset_email(self, to_email: str, reset_token: str, username: str) -> bool:
        """
        Send password reset email
        """
        subject = "Password Reset - Recipe Management System"
        
        # You can create a proper reset URL here
        reset_url = f"http://localhost:8000/reset-password?token={reset_token}"
        
        body = f"""
Hi {username},

You requested a password reset for your Recipe Management System account.

Click the link below to reset your password:
{reset_url}

Or use this reset code: {reset_token}

This link will expire in 1 hour for security reasons.

If you didn't request this reset, please ignore this email.

Best regards,
Recipe Management Team
        """
        
        return self._send_email(to_email, subject, body.strip())
    
    def send_welcome_email1(self, to_email: str, username: str) -> bool:      
        """
        Send welcome email after successful registration
        """
        subject = "Welcome to Recipe Management System!"
        
        body = f"""
Hi {username},

Welcome to Recipe Management System! 🍳

Your account has been successfully verified and you can now:
- Save your favorite recipes
- Create custom recipe collections
- Share recipes with friends
- Discover new delicious recipes

Start exploring: http://localhost:8000

Happy cooking!

Best regards,
Recipe Management Team
        """
        
        return self._send_email(to_email, subject, body.strip())

    def send_welcome_email(self, to_email: str, username: str) -> bool:
        print("send_welcome_email called")
        """
        Send welcome email after successful registration
        """
        subject = "Welcome to Recipe Management System!"

        body = f"""
    Hi {username},

    Welcome to Recipe Management System! 🍳

    Your account has been successfully verified and you can now:
    - Save your favorite recipes
    - Create custom recipe collections
    - Share recipes with friends
    - Discover new delicious recipes

    Start exploring: http://localhost:8000

    Happy cooking!

    Best regards,
    Recipe Management Team
        """

        return self._send_email(to_email, subject, body.strip())


# Create a global instance
email_service = EmailService()