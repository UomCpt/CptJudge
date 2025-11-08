import sys
import subprocess
import time
import os
    
# --- Configuration (Set by the main application logic) ---
TARGET_SCRIPT_FILENAME = "user_program.txt"
INPUT_FILENAME = "input.txt"  
EXPECTED_FILENAME = "expected.txt" 

def execute_and_test(test_number: int) -> tuple[bool, str]:
   
    
    # 1. Path Setup (Assumes files are placed in the current working directory by FastAPI)
    target_path = TARGET_SCRIPT_FILENAME
    input_path = INPUT_FILENAME
    expected_path = EXPECTED_FILENAME

    # 2. Read Expected Result
    try:
        with open(expected_path, 'r', encoding='utf-8') as f:
            expected_output = f.read().strip()
    except FileNotFoundError:
        return (False, f"Test Case: {test_number}\nError: Setup Failed - Expected file not found.")
    except Exception as e:
        return (False, f"Test Case: {test_number}\nError: File read failed for expected: {str(e)}")

    # Check for target and input files
    if not os.path.exists(target_path):
        return (False, f"Test Case: {test_number}\nError: User program file not found.")
    if not os.path.exists(input_path):
        return (False, f"Test Case: {test_number}\nError: Input file not found.")

    # 3. Execute Target Script
    start_time = time.time()
    try:
        # Run the script, piping input from the test file
        execution_result = subprocess.run(
            [sys.executable, target_path],
            stdin=open(input_path, 'r', encoding='utf-8'),
            capture_output=True,
            text=True,
            timeout=5,  # Add a timeout guard (e.g., 5 seconds)
            check=False
        )
        end_time = time.time()
        
        actual_output = execution_result.stdout.strip()
        time_spent = end_time - start_time

        # Check for runtime errors (non-zero exit code or stderr output from user code)
        if execution_result.returncode != 0 or execution_result.stderr:
            error_details = execution_result.stderr.strip() or f"Non-zero exit code: {execution_result.returncode}"
            
            # REQUIREMENT: Return failure details
            return (False, (
                f"Test Case: {test_number}\n"
                f"Error: Runtime or Execution Failure\n"
                f"Stderr: {error_details}\n"
                f"Expected: {repr(expected_output)}\n"
                f"Given: {repr(actual_output)}"
            ))

    except subprocess.TimeoutExpired:
        time_spent = time.time() - start_time
        return (False, (
            f"Test Case: {test_number}\n"
            f"Error: Time Limit Exceeded (>{time_spent:.2f}s)\n"
            f"Expected: {repr(expected_output)}\n"
            f"Given: N/A"
        ))
    except Exception as e:
        return (False, f"Test Case: {test_number}\nError: Executor setup failed: {str(e)}")

    # 4. Compare Results
    if actual_output == expected_output:
        # REQUIREMENT: Return total cases passed and time spent (sent to stdout)
        return (True, f"1/1|Time:{time_spent:.4f}")
    else:
        # REQUIREMENT: Return failure details
        return (False, (
            f"Test Case: {test_number}\n"
            f"Error: Output Mismatch\n"
            f"Expected: {repr(expected_output)}\n"
            f"Given: {repr(actual_output)}"
        ))

if __name__ == "__main__":
    # The executor is designed to run one test case at a time, 
    # taking the test number as a command-line argument.
    
    if len(sys.argv) < 2:
        print("Error: Missing test number argument.", file=sys.stderr)
        sys.exit(1)
    
    try:
        test_case_number = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid test number argument.", file=sys.stderr)
        sys.exit(1)

    is_success, output_msg = execute_and_test(test_case_number)
    
    if is_success:
        # Success output goes to stdout (empty stderr required)
        print(output_msg)
    else:
        # Failure output goes to stderr (empty stdout required)
        print(output_msg, file=sys.stderr)
        # Exit with a non-zero code to indicate failure to the calling process
        sys.exit(1)