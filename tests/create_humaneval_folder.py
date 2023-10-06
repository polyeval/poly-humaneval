import json
import os

with open("../data/humanevalpack.jsonl", "r", encoding="utf-8") as f:
    lines = f.readlines()
    json_objects = [json.loads(line) for line in lines]

import_str = """\
from typing import List, Tuple, Dict, Optional, Any
import math
import random
import copy
import string


"""

for idx, j in enumerate(json_objects):
    code = j["prompt"] + j["canonical_solution"] + j["test"]
    os.makedirs(f"../humaneval/", exist_ok=True)
    with open(f"../humaneval/{idx}.py", "w", encoding="utf-8") as f:
        f.write(code)

