import sys
import os.path
import unittest

import lisp_interpret
import lisp_functions
import lisp_verifications

from lisp_tests import *

if __name__ == "__main__":
    verbose = False
    if len(sys.argv)==1:
        print "Python Lisp Interpreter: usage 'python lisp.py [filename]'"
        
        interpreter = lisp_interpret.Interpreter({}, {})
        result = interpreter.parse_line("(+ 1 '(- 1 2))")
        print result
        
        unittest.main()
    else:
        if os.path.isfile(sys.argv[1]):
            if len(sys.argv)>2:
                for argflag in sys.argv[2:]:
                    if (argflag == "-v"):
                        verbose = True
                    else:
                        print "Unrecognized flag", argflag ,"is ignored"
            
            interpreter = lisp_interpret.Interpreter({}, {}, verbose)
            if verbose: print "Valid file:", sys.argv[1]
            with open(sys.argv[1], 'r') as thefile:
                ver = interpreter.verify_syntax(thefile)
                if not ver[0]:
                    print "Error:", ver[1]
                else:
                    if verbose: "File has no syntax errors"
                    interpreter.interpret(thefile)
        else:
            print"File doesn't exist or Invalid file path"