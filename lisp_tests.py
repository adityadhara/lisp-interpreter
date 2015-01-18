import unittest
import lisp_interpret
import lisp_verifications
import lisp_functions

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParseTest))
    suite.addTest(unittest.makeSuite(FunctionsVerificationsTest))
    suite.addTest(unittest.makeSuite(IsStaticTest))
    suite.addTest(unittest.makeSuite(VerifyLineTest))
    suite.addTest(unittest.makeSuite(EvalTest))
    return suite

class ParseTest(unittest.TestCase):
    
    def setUp(self):
        self.interpreter = lisp_interpret.Interpreter({}, {})
    
    def test_parse_line(self):
        #default answer: []
        result = self.interpreter.parse_line("")
        self.assertEquals([], result)
        
        #base case: symbol
        result = self.interpreter.parse_line('a')
        self.assertEquals(['a'], result)
        
        #some symbols in brackets
        result = self.interpreter.parse_line('(1 1 1)')
        self.assertEquals([['1', '1', '1']], result)
        
        #some nesting
        result = self.interpreter.parse_line('(+ 1 (- 1 2))')
        self.assertEquals([['+', '1', ['-', '1', '2']]], result)
        
        #comments
        result = self.interpreter.parse_line('(1 1 1) #hello there \'(1 2)')
        self.assertEquals([['1', '1', '1']], result)
        result = self.interpreter.parse_line('#this should result empty')
        self.assertEquals([], result)
        
        #using apostrophes
        result = self.interpreter.parse_line("'a")
        self.assertEquals([["'", "a"]], result)
        result = self.interpreter.parse_line("'whole")
        self.assertEquals([["'", "whole"]], result)
        result = self.interpreter.parse_line("'(1 1)")
        self.assertEquals([["'", ["1", "1"]]], result)
        result = self.interpreter.parse_line("(def a 'something)")
        self.assertEquals([['def', 'a', ["'", 'something']]], result)
        result = self.interpreter.parse_line("(def a '(1 2))")
        self.assertEquals([['def', 'a', ["'", ['1', '2']]]], result)
    
    def tearDown(self):
        del self.interpreter

class FunctionsVerificationsTest(unittest.TestCase):
    
    def setUp(self):
        self.func = lisp_functions.FUNCTIONS
        self.veri = lisp_verifications.VERIFICATIONS
        
    def test_basic_functions(self):
        #'+', "-", "*"
        items = ["+", "-", "*"]
        solutions = [3, -1, 2]
        for i in xrange(len(items)):
            self.assertTrue(self.veri[items[i]](['1', '-1']))
            self.assertTrue(self.veri[items[i]](['1', '1.0']))
            self.assertTrue(self.veri[items[i]](['1.00', '-1.0']))
            self.assertFalse(self.veri[items[i]](['1']))
            self.assertFalse(self.veri[items[i]](['1', '1', '1']))
            self.assertFalse(self.veri[items[i]](['-1.0', '7a']))
            
            result = self.func[items[i]](['1', '2'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, int)
            result = self.func[items[i]](['1', '2.0'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, float)
            result = self.func[items[i]](['1.0', '2.0'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, float)
        
        #"/" = different because result is always float
        self.assertTrue(self.veri['/'](['1', '-1']))
        self.assertTrue(self.veri['/'](['1', '1.0']))
        self.assertTrue(self.veri['/'](['1.00', '-1.0']))
        self.assertFalse(self.veri['/'](['1']))
        self.assertFalse(self.veri['/'](['1', '1', '1']))
        self.assertFalse(self.veri['/'](['-1.0', '7a']))
            
        result = self.func['/'](['1', '2'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
        result = self.func['/'](['1', '2.0'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
        result = self.func['/'](['1.0', '2.0'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
    
    def test_eq_functions(self):
        #"eq?" - OMG thats a lot
        self.assertTrue(self.veri['eq?'](['1', 'a']))
        self.assertTrue(self.veri['eq?'](['1', '1.0']))
        self.assertTrue(self.veri['eq?'](['1.00', ['a']]))
        self.assertFalse(self.veri['eq?'](['1']))
        self.assertFalse(self.veri['eq?'](['1', '1', '1']))
        
        result = self.func['eq?'](['1', '1'])
        self.assertEquals(result, "True")
        result = self.func['eq?'](['1', '1.0'])
        self.assertEquals(result, "True")
        result = self.func['eq?'](['1.0', '2.0'])
        self.assertEquals(result, "False")
        result = self.func['eq?'](['1.0', 'a'])
        self.assertEquals(result, "False")
        result = self.func['eq?'](['1.0', ['a', '1']])
        self.assertEquals(result, "False")
        result = self.func["eq?"](['a', 'a'])
        self.assertEquals(result, "True")
        result = self.func["eq?"](['a', ["'", 'a']])
        self.assertEquals(result, "True")
        result = self.func["eq?"](['a', ["'", 'b']])
        self.assertEquals(result, "False")
        result = self.func["eq?"]([["1", "1"], ["1", "1"]])
        self.assertEquals(result, "True")
        result = self.func["eq?"]([["1", "1"], ["1.0", "1.0"]])
        self.assertEquals(result, "True")
        result = self.func["eq?"]([["1", "1"], ["1", "2"]])
        self.assertEquals(result, "False")
        result = self.func["eq?"]([["1", "1"], ["'", ["1", "1"]]])
        self.assertEquals(result, "True")
    
    def test_quote_function(self):
        #quote
        self.assertTrue(self.veri['quote'](['1']))
        self.assertTrue(self.veri['quote'](['a']))
        self.assertTrue(self.veri['quote']([['-1.00', 'a']]))
        self.assertFalse(self.veri['quote'](['1', '1']))
        self.assertFalse(self.veri['quote'](['1', '1', '1']))
        self.assertFalse(self.veri['quote']([['-1.0'], ['7a']]))
            
        result = self.func['quote'](['1'])
        self.assertEquals(result, ["'", '1'])
        self.assertIsInstance(result, list)
        result = self.func['quote']([['1', '2.0']])
        self.assertEquals(result, ["'", ['1', '2.0']])
        result = self.func['quote']([["'", 'a']])
        self.assertEquals(result, ["'", 'a'])
        result = self.func['quote']([["'", ['1', '2.0']]])
        self.assertEquals(result, ["'", ['1', '2.0']])
        
    def tearDown(self):
        del self.func
        del self.veri

class IsStaticTest(unittest.TestCase):
    
    def setUp(self):
        self.interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
    
    def test_is_static_symbol(self):
        #numbers are
        parsed_text = self.interpreter.parse_line('1')
        self.assertFalse(self.interpreter.is_static_symbol(parsed_text))
        self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0]))
        
        #any defined function is
        for key in lisp_functions.FUNCTIONS:
            parsed_text = self.interpreter.parse_line(key)
            self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0]))
        
        #any apostrophe-d item is
        parsed_text = self.interpreter.parse_line("'a")
        self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0]))
        parsed_text = self.interpreter.parse_line("'(1 2)")
        self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0]))
        
        #others arent
        parsed_text = self.interpreter.parse_line('(1 2)')
        self.assertFalse(self.interpreter.is_static_symbol(parsed_text[0]))
        self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0][0]))
        self.assertTrue(self.interpreter.is_static_symbol(parsed_text[0][1]))
    
    def tearDown(self):
        del self.interpreter

