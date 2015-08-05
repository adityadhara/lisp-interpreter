from utils import is_atomic

def cons_fn(obj, env):
    """
    Concatenates args. If length of obj.args is greater than 2, a generic exception is thrown.
    1 - a new return-list is created
    2 - for both items, if item is atomic, it is added to list
    3 - for both items, if item is a list, the return list is extended with item.
    Doesn't evaluate all args.

    >>> dummyCls = type('dummy', (object,), {'args': [], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> from utils import Environment
    >>> env = Environment()
    >>> dummy.args = ['a', 'b']
    >>> print cons_fn(dummy, env)
    ['a', 'b']
    >>> dummy.args = ['a', ['b', 'c']]
    >>> print cons_fn(dummy, env)
    ['a', 'b', 'c']
    >>> dummy.args = [['a', 'b'], ['c', 'd']]
    >>> print cons_fn(dummy, env)
    ['a', 'b', 'c', 'd']
    >>> dummy.args = [['a', 'b'], ["'", ['a', 'b']]]
    >>> print cons_fn(dummy, env)
    ['a', 'b', ["'", ['a', 'b']]]
    >>> dummy.args = ['a', 'b', 'c']
    >>> print cons_fn(dummy, env)
    Traceback (most recent call last):
        ...
    Exception: you can't cons anything other than exactly two items

    :param obj:
    :param env:
    :return:
    """

    ret_list = []
    if len(obj.args) != 2:
        raise Exception("you can't cons anything other than exactly two items")
    for item in obj.args:
        if is_atomic(item):
            ret_list.append(item)
        else:
            ret_list.extend(item)
    return ret_list

def car_fn(obj, env):
    """
    Returns first item in list

    >>> dummyCls = type('dummy', (object,), {'args': [], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> from utils import Environment
    >>> env = Environment()

    :param obj:
    :param env:
    :return:
    """

