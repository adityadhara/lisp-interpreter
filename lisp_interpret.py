import sys
import re

class Interpreter():
    variables = {}
    verbose = False
    validations = {}
    functions = {}
    
    def __init__(self, functions_dict, validations_dict, verb = False):
        self.verbose = verb
        self.functions = functions_dict
        self.validations = validations_dict
        
    def is_symbol(self, elem):
        if not isinstance(elem, list):
            if not elem in self.variables:
                if not elem in self.functions:
                    return True
        else:
            if elem[0][0]=="'":
                return True
        return False
    
    def verify_line_syntax(self, l):
        return True
    
    def verify_file_syntax(self, f):
        return True
    
    def eval_line(self, l):
        self.verify_line_syntax(l)
        line_parsed = self.parse_line(l)
        result = self.eval(line_parsed, 0)
        if not result == None:
            print result

    def interpret(self, f):
        #read line by line, keeping track of line number
        #we assume file syntax is verified
        line_count = 0
        for line in f:
            line_count += 1
            line_parsed = self.parse_line(line)
            if verbose: print str(line_count)+":", line_parsed
            result = self.eval(line_parsed, line_count)
            if not result==None:
                print result
    
    def parse_line(self, line):
        #Find the elements in the str
        elements = [[]]
        
        text = line.strip()
        if text == "":
            return []
        
        quoting = False
        block = 0
        item = ""
        for i in re.split("([\s()'])", text):
            #YOU NEED TO CLEAN THIS UP
            if quoting == True:
                if (i == " " or i == ")") and block == 0:
                    last = elements.pop()
                    elements[-1].append(last)
                    quoting = False
                elif i == '' or i == ' ':
                    continue
                elif i == "(":
                    elements.append([])
                    block += 1
                elif i == ")":
                    last = elements.pop()
                    elements[-1].append(last)
                    block -= 1
                else:
                    elements[-1].append(i)
            if quoting == False:
                if i == '' or i == " ":
                    continue
                elif (i=="'"):
                    quoting = True
                    elements.append([])
                    elements[-1].append(i)
                elif i == "(":
                    elements.append([])
                elif i == ")":
                    last = elements.pop()
                    elements[-1].append(last)
                elif i[0] == "#":
                    break
                else:
                    elements[-1].append(i)
        return elements[0]

    def eval(self, elements, counter):
        if elements==[]: return None
        
        #evaluating all static non-list items
        if not isinstance(elements, list):
            if elements in self.variables:
                return self.eval(self.variables[elements], counter)
            if self.is_symbol(elements):
                return elements
        else:
            #evaluate all list elements
            for i in xrange(len(elements)):
                elements[i] = self.eval(elements[i], counter)
            
            #evaluate lists as functions now
            if elements[0] not in self.functions:
                print "Undefined function in line", str(counter) + ":", elements[0]
                return None
            else:
                params = elements[1:]
                if self.validations[elements[0]] (params):
                    self.functions[elements[0]] (params)
            
            
                
