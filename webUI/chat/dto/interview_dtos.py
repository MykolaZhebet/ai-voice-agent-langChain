from typing import List, TypedDict, Dict
from pydantic import BaseModel, Field, ValidationError

class Persona(BaseModel):
    name: str = Field(..., description="Full name of the persona")
    age: int = Field(..., description="Age in years")
    job: str = Field(..., description="Job title or role")
    traits: List[str] = Field(..., description="3-4 personality traits")
    communication_style: str = Field(..., description="Hot this person communicate")
    background: str = Field(..., description="One background detail shaping their perspective")

class PersonasList(BaseModel):
    personas: List[Persona] = Field(..., description="List of generated personas")

class InterviewState(TypedDict):
    # Configuration inputs:
    research_question: str
    target_demographic: str
    num_interviews: int
    num_questions: int

    #Generated data
    interview_questions: List[str]
    personas: List[Persona]

    #Current interview tracking
    current_persona_index: int
    current_question_index: int
    current_interview_history: List[Dict]

    # Results storage:
    all_interviews: List[Dict]
    synthesis: str


class Questions(BaseModel):
    """Configuration node: gets research question from the user"""
    questions: List = Field(..., description="List of interview questions")
