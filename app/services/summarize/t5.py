from flask import jsonify
import requests

class T5Summary:
    
    def __init__(self):
        self.hf_api_url = "https://000surya-chat-summary-api.hf.space/summarize"
        
    def summarize(self, user_text):
        try:
            if not user_text:
                return jsonify({"error": "No text provided"}), 400

            # Forward request to Hugging Face API
            response = requests.post(
                self.hf_api_url,
                json={"text": user_text},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                summary = result.get("summary", "")
                if summary:
                    return jsonify({"summary": summary})
                else:
                    return jsonify({"error": "No summary returned from API"}), 500
            else:
                return jsonify({"error": "Failed to fetch summary"}), 500

        except Exception as e:
            return jsonify({"error": str(e)}), 500
