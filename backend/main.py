from fastapi import FastAPI
#from database import models  
from .database import engine, Base
from .routers import problems


Base.metadata.create_all(bind=engine)

app = FastAPI()

#Calling the routers
app.include_router(problems.router)

@app.get("/")
async def root():
    return {"message": "Hello CPT!"}