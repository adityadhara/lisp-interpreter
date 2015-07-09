import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parses and evaluates lisp files.")
    parser.add_argument('files', metavar='File', type=str, nargs='+', help='files to parse serially')
    parser.add_argument('-w', '--write', metavar='out-file', type=str, help='Output to this file')

    args = parser.parse_args()

    import os
    import sys
    from parser import read_file, printout
    from engine import Environment, ASTBase

    for f in args.files:
        if not os.path.isfile(f):
            raise Exception("Unable to read file %r" % f)

        is_file = False
        if args.write is None:
            out_stream = sys.stdout
        else:
            is_file = True
            out_stream = file(args.write, 'w')

        env = Environment()
        for statement in read_file(f):
            st = ASTBase(statement[0])
            ret = st.evaluate(env)
            printout(ret, out_stream)

        if is_file:
            out_stream.close()
