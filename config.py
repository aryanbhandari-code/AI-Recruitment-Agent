import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Credentials
EMAIL_USER = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")

# Application Settings
EMAIL_SUBJECT_FILTER = "Application"  # The subject line to look for
CHECK_INTERVAL = 60  # Seconds to wait between checks (if running in loop)

# Dynamic Extraction Fields (Change these to change what the AI looks for)
TARGET_FIELDS = [
    "Candidate_Name",
    "Role_Applied_For",
    "Email",
    "Phone_Number",
    "Years_of_Experience",
    "Top_3_Tech_Skills",
    "Github_Link",
    "Portfolio_Link",
    "Relevance_Score_1_to_10"
]

# Google Form Mapping (Field Name -> Entry ID)
FORM_MAPPING = {
    "Candidate_Name": "entry.1299565629",
    "Email": "entry.286191000",
    "Years_of_Experience": "entry.1983711670",
    "Top_3_Tech_Skills": "entry.2049047617",
    "Github_Link": "entry.840037909"
}