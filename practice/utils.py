import os
import json
from django.conf import settings
from datetime import datetime

def log_activity(username, action):
    log_entry = {
        'username' : username,
        'action':  action,
        'time': datetime.now().isoformat()
    }

    file_path = settings.LOG_JSON_PATH

    if os.path.exists(file_path):
            with open(file_path, 'r+') as json_file:
                try:
                    file_data = json.load(json_file)
                    if isinstance(file_data, dict):
                        file_data = [file_data]
                    file_data.append(log_entry)
                except json.JSONDecodeError:
                    file_data = [log_entry]

                json_file.seek(0)
                json.dump(file_data, json_file, indent=4)
    else:
        with open(file_path, 'w') as json_file:
            json.dump(log_entry, json_file, indent=4)