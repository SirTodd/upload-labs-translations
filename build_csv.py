import pandas as pd
import os
import json

def merge_json_to_csv(output_file):
    merged_data = {}
    
    files = [f for f in os.listdir() if f.endswith('.json')]
    
    if not files:
        print("No JSON files found to merge.")
        return

    print(f"Found files: {', '.join(files)}")

    for filename in files:
        lang_code = os.path.splitext(filename)[0]
        file_path = os.path.join(filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for key, translation in data.items():
                    if key not in merged_data:
                        merged_data[key] = {}
                    
                    merged_data[key][lang_code] = translation
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    df = pd.DataFrame.from_dict(merged_data, orient='index')

    cols = list(df.columns)
    if 'en' in cols:
        cols.insert(0, cols.pop(cols.index('en')))
    df = df[cols]

    df.index.name = 'key'
    df.reset_index(inplace=True)

    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Success! Merged file saved as: {output_file}")

if __name__ == "__main__":
    merge_json_to_csv('locale.csv')