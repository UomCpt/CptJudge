from fastapi import FastAPI, UploadFile, File
import shutil
from c_executor import run_all_tests

app = FastAPI()

@app.post("/run")
async def run_tests(c_file: UploadFile = File(...)):
    # Save uploaded C file as program.c
    with open("program.c", "wb") as buffer:
        shutil.copyfileobj(c_file.file, buffer)

    # Run all test cases
    result = run_all_tests()

    return result
