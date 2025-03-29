from flask import Flask, render_template, request, redirect, url_for, flash, session
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import re
from typing import List, Dict
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "corporate-mail-pro-secret-123")
app.config['SESSION_TYPE'] = 'filesystem'

# SMTP Server configuration (can be set in .env)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

# Default email details
DEFAULT_SUBJECT = "Important Company Update"
DEFAULT_BODY = """\
Dear Team,

I hope this message finds you well.

This is an important update regarding our current initiatives. Please review the information below carefully and let me know if you have any questions or require clarification.

Key Points:
- [Point 1]
- [Point 2]
- [Point 3]

Action Items:
- [Action 1]
- [Action 2]

Timeline:
- [Date/Milestone]

Thank you for your attention to this matter.

Best regards,
[Your Name]
[Your Position]
[Your Company]
"""

def validate_emails(emails: List[str]) -> bool:
    """Validate all email addresses in the list"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return all(re.match(pattern, email) for email in emails)

def send_bulk_email(sender_name: str, sender_email: str, sender_password: str, subject: str, body: str, recipients: List[str]) -> Dict:
    """Send email to multiple recipients with comprehensive error handling"""
    # Validation checks
    if not recipients:
        return {"status": "error", "message": "No recipients specified"}
    
    if not validate_emails(recipients):
        return {"status": "error", "message": "One or more email addresses are invalid"}
    
    if not validate_emails([sender_email]):
        return {"status": "error", "message": "Sender email address is invalid"}
    
    if not subject.strip():
        return {"status": "error", "message": "Email subject cannot be empty"}
    
    if not body.strip():
        return {"status": "error", "message": "Email body cannot be empty"}
    
    if not sender_password.strip():
        return {"status": "error", "message": "SMTP password is required"}

    # Prepare email message
    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        # Store sent emails in session
        if 'sent_emails' not in session:
            session['sent_emails'] = []
        
        session['sent_emails'].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": f"{sender_name} <{sender_email}>",
            "subject": subject,
            "recipients": recipients,
            "body": body
        })
        
        return {
            "status": "success",
            "message": f"Email successfully sent to {len(recipients)} recipient(s) as {sender_name}",
            "recipients": recipients
        }
    except smtplib.SMTPAuthenticationError:
        return {"status": "error", "message": "Authentication failed - please check your email credentials"}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "error", "message": "Server rejected recipient addresses"}
    except smtplib.SMTPSenderRefused:
        return {"status": "error", "message": "Server rejected sender address"}
    except smtplib.SMTPException as e:
        return {"status": "error", "message": f"SMTP error occurred: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender_name = request.form.get("senderName", "").strip()
        sender_email = request.form.get("senderEmail", "").strip()
        sender_password = request.form.get("senderPassword", "").strip()
        subject = request.form.get("subject", "").strip()
        body = request.form.get("body", "").strip()
        recipients = request.form.getlist("recipients")
        
        # Filter out any empty strings and strip whitespace
        recipients = [email.strip() for email in recipients if email.strip()]
        
        result = send_bulk_email(sender_name, sender_email, sender_password, subject, body, recipients)
        
        if result['status'] == "success":
            flash(result['message'], "success")
            return render_template(
                "index.html",
                sender_name=sender_name,
                sender_email=sender_email,
                subject=subject,
                body=body,
                last_recipients=result['recipients']
            )
        else:
            flash(result['message'], "error")
            return render_template(
                "index.html",
                sender_name=sender_name,
                sender_email=sender_email,
                subject=subject,
                body=body,
                recipients=recipients
            )

    return render_template(
        "index.html",
        sender_name="",
        sender_email="",
        subject=DEFAULT_SUBJECT,
        body=DEFAULT_BODY,
        recipients=[]
    )

@app.route('/sent-emails')
def sent_emails():
    if 'sent_emails' not in session:
        return {"sent_emails": []}
    return {"sent_emails": session['sent_emails']}

if __name__ == "__main__":
    app.run(debug=True)