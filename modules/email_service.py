import imaplib
import email
from email.header import decode_header
import os
from pypdf import PdfReader
import config

class EmailService:
    def __init__(self):
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
            self.mail.login(config.EMAIL_USER, config.EMAIL_PASS)
            print("Connected to Gmail.")
        except Exception as e:
            print(f"Gmail Connection Failed: {e}")
            raise e

    def fetch_unread_applications(self):
        """Fetches unread emails matching the subject filter."""
        self.mail.select("inbox")
        # Search for UNREAD emails with specific subject
        search_query = f'(UNSEEN SUBJECT "{config.EMAIL_SUBJECT_FILTER}")'
        status, messages = self.mail.search(None, search_query)
        
        email_ids = messages[0].split()
        if email_ids:
            print(f"Found {len(email_ids)} new applications.")
        return email_ids

    def parse_email(self, email_id):
        """Extracts body and PDF text from a single email."""
        _, msg_data = self.mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        # Decode Subject
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes): subject = subject.decode()
        
        body_text = ""
        resume_text = "No Resume Found"

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disp = str(part.get("Content-Disposition"))

                # Extract Text Body
                if content_type == "text/plain" and "attachment" not in content_disp:
                    try:
                        body_text = part.get_payload(decode=True).decode()
                    except:
                        pass # Skip if encoding error
                
                # Extract PDF Attachment
                if "attachment" in content_disp and ".pdf" in part.get_filename():
                    print("Found Resume PDF.")
                    temp_path = f"temp_{email_id.decode()}.pdf"
                    with open(temp_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    
                    # Read PDF
                    try:
                        reader = PdfReader(temp_path)
                        resume_text = ""
                        for page in reader.pages:
                            resume_text += page.extract_text()
                    except Exception as e:
                        resume_text = f"[Error Reading PDF: {e}]"
                    
                    # Cleanup
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        else:
            try:
                body_text = msg.get_payload(decode=True).decode()
            except:
                pass

        return {
            "id": email_id,
            "subject": subject,
            "body": body_text,
            "resume": resume_text
        }

    def close(self):
        self.mail.close()
        self.mail.logout()
        print("Disconnected from Gmail.")