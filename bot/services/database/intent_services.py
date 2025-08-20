from bot.services.database.models.intent_logs import IntentLog 
from bot.services.database import get_async_session

async def insert_intent_log(input_message: str, intent_result: str, intent_score: float):
    async with get_async_session() as session:
        new_log = IntentLog(
            input_message=input_message,
            intent_result=intent_result,
            intent_score=round(intent_score, 4)  # biar sesuai format NUMERIC(5,4)
        )
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)
        return new_log
