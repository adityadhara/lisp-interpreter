from utils import is_symbol

def add_fn(obj, env):
    """
    Returns string value of sum of self.args. If item in self.args is a symbol, it is assumed
    it does not exist in env and an Exception is raised.

    >>> dummyCls = type('temp', (object,), {'args': ['1', '-2', '3.4'], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> sm = add_fn(dummy, {})
    >>> print sm
    2.4
    >>> print type(sm) is str
    True
    >>> dummy.args = ['1', 'a', '1.2']
    >>> sm = add_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - a
    >>> dummy.args = ['1', ["'", '1'], '1.5']
    >>> sm = add_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - ["'", '1']

    :param env: environment to evaluate in
    :return:
    """
    obj.evaluate_all_args()

    ret = 0
    for item in obj.args:
        if is_symbol(item):
            raise Exception("You can't add a non-defined symbol - %s" % item)
        ret += float(item)
    return str(ret)

def subtract_fn(obj, env):
    """
    Returns string value of difference of self.args. If item in self.args is a symbol, it is assumed
    it does not exist in env and an Exception is raised.

    >>> dummyCls = type('temp', (object,), {'args': ['9.4', '-2', '5'], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> sbt = subtract_fn(dummy, {})
    >>> print sbt
    6.4
    >>> print type(sbt) is str
    True
    >>> dummy.args = ['1', 'a', '1.2']
    >>> sbt = subtract_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - a
    >>> dummy.args = ['1', ["'", '1'], '1.5']
    >>> sbt = subtract_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - ["'", '1']

    :param env: environment to evaluate in
    :return: a string representation the sum of items in self.args
    """
    obj.evaluate_all_args()

    ret = 0
    first = True
    for item in obj.args:
        if is_symbol(item):
            raise Exception("You can't add a non-defined symbol - %s" % item)
        if first:
            ret += float(item)
            first = False
        else:
            ret -= float(item)
    return str(ret)

def multiply_fn(obj, env):
    """
    Returns string value of product of self.args. It is assumed that item in self.args is a symbol,
    it is assumed it does not exist in env and an Exception is raised.

    >>> dummyCls = type('temp', (object,), {'args': ['9.4', '-2', '5'], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> pr = multiply_fn(dummy, {})
    >>> print pr
    -94.0
    >>> print type(pr) is str
    True
    >>> dummy.args = ['1', 'a', '1.2']
    >>> pr = multiply_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - a
    >>> dummy.args = ['1', ["'", '1'], '1.5']
    >>> pr = multiply_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - ["'", '1']

    :param env: environment to evaluate in
    :return: a string representation the sum of items in self.args
    """
    obj.evaluate_all_args()

    ret = 1
    for item in obj.args:
        if is_symbol(item):
            raise Exception("You can't add a non-defined symbol - %s" % item)
        ret *= float(item)
    return str(ret)

def divide_fn(obj, env):
    """
    Returns string value of product of self.args. It is assumed that item in self.args is a symbol,
    it is assumed it does not exist in env and an Exception is raised.

    >>> dummyCls = type('temp', (object,), {'args': ['9.4', '-2', '5'], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> qu = divide_fn(dummy, {})
    >>> print qu
    -0.94
    >>> print type(qu) is str
    True
    >>> dummy.args = ['1', 'a', '1.2']
    >>> qu = divide_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - a
    >>> dummy.args = ['1', ["'", '1'], '1.5']
    >>> qu = divide_fn(dummy, {})
    Traceback (most recent call last):
        ...
    Exception: You can't add a non-defined symbol - ["'", '1']

    :param env: environment to evaluate in
    :return: a string representation the sum of items in self.args
    """
    obj.evaluate_all_args()

    ret = 1
    first = True
    for item in obj.args:
        if is_symbol(item):
            raise Exception("You can't add a non-defined symbol - %s" % item)
        if first:
            ret *= float(item)
            first = False
        else:
            ret /= float(item)
    return str(ret)
