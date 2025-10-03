import requests
from textblob import TextBlob

class T5Summary:
    def __init__(self):
        # self.hf_api_url = "https://000surya-chat-summary-api.hf.space/summarize"
        self.hf_api_url = "http://127.0.0.1:8000/analyze"

    def summarize_with_sentiment(self, texts):
        """
        Returns a list of dicts: [{'summary': ..., 'sentiment': {'label':..., 'score':...}}, ...]
        """
        if not texts:
            raise ValueError("No text provided")

        if isinstance(texts, str):
            texts = [texts]

        try:
            response = requests.post(
                self.hf_api_url,
                json={"texts": texts},
                headers={"Content-Type": "application/json"},
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
        
            results = response.json().get("results", [])

            return results

        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
