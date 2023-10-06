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

with open("../data/poly_fewshot_example.ped", "r") as f:
    desc_str = f.read()
problems = parse(desc_str)
print(len(problems.data))

prompts = []

for p_name, p in problems.data.items():
    for lang in langs:
        generator = LangGenerator.get_generator(lang=lang, problem=p)
        code_prompt = generator.gen_prompt()
        prompt_id = f"{lang}_{p_name}"
        if p_name == "Example_0":
            description = "return reversed input list."
            cpp_sol = "vector<string> reverseList(const vector<string>& strs) {\n    vector<string> reversedList(strs.rbegin(), strs.rend());\n    return reversedList;\n}"
        elif p_name == "Example_1":
            description = "only keep the odd numbers in the input list, and you should define a `check` helper function."
            cpp_sol = "bool check(int number) {\n    return number % 2 != 0;\n}\n\nvector<int> filterOdd(const vector<int>& numbers) {\n    vector<int> oddNumbers;    \n    for (int num : numbers) {\n        if (check(num)) {\n            oddNumbers.push_back(num);\n        }\n    }   \n    return oddNumbers;\n}"
        prompt = f"""\
Translate the following C++ code to {lang_names[lang]}:
```cpp
{cpp_sol}
```
Following the format:
```{lang}
{code_prompt}
```"""
        prompts.append({
            "task_id": prompt_id,
            "prompt": prompt,
        })

with open("../data/poly_fewshot_prompts.json", "w") as f:
    json.dump(prompts, f, indent=4)
