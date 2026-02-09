import google.generativeai as genai
import json
import config
import os

class AIExtractor:
    def __init__(self):
        # 1. Setup API Key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERROR: GEMINI_API_KEY not found in .env")
        genai.configure(api_key=api_key)

        # 2. DYNAMIC MODEL SELECTION (The "Smart" Fix)
        try:
            # Ask Google: "What models can I use?"
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            # Prioritize 'gemini-1.5-flash' (Fast & Free)
            target_model = "models/gemini-1.5-flash"
            
            if target_model in available_models:
                self.model_name = target_model
            else:
                # Fallback: Just pick the first available one (e.g., gemini-1.0-pro)
                self.model_name = available_models[0]
                print(f"Preferred model not found. Switching to: {self.model_name}")

            self.model = genai.GenerativeModel(self.model_name)
            
        except Exception as e:
            print(f"Could not auto-detect models. Defaulting to 'gemini-1.5-flash'. Error: {e}")
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_data(self, email_content):
        print(f"AI Processing (via {self.model_name})...")
        
        fields_str = ", ".join(config.TARGET_FIELDS)
        
        prompt = f"""
        Extract these fields from the text below: {fields_str}.
        
        Format: JSON
        Missing Info: "N/A"
        
        --- EMAIL SUBJECT ---
        {email_content.get('subject', '')}

        --- EMAIL BODY ---
        {email_content.get('body', '')[:1000]}
        
        --- RESUME TEXT ---
        {email_content.get('resume', '')[:3000]}
        """

        try:
            response = self.model.generate_content(prompt)
            
            # Clean up the text to ensure it's valid JSON
            text = response.text
            if "```json" in text:
                text = text.replace("```json", "").replace("```", "")
            elif "```" in text:
                text = text.replace("```", "")
            
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"AI Error: {e}")
            return {field: "Error" for field in config.TARGET_FIELDS}