**🤖 AI Recruitment Agent**

A production-grade AI Agent that automates the recruitment process by parsing candidate emails, extracting structured data from resumes using Google Gemini 1.5 Flash, and saving the results to a CSV database and Google Sheets.

🚀 Features
* **Automated Email Ingestion**: Monitors Gmail via IMAP for specific subject lines (e.g., "Application").
* **Smart Parsing**: Handles multipart emails to distinguish between body text and PDF attachments.
* **AI Extraction Engine**: Uses Gemini 1.5 Flash to dynamically extract fields like Name, Skills, Experience, and GitHub links from unstructured resume text.
* **Fail-Safe Storage**: Saves data to a local CSV (primary) to ensure zero data loss, with an optional webhook to sync with Google Sheets.
* **Self-Healing**: Automatically detects API availability and handles errors (401/429) gracefully without crashing.

🛠️ Tech Stack
* **Language**: Python 3.10+
* **AI Model**: Google Gemini 1.5 Flash (via google-generativeai)
* **Integrations**: Gmail (IMAP), Google Forms (Webhook)
* **Libraries**: pandas, pypdf, python-dotenv

📂 Project Structure
```
Plaintext
threadfactory-agent/
│
├── modules/
│   ├── email_service.py  # Handles Gmail connection & PDF parsing
│   ├── ai_engine.py      # The "Brain" - Talks to Gemini API
│   └── sheet_service.py  # Saves data to CSV & Google Sheets
│
├── config.py             # Configuration settings (Targets, API mappings)
├── main.py               # The main controller script
├── requirements.txt      # Project dependencies
└── .env                  # API Keys & Secrets (Not included in repo)
```
⚙️ Setup & Installation
Clone the repository:

Bash
```
git clone https://github.com/aryan-bhandari/AI-Recruitment-Agent.git
cd AI-Recruitment-Agent
```
Install dependencies:

Bash
```
pip install -r requirements.txt
```
Configure Environment Variables: Create a .env file in the root directory and add your keys:
```
Ini, TOML
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_FORM_URL=optional_google_form_url
```
Run the Agent:

Bash
```
python main.py
```
📊 How It Works
* **Listen**: The agent polls the inbox for unread emails with the subject "Application".
* **Read**: It downloads the PDF resume and reads the email body.
* **Think**: It sends the text to the Gemini API with a specific prompt to extract structured JSON data.
* **Act**: It saves the extracted candidate profile to candidates_database.csv and pushes it to the cloud.

🛡️ Security
* Uses **App Passwords** for Gmail authentication (no real passwords stored).
* **API Keys** are managed via .env files and excluded from version control.
* **Data** is stored locally for privacy and compliance.
