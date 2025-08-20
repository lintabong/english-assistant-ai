

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.llm_model import LLMModel
from bot.services.cache import Cache

from bot.handlers.base import BaseHandler
from bot.services.database.user_register_service import register_free_user, UserAlreadyExistsError


logger = logging.getLogger(__name__)

class CommandRegister(BaseHandler):
    def __init__(self, cache: Cache, llm_model: LLMModel):
        self.cache = cache
        self.llm_model = llm_model

    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user
        telegram_id = str(telegram_user.id)

        # default kosong kalau None
        username = telegram_user.username or ""
        name = telegram_user.full_name or ""
        email = ""  # user belum kasih email saat register
        password = ""

        try:
            new_user = await register_free_user(
                telegram_id=telegram_id,
                username=username
            )
            await update.message.reply_text(
                f"✅ Registrasi berhasil!\n\n"
                f"ID: {new_user.id}\n"
                f"Username: {new_user.username}\n"
                f"Paket: Free"
            )
            logger.info(f"User {telegram_id} berhasil registrasi dengan id {new_user.id}")

        except UserAlreadyExistsError as e:
            await update.message.reply_text("⚠️ Kamu sudah terdaftar sebelumnya.")
            logger.warning(str(e))

        except ValueError as e:
            await update.message.reply_text("❌ Paket free belum tersedia. Hubungi admin.")
            logger.error(str(e))

        except Exception as e:
            await update.message.reply_text("❌ Terjadi kesalahan saat registrasi.")
            logger.exception("Error saat registrasi user")
