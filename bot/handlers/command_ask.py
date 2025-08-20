import logging
import random
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
        telegram_id = str(telegram_user.id)

        async with get_async_session() as session:
            # Ambil user sekaligus pertanyaan dari conversation_items
            result = await session.execute(
                select(
                    ConversationItem.content,
                    ConversationSet.title,
                    ConversationSet.context,
                    ConversationSet.category,
                    ConversationSet.speaker
                )
                .join(ConversationSet, ConversationItem.set_id == ConversationSet.id)
                .join(User, User.conversation_set_id == ConversationItem.set_id)
                .where(
                    User.telegram_id == telegram_id,
                    User.is_active == True
                )
            )
            items = result.all()  # list of ConversationItem

            if not items:
                await update.message.reply_text("⚠️ Tidak ada pertanyaan untuk set ini atau user tidak aktif.")
                return

            # pilih random
            question_text, title, context, category, speaker = random.choice(items)
            print(title, context, category, speaker)
            # kirim pertanyaan
            await update.message.reply_text(f"❓ Heres the question:\n\n{question_text}")
