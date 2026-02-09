import time
from modules.email_service import EmailService
from modules.ai_engine import AIExtractor
from modules.sheet_service import SheetService

def run_agent():
    print("Recruitment Agent Starting...")
    
    # Initialize Services
    try:
        email_svc = EmailService()
        ai_bot = AIExtractor()
        sheet_svc = SheetService()
    except Exception as e:
        print(f"CRITICAL ERROR: Could not initialize services. {e}")
        return

    # 1. Fetch Emails
    email_ids = email_svc.fetch_unread_applications()
    
    if not email_ids:
        print("No new applications found.")
        email_svc.close()
        return

    # 2. Process Loop
    for e_id in email_ids:
        print(f"\n--- Processing Email ID: {e_id.decode()} ---")
        
        # Step A: Ingestion (Get content)
        email_data = email_svc.parse_email(e_id)
        
        # Step B: Cognition (Extract data)
        structured_data = ai_bot.extract_data(email_data)
        print(f"Extracted: {structured_data.get('Candidate_Name', 'Unknown')}")
        
        # Step C: Action (Save data)
        sheet_svc.save_candidate(structured_data)
        
        # Step D: Cleanup (Mark as Read)
        # Uncomment the line below to stop processing the same email twice
        # email_svc.mail.store(e_id, '+FLAGS', '\\Seen')

    email_svc.close()
    print("\nBatch Complete.")

if __name__ == "__main__":
    run_agent()