import subprocess
import time
import os

def run_java_file(file_path: str):
    """
    Εκτελεί ένα Java αρχείο και συγκρίνει τα αποτελέσματα με τα testcases.
    file_path: path στο αρχείο .java (π.χ. "uploads/Sum.java")
    Επιστρέφει:
        - Αν όλα τα tests περάσουν: {"passed": n, "results": [...]}
        - Αν κάποιο test αποτύχει: {"testcase": i, "expected": "...", "got": "..."}
    """

    # Παίρνουμε το όνομα της κλάσης χωρίς .java
    class_name = os.path.splitext(os.path.basename(file_path))[0]

    # Compile στον φάκελο WORKDIR (π.χ. /app)
    compile_process = subprocess.run(
        ["javac", "-d", ".", file_path],
        capture_output=True,
        text=True
    )

    if compile_process.returncode != 0:
        # Αν αποτύχει το compile, επιστρέφουμε το σφάλμα
        return {"error": "Compilation failed", "details": compile_process.stderr}

    results = []
    testcases_folder = "testcases"  # Σωστό path μέσα στο Docker
    i = 1

    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir("."))
    print("Files in testcases folder:", os.listdir("testcases"))

    while True:
        input_file = os.path.join(testcases_folder, f"input{i}.txt")
        expected_file = os.path.join(testcases_folder, f"expected{i}.txt")

        if not os.path.exists(input_file) or not os.path.exists(expected_file):
            break  # Δεν υπάρχουν άλλα testcases

        # Διαβάζουμε το expected αποτέλεσμα
        with open(expected_file, "r") as f:
            expected = f.read().strip()

        # Διαβάζουμε το input
        with open(input_file, "r") as f:
            run_input = f.read()

        # Εκτέλεση της Java κλάσης
        start = time.time()
        run_process = subprocess.run(
            ["java", "-cp", ".", class_name],
            input=run_input,
            capture_output=True,
            text=True
        )
        end = time.time()

        output = run_process.stdout.strip()

        # Αν αποτύχει κάποιο test case
        if output != expected:
            return {
                "testcase": i,
                "expected": expected,
                "got": output
            }

        # Αποθήκευση αποτελέσματος για επιτυχημένα testcases
        results.append({
            "testcase": i,
            "time": round(end - start, 4)
        })
        i += 1

    # Όλα τα tests περάσανε
    return {"passed": len(results), "results": results}
