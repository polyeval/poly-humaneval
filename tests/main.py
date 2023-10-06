from polyeval.parsing import parse
from polyeval.generators import LangGenerator
import json

a = """\
def compare_one(a:Any, b:Any) -> Any:
    a1 = a
    b1 = b
    if isinstance(a1, str): 
        a1 = a1.replace(',','.')
    if isinstance(b1, str): 
        b1 = b1.replace(',','.')
    if float(a1) == float(b1): 
        return None
    elif float(a1) > float(b1):
        return a
    else:
        return b\
"""
print(json.dumps(a))

# with open("../data/poly_humaneval.ped", "r", encoding="utf-8") as f:
#     ped = f.read()
# problems = parse(ped)
# print(len(problems.data.keys()))
#
# langs = [
#     "python",
# ]
# count = 0
# for name, problem in problems.data.items():
#     for lang in langs:
#         generator = LangGenerator.get_generator(lang, problem)
#         # print(f"{lang} prompt:")
#         print(generator.gen_codes()["main"])
#     count += 1
#     if count >= 7:
#         break
