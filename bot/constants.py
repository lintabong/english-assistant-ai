
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TELEGRAM_API = os.getenv('BOT_TELEGRAM_API')

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')

REDIS_TIME = int(os.getenv('REDIS_SAVE_TIME', 10))
REDIS_CONTEXT_EXPIRED_TIME = int(os.getenv('REDIS_CONTEXT_EXPIRED_TIME', 2))
REDIS_STATE_EXPIRED_TIME = int(os.getenv('REDIS_STATE_EXPIRED_TIME', 2))
REDIS_SESSION_EXPIRED_TIME = int(os.getenv('REDIS_SESSION_EXPIRED_TIME', 2))
REDIS_MCP_EXPIRED_TIME = 1

REPLY_QUESTION_NOT_FOUND = '⚠️ Tidak ada pertanyaan untuk set ini atau user tidak aktif.'


BASE_SPEECH_TO_RAW_TEXT = """
You are a strict English transcriber. Transcribe this audio exactly as spoken, without fixing grammar or spelling. \
The output must be 100% faithful to the speaker’s words. Do not paraphrase or correct anything. \
If you cannot understand a part, write [inaudible]. This way, the transcript will fully reflect how clearly \
the user spoke in English."""

BASE_ANALYZE_AND_SCORE = """
You are an English writing assistant and evaluator. 
Your task is to do the following for the user's transcript:

1. Correct the English grammar, word choice, and sentence structure, while keeping the meaning the same. 
2. Score the **original English text** (the text the user wrote, before correction) from 0 to 100 for grammar, fluency, and word usage. Do not base this score on your corrected version.
3. Score the **context/relevance** from 0 to 100: how well the original text answers the question technically, especially for IT interview questions. Consider correctness, completeness, and relevance of technical content.  

Return your answer in **JSON format** exactly like this:

{{
    "corrected_text": "<the corrected English text here>",
    "english_score": <0-100>,
    "context_score": <0-100>
}}

Question: {my_question}
Context/Relevance: {my_context}
"""
