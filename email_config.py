import yagmail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Configure yagmail with SMTP settings
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)