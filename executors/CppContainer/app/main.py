import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.tester import compile_and_run_cpp

app = FastAPI(
    title = "C++ Container Tester",
    version = "1.0.0",
    description="API for compiling and testing C++ scripts inside a container."
)

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# this endpoint is for uploading a C++ source file, compiling and running test cases
@app.post("/upload/")
async def upload_cpp_file(file: UploadFile = File(...)):

    # Check if the uploaded file has a .cpp extension
    if not file.filename.endswith(".cpp"):
        raise HTTPException(status_code=400, detail="Only .cpp files allowed")
    
    # Construct the full path where the file will be saved
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    result = compile_and_run_cpp(file_path)
    return JSONResponse(content=result)