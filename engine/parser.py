import re


def count_brackets(line):
    """
    Returns the surplus of left-parentheses to right-parantheses of a given string.

    >>> print count_brackets("")
    0
    >>> print count_brackets("blah words[]")
    0
    >>> print count_brackets("(some more words) and more")
    0
    >>> print count_brackets("(again and again - returns 1")
    1
    >>> print count_brackets("and again) - returns -1")
    -1

    :param line: string
    :return: (count of left-parens in line) - (count of right-parens in line)
    """

    left_bracks = line.count('(')
    right_bracks = line.count(')')
    return left_bracks-right_bracks


def read_file(file_path):
    """
    Reads the file f for statements. Statements are defined as nested lists of strings in the same manner
    of lisp instructions. Reading is done line by line and if count_brackets(line) < 0, the next line is
    appended with a space in the middle, until the line has count_brackets(line) == 0. All blank
    lines are skipped. If a line has more closing brackets than opening ones, an error is thrown. showing the count of
    the line in question.

    >>> f = file('test.lisp', 'w')
    >>> f.write('(blah (something)) # comment\\n')
    >>> f.write('((blah something else\\n')
    >>> f.write('     continued line) # comment\\n')
    >>> f.write('\t more continuation)\\n')
    >>> f.write('\\n')
    >>> f.write('1\\n')
    >>> f.write('  (a  b   c)  \\n')
    >>> f.write("(a b '(c d))\\n")
    >>> f.write("'a\\n")
    >>> f.write("'(a b)\\n")
    >>> f.write("('(a b) c)\\n")
    >>> f.write("'(a b)")
    >>> f.close()
    >>> for item in read_file('test.lisp'):
    ...     print item
    [['blah', ['something']]]
    [[['blah', 'something', 'else', 'continued', 'line'], 'more', 'continuation']]
    ['1']
    [['a', 'b', 'c']]
    [['a', 'b', ["'", ['c', 'd']]]]
    [["'", 'a']]
    [["'", ['a', 'b']]]
    [[["'", ['a', 'b']], 'c']]
    [["'", ['a', 'b']]]
    >>> f = file('test.lisp', 'w')
    >>> f.write('(a b c))\\n')
    >>> f.close()
    >>> for item in read_file('test.lisp'):
    ...     print item
    Traceback (most recent call last):
        ...
    Exception: Mismatched parentheses ending at line 1 of test.lisp - '(a b c))'
    >>> import os # Cleanup test
    >>> os.remove('test.lisp')

    :param f: text file
    :return: string statement
    """

    f = file(file_path)

    cur_line_count = 0
    cur_line = ""
    def mismatch_excp():
        return Exception("Mismatched parentheses ending at line %r of %s - %r" %
                         (cur_line_count, file_path, cur_line))
    statement_stack = [[]]
    n = 0
    for line in f.readlines():
        if '#' in line:
            pre_comment_data = line.split('#')[0]
            cur_line = pre_comment_data.strip()
        else:
            cur_line = line.strip()

        cur_line_count += 1
        if cur_line is "":
            continue

        n += count_brackets(cur_line)
        if n < 0:
            raise mismatch_excp()

        # create parse friendly array
        items = re.split("([()'\s])", cur_line)

        for thing in items:
            if thing.strip() is '':
                continue
            elif thing is "(":
                statement_stack.append([])
            elif thing is "'":
                statement_stack.append([])
                statement_stack[-1].append(thing)
                continue
            elif thing is ")":
                last = statement_stack.pop()
                statement_stack[-1].append(last)
            else:
                statement_stack[-1].append(thing)

            if len(statement_stack[-1]) > 0 and statement_stack[-1][0] is "'":
                last = statement_stack.pop()
                statement_stack[-1].append(last)

        if n > 0:
            continue
        else:
            yield statement_stack.pop()
            statement_stack.append([])
            n = 0

    if n > 0:
        raise mismatch_excp()


def printout(statement, out_stream):
    """
    This function prints nested list statements as human readable text to the out_stream

    >>> import sys
    >>> out = sys.stdout
    >>> printout(None, out)
    >>> printout('a', out)
    a
    >>> printout(['a'], out)
    (a)
    >>> printout(['a', 'b', 'c'], out)
    (a b c)
    >>> printout(['a', 'b', ['c', 'd', 'e'], 'f'], out)
    (a b (c d e) f)
    >>> printout(["'", 'a'], out)
    'a
    >>> printout(["'", ['a', 'b', ['c', 'd', 'e'], 'f']], out)
    '(a b (c d e) f)
    >>> printout(['a', 'b', ["'", ['c', 'd', 'e']], 'f', ['g', 'h']], out)
    (a b '(c d e) f (g h))

    :param statement: list of lists
    :return: Nothing
    """

    if statement is None:
        return

    def recursive_helper(l):
        if type(l) is not list:
            return l

        ret = ""
        if l[0] is "'":
            ret += "'" + recursive_helper(l[1])
        else:
            ret += "("
            first = True
            for item in l:
                if first:
                    first = False
                else:
                    ret += " "
                if type(item) is list:
                    ret += recursive_helper(item)
                else:
                    ret += item
            ret += ")"
        return ret

    if type(statement) is list:
        out_stream.write(recursive_helper(statement))
    else:
        out_stream.write(statement)
    out_stream.write("\n")