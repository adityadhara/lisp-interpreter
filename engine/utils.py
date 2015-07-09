
def is_atomic(item):
    """
    Returns whether a given item is atomic by definition in lisp: item is not a list, and
    if it is a list, it's a list with item[0] = "'".

    >>> print is_atomic("hello")
    True
    >>> print is_atomic(['hello'])
    False
    >>> print is_atomic(['hello', '+'])
    False
    >>> print is_atomic(["'", 'hello', "bye"])
    True
    >>> print is_atomic([["'", 'hello', "bye"]])
    False
    >>> print is_atomic('+')
    True

    :param item: any item
    :return: True if item is atomic, else False
    """

    if type(item) is list:
        if len(item) == 0:
            return False
        if item[0] is not "'":
            return False
    return True

def is_symbol(item):
    """
    Returns whether a given item is a symbol by definition in lisp: item is atomic and not a number
    or forced to be a symbol using "'"

    >>> print is_symbol('a')
    True
    >>> print is_symbol(['1', '2']) # Not atomic
    False
    >>> print is_symbol(["'", ['hello', 'bye']]) # forced to symbol
    True
    >>> print is_symbol('1') # symbol can't be a number
    False
    >>> print is_symbol(["'", '1'])
    True

    :param item: any item
    :return: True if symbol, else false
    """

    if not is_atomic(item):
        return False

    if type(item) is list:  # The only time a list passes the is_atomic test is if item[0] is "'".
        return True

    try:
        float(item)
    except ValueError:
        return True

    return False

class Environment:
    """
    The Environment class is an implementation of managing variables and scopes. The Environment
    class has an env dict that acts as the Heap - a store of all the created variables. Each
    instance of Environment has access to the env, and a locals list to keep track of it's
    defined variables.

    >>> env = Environment()
    >>> env['x'] = 'blah'
    >>> print env['x']
    blah
    >>> env2 = Environment()
    >>> env2['y'] = 'blah2'
    >>> print env2['x']
    blah
    >>> del env
    >>> print env2['x']
    Traceback (most recent call last):
        ...
    KeyError: 'x'
    >>> print env2['y']
    blah2
    >>> def test_scopes():
    ...     env3 = Environment()
    ...     env3['z'] = 'blah3'
    ...     print env3['y']
    ...     print env3['z']
    >>> test_scopes()
    blah2
    blah3
    >>> print env2['y']
    blah2
    >>> print env2['z']
    Traceback (most recent call last):
        ...
    KeyError: 'z'

    """
    env = {}

    def __init__(self):
        self.scope = []

    def __setitem__(self, key, value):
        Environment.env[key] = value
        self.scope.append(key)

    def __getitem__(self, item):
        return Environment.env[item]

    def __delitem__(self, item):
        del Environment.env[item]
        self.scope.remove(item)

    def __contains__(self, item):
        if (not isinstance(item, list)) and is_symbol(item):
            return Environment.env.__contains__(item)

    def __del__(self):
        self.gc()

    def gc(self):
        """
        This makeshift garbage collecter deletes all items in the scope. Called on dereference.
        """
        for item in self.scope:
            del self.env[item]
        self.scope = []
