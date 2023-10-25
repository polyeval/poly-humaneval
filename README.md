# PolyHumanEval
PolyEval version of OpenAI HumanEval (data + testing + multilingual solutions)

### Usage
```
$ python code/check_poly_humaneval.py --lang {the_language_to_test_here}
```


### Modification 
- HumanEval/22: change test `filter_integers([4, {}, [], 23.2, 9, 'adasd'])` to `filter_integers([4, 23.2, 9, 'adasd')`
- HumanEval/71: do not round to 2 decimals; more precise result
- HumanEval/90: change test `next_smallest([1, 0**0])` to `next_smallest([1, 0])`
- HumanEval/92: chang testcase (3.0, 4, 7) to (3.001, 4, 7) because some language(such as javascript) can't distinguish 3.0 and 3
- HumanEval/95: change test `check_dict_case({"p":"pineapple", 5:"banana", "a":"apple"})` to `check_dict_case({"p":"pineapple", "5":"banana", "a":"apple"})`
- HumanEval/103: change return -1 to return null, thus tests that expects -1 also change to null. Return without "0b", and change "round .5 to even" behavior to always ceiling.
- HumanEval/112: change the second return value to string, use "YES" and "NO" to represent palindrome and not palindrome
- HumanEval/116: delete the negative test case because of different representations in different languages (one's complement vs. two's complement)
- HumanEval/125: change the return number to a list of string with one element represent the number
- HumanEval/137: change the return type from any to double
- HumanEval/139: change test `special_factorial(7)` to `special_factorial(6)` because the former is too large for some languages

