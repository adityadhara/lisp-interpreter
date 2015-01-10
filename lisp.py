import sys
import os.path
import lisp_verify
import lisp_interpret

if __name__ == "__main__":
    if len(sys.argv)==1:
        print "Please enter a file to interpret"
        sys.exit()
    else:
        if os.path.isfile(sys.argv[1]):
            print "Valid file"
            with open(sys.argv[1], 'r') as thefile:
                lisp_verify.verify(thefile)
                lisp_interpret.interpret(thefile)
        else:
            print"File doesn't exist or Invalid file path"
