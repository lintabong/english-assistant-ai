
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache
from bot.services.database import llm_services
from bot.handlers.base import BaseHandler
from bot.helpers import text_utils, llm_utils
from bot.constants import (
    BASE_SPEECH_TO_RAW_TEXT,
    BASE_ANALYZE_AND_SCORE
)

logger = logging.getLogger(__name__)

class Voice(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel):
        self.cache = cache
        self.llm_model = llm_model

    async def receive_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.message.from_user
        logger.info(f'voice in from {str(telegram_user.id)}')

        question_context = self.cache.get_context(telegram_user.id)

        if not question_context:
            await update.message.reply_text('we cant found the question, please /ask first')

        file = await update.message.voice.get_file()
        file_path = 'voice.ogg'
        await file.download_to_drive(file_path)

        myfile = self.llm_model.client.files.upload(file=file_path)
        response = self.llm_model.generate_text_from_spech(myfile)

        await self.parse_and_save_llm_response(
            question_context['user_id'],
            response,
            BASE_SPEECH_TO_RAW_TEXT,
        )

        text_from_spech = response.text if hasattr(response, 'text') else str(response)

        chat = self.llm_model.generate_analyze_and_text_score_with_question(
            question=question_context['question'],
            context=question_context['context']
        )

        response = chat.send_message(text_from_spech)
        response_in_json = llm_utils.parse_result(response.text)

        await self.parse_and_save_llm_response(
            question_context['user_id'],
            response,
            BASE_ANALYZE_AND_SCORE
                .replace('my_question', question_context['question'])
                .replace('my_context', question_context['context']),
            text_from_spech
        )

        message = text_utils.build_voice_to_text_reply(text_from_spech, response_in_json)

        self.cache.clear_context(str(telegram_user.id))

        await update.message.reply_text(message, parse_mode="HTML")

    async def parse_and_save_llm_response(self, user_id, response, system_instruction, message=None):
        await llm_services.insert_llm_log(
            user_id=user_id,
            message='audio' if not message else message,
            system_instruction=system_instruction,
            response=response.text,
            input_token=response.usage_metadata.prompt_token_count,
            output_token=response.usage_metadata.candidates_token_count
        )