class VerifyLineTest(unittest.TestCase):
    def setUp(self):
        self.interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
    def test_verify_defaults(self):
        #defaults
        result = self.interpreter.verify_line_syntax("", 0) #default syntax ok
        self.assertIsInstance(result, tuple)
        self.assertTrue(result[0])
        self.assertEquals(result[1], "")
    
    def test_verify_parens(self):
        #parens
        result = self.interpreter.verify_line_syntax(")", 0) #any extra parens
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = self.interpreter.verify_line_syntax("(", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        result = self.interpreter.verify_line_syntax(")(", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = self.interpreter.verify_line_syntax("(1 0))", 0) #finds issues if brackets are miscounted
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = self.interpreter.verify_line_syntax("(1 (0) (0 1)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        result = self.interpreter.verify_line_syntax("(1 1) (1 0)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Cannot have two lists in one line: 0")
    
    def test_verify_trailing_spaces(self):
        #trailing spaces (should be trimmed
        result = self.interpreter.verify_line_syntax(" 1  ", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax(" '(1 1)  ", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("   ) ", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
    
    def test_verify_outside_parens(self):
        #value outside parens
        result = self.interpreter.verify_line_syntax("(+ 1 1) 1", 0) # no character should be out of brackets
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Invalid entry outside of parentheses in line: 0")
        result = self.interpreter.verify_line_syntax("1 (+ 1 1)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Invalid entry outside of parentheses in line: 0")
        result = self.interpreter.verify_line_syntax("'(1 1)", 0) #only value in front of parens is "'"
        self.assertTrue(result[0])
    
        #lists outside parens
        result = self.interpreter.verify_line_syntax("+ 1 1", 0) # all lists should be in brackets
        self.assertFalse(result[0])
        self.assertEquals(result[1], "You must have lists in parentheses, in line: 0")
    
    def test_verify_apostrophe(self):
        #apostrophes formats
        result = self.interpreter.verify_line_syntax("(1 'a)", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("'(1 1)", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("(0 '(1 1))", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("('0 1)", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("'0", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("(0 ')", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = self.interpreter.verify_line_syntax("'", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = self.interpreter.verify_line_syntax("'(0 ' 0)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = self.interpreter.verify_line_syntax("''", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
    
    def test_verify_comments(self):
        #comments
        result = self.interpreter.verify_line_syntax("#( 1 1#blah", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("'(1 1) #blah", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("(1 1) #blah 'should be ok", 0)
        self.assertTrue(result[0])
        result = self.interpreter.verify_line_syntax("(1 1 #) not ok", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        
    def tearDown(self):
        del self.interpreter

class EvalTest(unittest.TestCase):
    def setUp(self):
        self.interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
    def test_eval(self):
        #default answer: None
        result = self.interpreter.eval_line("", 0)
        self.assertEquals(None, result)
        
        #base case: symbol
        result = self.interpreter.eval_line('1', 1)
        self.assertEquals('1', result)
        result = self.interpreter.eval_line("'(1 1)", 2)
        self.assertEquals("'(1 1)", result)
        
        #some processing in brackets
        result = self.interpreter.eval_line('(+ 1 1)', 3)
        self.assertEquals('2', result)
        
        #some nesting
        result = self.interpreter.eval_line('(+ 1 (- 1 2))', 4)
        self.assertEquals('0', result)
        
        #comments
        result = self.interpreter.eval_line('(+ 1 1) #hello there \'(1 2)', 5)
        self.assertEquals('2', result)
        result = self.interpreter.eval_line('#this should result empty', 6)
        self.assertEquals(None, result)
        
        #variables
        result = self.interpreter.eval_line('a', 7) #uninitiated variable
        self.assertEquals(None, result)
        self.interpreter.variables['a'] = '1' #initiate variables illegally
        result = self.interpreter.eval_line('a', 8)
        self.assertEquals('1', result)
        result = self.interpreter.eval_line('(+ a 1) #a', 9)
        self.assertEquals('2', result)
        
        #variables through "eq"
        
    def tearDown(self):
        del self.interpreter