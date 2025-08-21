
import random
import logging
from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy.future import select

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache
from bot.handlers.base import BaseHandler
from bot.services.database import get_async_session
from bot.services.database.models.user import User
from bot.services.database.models.conversation_item import ConversationItem
from bot.services.database.models.conversation_set import ConversationSet

logger = logging.getLogger(__name__)

class CommandAsk(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel):
        self.cache = cache
        self.llm_model = llm_model

    async def ask_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user

        async with get_async_session() as session:
            result = await session.execute(
                select(
                    ConversationItem.content,
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

            question, title, context, category, speaker, user_id, telegram_user_id = random.choice(items)

            context_question = {
                'title': title,
                'context': context,
                'question': question,
                'category': category,
                'speaker': speaker,
                'user_id': user_id,
                'telegram_user_id': telegram_user_id
            }

            self.cache.save_context(str(telegram_user.id), context_question)

            await update.message.reply_text(f"❓ Here is the question:\n\n{question}")
