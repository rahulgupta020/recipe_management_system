import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_gmail(sender_email, sender_password, to_email, subject, body):
    """
    Send email using Gmail SMTP
    Note: You need to enable "App Passwords" in Gmail for this to work
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    send_email_gmail(
        sender_email="coolrahulg95@gmail.com",
        sender_password="oftt xdxi lzsw szyr",  # Not your regular password!
        to_email="coolrahulb1995@gmail.com",
        subject="Test Email from Python",
        body="Hello! This is a test email sent from Python."
    )
