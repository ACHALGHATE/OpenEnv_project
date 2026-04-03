from pydantic import BaseModel
from typing import List, Optional, Dict

class Observation(BaseModel):
    task_type: str
    inbox: List[Dict] = []
    tickets: List[Dict] = []
    calendar: List[Dict] = []
    history: List[Dict] = []

class Action(BaseModel):
    action_type: str
    target_id: Optional[int] = None
    content: Optional[str] = None

class Reward(BaseModel):
    score: float
    feedback: str