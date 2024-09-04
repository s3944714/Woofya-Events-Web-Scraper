import subprocess

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(['python', f'/home/rob/Woofya-Events-Web-Scraper/scrapers/{script_name}'], check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"{script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")

def main():
    scripts = [
        'Website_Yappack.py',
        'Travelnuity.py'
    ]
    
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
