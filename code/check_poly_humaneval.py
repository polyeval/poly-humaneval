from polyeval.parsing import parse
from polyeval.eval import ProjectTemplate, EvalStatus, gen_codes, create_project

from tqdm import tqdm
import sys
import os
import shutil
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

langs = ["cpp", "csharp", "dart", "go", "java", "javascript", "kotlin", "php", "python", "ruby", "rust", "scala",
         "swift", "typescript"]

suffix = {
    "cpp": "cpp",
    "csharp": "cs",
    "dart": "dart",
    "go": "go",
    "java": "java",
    "javascript": "js",
    "kotlin": "kt",
    "php": "php",
    "python": "py",
    "ruby": "rb",
    "rust": "rs",
    "scala": "scala",
    "swift": "swift",
    "typescript": "ts"
}
print(f"Loading project templates...")

cur_langs = langs
idxs = list(range(164))
if len(sys.argv) >= 2:
    cur_langs = [sys.argv[1]]
if len(sys.argv) == 3:
    idxs = [int(sys.argv[2])]
if len(sys.argv) == 4:
    idxs = list(range(int(sys.argv[2]), int(sys.argv[3]) + 1))
if len(sys.argv) > 4:
    raise Exception("args error")

templates = {}
for lang in cur_langs:
    templates[lang] = ProjectTemplate(os.path.join(ROOT, "./project-templates", lang))
print(f"Loading problem description and solution...")
with open(os.path.join(ROOT, "./data/poly_humaneval.ped"), "r") as f:
    desc_str = f.read()
    problems = parse(desc_str)
with open(os.path.join(ROOT, "./data/poly_humaneval_sol.json"), "r") as f:
    solutions = json.load(f)






def evaluate(proj):
    ret_stat, msg = proj.evaluate(compile_timeout=60, run_timeout=10, keep_when_fail=True)
    if ret_stat != EvalStatus.Pass:
        return False
    return True


for lang in cur_langs:
    projects = []
    print(f"Generating {lang} projects...")
    for idx in tqdm(idxs):
        problem = list(problems.values())[idx]
        solution = solutions[lang][problem.name]
        codes = gen_codes(lang=lang, problem=problem, target_code=solution)
        proj_name = f"{lang}_{idx}"
        proj = create_project(templates[lang], proj_name, codes, root=os.path.join(ROOT, ".polyeval/"), overwrite=True)
        projects.append([proj_name, proj])
    print(f"Evaluating {lang} projects...")
    for proj in tqdm(projects):
        ret_stat, msg = proj[1].evaluate(compile_timeout=60, run_timeout=10, keep_when_fail=True)
        if ret_stat != EvalStatus.Pass:
            print(f"{proj[0]} failed")
