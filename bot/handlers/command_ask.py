
import os
import random
import logging
import tempfile
# from pydub import AudioSegment
from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy.future import select

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache
from bot.services.storage import StorageManager
from bot.handlers.base import BaseHandler
from bot.services.database import get_async_session
from bot.services.database.models.user import User
from bot.services.database.models.conversation_item import ConversationItem
from bot.services.database.models.conversation_set import ConversationSet

logger = logging.getLogger(__name__)

class CommandAsk(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel, storage: StorageManager):
        self.cache = cache
        self.llm_model = llm_model
        self.storage = storage

    async def ask_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user

        async with get_async_session() as session:
            result = await session.execute(
                select(
                    ConversationItem.content,
                    ConversationItem.path,
                    ConversationSet.title,
                    ConversationSet.context,
                    ConversationSet.category,
                    ConversationSet.speaker,
                    User.id,
                    User.telegram_id
                )
                .join(ConversationSet, ConversationItem.set_id == ConversationSet.id)
                .join(User, User.conversation_set_id == ConversationItem.set_id)
                .where(
                    User.telegram_id == str(telegram_user.id),
                    User.is_active == True
                )
            )
            items = result.all()

            if not items:
                await update.message.reply_text("⚠️ Tidak ada pertanyaan untuk set ini atau user tidak aktif.")
                return

            question, audio_path, title, context, category, speaker, user_id, telegram_user_id = random.choice(items)

            context_question = {
                'title': title,
                'audio_path' : audio_path,
                'context': context,
                'question': question,
                'category': category,
                'speaker': speaker,
                'user_id': user_id,
                'telegram_user_id': telegram_user_id
            }

            self.cache.save_context(str(telegram_user.id), context_question)

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_path = tmp_file.name

                self.storage.get_file(context_question['audio_path'], tmp_path)

                await update.message.reply_voice(voice=open(tmp_path, "rb"))

                os.remove(tmp_path)

            except Exception as e:
                logger.error(f"Gagal mengirim audio: {e}")
