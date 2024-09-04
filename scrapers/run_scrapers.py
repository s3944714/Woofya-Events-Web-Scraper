import subprocess
import os

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"{script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")

def main():
    scripts = [
        'Website_Yappack.py',
        'Travelnuity.py',
        'scrape_stella_insurance.py'  # Add the Stella Insurance script here
    ]
    
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
