from bot.services.database.models.llm_logs import LLMLog
from bot.services.database import get_async_session

async def insert_llm_log(message: str, intent: str, system_instruction: str, response: str, input_token: int, output_token: int):
    async with get_async_session() as session:
        new_log = LLMLog(
            message=message,
            intent=intent,
            system_instruction=system_instruction,
            response=response,
            input_token=input_token,
            output_token=output_token
        )
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)
        return new_log
