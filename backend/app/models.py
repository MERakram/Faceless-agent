from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ChatMode(str, Enum):
    REGULAR = "regular"
    UNCENSORED = "uncensored"

class PersonaResponse(BaseModel):
    id: int
    description: str
    is_custom: bool

class CustomPersonaRequest(BaseModel):
    description: str

class ChatRequest(BaseModel):
    message: str
    persona: str
    mode: ChatMode = ChatMode.REGULAR
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    persona: str
    mode: str
    filtered: bool = False

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
