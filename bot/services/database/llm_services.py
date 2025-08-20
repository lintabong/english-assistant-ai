

from bot.services.database.models.llm_log import LLMLog
from bot.services.database import get_async_session

async def insert_llm_log(
        user_id: str | None,
        message: str,
        system_instruction: str | None,
        response: str,
        input_token: int = 0,
        output_token: int = 0
    ):
    async with get_async_session() as session:
        new_log = LLMLog(
            user_id=user_id,
            message=message,
            system_instruction=system_instruction,
            response=response,
            input_token=input_token,
            output_token=output_token
        )
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)
        return new_log
