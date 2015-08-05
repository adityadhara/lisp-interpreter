from utils import is_atomic, Environment
import types

# ops = ['+', '-', '/', '*', 'eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond']

class ASTBase:
    """
    This is a basic AST that defines and handles all operations defined in operations.py
    and any lambdas that are custom defined by the script.
    It handles evaluating the list of arguments provided, by defining evaluate_arg,
    evaluate_tree and a placeholder evaluate_operation which raises a generic exception.
    This class is extended to create the various AST's in operations.py which all
    override the evaluate_operation function.
    """

    def __init__(self, statement):
        """
        On instantiation, args are stored as self.args and a local environment is created for
        any evaluations of arguments.

        >>> e_atomic = ASTBase('a')
        >>> print e_atomic.statement
        a
        >>> e_atomic = ASTBase(["'", ['a', 'b']])
        >>> print e_atomic.statement
        ["'", ['a', 'b']]
        >>> e_list = ASTBase(['a', 'b', 'c'])
        >>> print e_list.statement
        ['a', 'b', 'c']

        :param statement: lisp parsed statement
        :return: Nothing
        """
        self.statement = statement
        self.tree_type = None
        self.op = None
        self.args = None
        self.result = None
        self.local_env = Environment()

    def find_type(self, env):
        """
        1 - if statement is atomic, it is stored in args and op is 'atom'
        2 - if first element is in the ops or env as a function, it becomes the 'op' property and
            rest of the list is stored in args (as a list).
        3 - else op property is 'list' and args is a list.

        :param env: dictionary of environment variables
        :return: Nothing

        >>> env = Environment()
        >>> e_nil = ASTBase([])
        >>> e_nil.find_type(env)
        >>> print e_nil.tree_type
        nil
        >>> print e_nil.op
        None
        >>> print e_nil.args
        []
        >>> e_var = ASTBase('a')
        >>> env2 = Environment()
        >>> env2['a'] = 'blah'
        >>> e_var.find_type(env2)
        >>> print e_var.tree_type
        var
        >>> print e_var.op
        None
        >>> print e_var.args
        a
        >>> del env2 # This shuold dereference 'a' from environment
        >>> e_atomic = ASTBase('a')
        >>> e_atomic.find_type(env)
        >>> print e_atomic.tree_type
        atom
        >>> print e_atomic.op
        None
        >>> print e_atomic.args
        a
        >>> e_atomic = ASTBase(["'", ['a', 'b']])
        >>> e_atomic.find_type(env)
        >>> print e_atomic.tree_type
        atom
        >>> print e_atomic.op
        None
        >>> print e_atomic.args
        ["'", ['a', 'b']]
        >>> e_op = ASTBase(['+', 'a', 'b'])
        >>> e_op.find_type(env)
        >>> print e_op.tree_type
        op
        >>> print e_op.op
        +
        >>> print e_op.args
        ['a', 'b']
        >>> e_lamb = ASTBase(['+', 'b', ['c', 'd']])
        >>> env['+'] = lambda (x,y): x+y
        >>> e_lamb.find_type(env)
        >>> print e_lamb.tree_type
        lambda
        >>> print e_lamb.op
        +
        >>> print e_lamb.args
        ['b', ['c', 'd']]
        >>> e_list = ASTBase(['a', 'b', ['c', 'd']])
        >>> e_list.find_type(env)
        >>> print e_list.tree_type
        list
        >>> print e_list.op
        None
        >>> print e_list.args
        ['a', 'b', ['c', 'd']]

        """
        if isinstance(self.statement, list) and len(self.statement) == 0:
            self.tree_type = 'nil'
            self.args = self.statement
        elif is_atomic(self.statement):
            if is_symbol(self.statement) and (not isinstance(self.statement, list)) and (self.statement in env):
                self.tree_type = 'var'
                self.args = self.statement
            else:
                self.tree_type = 'atom'
                self.args = self.statement
        elif type(self.statement) is list:
            first_is_list = isinstance(self.statement[0], list)
            is_lambda = self.statement[0] in env and isinstance(env[self.statement[0]], types.LambdaType)
            is_func = self.statement[0] in ops
            if (not first_is_list) and (is_lambda or is_func):
                self.tree_type = 'lambda' if is_lambda else 'op'
                self.op = self.statement[0]
                self.args = self.statement[1:]
            else:
                self.tree_type = 'list'
                self.args = self.statement

    def evaluate_arg(self, index):
        """
        The index-th argument is evaluated. and placed back into self.args

        :param index: position in list of args
        :return: Nothing
        """
        e = ASTBase(self.args[index])
        self.args[index] = e.evaluate(self.local_env)

    def evaluate_all_args(self):
        for i in xrange(self.args.__len__()):
            self.evaluate_arg(i)

    def evaluate(self, env):
        """
        First, find_type is called.
        1 - If self.op is atom and symbol, env is checked and corresponding value is returned
        1 - If self.op is atom and not a symbol in env, args is returned
        2 - If self.op is list, each element of args is evaluated and fed into another list.
            That resulting list is returned.
        3 - If self.op is everything else, the respective operation or lambda is called. The priority
            goes to lambda, of course.
        The computed result is stored in self.result. This result is then completed in

        >>> env = Environment()
        >>> number = ASTBase('3.14159')
        >>> print number.evaluate(env)
        3.14159
        >>> symbol = ASTBase('a')
        >>> print symbol.evaluate(env)
        a
        >>> li = ASTBase(['a', '1', '1.2'])
        >>> print li.evaluate(env)
        ['a', '1', '1.2']
        >>> ops = ASTBase(['+', '1', '1.2'])
        >>> print ops.evaluate(env)
        2.2
        >>> lamb = ASTBase(['sub', '1', '2'])
        >>> env['sub'] = lambda x,y: x.args
        >>> print lamb.evaluate(env)
        ['1', '2']

        :param env: dictionary of variables
        :return: evaluated atom after
        """

        # evaluate function
        if self.result is not None:
            return self.result

        self.find_type(env)

        if self.tree_type is 'nil':
            self.result = self.args
        elif self.tree_type is 'var':
            self.result = env[self.args]
        elif self.tree_type is 'atom' or self.tree_type is 'list':
            self.result = self.args
        elif self.tree_type is 'lambda':
            self.result = env[self.op](self, env)
        elif self.tree_type is 'op':
            self.result = ops[self.op](self, env)

        return self.result

from arithmetics import *
from simple_comps import *
from define import *

ops = {
    '+': add_fn,
    '-': subtract_fn,
    '*': multiply_fn,
    '/': divide_fn,
    'eq?': equality_fn,
    'quote': quote_fn,
    'define': define_fn
}
