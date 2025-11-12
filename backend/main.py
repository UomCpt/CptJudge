from fastapi import FastAPI, Depends
from database import models
from database import engine
from sqlalchemy.orm import Session
from database import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()


@app.get("/teams/{team_id}/problems/{problem_id}/submissions")
def get_submissions(team_id: int, problem_id: int, db: Session = Depends(get_db)):
    submissions = db.query(models.Submission).filter(
        models.Submission.team_id == team_id,
        models.Submission.problem_id == problem_id
    ).all()
    
    result = []
    for s in submissions:
        item = {"create_at": s.created_at}
        if s.solved:
            item["average_time"] = s.average_time
        else:
            item["passed_test_cases"] = s.passed_test_cases
        result.append(item)
    return {'data': result}