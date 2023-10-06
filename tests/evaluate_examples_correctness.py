from polyeval.parsing import parse
from polyeval.generators import LangGenerator
from polyeval.eval.project_template import ProjectTemplate

import json

with open("../data/poly_fewshot_example.ped", "r") as f:
    desc_str = f.read()
problems = parse(desc_str)

with open("../data/poly_fewshot_sol.json", "r") as f:
    solutions = json.load(f)

langs = ["cpp", "csharp", "dart", "go", "java", "javascript", "kotlin", "php", "python", "ruby", "rust", "scala",
         "swift", "typescript"]

langs = ["cpp"]

for p_name, p in problems.data.items():
    for lang in langs:
        sol = solutions[p_name][lang]
        lang = "cppm"
        generator = LangGenerator.get_generator(lang=lang, problem=p)
        codes = generator.gen_codes()
        print(codes)
        proj_name = f"{lang}__{p_name}".replace("/", "-")
        print(f"{proj_name} Start")
        template = ProjectTemplate(f"../project_templates/{lang}")
        proj = template.create_project(proj_name, sol, codes, ".polyeval")
        print("Project create over")
        build_stat, msg = proj.compile()
        if not build_stat:
            print(msg)
            raise Exception(f"{proj_name} {msg}")
        print(msg)
        run_stat, msg = proj.run()
        if not run_stat:
            print(msg)
            raise Exception(f"{proj_name} {msg}")
        print(msg)
        check_stat, _ = proj.check_output()
        if not check_stat:
            raise Exception(f"Check failed for {proj_name}")

        # finally:
        #     proj.delete_folder()
        # proj.delete_folder()
        print(f"{proj_name} OK")
