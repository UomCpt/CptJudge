from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from executor import run_java_file

app = FastAPI(title="Java Tester")

# Φάκελος όπου θα αποθηκεύονται προσωρινά τα uploaded Java αρχεία
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/run/")
async def run_java(file: UploadFile = File(...)):
    # Έλεγχος αν το αρχείο είναι .java
    if not file.filename.endswith(".java"):
        raise HTTPException(status_code=400, detail="Only .java files are allowed.")

    # Αποθήκευση του αρχείου στον φάκελο uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Τρέξιμο του executor
    result = run_java_file(file_path)

    return JSONResponse(content={"result": result})
