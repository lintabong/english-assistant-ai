
import os
import io
import logging
import asyncio
import mysql.connector
from dotenv import load_dotenv

from telegram import Bot
from bot.services.llm_model import LLMModel

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s >> %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def run():
    llm_model = LLMModel()

    bot = Bot(token=os.getenv('BOT_TELEGRAM_API'))

    conn = mysql.connector.connect(**{
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQL_HOST'),
        'database': os.getenv('MYSQL_DATABASE'),
        'port': int(os.getenv('MYSQL_PORT', '3306')),
    })
    cursor = conn.cursor()

    query = """
        SELECT id, telegram_id, conversation_set_id
        FROM users
        WHERE is_active = 1;
    """

    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        telegram_id = user[1]

        chat = llm_model.generate_conversation()
        response =  chat

        await bot.send_message(telegram_id, str(response.text).replace('**', ''))

    logging.info(f'A conversation sent to {user[1]}: {str(response.text)[:20]} ...')

    cursor.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(run())
