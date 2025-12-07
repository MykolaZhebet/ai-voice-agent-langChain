from typing import Dict
import logging
logger = logging.getLogger(__name__)
from chat.dto.interview_dtos import InterviewState
from chat.services.ask_ai_agent import ask_ai_agent

def analyzing_node(state: InterviewState) -> Dict:
    """Synthesis Node - Analyzes all completed interviews and generates actionable insights
    """
    analyzing_prompt_template = """Analyze these {num_interviews} user interviews about "{research_question}" among {target_demographic} and concise yet comprehensive analysis:

        1. KEY THEMES: What patterns and common themes emerged across all interviews? Look for similarities in responses, shared concerns, and recurring topics.

        2. DIVERSE PERSPECTIVES: What different viewpoints or unique insights did different personas provide? Highlight contrasting opinions or approaches.

        3. PAIN POINTS & OPPORTUNITIES: What challenges, frustrations, or unmet needs were identified? What opportunities for improvement emerged?

        4. ACTIONABLE RECOMMENDATIONS: Based on these insights, what specific actions should be taken? Provide concrete, implementable suggestions.

        Keep the analysis thorough but well-organized and actionable.

        Interview Data:
        {interview_summary}
    """
    logger.info("Analyzing all interviews...")

    # Compile all responses in a structured format
    interview_summary = f"""Research Question: {state['research_question']}\n
        Target Demographic: {state['target_demographic']}\n
        Number of Interviews: {len(state['all_interviews'])}
    """
    for i, interview in enumerate(state['all_interviews'], 1):
        p = interview['persona']
        interview_summary += f"""Interview {i} - {p.name} ({p.age}, {p.job}):\n
        Persona Traits: {p.traits}\n"""

        for j, qa in enumerate(interview['responses'], 1):
            interview_summary += f"""Q{j}: {qa['question']}\n
            A{j}: {qa['answer']}\n"""

        interview_summary += "\n"

    prompt = analyzing_prompt_template.format(
        num_interviews=len(state['all_interviews']),
        research_question=state['research_question'],
        target_demographic=state['target_demographic'],
        interview_summary=interview_summary
    )

    try:
        analyzed_response = ask_ai_agent(prompt)
    except Exception as e:
        analyzed_response = f"Error during analyzing: {e}\n\nRaw interview data available for manual analysis."        
        
    debug_str = "\n" + "="*60
    debug_str += "Research Insights"
    debug_str += "="*60
    debug_str += f"Research topic: {state['research_question']}"
    debug_str += f"Demographic: {state['target_demographic']}"
    debug_str += f"Interviews Conducted: {len(state['all_interviews'])}"
    debug_str += "-"*60
    debug_str += analyzed_response
    logger.info(debug_str)

    return {"synthesis": analyzed_response}