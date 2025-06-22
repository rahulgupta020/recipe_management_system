import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SES_EMAIL_FROM = 'kajalrg1999@gmail.com'


ses = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY

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
