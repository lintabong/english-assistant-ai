
import os
import io
import logging
import asyncio
import mysql.connector
from dotenv import load_dotenv

from telegram import Bot

from bot.services.cache import Cache
from bot.services.storage import StorageManager

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s >> %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def run():
    cache = Cache()
    storage = StorageManager()

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
    user_conversations = cursor.fetchall()
    for user in user_conversations:
        cursor.execute("""
            SELECT ci.id, ci.content, ci.path,
                cs.title, cs.context, cs.category, cs.speaker
            FROM conversation_items ci
            JOIN conversation_sets cs ON ci.set_id = cs.id
            WHERE ci.set_id = %s
            ORDER BY RAND()
            LIMIT 1;
        """, (user[2],))

        conversation = cursor.fetchone()

        context_question = {
            'title': conversation[3],
            'audio_path': conversation[2],
            'context': conversation[4],
            'question': conversation[1],
            'category': conversation[5],
            'speaker': conversation[6],
            'user_id': user[0],
            'telegram_user_id': user[1]
        }

        file_bytes = storage.get_file(conversation[2])
        voice_file = io.BytesIO(file_bytes)
        voice_file.name = 'question.mp3'

        cache.save_context(user[1], context_question)

        await bot.send_voice(user[1], voice_file)

        logging.info(f'Question-{conversation[0]} is sent to {user[1]}: {conversation[1]}')

    cursor.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(run())
