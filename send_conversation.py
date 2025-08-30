
from bot.services.llm_model import LLMModel

llm_model = LLMModel()

response = llm_model.generate_conversation()
print(response.text)
