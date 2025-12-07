import logging
import sys
from deprecation import deprecated
from typing import Dict, List, TypedDict
import time
import os, getpass
import django
# from IPython.display import Image, display

from langchain_cerebras import ChatCerebras
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END


logger = logging.getLogger(__name__)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chat.services.llm_service import LlmStruct
from chat.services.product_context_service import ProductContextLoaderService
from chat.dto.interview_dtos import InterviewState
from chat.services.interview_nodes.interview_node import interview_node
from chat.services.interview_nodes.configuration_node import configuration_node
from chat.services.interview_nodes.analyzing_node import analyzing_node
from chat.services.interview_nodes.persona_generation_node import persona_generation_node

"""
Each node is a specialized agent that performs one specific task and updates the shared state for other nodes to use.
Configuration node: gets research question from the user
Persona generation node: creates synthetic users
Interview node: conducts our interviews
Analyzing node: analyzes and present results"""

@deprecated('This function only for testing purposes')
def questions_generator():
    """Send prompt to Cerebras AI and return response: 3 generated queries"""
    # llm = ChatCerebras(model='llama-3.3-70b', temperature=0.7, max_tokens=800)
    
    prompt = f"""Generate exactly 3 interview questions about: model context protocol
    Requirements:
    - Each question must be open-ended (not yes/no)
    - Keep questions conversational and clear
    - One question per line
    - No numbering, bullets, or extra formatting

    Topic: model context protocol"""
    
    response = LlmStruct().invoke(
        [
         {  
            'role': "user",
            'content': f"You are a helpful assistant. Provide a direct, clear response without showing your thinking process {prompt}",
        }]
    )
    return response.content
    
    ##response.pretty_print()
    # return response.json()


##cerebras_key = os.getenv('CEREBRAS_API_KEY')


def interview_router(state: InterviewState):
    """Route between continuing interviews or ending"""
    if state['current_persona_index'] >= len(state['personas']):
        return "analyze"
    else:
        return "interview"

def build_interview_workflow():
    """Build complete interview workflow graph"""
    workflow = StateGraph(InterviewState)

    # Add all nodes
    workflow.add_node('config', configuration_node)
    workflow.add_node('personas', persona_generation_node)
    workflow.add_node('interview', interview_node)
    workflow.add_node('analyze', analyzing_node)

    # Define the workflow connections
    workflow.set_entry_point('config')
    workflow.add_edge('config', 'personas')
    workflow.add_edge('personas', 'interview')

    # Conditional routing based on interview progress
    workflow.add_conditional_edges(
        "interview",
        interview_router,
        {
            "interview": "interview", # Continue interviewing
            "analyze": "analyze" # All done, analyze results
        }
    )

    workflow.add_edge('analyze', END)
    logger.info("Workflow builder ready")
    return workflow.compile()


def text_langgraph_research_agent_entrypoint():    
    """Execute complete LangGraph research workflow"""
    DEFAULT_NUM_QUESTIONS = int(os.getenv('DEFAULT_NUM_QUESTIONS'))
    DEFAULT_NUM_INTERVIEWS = int(os.getenv('DEFAULT_NUM_INTERVIEWS'))
    logger.info(f"Number of question {DEFAULT_NUM_QUESTIONS} for {DEFAULT_NUM_INTERVIEWS} persona(s)")
    research_question = input("What research question would you like to explore? ") or "Which car is better BMW or Mercedes"
    target_demographic = input("What kinds of users would you like to interview? ") or "city driver"

    workflow = build_interview_workflow()
    start_time = time.time()
    # Initialize state. This is needed before saving our values later
    initial_state = {
        "research_question": research_question,
        "target_demographic": target_demographic,
        "num_interviews": DEFAULT_NUM_INTERVIEWS,
        "num_questions": DEFAULT_NUM_QUESTIONS,
        "interview_questions": [],
        "personas": [],
        "current_persona_index": 0,
        "current_question_index": 0,
        "current_interview_history": [],
        "all_interviews": [],
        "synthesis": ""
    }

    try:
        final_state = workflow.invoke(initial_state, {"recursion_limit": 100})
        total_time = time.time() - start_time
        logger.info(f"Workflow complete for {len(final_state['all_interviews'])} interviews in {total_time:.1f}sec.")
        return final_state
    except Exception as e:
        logger.error(f"Error during workflow execution", exc_info=e)
        return None

    # Configuration Constants
    
        # result = research_orchestrator()
        # print(result)L.i
    # else:
        # logger.warning('Please provide promt for research')
    


if __name__ == '__main__':
    # Setup environ
    # sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webUI.settings")
    # Setup django
    django.setup()
    # Setup django
    # DEFAULT_NUM_INTERVIEWS = 10
    # DEFAULT_NUM_QUESTIONS = 5
    # os.environ["CEREBRAS_API_KEY"]=""
    text_langgraph_research_agent_entrypoint()

    
    # Run livekit in CLI mode
    # cli.run_app(WorkerOptions(entrypoint_fnc=text_research_agent_entrypoint))