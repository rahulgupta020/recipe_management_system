# app/utils/whatsapp_service.py

from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
twilio_whatsapp_number = "whatsapp:+14155238886"  # Sandbox number

client = Client(account_sid, auth_token)

def send_otp_whatsapp(phone_number: str, otp: str):
    """
    Sends OTP via WhatsApp using Twilio.
    phone_number - e.g. '+919876543210'
    """
    message_body = f"Your OTP for registration is: {otp}"

    message = client.messages.create(
        from_=twilio_whatsapp_number,
        to=f"whatsapp:{phone_number}",
        body=message_body
    )

    print("WhatsApp SID:", message.sid)
