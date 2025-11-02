from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
    
class Team(BaseModel):
    id: int
    username: EmailStr
    password: str
    score: int
    attempted: int
    solved: int
    
class Problem(BaseModel):
    id: int
    description: set
    
class Submission(BaseModel):
    id: int
    created_at: datetime
    team_id: int
    
class Solved(BaseModel):
    id: int
    created_at: datetime
    team_id: int