import yagmail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

try:
    # Configure yagmail with SMTP settings
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    print("✅ Email configuration successful")
except Exception as e:
    print(f"❌ Email configuration failed: {e}")
    yag = None