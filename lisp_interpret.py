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
        
        #map def to def_
        #functions_dict['def'] = lambda x: functions_dict['def_'](x, self.vars)
    
    #Utility functions:
    def is_static_symbol(self, elem):
        if not isinstance(elem, list):
            if elem in self.variables:
                return False
            elif re.match("^[+-]?\d(>?\.\d+)?$", elem):
                return True
            elif elem in self.functions:
                return True
        elif elem[0]=="'":
            return True
        return False
    
    #pre-processing verification
    def verify_line_syntax(self, line, counter):
        #first check if brackets are ok
        sum = 0
        l = line.strip()
        
        #everything after comments is ignored
        if "#" in l:
            l = l[:l.index("#")]
        
        #There can only be one symbol
        #Every multiple item must be in parens
        #if apostrophes are used, a symbol or list comes immediately after
        if re.search("[()]", l):
            completed = False
            for i in l:
                if i == "(":
                    if completed:
                        return (False, "Cannot have two lists in one line: " + str(counter))
                    sum += 1
                elif i == ")":
                    sum -= 1
                    if sum == 0:
                        completed = True
                    elif sum<0:
                        return (False, "')' seen before opening bracket '(': " + str(counter))
                elif (not (i==" " or i=="'")) and sum == 0:
                    return (False, "Invalid entry outside of parentheses in line: " + str(counter))
            if sum>0:
                return (False, "Mismatched bracket in line: " + str(counter))    
        else:
            if " " in l:
                return (False, "You must have lists in parentheses, in line: " + str(counter))
        
        if re.search("'", l):
            if not len(re.findall("(\(|^| )'[^\s\)]", l)) == len(re.findall("'", l)):
                return (False, "There must be a symbol or list after apostrophe: " + str(counter))
        return (True, "")
    
    #Interpreting functions: single line, file
    def eval_line(self, l):
        verify = self.verify_line_syntax(l, 0)
        if not verify[0]:
            print verify[1]
            return None
        
        line_parsed = self.parse_line(l)
        result = None
        if len(line_parsed)>0:
            result = self.eval(line_parsed[0], 0)
        return result

    def interpret(self, f):
        #read line by line, keeping track of line number
        #we assume file syntax is verified
        line_count = 0
        for line in f:
            line_count += 1
            line_parsed = self.parse_line(line)
            if verbose: print str(line_count)+":", line_parsed
            result = self.eval(line_parsed, line_count)
            if result==None:
                break
            elif result=="":
                continue
            else:
                yield result
    
    #Processing functions: The two most important functions: parsing and evaluating
    def parse_line(self, line):
        #Find the elements in the str
        elements = [[]]
        
        if "#" in line: #handle comments
            line = line[:line.index("#")]
        text = line.strip()
        
        if text == "": #default
            return []
        
        pieces = re.split("([\s()'])", text)
        for i in xrange(len(pieces)):
            if pieces[i] == '' or pieces[i] == " ":
                continue
            elif (pieces[i]=="'"):
                elements.append([])
                elements[-1].append(pieces[i])
            elif pieces[i] == "(":
                elements.append([])
            elif pieces[i] == ")":
                last = elements.pop()
                elements[-1].append(last)
            else:
                elements[-1].append(pieces[i])
                
            if len(elements[-1])>1: #if last element has apostrophe and another element, step up
                if elements[-1][0]=="'":
                    last = elements.pop()
                    elements[-1].append(last)
        return elements[0]

    def eval(self, elements, counter):
        #any evaluations is returned "correctly in string format"
        #any validation error returns None
        #the only time a return happens is if a static symbol is returned (atom or apostrophe-d list)
        #any other evaluations are called recursively back to eval until a static symbol is evaluated
        if elements==[] or elements==None: return None
        
        def correct_return(item):
            #add case for when item is a apostrophed object list
            if isinstance(item, list):
                if item[0]=="'":
                    return "'("+" ".join([correct_return(i) for i in item[1]]) + ")"
                else:
                    return "("+" ".join([correct_return(i) for i in item]) + ")"
            else:
                return str(item)
        
        #evaluating all static non-list items
        if not isinstance(elements, list):
            if not isinstance(elements, str): #RETURN ENDS THE RECURSION
                return str(elements)
            if self.is_static_symbol(elements): #RETURN ENDS THE RECURSION
                return elements
            elif elements in self.variables:
                return self.eval(self.variables[elements], counter)
            else:
                print "Unknown value in line", str(counter)+":" , elements
                return None
        else:
            #returns if list is static symbol
            if self.is_static_symbol(elements): #RETURN ENDS THE RECURSION
                return correct_return(elements)
            
            #evaluate all list elements
            for i in xrange(len(elements)):
                elements[i] = self.eval(elements[i], counter)
                
            #evaluate lists as functions now
            if elements[0] not in self.functions:
                if len(elements)==1:
                    return self.eval(elements[0], counter)
                else:
                    print "Undefined function in line", str(counter) + ":", elements[0]
                    return None
            else:
                params = elements[1:]
                if self.validations[elements[0]] (params):
                    return self.eval(self.functions[elements[0]] (params), counter)
                else:
                    print "Validation failed in line", str(counter) + ":", elements[0]
                    return None