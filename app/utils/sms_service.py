# app/utils/sms_service.py

from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp_sms(phone_number: str, otp: str):
    message = client.messages.create(
        body=f"Your OTP for Recipe App is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number  # Use E.164 format (e.g., +919876543210)
    )
    return message.sid
