from typing import Dict
import sys
import logging
logger = logging.getLogger(__name__)
from chat.services.llm_service import LlmStruct
from chat.dto.interview_dtos import InterviewState, PersonasList

    
def persona_generation_node(state: InterviewState) -> Dict:
    """Persona generation node: creates synthetic users"""
    num_personas = state['num_interviews']
    demographic = state['target_demographic']
    max_retries = 5
    ###Tuple of prompts 
    persona_prompt = """
        Generate exactly {num_personas} unique personas for an interview.
        Each should belong to the tartget demographic: {demographic}.
        Respond only in JSON using this format: {{ personas: [...] }}
    """

    logger.info(f"Creating {num_personas} personas...")
    persona_prompt_prepared = persona_prompt.format(num_personas=num_personas, demographic=demographic);
    logger.info(persona_prompt_prepared)

    structured_llm = LlmStruct().with_structured_output(PersonasList)

    for attempt in range(max_retries):
        try:
            raw_output = structured_llm.invoke([{"role": "user", "content": persona_prompt_prepared}])
            if raw_output is None:
                raise ValueError("LLM returned None")
            validated = PersonasList.model_validate(raw_output)
            amount_validated_personas = len(validated.personas)
            if amount_validated_personas != num_personas:
                raise ValueError(f"Expected {num_personas} personas, got {amount_validated_personas}")
            else:
                logger.info("Persona generated successfully")
            
            personas = validated.personas
            for i, p in enumerate(personas):
                logger.info(f"Persona {i}: {p}")
            return {
                "personas": personas,
                "current_persona_index": 0,
                "current_question_index": 0,
                "all_interviews": []
            }
        
        except Exception as e:
            logger.error(f"Failed attempt {attempt} to generate persona", exc_info=e)

        if attempt == max_retries -1:
            raise RuntimeError(f"Failed to generate persona after {max_retries} attempts")


