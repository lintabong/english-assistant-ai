import re
import json

def parse_result(raw_text):
    """
    Parse AI JSON result which may include code block ```json ... ```
    Returns a dictionary with keys:
    - corrected_text
    - english_score
    - context_score
    """
    try:
        # Hapus code block ```json ... ```
        cleaned_text = re.sub(r"```json\s*|\s*```", "", raw_text, flags=re.IGNORECASE).strip()

        # Parse JSON
        data = json.loads(cleaned_text)
        corrected_text = data.get("corrected_text", "")
        english_score = data.get("english_score", 0)
        context_score = data.get("context_score", 0)
        
        return {
            "corrected_text": corrected_text,
            "english_score": english_score,
            "context_score": context_score
        }
    except json.JSONDecodeError:
        # jika JSON tidak valid
        return {
            "corrected_text": "",
            "english_score": 0,
            "context_score": 0
        }