import re

def add(li):
    if "." in li[0] or "." in li[1]:
        return float(li[0])+float(li[1])
    else:
        return int(li[0])+int(li[1])

def subtract(li):
    if "." in li[0] or "." in li[1]:
        return float(li[0])-float(li[1])
    else:
        return int(li[0])-int(li[1])

def divide(li):
    return float(li[0])/float(li[1])

def multiply(li):
    if "." in li[0] or "." in li[1]:
        return float(li[0])*float(li[1])
    else:
        return int(li[0])*int(li[1])
    
def eq(li):
    #correct for an apostrophes
    for i in xrange(len(li)):
        if isinstance(li[i], list):
            if li[i][0] == "'":
                li[i] = li[i][1]
    
    #handle lists and then handle string types
    if isinstance(li[0], list):
        if isinstance(li[1], list):
            if not len(li[0])==len(li[1]): #first clue
                return "False"
            for i in xrange(len(li)): #check each element
                if not eq([li[0][i], li[1][i]])=="True":
                    return "False"
            return "True"
    elif isinstance(li[0], str) and isinstance(li[1], str):
        #if comparing numbers
        if re.match("^[+-]?\d(>?\.\d+)?$", li[0]):
            if re.match("^[+-]?\d(>?\.\d+)?$", li[1]):
                if float(li[0])==float(li[1]):
                    return "True"
        
        if li[0]==li[1]:
            return "True"
    
    #default
    return "False"
    
def quote(li):
    #if already apostrophe-d, return
    if isinstance(li[0], list):
        if li[0][0] == "'":
            return li[0]
    ret = ["'"]
    ret.append(li[0])
    return ret

FUNCTIONS = {}
FUNCTIONS['+'] = add
FUNCTIONS['-'] = subtract
FUNCTIONS['/'] = divide
FUNCTIONS['*'] = multiply
FUNCTIONS['eq?'] = eq
FUNCTIONS['quote'] = quote