Bulk Email Sender

A simple Python script for sending bulk emails through Gmail.

Features
Send personalized emails to a list of recipients (from a CSV file)
Uses Gmail SMTP
Delay between sends to avoid spam flags
Logs which emails sent successfully or failed
Setup
Clone the repo and install requirements:
bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   pip install -r requirements.txt
Turn on 2-Step Verification on your Google account, then create an App Password here: https://myaccount.google.com/apppasswords
Add your Gmail address and app password to a .env file:
env
   GMAIL_ADDRESS=you@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
Add your recipients to recipients.csv:
csv
   name,email
   Jane Doe,jane@example.com
   John Smith,john@example.com
Usage
bash
python send_bulk_email.py --recipients recipients.csv --template template.txt
Note

Only send to people who've agreed to receive emails from you, and follow anti-spam laws (e.g. CAN-SPAM, GDPR). Don't use this for spam.



   
