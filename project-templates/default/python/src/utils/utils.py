from __future__ import annotations

import math


def escape_string(s: str):
    new_s = []
    for c in s:
        if c == "\\":
            new_s.append("\\\\")
        elif c == "\"":
            new_s.append("\\\"")
        elif c == "\n":
            new_s.append("\\n")
        elif c == "\t":
            new_s.append("\\t")
        elif c == "\r":
            new_s.append("\\r")
        else:
            new_s.append(c)
    return "".join(new_s)


class PolyEvalType:
    def __init__(self, type_str: str):
        self.type_str = type_str
        self.type_name: str = None
        self.value_type: PolyEvalType = None
        self.key_type: PolyEvalType = None

        if "<" not in type_str:
            self.type_name = type_str
            return
        else:
            idx = type_str.index("<")
            self.type_name = type_str[:idx]
            other_str = type_str[idx + 1:-1]
            if "," not in other_str:
                self.value_type = PolyEvalType(other_str)
            else:
                idx = other_str.index(",")
                self.key_type = PolyEvalType(other_str[:idx])
                self.value_type = PolyEvalType(other_str[idx + 1:])


def gen_void(value):
    assert value is None
    return "null"


def gen_int(value):
    assert isinstance(value, int) or (isinstance(value, float) and value.is_integer())
    value = int(value)
    return str(value)


def gen_long(value):
    assert isinstance(value, int)
    return str(value) + "L"


def gen_double(value):
    assert isinstance(value, int) or isinstance(value, float)
    value = float(value)
    if math.isnan(value):
        return "nan"
    elif math.isinf(value):
        if value > 0:
            return "inf"
        else:
            return "-inf"
    value_str = "{:.6f}".format(value).rstrip("0")
    if value_str.endswith("."):
        value_str += "0"
    if value_str == "-0.0":
        value_str = "0.0"
    return value_str


def gen_bool(value):
    assert isinstance(value, bool)
    return "true" if value else "false"


def gen_char(value):
    assert isinstance(value, str)
    return "'" + escape_string(value) + "'"


def gen_string(value):
    assert isinstance(value, str)
    return '"' + escape_string(value) + '"'


def gen_any(value):
    if isinstance(value, bool):
        return gen_bool(value)
    elif isinstance(value, int) or isinstance(value, float):
        return gen_double(value)
    elif isinstance(value, str):
        return gen_string(value)
    assert False


def gen_list(value, t: PolyEvalType):
    assert isinstance(value, list)
    v_strs = [to_poly_eval_str_with_type(value, t.value_type) for value in value]
    v_str = ", ".join(v_strs)
    return f"[{v_str}]"


def gen_mlist(value, t: PolyEvalType):
    assert isinstance(value, list)
    v_strs = [to_poly_eval_str_with_type(value, t.value_type) for value in value]
    v_str = ", ".join(v_strs)
    return f"[{v_str}]"


def gen_unorderedlist(value, t: PolyEvalType):
    assert isinstance(value, list)
    v_strs = sorted([to_poly_eval_str_with_type(value, t.value_type) for value in value])
    v_str = ", ".join(v_strs)
    return f"[{v_str}]"


def gen_dict(value, t: PolyEvalType):
    assert isinstance(value, dict)
    v_strs = []
    for key, val in value.items():
        k_str = to_poly_eval_str_with_type(key, t.key_type)
        v_str = to_poly_eval_str_with_type(val, t.value_type)
        v_strs.append(f"{k_str}=>{v_str}")
    v_strs = sorted(v_strs)
    v_str = ", ".join(v_strs)
    return f"{{{v_str}}}"


def gen_mdict(value, t: PolyEvalType):
    assert isinstance(value, dict)
    v_strs = []
    for key, val in value.items():
        k_str = to_poly_eval_str_with_type(key, t.key_type)
        v_str = to_poly_eval_str_with_type(val, t.value_type)
        v_strs.append(f"{k_str}=>{v_str}")
    v_strs = sorted(v_strs)
    v_str = ", ".join(v_strs)
    return f"{{{v_str}}}"


def gen_optional(value, t: PolyEvalType):
    if value is None:
        return "null"
    else:
        return to_poly_eval_str(value, t.value_type)


def to_poly_eval_str(value, t: PolyEvalType):
    type_name = t.type_name
    if type_name == "void":
        return gen_void(value)
    elif type_name == "int":
        return gen_int(value)
    elif type_name == "long":
        return gen_long(value)
    elif type_name == "double":
        return gen_double(value)
    elif type_name == "bool":
        return gen_bool(value)
    elif type_name == "char":
        return gen_char(value)
    elif type_name == "string":
        return gen_string(value)
    elif type_name == "any":
        return gen_any(value)
    elif type_name == "list":
        return gen_list(value, t)
    elif type_name == "mlist":
        return gen_mlist(value, t)
    elif type_name == "unorderedlist":
        return gen_unorderedlist(value, t)
    elif type_name == "dict":
        return gen_dict(value, t)
    elif type_name == "mdict":
        return gen_mdict(value, t)
    elif type_name == "optional":
        return gen_optional(value, t)
    assert False, f"Unknown type {type_name}"


def to_poly_eval_str_with_type(value, t: PolyEvalType):
    return to_poly_eval_str(value, t) + ":" + t.type_str


def my_stringify(value, type_str: str):
    return to_poly_eval_str_with_type(value, PolyEvalType(type_str))
