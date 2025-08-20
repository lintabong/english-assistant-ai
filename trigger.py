from telegram.ext import Application, ContextTypes
import asyncio

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = 123456789  # isi dengan chat id

async def send_periodic(app):
    while True:
        await app.bot.send_message(chat_id=CHAT_ID, text="⏰ Reminder dari bot!")
        await asyncio.sleep(60)  # setiap 60 detik

def main():
    app = Application.builder().token(TOKEN).build()
    app.post_init(send_periodic)  # jalankan setelah bot mulai
    app.run_polling()

if __name__ == "__main__":
    main()
