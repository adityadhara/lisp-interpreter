"""
The main executable code:

1) parses args for files
2) determines output - sets to stdout, or "--write" arg if given
3) runs the parser on each file and runs each line using a global environment

if the file paths provided entered doesnt exist, a generic exception is thrown
"""

if __name__ == '__main__':

    # parse args
    import argparse
    parser = argparse.ArgumentParser(description="Parses and evaluates lisp files.")
    parser.add_argument('files', metavar='File', type=str, nargs='+', help='files to parse serially')
    parser.add_argument('-w', '--write', metavar='out-file', type=str, help='Output to this file')

    args = parser.parse_args()

    # determine output - set to stdout, or "--write" arg if given
    import sys
    is_file = False
    if args.write is None:
        out_stream = sys.stdout
    else:
        is_file = True
        out_stream = file(args.write, 'w')

    # run the parser on each file, and run each line using a global environment
    import os
    from engine import read_file, printout, Environment, ASTBase

    for f in args.files:
        if not os.path.isfile(f):
            raise Exception("Unable to read file %r" % f)

        # env acts as the "global" environment for the lisp file
        env = Environment()
        for statement in read_file(f):
            st = ASTBase(statement[0])
            ret = st.evaluate(env)
            printout(ret, out_stream)

        if is_file:
            out_stream.close()
