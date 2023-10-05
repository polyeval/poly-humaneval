from polyeval.parsing import parse
from polyeval.generators import LangGenerator

with open("../poly_humaneval.ped", "r", encoding="utf-8") as f:
    ped = f.read()
problems = parse(ped)
print(len(problems.data.keys()))

langs = [
    "python",
]
count = 0
for name, problem in problems.data.items():
    for lang in langs:
        generator = LangGenerator.get_generator(lang, problem)
        # print(f"{lang} prompt:")
        print(generator.gen_codes()["main"])
    count += 1
    if count >= 7:
        break
