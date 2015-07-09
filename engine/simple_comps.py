from utils import is_symbol, is_atomic

def equality_fn(obj, env):
    """

    finds equality between two arguments. If length of arguments is larger than 2,
    an exception is thrown. Otherwise, the following logic is followed:

    1 - check if both are lists or both are not lists
    2 - check length of args are same (remember we use strings)
    3 - if not a list, check if both items are same
    4 - if a list, recursively check items in both lists using the above criteria

    >>> dummyCls = type('dummy', (object,), {'args': [], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> from utils import Environment
    >>> env = Environment()
    >>> dummy.args = ['1', '1']
    >>> print equality_fn(dummy, env)
    True
    >>> dummy.args = ['1', 'a']
    >>> print equality_fn(dummy, env)
    False
    >>> dummy.args = ['1', '1.0']
    >>> print equality_fn(dummy, env)
    True
    >>> dummy.args = ['1', ['1', 'a']]
    >>> print equality_fn(dummy, env)
    False
    >>> dummy.args = [['1', 'a'], '1']
    >>> print equality_fn(dummy, env)
    False
    >>> dummy.args = [['1', '2'], ['1', '2', '3']]
    >>> print equality_fn(dummy, env)
    False
    >>> dummy.args = [['1', '2.0', '3'], ['1', '2', '3']]
    >>> print equality_fn(dummy, env)
    True
    >>> dummy.args = [['1', '2', ['3', '4', ['5']]], ['1', '2', ['3', '4', '5']]]
    >>> print equality_fn(dummy, env)
    False
    >>> dummy.args = [['1', '2', ['3', '4', ['5']]], ['1', '2', ['3', '4', ['5']]]]
    >>> print equality_fn(dummy, env)
    True
    >>> type_test = equality_fn(dummy, env)
    >>> print isinstance(type_test, str)
    True

    :param obj:
    :param env:
    :return:
    """
    if len(obj.args) > 2:
        raise Exception("You can only compare two items")

    obj.evaluate_all_args()

    def comparison_helper(items1, items2):
        first_is_list = isinstance(items1, list)
        second_is_list = isinstance(items2, list)

        # check if list
        if first_is_list != second_is_list:
            return False

        if first_is_list:
            # check if same size
            if len(items1) != len(items2):
                return False
            for x in xrange(len(items1)):
                if not comparison_helper(items1[x], items2[x]):
                    return False
            return True
        else:
            try:
                first_num = float(items1)
                try:
                    return first_num == float(items2)
                except:
                    return False
            except:
                return items1 == items2

    return str(comparison_helper(obj.args[0], obj.args[1]))

def quote_fn(obj, env):
    """

    Sets everything provided as a quoted symbol. The arguments are not evaluated. If args
    are already quoted symbols, they are simply returned

    >>> dummyCls = type('dummy', (object,), {'args': [], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> from utils import Environment
    >>> env = Environment()
    >>> dummy.args = ['a', 'b']
    >>> print quote_fn(dummy, env)
    ["'", ['a', 'b']]
    >>> dummy.args = 'a'
    >>> print quote_fn(dummy, env)
    ["'", 'a']
    >>> dummy.args = ["'", ['a', 'b']]
    >>> print quote_fn(dummy, env)
    ["'", ['a', 'b']]
    >>> dummy.args = ["'", 'a']
    >>> print quote_fn(dummy, env)
    ["'", 'a']

    :param obj:
    :param env:
    :return:
    """

    if isinstance(obj.args, list) and obj.args[0] is "'":
        return obj.args
    else:
        return ["'", obj.args]