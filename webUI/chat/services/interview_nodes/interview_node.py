from typing import Dict
import logging
logger = logging.getLogger(__name__)
from chat.dto.interview_dtos import InterviewState
from chat.services.ask_ai_agent import ask_ai_agent

def interview_node(state: InterviewState) -> Dict:
    """Interview Node - Conducts the actual Q&A with each persona, one question at a time
    Conduct interview with current persona
    """
    # Generate response as this persona with detailed character context
    interview_prompt = """You are {persona_name}, a {persona_age}-year-old {persona_job} who is {persona_traits}.
        Answer the following question in 2-3 sentences:

        Question: {question}

        Answer as {persona_name} in your own authentic voice. Be brief but creative and unique, and make each answer conversational.
        BE REALISTIC - do not be overly optimistic. Mimic real human behavior based on your persona, and give honest answers."""

    persona = state['personas'][state['current_persona_index']]
    question = state['interview_questions'][state['current_question_index']]

    logger.info(f"Interview: {state['current_persona_index']} - {persona.name}. Question: {question}")
    # Generate response as this persona with detailed character context
    prompt = interview_prompt.format(persona_name=persona.name,persona_age=persona.age, persona_job=persona.job, persona_traits=persona.traits, question=question)
    answer = ask_ai_agent(prompt)
    logger.info(f"Answ: {answer}")

    # Update state with interview history
    history = state.get('current_interview_history', []) + [{
        'question': question,
        'answer': answer
    }]

    #Check if this interview is complete
    if state['current_question_index'] + 1 >= len(state['interview_questions']):
        #Interview complete -save it and move to next persona
        logger.info("Interview finished")
        return {
            "all_interviews": state['all_interviews'] + [{
                "persona": persona,
                "responses": history
            }],
            "current_interview_history": [],
            "current_question_index": 0,
            "current_persona_index": state['current_persona_index'] + 1
        }
    
    logger.info("Next question...")
    return {
        "current_interview_history": history,
        "current_question_index": state['current_question_index'] + 1
    }


