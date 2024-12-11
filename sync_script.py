import os
import requests

# API Base URL
API_BASE_URL = "https://magpie-credible-polecat.ngrok-free.app"  
PS_HISTORY_FILE = f"C:/Users/{os.environ.get('USERNAME')}/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"

def read_powershell_history():                                          

    if not os.path.exists(PS_HISTORY_FILE):
        print("PowerShell history file not found.")
        return []
    try:
        with open(PS_HISTORY_FILE, "r", encoding="utf-8") as f:
            commands = f.readlines()
        return [cmd.strip() for cmd in commands if cmd.strip()]
    except Exception as e:
        print(f"Error reading PowerShell history: {e}")
        return []

def fetch_commands_from_api(user_id):

    url = f"{API_BASE_URL}/commands"
    params = {"user_id": user_id}

    print("Fetching commands with parameters:", params)

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            commands = response.json()
            print(f"Fetched {len(commands)} commands from the API.")
            return commands
        else:
            print(f"Failed to fetch commands: {response.status_code}, {response.text}")
            return []
    except requests.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return []

def upload_commands_to_api(commands, user_id):

    url = f"{API_BASE_URL}/commands"
    payload = {"commands": [{"command": cmd, "user_id": user_id} for cmd in commands]}
    print("Payload being sent to API:", payload)

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            print("Commands uploaded successfully!")
        else:
            print(f"Failed to upload commands: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Error connecting to the API: {e}")

def append_to_local_history(commands, file_path):
    try:
        print(f"Appending commands to: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            for cmd in commands:
                if cmd.strip():                                             #Avoid empty commands
                    f.write(cmd + "\n")
        print("Commands appended successfully.")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

if __name__ == "__main__":
    user_id = "sasuke"
    
    print("Reading PowerShell history...")                                  #Read Local PowerShell History
    ps_commands = read_powershell_history()
                                                                    
    if ps_commands:
        print("\nUploading PowerShell commands to the API...")              #Upload Commands to the API
        upload_commands_to_api(ps_commands, user_id)
    else:
        print("No commands to upload.")
                                                                    
    print("\nFetching commands from the API...")
    fetched_commands = fetch_commands_from_api(user_id)                     #Fetch Commands from the API

    if fetched_commands:
        commands_to_append = [cmd["command"] for cmd in fetched_commands]   #Extract only the 'command' field                                                          
        print("\nAppending commands to PowerShell history file...")         #Append to PowerShell history
        append_to_local_history(commands_to_append, PS_HISTORY_FILE)
    else:
        print("No commands found in the API.")

