import json
from typing import List
from platformdirs import user_data_dir
from pathlib import Path

# init the data files
app = "zxdf"
author = "choneface"
data_dir = user_data_dir(app, author, ensure_exists=True)

skill_metadata_file = Path(data_dir) / "skills.json" 


def saveSkillMetadata(skillmetadata: dict) -> None:
    if skill_metadata_file.exists():
        with open(skill_metadata_file, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = {"skills": []}

    # needs deduping but eff that for right now
    content["skills"].append(skillmetadata)

    with open(skill_metadata_file, "w", encoding="utf-8") as f:
        json.dump(content, f)

def fetchSkillMetadata() -> List:
    if skill_metadata_file.exists():
        with open(skill_metadata_file, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = {"skills": []}

    return content["skills"]
