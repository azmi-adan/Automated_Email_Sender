import smtplib  # Module to send emails using SMTP
import os  # Module to access environment variables
from email.message import EmailMessage  # Class to create an email message
from dotenv import load_dotenv  # Module to load environment variables from a .env file

# Load environment variables from .env file
load_dotenv()

# Get email credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Your email password or app password

# List of recipients (people who will receive the email)
recipients = ["azmi.harar@student.moringaschool.com", "azmi.adan2024@gmail.com"]

# Email subject (title of the email)
subject = "Important Update"

# Email body (content of the email)
body = """\
Dear Team,

I hope this email finds you well.

This is just a quick update regarding our ongoing projects. Please let me know if you have any questions.

Best Regards,  
Azmi Adan
"""

def send_bulk_email():
    """Function to send an email to multiple recipients"""
    
    # Create an email message object
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS  # Sender's email address
    msg["To"] = ", ".join(recipients)  # Convert list of recipients into a string
    msg["Subject"] = subject  # Set the subject of the email
    msg.set_content(body)  # Set the body/content of the email

    try:
        # Connect to Gmail's SMTP server using SSL encryption
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Log in using credentials
            server.send_message(msg)  # Send the email
        print("✅ Email sent successfully!")  # Print success message

    except Exception as e:
        # If an error occurs, print the error message
        print(f"❌ Error sending email: {e}")

# Call the function to send the email
send_bulk_email()
