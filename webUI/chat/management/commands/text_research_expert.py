import os, sys, argparse
import django
from livekit.plugins import openai, silero, cartesia
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)

from exa_py import Exa
from cerebras.cloud.sdk import Cerebras

import logging
logger = logging.getLogger(__name__)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def search_web(query, num=5):
    """Search the web using Exa's search API"""
    exa_key = os.getenv('EXA_API_KEY')
    exa = Exa(api_key = exa_key)
    result = exa.search_and_contents(
        query,
        type = "auto",
        num_results = num,
        text={"max_characters": 1000}##Max content to fetch from each page
    )
    logger.info("AI search results ready")
    return result.results

def ask_ai_agent(prompt):
    """Get AI resposne based on web search AI results"""
    cerebras_key = os.getenv('CEREBRAS_API_KEY')
    chat_client = Cerebras(api_key = cerebras_key)
    chat_completion = chat_client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        # model='llama-4-scout-17b-16e-instruct',
        model='llama-3.3-70b',
        max_tokens= 600,
        temperature = 0.2 ##Give precise response
    )
    logger.info("AI response ready")
    return chat_completion.choices[0].message.content
    
def research_orchestrator(query):
    """Main research function that orchestrates the process by calling search tool and providing right prompt to the LLM"""
    
    logger.info(f"Start AI research on topic: '{query}'")

    search_results = search_web(query)
    logger.info(f"Search tool found {len(search_results)} relevant sources")

    # Gather content from these sources
    sources = []
    for result in search_results:
        content = result.text
        title = result.title
        if content and len(content) > 200:
            sources.append({
                "title": title,
                "content": content
            })
    logger.info(f"Gathered info for {len(sources)} sources")
    
    if not sources:
        return {"summary": "No sources found", "insights": []}
    
    ## Prepare search result context for AI analysis
    search_context = f"Research query: {query}\n\nSources:\n"
    for i, source in enumerate(sources[:4], 1):
        logger.info(f"source info: {source['title']}")
        search_context += f"{i}. {source['title']}: {source['content'][:400]}...\n\n"

    prompt = f"""{search_context}

    Based on these sources, provide:
    1. A comprehensive summary (2-3 sentences)
    2. Three key insights as bullet points

    Format your response exactly like this:
    SUMMARY: [your summary here]

    INSIGHTS:
    - [insight 1]
    - [insight 2]
    - [insight 3]"""
    
    response = ask_ai_agent(prompt)
    logger.info("Analysis complete")

    return {"query": query, "sources": len(sources), "response": response}


def text_research_agent_entrypoint():    
    if args.query:
        result = research_orchestrator(args.query)
        print(result)
    else:
        logger.warning('Please provide promt for research')
    


if __name__ == '__main__':
    # Setup environ
    # sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webUI.settings")
    # Setup django
    django.setup()
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="Query for research")
    args = parser.parse_args()

    text_research_agent_entrypoint()

    
    # Run livekit in CLI mode
    # cli.run_app(WorkerOptions(entrypoint_fnc=text_research_agent_entrypoint))