
import html
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache
from bot.handlers.base import BaseHandler
from bot.helpers.llm_utils import parse_result

logger = logging.getLogger(__name__)

class Voice(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel):
        self.cache = cache
        self.llm_model = llm_model

    async def receive_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info(f'user: {str(update)}')

        file = await update.message.voice.get_file()
        file_path = 'voice.ogg'
        await file.download_to_drive(file_path)

        myfile = self.llm_model.client.files.upload(file=file_path)
        response = self.llm_model.generate_text_from_spech(myfile)

        text_from_spech = response.text if hasattr(response, 'text') else str(response)

        chat = self.llm_model.generate_analyze_and_text_score(
            question='How do you handle errors and exceptions in Python?'
        )

        response = chat.send_message(text_from_spech)
        response_in_json = parse_result(response.text)

        message = (
            f"<b>📌 Original Transcript:</b>\n"
            f"{html.escape(text_from_spech)}\n\n"
            f"<b>✅ Corrected English:</b>\n"
            f"{response_in_json['corrected_text']}\n\n"
            f"<b>📝 Scores:</b>\n"
            f"English: {response_in_json['english_score']}/100\n"
            f"Context: {response_in_json['context_score']}/100"
        )

        await update.message.reply_text(message, parse_mode="HTML")
