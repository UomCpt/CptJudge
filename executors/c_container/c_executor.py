import subprocess
import os
import time
import sys
import glob

# Configuration
C_FILE = "program.c"
EXECUTABLE = "./a.out"
TESTS_DIR = "tests"

def compile_c_code(c_file, executable):
    #Compiles the C source file.
    try:
       
        result = subprocess.run(
            ["gcc", c_file, "-o", executable],
            capture_output=True,
            text=True,
            check=False  # Don't raise an exception for non-zero exit codes (like compiler errors)
        )
        if result.returncode != 0:
            # If compilation fails, output the error to stderr and exit
            sys.stderr.write(f"Compilation Error:\n{result.stderr}\n")
            sys.exit(1)
        return True
    except FileNotFoundError:
        sys.stderr.write(f"Error: Compiler 'gcc' not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred during compilation: {e}\n")
        sys.exit(1)

def run_test(executable, input_file, expected_output_file, test_number):
    #Runs a single test case and compares output.
    try:
        with open(input_file, 'r') as f_in:
            # Run the executable, piping the content of the input file to stdin
            program_result = subprocess.run(
                [executable],
                stdin=f_in,
                capture_output=True,
                text=True,
                timeout=5  
            )
    except subprocess.TimeoutExpired:
        actual_result = "Program Timeout (over 5 seconds)"
        expected_result = open(expected_output_file, 'r').read().strip()
        return False, test_number, "Timeout", expected_result, actual_result
    except Exception as e:
        actual_result = f"Runtime Error: {e}"
        expected_result = open(expected_output_file, 'r').read().strip()
        return False, test_number, actual_result, expected_result, "N/A"

    # Read the expected output
    with open(expected_output_file, 'r') as f_expected:
        expected_output = f_expected.read().strip()

    # Get the actual output
    actual_output = program_result.stdout.strip()

    # Check for runtime errors
    if program_result.returncode != 0:
        return False, test_number, program_result.stderr, expected_output, actual_output

    # Compare results
    if actual_output == expected_output:
        return True, None, None, None, None
    else:
        # Failed on content mismatch
        return False, test_number, program_result.stderr, expected_output, actual_output

def main():
    if not compile_c_code(C_FILE, EXECUTABLE):
        return

    input_files = sorted(glob.glob(os.path.join(TESTS_DIR, "input_*.txt")))
    expected_files = sorted(glob.glob(os.path.join(TESTS_DIR, "expected_*.txt")))

    if not input_files or not expected_files:
        sys.stderr.write("Error: No input or expected files found in the 'tests' directory.\n")
        sys.exit(1)

    if len(input_files) != len(expected_files):
        sys.stderr.write("Error: Number of input and expected files do not match.\n")
        sys.exit(1)

    
    test_cases = [(str(i+1), inp, exp) for i, (inp, exp) in enumerate(zip(input_files, expected_files))]


    if not test_cases:
        sys.stderr.write("Error: No test cases found in the 'tests' directory.\n")
        sys.exit(1)

    passed_count = 0
    start_time = time.time()
    
    for test_number, input_file, expected_file in test_cases:
        passed, failed_test_num, stderr, expected, actual = run_test(
            EXECUTABLE, input_file, expected_file, test_number
        )

        if passed:
            passed_count += 1
        else:
            # Return details of the failed test case to stderr
            error_message = (
                f"Failed Test Case: {failed_test_num}\n"
                f"--- Expected Result ---\n{expected}\n"
                f"--- Actual Result ---\n{actual}\n"
                f"--- Program Stderr ---\n{stderr if stderr else 'None'}\n"
            )
            sys.stderr.write(error_message)
            # Exit after the first failure as per typical testing setups
            sys.exit(1) 

    end_time = time.time()
    total_time = end_time - start_time
    
    # If all tests passed, return the success message to stdout, and nothing to stderr 
    print(f"Total Cases Passed: {passed_count}/{len(test_cases)}")
    print(f"Time Spent: {total_time:.4f} seconds")

if __name__ == "__main__":
    main()


def run_all_tests():
    try:
        compile_c_code(C_FILE, EXECUTABLE)
    except SystemExit:
        return {"status": "compile_error"}

    input_files = sorted(glob.glob(os.path.join(TESTS_DIR, "input_*.txt")))
    expected_files = sorted(glob.glob(os.path.join(TESTS_DIR, "expected_*.txt")))

    if not input_files or not expected_files:
        return {"status": "error", "message": "Missing input or expected files"}
    if len(input_files) != len(expected_files):
        return {"status": "error", "message": "Mismatched number of test files"}

    test_cases = [
        (str(i + 1), inp, exp)
        for i, (inp, exp) in enumerate(zip(input_files, expected_files))
    ]

    passed_count = 0
    start_time = time.time()

    for test_number, input_file, expected_file in test_cases:
        passed, failed_test_num, stderr, expected, actual = run_test(
            EXECUTABLE, input_file, expected_file, test_number
        )

        if passed:
            passed_count += 1
        else:
            return {
                "status": "failed",
                "failed_case": failed_test_num,
                "expected": expected,
                "actual": actual,
                "stderr": stderr,
            }

    total_time = time.time() - start_time
    return {
        "status": "passed",
        "cases_passed": passed_count,
        "total_cases": len(test_cases),
        "time": round(total_time, 4),
    }
