from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
    
class Team(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    score: int
    attempted: int
    solved: int
    
class Problem(BaseModel):
    id: int
    name: str
    description: set
    
class Submission(BaseModel):
    id: int
    created_at: datetime
    team_id: int
    solved: bool
    problem_id: int
    average_time: int