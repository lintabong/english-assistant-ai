import logging
from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache

from bot.handlers.base import BaseHandler

logger = logging.getLogger(__name__)

class Voice(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel):
        self.cache = cache
        self.llm_model = llm_model

    async def receive_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info(f'user: {str(update)}')

