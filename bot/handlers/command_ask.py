
import io
import logging
from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy import func
from sqlalchemy.future import select

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache
from bot.services.storage import StorageManager
from bot.handlers.base import BaseHandler
from bot.services.database import get_async_session
from bot.services.database.models.user import User
from bot.services.database.models.conversation_item import ConversationItem
from bot.services.database.models.conversation_set import ConversationSet

from bot.constants import REPLY_QUESTION_NOT_FOUND

logger = logging.getLogger(__name__)

class CommandAsk(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel, storage: StorageManager):
        self.cache = cache
        self.llm_model = llm_model
        self.storage = storage

    async def ask_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user

        logger.info(f'User {telegram_user.id} type /ask')

        async with get_async_session() as session:
            result = await session.execute(
                select(
                    ConversationItem.id,
                    ConversationItem.content,
                    ConversationItem.path,
                    ConversationSet.title,
                    ConversationSet.context,
                    ConversationSet.category,
                    ConversationSet.speaker,
                    User.id
                )
                .join(ConversationSet, ConversationItem.set_id == ConversationSet.id)
                .join(User, User.conversation_set_id == ConversationItem.set_id)
                .where(
                    User.telegram_id == str(telegram_user.id),
                    User.is_active.is_(True)
                )
                .order_by(func.random())
                .limit(1)
            )
            item = result.first()

            if not item:
                await update.message.reply_text(REPLY_QUESTION_NOT_FOUND)
                return

            (question_id, question, audio_path, title, context,
                category, speaker, user_id) = item

            context_question = {
                'title': title,
                'audio_path': audio_path,
                'context': context,
                'question': question,
                'category': category,
                'speaker': speaker,
                'user_id': user_id,
                'telegram_user_id': telegram_user.id
            }

            log = 'overwrite' if self.cache.get_context(telegram_user.id) else 'saved'

            self.cache.save_context(telegram_user.id, context_question)

            logger.info(f'Question for {telegram_user.id} {log} to cache')

            try:
                file_bytes = self.storage.get_file(audio_path)
                voice_file = io.BytesIO(file_bytes)
                voice_file.name = 'question.mp3'
                await update.message.reply_voice(voice=voice_file)

                logger.info(f'Question-{question_id} sent to {telegram_user.id}: - {question}')

            except Exception as e:
                logger.error(f'Failed send question: {str(e)}')
