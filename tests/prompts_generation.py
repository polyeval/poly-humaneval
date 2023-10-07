from polyeval.parsing import parse
from polyeval.generators import LangGenerator
from polyeval.eval.project_template import ProjectTemplate

import json

langs = ["cpp", "csharp", "dart", "go", "java", "javascript", "kotlin", "php", "python", "ruby", "rust", "scala",
         "swift", "typescript"]

lang_names = {
    "cpp": "C++",
    "csharp": "C#",
    "dart": "Dart",
    "go": "Go",
    "java": "Java",
    "javascript": "JavaScript",
    "kotlin": "Kotlin",
    "python": "Python",
    "php": "PHP",
    "ruby": "Ruby",
    "rust": "Rust",
    "scala": "Scala",
    "swift": "Swift",
    "typescript": "TypeScript"
}

with open("../data/poly_humaneval.ped", "r") as f:
    desc_str = f.read()
problems = parse(desc_str)
print(len(problems.data))

with open("../data/poly_humaneval_sol_py.json", "r") as f:
    solutions = json.load(f)

with open("../data/poly_fewshot_prompts.json", "r") as f:
    fewshot_prompts = json.load(f)

prompts = []

for p_name, p in problems.data.items():
    py_solution = solutions[p_name]
    for lang in langs:
        if lang == "python":
            continue
        generator = LangGenerator.get_generator(lang=lang, problem=p)
        code_prompt = generator.gen_prompt()
        prompt_id = f"{lang}_{p_name}"
        prompt = f"""\
Translate the following Python code to {lang_names[lang]}:
```python
{py_solution}
```
Following the format:
```{lang}
{code_prompt}
```"""
        # messages = fewshot_prompts["python"][lang]["messages"]
        old_messages = fewshot_prompts["python"][lang]["messages"]
        assert len(old_messages) == 5
        messages = [item for item in old_messages]
        messages.append({
            "role": "user",
            "content": prompt
        })
        prompt_obj = {
            "task_id": prompt_id,
            "messages": messages
        }
        prompts.append(prompt_obj)

prompts = sorted(prompts, key=lambda x: x["task_id"])
print(len(prompts))

with open("../data/poly_humaneval_prompts.json", "w") as f:
    json.dump(prompts, f, indent=4)
