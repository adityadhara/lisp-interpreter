import re

def verify_arithmetic(li):
    if len(li)==2:
        if re.match("^[+-]?\d(>?\.\d+)?$", li[0]):
            if re.match("^[+-]?\d(>?\.\d+)?$", li[1]):
                return True
    return False

def verify_quote(li):
    if len(li)==1:
        return True
    return False

def verify_eq(li):
    if len(li) == 2:
        return True
    return False


def verify_def_variable_set(li):
    if len(li) == 2:
        for item in li:
            if item is list:
                return False
        
        if re.match("^[+-]?\d(>?\.\d+)?$", li[0]):
            return False
            

VERIFICATIONS = {}
VERIFICATIONS["+"] = verify_arithmetic
VERIFICATIONS['-'] = verify_arithmetic
VERIFICATIONS['/'] = verify_arithmetic
VERIFICATIONS['*'] = verify_arithmetic
VERIFICATIONS['eq?'] = verify_eq
VERIFICATIONS['quote'] = verify_quote