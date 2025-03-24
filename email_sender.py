import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# List of recipients
recipients = ["azmi.harar@student.moringaschool.com", "azmi.adan2024@gmail.com"]

# Email content
subject = "Important Update"
body = """\
Dear Team,

I hope this email finds you well. 

This is just a quick update regarding our ongoing projects. Please let me know if you have any questions.

Best Regards,  
Azmi Adan
"""

def send_bulk_email():
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Send email
send_bulk_email()
