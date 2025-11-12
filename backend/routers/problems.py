from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session 
from sqlalchemy import select, func, or_, and_
from typing import Optional, List

# Accesses files within the 'backend/database' directory
from ..database import schemas, models, get_db 

# --- Configuration ---
router = APIRouter(
    prefix="/problems",
    tags=['Problems']
)


# --- Endpoint to Fetch Problems and Status ---
# RESPONSE MODEL: Changed to List[ProblemStatus] or a single ProblemStatus
@router.get("/", response_model=List[schemas.ProblemStatus] | schemas.ProblemStatus)
def get_problems(
    # NOTE: team_id is now a dependency with a default value of 1 (as per your code)
    team_id: int = 1, #Assumes thaat this is the logged in team (now assumed to be the team with id == 1)
    # Optional: Problem ID to fetch a single problem
    problem_id: Optional[int] = Query(None, description="Optional Problem ID"),
    # Inject the database session
    db: Session = Depends(get_db)
):
    
    # --- Status Query Subqueries (Required by BOTH modes) ---
    
    # 1. Get all Problem IDs the team has SOLVED
    solved_problems_q = (
        select(models.Submission.problem_id)
        .filter(
            and_(
                models.Submission.team_id == team_id,
                models.Submission.solved == True
            )
        )
        .distinct()
        .subquery()
    )

    # 2. Get all Problem IDs the team has ATTEMPTED
    attempted_problems_q = (
        select(models.Submission.problem_id)
        .filter(models.Submission.team_id == team_id)
        .distinct()
        .subquery()
    )
    
    
    # --- Case 1: Fetch a Specific Problem by ID (NOW with Status Calculation) ---
    if problem_id is not None:
        problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
        
        if not problem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Problem with ID {problem_id} not found")
        
        # --- Calculate Status for the Single Problem ---
        status_string = "Not Attempted"
        
        # Check if solved (Highest priority)
        is_solved = db.query(solved_problems_q).filter(solved_problems_q.c.problem_id == problem_id).first()
        if is_solved:
            status_string = "Solved"
        else:
            # Check if attempted (only if not solved)
            is_attempted = db.query(attempted_problems_q).filter(attempted_problems_q.c.problem_id == problem_id).first()
            if is_attempted:
                status_string = "Attempted"

        # Returns the ProblemStatus schema with the calculated status
        return schemas.ProblemStatus(
            id=problem.id,
            name=problem.name,
            description=problem.description,
            status=status_string
        )


    # --- Case 2: Fetch ALL Problems with Calculated Status ---

    # 3. Fetch all problems
    all_problems = db.query(models.Problem).all()
    
    result_list = []
    
    # 4. Determine status for each problem
    for problem in all_problems:
        status_string = "Not Attempted"
        problem_id_loop = problem.id # Use a new variable for clarity inside the loop

        # Check if solved (Highest priority)
        is_solved = db.query(solved_problems_q).filter(solved_problems_q.c.problem_id == problem_id_loop).first()
        if is_solved:
            status_string = "Solved"
        else:
            # Check if attempted (only if not solved)
            is_attempted = db.query(attempted_problems_q).filter(attempted_problems_q.c.problem_id == problem_id_loop).first()
            if is_attempted:
                status_string = "Attempted"

        # Create the final response object
        result_list.append(schemas.ProblemStatus(
            id=problem.id,
            name=problem.name,
            description=problem.description,
            status=status_string
        ))

    return result_list