import requests
import pandas as pd
import os
import config
from datetime import datetime

class SheetService:
    def save_candidate(self, data):
        """
        Saves candidate data to local CSV (Primary) and Google Sheets (Secondary).
        """
        # 1. ALWAYS save to local CSV first (This is your proof of work)
        csv_success = self._save_to_local_csv(data)
        
        # 2. Try pushing to Google Sheets (If configured)
        cloud_success = False
        if config.GOOGLE_FORM_URL and "docs.google.com" in config.GOOGLE_FORM_URL:
            cloud_success = self._push_to_google_form(data)
        
        return csv_success or cloud_success

    def _save_to_local_csv(self, data):
        try:
            filename = "candidates_database.csv"
            
            # Add a timestamp so you know when the bot ran
            data['Processed_At'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            df = pd.DataFrame([data])
            
            # Check if file exists to determine if we need a header
            if os.path.exists(filename):
                df.to_csv(filename, mode='a', header=False, index=False)
            else:
                df.to_csv(filename, mode='w', header=True, index=False)
                
            print(f"Saved to local file: {filename}")
            return True
        except Exception as e:
            print(f"CSV Save Failed: {e}")
            return False

    def _push_to_google_form(self, data):
        try:
            # Map the data to the Google Form Entry IDs
            form_data = {}
            for field, value in data.items():
                if field in config.FORM_MAPPING:
                    entry_id = config.FORM_MAPPING[field]
                    form_data[entry_id] = value
            
            # Send the POST request
            response = requests.post(config.GOOGLE_FORM_URL, data=form_data)
            
            if response.status_code == 200:
                print(f"Pushed to Google Sheets successfully.")
                return True
            else:
                # If it fails (like Error 401), we just log it and move on
                print(f"Google Sheet Push Skipped (Status: {response.status_code}). Check Form permissions.")
                return False
                
        except Exception as e:
            print(f"Google Sheet Connection Failed: {e}")
            return False