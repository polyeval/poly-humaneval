from polyeval.parsing import parse
from polyeval.generators import LangGenerator
from polyeval.eval.project_template import ProjectTemplate

import json

with open("../data/poly_humaneval.ped", "r") as f:
    desc_str = f.read()
problems = parse(desc_str)
print(len(problems.data))

template = ProjectTemplate(f"./python")

with open("../output/humaneval_results.json", "r") as f:
    solutions = json.load(f)

results = {}
for problem_name, problem in problems.data.items():
    problem_he_idx = problem_name.split("/")[1]
    # add leading 0 to 3 digits
    problem_he_idx = problem_he_idx.zfill(3)
    problem_sol_idx = f"Python_humaneval-{problem_he_idx}"
    if problem_name in solutions:
        target_code = solutions[problem_name]["code"]
        generator = LangGenerator.get_generator(lang="python", problem=problem)
        codes = generator.gen_codes()
        prompt = generator.gen_prompt()
        prompt_lines = prompt.split("\n")
        def_lines = [line for line in prompt_lines if line.startswith("def") and line.strip().endswith(":")]
        def_cnt = len(def_lines)
        target_code_def_cnt = target_code.count("def ")
        for def_line in def_lines:
            if def_line not in target_code:
                raise Exception(f"Prompt {def_line} not in target_code")
        proj_name = f"{problem_sol_idx}_python".replace("/", "-")
        proj = template.create_project(proj_name, target_code, codes, "./.polyeval")
        build_stat, msg = proj.compile()
        if not build_stat:
            print(msg)
        run_stat, msg = proj.run()
        if not run_stat:
            print(msg)
        check_stat, _ = proj.check_output()
        results[problem_name] = target_code
        proj.delete_folder()

with open("../data/poly_humaneval_sol_py.json", "w") as f:
    json.dump(results, f, indent=4)
