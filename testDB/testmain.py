import os
import subprocess

def run_test_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(f"Running {script_name}...\n")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    print("========================================")

if __name__ == "__main__":
    print(os.getcwd())
    test_scripts = [
        # "testAiomysql.py",
        "testSqlalchemy.py",
        "testMysqlConnector.py",
        "testMysqldb.py",
        "testPyodbc.py"
        
    ]
    
    for script in test_scripts:
        run_test_script(script)
