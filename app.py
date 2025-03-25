from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Default email details
default_subject = "Important Update"
default_body = """\
Dear Team,

I hope this email finds you well.

This is just a quick update regarding our ongoing projects. Please let me know if you have any questions.

Best Regards,  
Azmi Adan
"""
default_recipients = ["phoebe@angani.co", "azmi.adan2024@gmail.com"]

def send_bulk_email(subject, body, recipients):
    """Function to send an email to multiple recipients"""
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error sending email: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form.get("subject", default_subject)
        body = request.form.get("body", default_body)
        recipients = request.form.getlist("recipients")

        if not recipients:
            flash("❌ Please add at least one recipient.")
            return redirect(url_for("index"))

        message = send_bulk_email(subject, body, recipients)
        flash(message)
        return redirect(url_for("index"))

    return render_template("index.html", subject=default_subject, body=default_body, recipients=default_recipients)

if __name__ == "__main__":
    app.run(debug=True)
