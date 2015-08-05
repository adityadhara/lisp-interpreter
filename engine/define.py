

def define_fn(obj, env):
    """
    Returns string value of sum of self.args. If item in self.args is a symbol, it is assumed
    it does not exist in env and an Exception is raised.

    >>> dummyCls = type('temp', (object,), {'args': ['a', '-2'], 'evaluate_all_args': lambda x: True})
    >>> dummy = dummyCls()
    >>> env = {}
    >>> action = define_fn(dummy, env)
    >>> print env['a']
    -2
    >>> print action
    None
    >>> dummy.args = ['b', ['1', '2']]
    >>> action = define_fn(dummy, env)
    >>> print env['b']
    ['1', '2']
    >>> dummy.args = ['c', 'd', 'e']
    >>> action = define_fn(dummy, env)
    Traceback (most recent call last):
        ...
    Exception: Invalid number of arguments for 'define' - c
    >>> dummy.args = ['a']
    >>> action = define_fn(dummy, env)
    Traceback (most recent call last):
        ...
    Exception: Invalid number of arguments for 'define' - a

    :param obj:
    :param env:
    :return:
    """
    obj.evaluate_all_args()

    if (len(obj.args) != 2):
        raise Exception("Invalid number of arguments for 'define' - %s" % str(obj.args[0]))

    env[obj.args[0]] = obj.args[1]
    return None