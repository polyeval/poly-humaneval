library utils;

import 'dart:io';
import 'dart:collection';
import 'dart:math';

String _escapeString(String s) {
    StringBuffer newS = new StringBuffer();
    for (int i = 0; i < s.length; i++) {
        String c = s[i];
        switch (c) {
            case '\\':
                newS.write("\\\\");
                break;
            case '\"':
                newS.write("\\\"");
                break;
            case '\n':
                newS.write("\\n");
                break;
            case '\t':
                newS.write("\\t");
                break;
            case '\r':
                newS.write("\\r");
                break;
            default:
                newS.write(c);
        }
    }
    return newS.toString();
}

class _PolyEvalType {
    String typeStr = "";
    String typeName = "";
    _PolyEvalType? valueType;
    _PolyEvalType? keyType;

    _PolyEvalType(String typeStr) {
        this.typeStr = typeStr;
        if (!typeStr.contains("<")) {
            this.typeName = typeStr;
        } else {
            int idx = typeStr.indexOf("<");
            this.typeName = typeStr.substring(0, idx);
            String otherStr = typeStr.substring(idx + 1, typeStr.length - 1);
            if (!otherStr.contains(",")) {
                this.valueType = new _PolyEvalType(otherStr);
            } else {
                int idx = otherStr.indexOf(",");
                this.keyType = new _PolyEvalType(otherStr.substring(0, idx));
                this.valueType = new _PolyEvalType(otherStr.substring(idx + 1));
            }
        }
    }
}

String _genVoid(Object? value) {
    assert(value == null);
    return "null";
}

String _genInt(Object? value) {
    assert(value is int);
    return value.toString();
}

String _genLong(Object? value) {
    assert(value is int);
    return value.toString() + "L";
}

String _genDouble(Object? value) {
    assert(value is double);
    double f = value as double;
    if (f.isNaN) {
        return "nan";
    } else if (f.isInfinite) {
        if (f > 0) {
            return "inf";
        } else {
            return "-inf";
        }
    }
    String valueStr = f.toStringAsFixed(6);
    while (valueStr.endsWith("0")) {
        valueStr = valueStr.substring(0, valueStr.length - 1);
    }
    if (valueStr.endsWith(".")) {
        valueStr += "0";
    }
    if (valueStr == "-0.0") {
        valueStr = "0.0";
    }
    return valueStr;
}

String _genBool(Object? value) {
    assert(value is bool);
    return (value as bool) ? "true" : "false";
}

String _genChar(Object? value) {
    assert(value is String);
    return "'" + _escapeString((value as String)) + "'";
}

String _genString(Object? value) {
    assert(value is String);
    return "\"" + _escapeString(value as String) + "\"";
}

String _genAny(Object? value) {
    if (value is bool) {
        return _genBool(value);
    } else if (value is int) {
        return _genInt(value);
    } else if (value is double) {
        return _genDouble(value);
    } else if (value is String) {
        return _genString(value);
    }
    assert(false);
    return "";
}

String _genList(Object? value, _PolyEvalType t) {
    assert(value is List);
    List list = value as List;
    List<String> vStrs = [];
    for (var v in list) {
        vStrs.add(_toPolyEvalStrWithType(v, t.valueType!));
    }
    String vStr = vStrs.join(", ");
    return "[$vStr]";
}

String _genMlist(Object? value, _PolyEvalType t) {
    assert(value is List);
    List list = value as List;
    List<String> vStrs = [];
    for (var v in list) {
        vStrs.add(_toPolyEvalStrWithType(v, t.valueType!));
    }
    String vStr = vStrs.join(", ");
    return "[$vStr]";
}

String _genUnorderedlist(Object? value, _PolyEvalType t) {
    assert(value is List);
    List list = value as List;
    List<String> vStrs = [];
    for (var v in list) {
        vStrs.add(_toPolyEvalStrWithType(v, t.valueType!));
    }
    vStrs.sort();
    String vStr = vStrs.join(", ");
    return "[$vStr]";
}

String _genDict(Object? value, _PolyEvalType t) {
    assert(value is Map);
    Map map = value as Map;
    List<String> vStrs = [];
    map.forEach((key, value) {
        String kStr = _toPolyEvalStrWithType(key, t.keyType!);
        String vStr = _toPolyEvalStrWithType(value, t.valueType!);
        vStrs.add("$kStr=>$vStr");
    });
    vStrs.sort();
    String vStr = vStrs.join(", ");
    return "{$vStr}";
}

String _genMdict(Object? value, _PolyEvalType t) {
    assert(value is Map);
    Map map = value as Map;
    List<String> vStrs = [];
    map.forEach((key, value) {
        String kStr = _toPolyEvalStrWithType(key, t.keyType!);
        String vStr = _toPolyEvalStrWithType(value, t.valueType!);
        vStrs.add("$kStr=>$vStr");
    });
    vStrs.sort();
    String vStr = vStrs.join(", ");
    return "{$vStr}";
}

String _genOptional(Object? value, _PolyEvalType t) {
    return value != null ? _toPolyEvalStr(value, t.valueType!) : "null";
}

String _toPolyEvalStr(Object? value, _PolyEvalType t) {
    String typeName = t.typeName;
    if (typeName == "void") {
        return _genVoid(value);
    } else if (typeName == "int") {
        return _genInt(value);
    } else if (typeName == "long") {
        return _genLong(value);
    } else if (typeName == "double") {
        return _genDouble(value);
    } else if (typeName == "bool") {
        return _genBool(value);
    } else if (typeName == "char") {
        return _genChar(value);
    } else if (typeName == "string") {
        return _genString(value);
    } else if (typeName == "any") {
        return _genAny(value);
    } else if (typeName == "list") {
        return _genList(value, t);
    } else if (typeName == "mlist") {
        return _genMlist(value, t);
    } else if (typeName == "unorderedlist") {
        return _genUnorderedlist(value, t);
    } else if (typeName == "dict") {
        return _genDict(value, t);
    } else if (typeName == "mdict") {
        return _genMdict(value, t);
    } else if (typeName == "optional") {
        return _genOptional(value, t);
    }
    assert(false);
    return "";
}

String _toPolyEvalStrWithType(Object? value, _PolyEvalType t) {
    return _toPolyEvalStr(value, t) + ":" + t.typeStr;
}

String myStringify(Object? value, String typeStr) {
    return _toPolyEvalStrWithType(value, new _PolyEvalType(typeStr));
}




