# Automated Email Sender

## Overview
This script allows you to send bulk emails using Python's `smtplib` module and Gmail's SMTP server. It retrieves email credentials from environment variables for security and sends an email to multiple recipients.

## Features
- Sends emails using Gmail's SMTP server
- Uses environment variables to store credentials securely
- Sends a single email to multiple recipients
- Provides error handling for failed email deliveries

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required dependencies (listed below)

## Installation
1. Clone this repository:
   ```sh
   git clone <repository-url>
   cd Automated_Email_Sender
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your email credentials:
   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```
   > **Note:** If using Gmail, generate an [App Password](https://myaccount.google.com/apppasswords) instead of using your regular password.

## Usage
1. Open a terminal and navigate to the project directory.
2. Run the script:
   ```sh
   python3 email_sender.py
   ```

## Code Explanation
- **Imports Required Modules**: `smtplib`, `os`, `email.message.EmailMessage`, and `dotenv`.
- **Loads Environment Variables**: Retrieves email credentials from a `.env` file.
- **Defines Recipients & Email Content**: Specifies recipient list, subject, and body.
- **Creates `send_bulk_email` Function**:
  - Constructs an email message.
  - Logs into Gmail's SMTP server.
  - Sends the email.
- **Executes the Function**: Calls `send_bulk_email()` to send the email.

## Error Handling
If an error occurs during email sending, the script catches and prints the error message.

## Security Considerations
- Never hardcode credentials in the script.
- Always use `.env` to store sensitive information.
- Add `.env` to `.gitignore` to prevent accidental exposure.

## License
This project is open-source and available under the MIT License.

