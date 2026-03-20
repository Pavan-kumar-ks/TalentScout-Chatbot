import json
import os

FILE_PATH = "data/candidates.json"


def save_candidate(candidate_data):
    try:
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, "w") as f:
                json.dump([], f)

        with open(FILE_PATH, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

        data.append(candidate_data)

        with open(FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Candidate saved successfully!")

    except Exception as e:
        print("❌ Error saving candidate:", e)