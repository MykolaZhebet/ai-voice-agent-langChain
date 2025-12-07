from typing import Dict
import logging
logger = logging.getLogger(__name__)
from chat.dto.interview_dtos import InterviewState, Questions
import os
from chat.services.llm_service import LlmStruct

def configuration_node(state: InterviewState) -> Dict:
    """Configuration node: gets research question from the user
    Generate interview questions using AI
    """

    DEFAULT_NUM_QUESTIONS = int(os.getenv('DEFAULT_NUM_QUESTIONS'))
    DEFAULT_NUM_INTERVIEWS = int(os.getenv('DEFAULT_NUM_INTERVIEWS'))

    questions_gen_prompt = """Generate exactly {DEFAULT_NUM_QUESTIONS} interview questions about:
        {research_question}. Use the provided structured output to format the questions.
    """
    logger.info(f"Configuring research: {state['research_question']}")
    logger.info(f"Planning {DEFAULT_NUM_INTERVIEWS} interviews with {DEFAULT_NUM_QUESTIONS} questions each")
    structured_llm = LlmStruct().with_structured_output(Questions)
    questions = structured_llm.invoke(questions_gen_prompt.format(DEFAULT_NUM_QUESTIONS=DEFAULT_NUM_QUESTIONS, research_question=state['research_question']))
    # questions = questions.questions
    return {
        "num_questions": DEFAULT_NUM_QUESTIONS,
        "num_interviews": DEFAULT_NUM_INTERVIEWS,
        "interview_questions": questions.questions
    }

