
import os
import logging
from telegram.ext import (
    ApplicationBuilder, 
    filters,
    CommandHandler, 
    MessageHandler
)
from bot.config import setup_logging

from bot.services.cache import Cache
from bot.services.llm_model import LLMModel

from bot.handlers.command_ask import CommandAsk
from bot.handlers.command_register import CommandRegister
from bot.handlers.voice import Voice
from bot.handlers.message import Message

from bot.constants import BOT_TELEGRAM_API

setup_logging()

logger = logging.getLogger(__name__)

class TelegramFinanceBot:
    def __init__(self):
        self.token = BOT_TELEGRAM_API
        self.app = ApplicationBuilder().token(self.token).build()

        self.cache = Cache()
        self.llm_model = LLMModel()

        self.command_ask = CommandAsk(self.cache, self.llm_model)
        self.command_register = CommandRegister(self.cache, self.llm_model)
        self.message_handler = Message(self.cache, self.llm_model)
        self.voice_handler = Voice(self.cache, self.llm_model)

        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler('register', self.command_register.register))
        self.app.add_handler(CommandHandler('ask', self.command_ask.ask_question))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.receive_message))
        self.app.add_handler(MessageHandler(filters.VOICE, self.voice_handler.receive_voice))

    def run(self):
        logger.info('Bot is starting...')
        self.app.run_polling()

def main():
    bot = TelegramFinanceBot()
    bot.run()

if __name__ == '__main__':
    main()
