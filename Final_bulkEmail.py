# -*- coding: utf-8 -*-
"""
Created on Sun May 24 05:45:08 2026

@author: aaryan
"""

import smtplib
import os
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ─────────────────────────────────────────────
# ✏️  CONFIGURE THESE SETTINGS
# ─────────────────────────────────────────────

EXCEL_FILE  = "C:\\Users\\anous\\Downloads\\NSRO-4-ASISSE_Name_Wise.xlsx"
SHEET_NAME  = "PRAVEEN KUMAR2"

EMAIL_COLUMN      = "Email"
PDF_COLUMN        = "GSTIN"
ENTERPRISE_COLUMN = "Enterprise_Name"

PDF_FOLDER = r"C:\Users\anous\Downloads\Individual Notices"

SENDER_EMAIL    = "praveen_155@yahoo.co.in"
SENDER_PASSWORD = "aglbscnuzmubmcmy"
CC_EMAIL        = "praveen.kr68@gov.in"

EMAIL_SUBJECT = "ASISSE NOTICE 2026"
EMAIL_BODY    = """\
Dear Sir/Ma'am 

({company}),

Greetings from the National Statistical Office (NSO), Ministry of Statistics & Programme Implementation (MoSPI).


Please find attached the notice regarding submission of returns under the Annual Survey of Incorporated Service Sector Enterprises (ASISSE) including Trading for the Financials Year 2024-25.

The ASISSE survey is an important statistical initiative undertaken by MoSPI to collect reliable and comprehensive data on the services sector including trading. The information furnished by enterprises helps in:

1. Assessing the contribution of the services and trading sector to the economy,

2. Formulation of evidence-based government policies,

3. Estimation of Gross Domestics Products (GDP) / National Income and other macroeconomic indicators including engagement of workforce,

4. Supporting planning, research, and development activities.

Your cooperation in providing timely and accurate information is highly valuable and will contribute significantly to strengthening the national statistical system.

The enterprise may kindly login through the following portal to file the return:

https://ensd.esigma.mospi.gov.in/ASISSE/prod-survey/login


The login credentials have been mentioned in the attached Notice under Para No. 2.

You are requested to submit the return within the stipulated timeline mentioned in the notice i.e. One month w.e.f. 15.05.2026.

In case of any query or assistance, kindly contact the undersigned 

We look forward to your kind cooperation.


Thanks & Regards

Praveen Kumar 
SENIOR STATISTICAL OFFICER​
Ministry of Statistics & Programme Implementation
National Statistics Office (Field Operations Division)
Regional Office,4th Floor, A 2-3 Wing
CGO Complex, CBD Belapur
Navi Mumbai - 400614
Phone (O) : 022-27572217
Mob : 9868543720​​
Alternate Email ID : praveen.kr68@gov.in
"""

SMTP_SERVER  = "smtp.mail.yahoo.com"
SMTP_PORT    = 587
DELAY        = 5    # seconds between each email
BATCH_SIZE   = 7    # send 7 emails then pause
BATCH_PAUSE  = 300  # pause 5 minutes after every 7 emails

# ─────────────────────────────────────────────
# SCRIPT — no changes needed below this line
# ─────────────────────────────────────────────

def build_message(recipient, body, pdf_path):
    msg = MIMEMultipart()
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = recipient
    msg["Cc"]      = CC_EMAIL
    msg["Subject"] = EMAIL_SUBJECT
    msg.attach(MIMEText(body, "plain"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(pdf_path)}"
    )
    msg.attach(part)
    return msg


def send_batch(batch):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        for (i, email, company, pdf_path) in batch:
            try:
                personalized_body = EMAIL_BODY.format(company=company)
                msg = build_message(email, personalized_body, pdf_path)
                server.sendmail(SENDER_EMAIL, [email, CC_EMAIL], msg.as_string())
                print(f"  Row {i+2}: ✅ Sent to {email} ({company})")
                time.sleep(DELAY)
            except Exception as e:
                print(f"  Row {i+2}: ❌ Failed for {email} → {e}")


def main():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    if EMAIL_COLUMN not in df.columns or PDF_COLUMN not in df.columns:
        print(f"❌ Could not find columns '{EMAIL_COLUMN}' and/or '{PDF_COLUMN}'")
        print(f"   Columns found in your file: {list(df.columns)}")
        return

    to_send = []
    for i, row in df.iterrows():
        email    = str(row[EMAIL_COLUMN]).strip()
        pdf_name = str(row[PDF_COLUMN]).strip() + ".pdf"
        company  = str(row[ENTERPRISE_COLUMN]).strip()

        if PDF_FOLDER:
            pdf_path = os.path.join(PDF_FOLDER, pdf_name)
        else:
            pdf_path = pdf_name

        if not email or email.lower() in ("nan", ""):
            print(f"  Row {i+2}: Skipping — no email address")
            continue

        if not os.path.isfile(pdf_path):
            print(f"  Row {i+2}: ⚠️  PDF not found → {pdf_path}  (skipping)")
            continue

        to_send.append((i, email, company, pdf_path))

    total = len(to_send)
    for batch_start in range(0, total, BATCH_SIZE):
        batch = to_send[batch_start:batch_start + BATCH_SIZE]
        batch_num = (batch_start // BATCH_SIZE) + 1
        print(f"\n📦 Batch {batch_num} — sending {len(batch)} emails...")
        send_batch(batch)

        if batch_start + BATCH_SIZE < total:
            print(f"\n⏸️  Pausing for {BATCH_PAUSE//60} minutes before next batch...")
            for remaining in range(BATCH_PAUSE, 0, -30):
                print(f"   ⏳ {remaining} seconds remaining...")
                time.sleep(30)
            print("▶️  Resuming...\n")

    print(f"\nDone! All batches completed.")


if __name__ == "__main__":
    main()