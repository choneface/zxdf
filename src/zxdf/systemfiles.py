import json
import os
from platformdirs import user_data_dir
from pathlib import Path

# init the data files
app = "zxdf"
author = "choneface"
data_dir = user_data_dir(app, author, ensure_exists=True)

skill_metadata_file = data_dir + "/" + "skills.json" 


def saveSkillMetadata(skillmetadata):
    if Path(skill_metadata_file).exists():
        with open(skill_metadata_file, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = {"skills": []}

    # needs deduping but eff that for right now
    content["skills"].append(skillmetadata)

    with open(skill_metadata_file, "w", encoding="utf-8") as f:
        content = json.dump(content, f)
