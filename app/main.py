# # main.py

# from fastapi import FastAPI
# from app.routes import auth, users_router, recipes_router, categories_router
# from starlette.middleware.sessions import SessionMiddleware
# import os
# from dotenv import load_dotenv

# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     SessionMiddleware,
#     secret_key=os.getenv("SECRET_KEY")
# )

# from app.routes.social_auth_router import router as social_auth_router
# app.include_router(social_auth_router)

# app.include_router(auth.router)
# app.include_router(users_router.router)
# # app.include_router(recipes_router.router)
# # app.include_router(categories_router.router)



import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = 'eu-north-1'
SES_EMAIL_FROM = 'kajalrg1999@gmail.com'

ses = boto3.client(
    "ses",
    region_name=AWS_REGION,
)

def send_email(to_email, subject, body):
    response = ses.send_email(
        Source=SES_EMAIL_FROM,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body}
            }
        }
    )
    print("Email sent! Message ID:", response['MessageId'])

# Example usage
send_email("kajalrg1999@gmail.com", "Test Email", "This is a test email from AWS SES")
