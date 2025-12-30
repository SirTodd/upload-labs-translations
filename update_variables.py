import json
import os
import re

def extract_variables(text):
    """Finds all instances of {variable} in a string."""
    if not isinstance(text, str):
        return []
    return re.findall(r"\{.*?\}", text)

def sync_variables():
    current_dir = os.getcwd()
    en_path = os.path.join(current_dir, "en.json")

    if not os.path.exists(en_path):
        print("Error: en.json not found in the current directory.")
        return

    with open(en_path, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    target_files = [
        f for f in os.listdir(current_dir) 
        if f.endswith(".json") and f != "en.json"
    ]

    for filename in target_files:
        file_path = os.path.join(current_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            target_data = json.load(f)

        modified = False

        for key, en_value in en_data.items():
            if key in target_data:
                en_vars = extract_variables(en_value)
                target_value = target_data[key]

                if en_vars and isinstance(target_value, str):
                    new_value = re.sub(r"\{.*?\}", lambda m: en_vars[0], target_value)
                    
                    if new_value != target_value:
                        target_data[key] = new_value
                        modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    target_data, 
                    f, 
                    indent=4, 
                    ensure_ascii=False, 
                    separators=(",", ":")
                )
            print(f"Synced variables in: {filename}")
        else:
            print(f"No changes needed for: {filename}")

if __name__ == "__main__":
    sync_variables()