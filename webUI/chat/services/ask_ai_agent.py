import logging

logger = logging.getLogger(__name__)
from chat.services.llm_service import LlmStruct
def ask_ai_agent(prompt):
    """Get AI resposne based on web search AI results"""
    
    system_prompt = """You are a helpful assistant. Provide a direct, clear response without showing your thinking process. Respond directly without using <think> tags or showing internal reasoning."""
    response = LlmStruct().invoke([{"role":"system", "content": system_prompt}, {"role": "user", "content": prompt}])
    logger.info("AI response ready")
    return response.content
