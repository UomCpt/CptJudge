import os
import subprocess
import time
from fastapi import HTTPException

TEST_DIR = "app/testcases"

def compile_and_run_cpp(file_path: str):
    # Compile C++ source file
    binary_path = os.path.splitext(file_path)[0]

    # invoke the g++ compiler
    compile_proc = subprocess.run(
        ["g++", file_path, "-o", binary_path],
        capture_output=True,
        text=True
    )

    # check for compilation errors
    if compile_proc.returncode != 0:
        raise HTTPException(status_code=400, detail=f"Compilation failed:\n{compile_proc.stderr}")
    
    total_cases = 0
    passed_cases = 0
    start_time = time.time()

    # iterate input testcases
    for filename in sorted(os.listdir(TEST_DIR)):
        if filename.startswith("input"):
            total_cases += 1
            case_number = filename.replace("input", "").replace(".txt", "")
            input_file = os.path.join(TEST_DIR, filename)
            expected_file = os.path.join(TEST_DIR, f"expected{case_number}.txt")

            # Run the compiled binary, feeding the input file via stdin
            with open(input_file, "r") as fin:
                proc = subprocess.run(
                    [binary_path],
                    stdin=fin,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            # runtime errors check
            if proc.returncode != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Runtime error on test case {case_number}:\n{proc.stderr}"
                )
            
            # Step 5: Compare program output to expected output
            with open(expected_file, "r") as fexp:
                expected_output = fexp.read().strip()
            actual_output = proc.stdout.strip()

            # If outputs don't match, return mismatch info
            if actual_output != expected_output:
                stderr_output = (
                    f"Failed on testcase {case_number}\n"
                    f"Expected: {expected_output}\n"
                    f"Got: {actual_output}\n"
                )

                return {"stderr": stderr_output, "passed":passed_cases}
            passed_cases += 1
    
    # summary after all tests
    total_time = round(time.time()- start_time, 4)
    return {"stderr": "", "passed": passed_cases, "time": total_time}