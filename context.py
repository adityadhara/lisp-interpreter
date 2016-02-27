
class VarObject:
    """
    A utility container for variables in the context. This allows non-deep
    copying of variables (e.g. strings are passed by reference in contexts)
    
    @param value    object  python object stored
    @param context  Context object that possesses this variable
    @param var_type string  indicating what type this variable is 
                            #TODO: implement this)
    @param is_param bool    indicating whether this variable is a param
    
    @return VarObject
    """
    def __init__(self, value, context, var_type, is_param):
        self.value = value
        self.context = context
        self.var_type = var_type
        self.is_param = is_param


class Context:
    """
    ## Design
    
    This class is used for managing contexts in programming or templating 
    langauge implementations. The idea is to accomplish:
    1 - O(1) lookup of variables
    2 - Maintain shadowing - if a new context creates a variable of the same 
        name, it should be used instead
    3 - Keep track of context locals in each context object
    4 - Garbage collection - a variable is deleted if no reference to it
        exists
    

    for code that looks like:
        x=1
        func_a() {
            x = 2
            func_b() {
                y = 3
                print x + y
            }
        }
    
    The contexts created should behave like a stack of the form:
        global<-func_a<-func_b<-func_c
    Where global contains x, func_a shadows x and func_b contains y
    
    This situation illustrates the first two goals above:
    1 - When variable lookups happens at the return statement x+y, the Context
        instance in func_c must have constant time in providing the value of x 
        and y from their respective contexts, in this case x=2 from func_a's 
        context and y=3 from func_b's context
    
    The third goal is a little abstract. Apart from the actual implementation of
    #1 and #2, keeping context locals can be helpful in debugging for both the 
    end user of the language and the correctness of my implementation

    The fourth goal is for cases like below:
        x=1
        func_a(x) {
            return func_b(y) {
                print x + y
            }
        }

        func_c() {
            2adder = func_a(2)
            2adder(3)   #=> should print 5
        }
    
    So while func_b is being defined, it would be as expected:
        global<-func_a<-func_b
    But when the 2adder variable is created, the contexts would have to look 
    something like this:
    global<-func_a<-func_b
        ^
        +---func_c
    Where the link and shadowing from global to func_b is maintained even though
    b is no longer defined, because it is a returnable object


    NOTE: For a lot of the following, I can (and I'm going to) use python's gc to
    manage references and memory allocation

    """

    def __init__(self, name, parent_context=None, context_defaults={}):
        """
        Create an instance with defaults
        
        Create with or without defaults
        >>> parent_cxt = Context('test', None, {'var': 'value'})
        >>> parent_cxt.variables['var'].value
        'value'
        >>> child_cxt = Context('child', parent_cxt)
        >>> child_cxt.name
        'test<-child'

        Implementation of above four conditions
        >>> parent_cxt = Context('parent')
        >>> parent_cxt.set_var('eggs', 'green')
        >>> parent_cxt.set_var('protein', 'ham')
        >>> child_cxt = Context('child', parent_cxt)
        >>> child_cxt.set_var('num_hats', 2)
        >>> child_cxt.set_var('protein', 'bacon')
        >>> child_cxt.get_var('num_hats')   # local variable
        2
        >>> child_cxt.get_var('eggs')       # parent context
        'green'
        >>> child_cxt.get_var('protein')    # shadow variable
        'bacon'
        >>> parent_cxt.get_var('protein')   # local to parent_cxt
        'ham'
        >>> del parent_cxt
        >>> child_cxt.get_var('protein')    # aint no shadow when you shine
        'bacon'
        >>> child_cxt.get_var('eggs')       # still can access parent objects
        'green'

        @param name             string  name for context
        @param context_defaults dict    containing default values
        @param parent_context   Context the parent containing this 
        
        @return Context instance
        """

        # import references to variables from parent class
        self.variables = {}
        self.local_vars = set()
        if parent_context:
            self.name = parent_context.name + '<-' + name
            for key in parent_context.variables:
                self.set_var(key, parent_context.get_var_obj(key))
        else:
            self.name = name
        
        # add defaults into variables
        for key in context_defaults:
            self.set_var(key, context_defaults[key])


    def set_var(self, name, value, is_param=False):
        """
        This takes care of setting variable. This makes sure a variable is 
        wrapped in a VarObject class

        @param name  string name of variable to set
        @param value object Any python object to store for name
        @param is_param bool Indicate whether this variable is a param

        @return None
        """
        if isinstance(value, VarObject):
            self.variables[name] = value
        else:
            self.variables[name] = VarObject(
                    value=value,
                    context=self,
                    var_type=None,
                    is_param=is_param
                    )
            self.local_vars.add(name)


    def get_var_obj(self, name):
        """
        Gets the VarObject under that name

        @param name string name of variable

        @return VarObject
        """
        if name in self.variables:
            return self.variables[name]
        #TODO: Probably should implement an error for name not in vars


    def get_var(self, name):
        """
        Gets variable outside it's VarObject wrapper. Raises error if not found

        @param name string name of variable to get

        @return object
        """
        if name in self.variables:
            return self.variables[name].value
        else:
            raise Exception('Variable \'' + name + '\' not defined')


    def unset_var(self, name):
        """
        Unsets variable of that name if it's context is this

        >>> cxt1 = Context('parent', None, {'var': 'value'})
        >>> cxt2 = Context('child', cxt1, {'var2': 'value2'})
        >>> cxt2.unset_var('var')
        >>> print cxt2.get_var('var')
        Traceback (most recent call last):
            ...
        Exception: Variable 'var' not defined
        >>> print cxt1.get_var('var')
        value
        >>> cxt2.unset_var('var2')
        >>> cxt2.get_var('var2')
        Traceback (most recent call last):
            ...
        Exception: Variable 'var2' not defined

        @param name string name of variable to unset

        @return None
        """
        del self.variables[name]    # no need to do more complex logic because 
                                    # python gc
