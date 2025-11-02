
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,text, ForeignKey
from .database import Base
# from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key = True, nullable = False)
    # name = Column(String,nullable=False)
    username = Column(String, nullable = False)
    password = Column(String,nullable=False)
    score = Column(Integer,nullable=False)
    attempted = Column(Integer,nullable=False)
    solved = Column(Integer,nullable=False)
    
    
class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key = True, nullable = False)
    # name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    
class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    

class Solved(Base):
    __tablename__ = "solved"
     
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    


    

    
