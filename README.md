# PolyHumanEval
PolyEval version of OpenAI HumanEval (data + testing + multilingual solutions)

Modification: 
- HumanEval/22: change test `filter_integers([4, {}, [], 23.2, 9, 'adasd'])` to `filter_integers([4, 23.2, 9, 'adasd')`
- HumanEval/71: do not round to 2 decimals; more precise result
- HumanEval/90: change test `next_smallest([1, 0**0])` to `next_smallest([1, 0])`
- HumanEval/95: change test `check_dict_case({"p":"pineapple", 5:"banana", "a":"apple"})` to `check_dict_case({"p":"pineapple", "5":"banana", "a":"apple"})`
- HumanEval/103: change return -1 to return null, thus tests that expects -1 also change to null. Also return without "0b".
- HumanEval/112: change the second return value to string, use "YES" and "NO" to represent palindrome and not palindrome
- HumanEval/125: change the return number to a list of string with one element represent the number
- HumanEval/139: change test `special_factorial(7)` to `special_factorial(6)`

