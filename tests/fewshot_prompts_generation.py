
from polyeval.parsing import parse
from polyeval.generators import LangGenerator

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

with open("../data/poly_fewshot_example.ped", "r") as f:
    desc_str = f.read()
problems = parse(desc_str)

with open("../data/poly_fewshot_sol.json", "r") as f:
    solutions = json.load(f)

prompts = {}
for src_lang in langs:
    prompts[src_lang] = {}
    for tgt_lang in langs:
        if src_lang == tgt_lang:
            continue
        prompts[src_lang][tgt_lang] = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people perform tasks."
                },
            ]
        }

for p_name, p in problems.data.items():
    for src_lang in langs:
        src_code = solutions[p_name][src_lang]
        for tgt_lang in langs:
            if src_lang == tgt_lang:
                continue
            tgt_code = solutions[p_name][tgt_lang]
            generator = LangGenerator.get_generator(lang=tgt_lang, problem=p)
            code_prompt = generator.gen_prompt()
            user_content = f"""\
Translate the following {lang_names[src_lang]} code to {lang_names[tgt_lang]}:
```{src_lang}
{src_code}
```
Following the format:
```{tgt_lang}
{code_prompt}
```"""
            assistant_content = f"""\
```{tgt_lang}
{tgt_code}
```"""
            prompts[src_lang][tgt_lang]["messages"].append({
                "role": "user",
                "content": user_content
            })

            prompts[src_lang][tgt_lang]["messages"].append({
                "role": "assistant",
                "content": assistant_content
            })

with open("../data/poly_fewshot_prompts.json", "w") as f:
    json.dump(prompts, f, indent=4)