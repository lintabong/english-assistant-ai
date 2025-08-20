
import os
from google import genai
from google.genai import types
from bot.constants import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    BASE_ANALYZE_AND_SCORE,
    BASE_SPEECH_TO_RAW_TEXT
)


class LLMModel:
    def __init__(self):
        os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
        self.client = genai.Client()

    def build_history(self, history: list[dict]):
        result = []
        for message in history:
            row = types.Content(
                role=message['role'], 
                parts=[types.Part.from_text(text=message['content'])]
            )
            result.append(row)
        return result

    def generate_analyze_and_text_score(self, question):
        return self.client.chats.create(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=BASE_ANALYZE_AND_SCORE.replace('my_question', question))
        )
    
    def generate_analyze_and_text_score_with_question(self, question):
        return self.client.chats.create(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=BASE_ANALYZE_AND_SCORE.replace('my_question', question))
        )

    def generate_text_from_spech(self, myfile):
        return self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[BASE_SPEECH_TO_RAW_TEXT, myfile
            ]
        )
