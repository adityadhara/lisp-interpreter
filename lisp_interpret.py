print "imported lisp_interpreter"

import sys
import re
from lisp_verify import *

vars = {"var1": "hello"}
lambdas = {}
verbose = False

def interpret(f, verb = True):
    #global verbose
    #verbose = verb
    
    #read line by line
    line_count = 0
    for line in f:
        line_count += 1
        if verbose: print str(line_count)+":", line.strip()
        result = eval(line, line_count)
        if not result==None:
            print result

def eval(input, counter):
    
    #Find the elements in the str
    text = input.strip()
    if "#" in text: #remove comments
        text = text[0:text.index("#")]
        text = text.strip()
    if text == "": return
    if text[0]=="(":
        text = text[1:len(text)-1]
    if verbose: print text

    elements = []
    nesting = False
    temp_elem = ""
    for i in text:
        if i == " ":
            if not nesting:
                elements.append(temp_elem)
                temp_elem = ""
                continue
        if i == "(":
            nesting = True
        if i == ")":
            nesting = False
        if i == "#":
            break
        temp_elem = temp_elem + i
    if temp_elem: elements.append(temp_elem) #add trailing pieces
    if verbose: print elements

    #Now that we have elements, process them
    if len(elements)==1:
        if elements[0][0]=="(":
            elements[0] = eval(elements[0][1:len(elements[0])-1], counter)
        else:
            if elements[0][0] == "'":
                return elements[1:]
            else:
                if elements[0] in vars.keys():
                    return vars[elements[0]]
                return elements[0] #NEEDS TO BE FIXED HERE - what about uninitiated varibles?
    else:
        return process(elements, counter)

def process(li, counter):
    op = li[0]
    
    for i in xrange(len(li)):
        li[i] = str(eval(li[i], counter))

    if op=='+':
        validate(op, li, counter)
        if "." in li[1] or "." in li[2]:
            return float(li[1])+float(li[2])
        else:
            return int(li[1])+int(li[2])
    elif op=='-':
        validate(op, li, counter)
        if "." in li[1] or "." in li[2]:
            return float(li[1])-float(li[2])
        else:
            return int(li[1])-int(li[2])

    return li

def validate(op, li, counter):

    if op=='+':
        if len(li)<=3:
            if li[1][0]=="(" or re.match("^[+-]?\d(>?\.\d+)?$", li[1]):
                if li[2][0]=="(" or re.match("^[+-]?\d(>?\.\d+)?$", li[2]):
                    return
        print "There is an error in line", counter
        sys.exit()

    return
