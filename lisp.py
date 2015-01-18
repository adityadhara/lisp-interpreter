import sys
import os.path
import unittest

import lisp_interpret
import lisp_functions
import lisp_verifications
import lisp_tests 

if __name__ == "__main__":
    verbose = False
    #if len(sys.argv)==2:
    if len(sys.argv)==1:
        print '''Python Lisp Interpreter: usage python lisp.py [params]
    Params:
        file
        '-t' to run tests
        '-v' to run it verbose'''
    else:
        #File = True
        File = None
        Is_Verbose = None
        Is_Testing = None
        for item in sys.argv[1:]:
            if (not File) and os.path.isfile(item):
                File = item
            elif (not Is_Verbose) and item=="-v":
                Is_Verbose = True
            elif (not Is_Testing) and item=="-t":
                Is_Testing = True
            else:
                print "Unrecognized flag", item ,"is ignored"
        
        if Is_Verbose:
            verbose = True
        if File:
            interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS, verbose)
            if verbose: print "Valid file:", sys.argv[1]
            #with open("sample.lisp", 'r') as thefile:
            with open(sys.argv[1], 'r') as thefile:
                for result in interpreter.interpret(thefile):
                    print result
        if Is_Testing:
            suite = lisp_tests.test_suite()
            runner = unittest.TextTestRunner()
            runner.run(suite)