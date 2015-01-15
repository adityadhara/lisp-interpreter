import unittest
import lisp_interpret
import lisp_verifications
import lisp_functions

class ParseTest(unittest.TestCase):
    
    def test1_parse_line(self):
        interpreter = lisp_interpret.Interpreter({}, {})
        
        #default answer: []
        result = interpreter.parse_line("")
        self.assertEquals([], result)
        
        #base case: symbol
        result = interpreter.parse_line('a')
        self.assertEquals(['a'], result)
        
        #some symbols in brackets
        result = interpreter.parse_line('(1 1 1)')
        self.assertEquals([['1', '1', '1']], result)
        
        #some nesting
        result = interpreter.parse_line('(+ 1 (- 1 2))')
        self.assertEquals([['+', '1', ['-', '1', '2']]], result)
        
        #comments
        result = interpreter.parse_line('(1 1 1) #hello there \'(1 2)')
        self.assertEquals([['1', '1', '1']], result)
        result = interpreter.parse_line('#this should result empty')
        self.assertEquals([], result)
        
        #using apostrophes
        result = interpreter.parse_line("'a")
        self.assertEquals([["'", "a"]], result)
        result = interpreter.parse_line("'(1 1)")
        self.assertEquals([["'", ["1", "1"]]], result)
        result = interpreter.parse_line("(def a 'something)")
        self.assertEquals([['def', 'a', ["'", 'something']]], result)
        result = interpreter.parse_line("(def a '(1 2))")
        self.assertEquals([['def', 'a', ["'", ['1', '2']]]], result)

    def test2_functions_verifications(self):
        func = lisp_functions.FUNCTIONS
        veri = lisp_verifications.VERIFICATIONS
        
        #'+', "-", "*"
        items = ["+", "-", "*"]
        solutions = [3, -1, 2]
        for i in xrange(len(items)):
            self.assertTrue(veri[items[i]](['1', '-1']))
            self.assertTrue(veri[items[i]](['1', '1.0']))
            self.assertTrue(veri[items[i]](['1.00', '-1.0']))
            self.assertFalse(veri[items[i]](['1']))
            self.assertFalse(veri[items[i]](['1', '1', '1']))
            self.assertFalse(veri[items[i]](['-1.0', '7a']))
            
            result = func[items[i]](['1', '2'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, int)
            result = func[items[i]](['1', '2.0'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, float)
            result = func[items[i]](['1.0', '2.0'])
            self.assertEquals(solutions[i], result)
            self.assertIsInstance(result, float)
        
        #"/" = different because result is always float
        self.assertTrue(veri['/'](['1', '-1']))
        self.assertTrue(veri['/'](['1', '1.0']))
        self.assertTrue(veri['/'](['1.00', '-1.0']))
        self.assertFalse(veri['/'](['1']))
        self.assertFalse(veri['/'](['1', '1', '1']))
        self.assertFalse(veri['/'](['-1.0', '7a']))
            
        result = func['/'](['1', '2'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
        result = func['/'](['1', '2.0'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
        result = func['/'](['1.0', '2.0'])
        self.assertEquals(0.5, result)
        self.assertIsInstance(result, float)
        
        #"eq?" - OMG thats a lot
        self.assertTrue(veri['eq?'](['1', 'a']))
        self.assertTrue(veri['eq?'](['1', '1.0']))
        self.assertTrue(veri['eq?'](['1.00', ['a']]))
        self.assertFalse(veri['eq?'](['1']))
        self.assertFalse(veri['eq?'](['1', '1', '1']))
        
        result = func['eq?'](['1', '1'])
        self.assertEquals(result, "True")
        result = func['eq?'](['1', '1.0'])
        self.assertEquals(result, "True")
        result = func['eq?'](['1.0', '2.0'])
        self.assertEquals(result, "False")
        result = func['eq?'](['1.0', 'a'])
        self.assertEquals(result, "False")
        result = func['eq?'](['1.0', ['a', '1']])
        self.assertEquals(result, "False")
        result = func["eq?"](['a', 'a'])
        self.assertEquals(result, "True")
        result = func["eq?"](['a', ["'", 'a']])
        self.assertEquals(result, "True")
        result = func["eq?"](['a', ["'", 'b']])
        self.assertEquals(result, "False")
        result = func["eq?"]([["1", "1"], ["1", "1"]])
        self.assertEquals(result, "True")
        result = func["eq?"]([["1", "1"], ["1.0", "1.0"]])
        self.assertEquals(result, "True")
        result = func["eq?"]([["1", "1"], ["1", "2"]])
        self.assertEquals(result, "False")
        result = func["eq?"]([["1", "1"], ["'", ["1", "1"]]])
        self.assertEquals(result, "True")
        
        #quote
        self.assertTrue(veri['quote'](['1']))
        self.assertTrue(veri['quote'](['a']))
        self.assertTrue(veri['quote']([['-1.00', 'a']]))
        self.assertFalse(veri['quote'](['1', '1']))
        self.assertFalse(veri['quote'](['1', '1', '1']))
        self.assertFalse(veri['quote']([['-1.0'], ['7a']]))
            
        result = func['quote'](['1'])
        self.assertEquals(result, ["'", '1'])
        self.assertIsInstance(result, list)
        result = func['quote']([['1', '2.0']])
        self.assertEquals(result, ["'", ['1', '2.0']])
        result = func['quote']([["'", 'a']])
        self.assertEquals(result, ["'", 'a'])
        result = func['quote']([["'", ['1', '2.0']]])
        self.assertEquals(result, ["'", ['1', '2.0']])
        
        #quote
        self.assertTrue(veri['quote'](['1']))
        self.assertTrue(veri['quote'](['a']))
        self.assertTrue(veri['quote']([['-1.00', 'a']]))
        self.assertFalse(veri['quote'](['1', '1']))
        self.assertFalse(veri['quote'](['1', '1', '1']))
        self.assertFalse(veri['quote']([['-1.0'], ['7a']]))
            
        result = func['quote'](['1'])
        self.assertEquals(result, ["'", '1'])
        self.assertIsInstance(result, list)
        result = func['quote']([['1', '2.0']])
        self.assertEquals(result, ["'", ['1', '2.0']])
        result = func['quote']([["'", 'a']])
        self.assertEquals(result, ["'", 'a'])
        result = func['quote']([["'", ['1', '2.0']]])
        self.assertEquals(result, ["'", ['1', '2.0']])

    def test3_is_static_symbol(self):
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
        #numbers are
        parsed_text = interpreter.parse_line('1')
        self.assertFalse(interpreter.is_static_symbol(parsed_text))
        self.assertTrue(interpreter.is_static_symbol(parsed_text[0]))
        
        #any defined function is
        for key in lisp_functions.FUNCTIONS:
            parsed_text = interpreter.parse_line(key)
            self.assertTrue(interpreter.is_static_symbol(parsed_text[0]))
        
        #any apostrophe-d item is
        parsed_text = interpreter.parse_line("'a")
        self.assertTrue(interpreter.is_static_symbol(parsed_text[0]))
        parsed_text = interpreter.parse_line("'(1 2)")
        self.assertTrue(interpreter.is_static_symbol(parsed_text[0]))
        
        #others arent
        parsed_text = interpreter.parse_line('(1 2)')
        self.assertFalse(interpreter.is_static_symbol(parsed_text[0]))
        self.assertTrue(interpreter.is_static_symbol(parsed_text[0][0]))
        self.assertTrue(interpreter.is_static_symbol(parsed_text[0][1]))

    def test4_verify_line(self):
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
        #defaults
        result = interpreter.verify_line_syntax("", 0) #default syntax ok
        self.assertIsInstance(result, tuple)
        self.assertTrue(result[0])
        self.assertEquals(result[1], "")
        
        #parens
        result = interpreter.verify_line_syntax(")", 0) #any extra parens
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = interpreter.verify_line_syntax("(", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        result = interpreter.verify_line_syntax(")(", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = interpreter.verify_line_syntax("(1 0))", 0) #finds issues if brackets are miscounted
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        result = interpreter.verify_line_syntax("(1 (0) (0 1)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        result = interpreter.verify_line_syntax("(1 1) (1 0)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Cannot have two lists in one line: 0")
        
        #trailing spaces (should be trimmed
        result = interpreter.verify_line_syntax(" 1  ", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax(" '(1 1)  ", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("   ) ", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "')' seen before opening bracket '(': 0")
        
        #value outside parens
        result = interpreter.verify_line_syntax("(+ 1 1) 1", 0) # no character should be out of brackets
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Invalid entry outside of parentheses in line: 0")
        result = interpreter.verify_line_syntax("1 (+ 1 1)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Invalid entry outside of parentheses in line: 0")
        result = interpreter.verify_line_syntax("'(1 1)", 0) #only value in front of parens is "'"
        self.assertTrue(result[0])
        
        #lists outside parens
        result = interpreter.verify_line_syntax("+ 1 1", 0) # all lists should be in brackets
        self.assertFalse(result[0])
        self.assertEquals(result[1], "You must have lists in parentheses, in line: 0")
        
        #apostrophes formats
        result = interpreter.verify_line_syntax("(1 'a)", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("'(1 1)", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("(0 '(1 1))", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("('0 1)", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("'0", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("(0 ')", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = interpreter.verify_line_syntax("'", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = interpreter.verify_line_syntax("'(0 ' 0)", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        result = interpreter.verify_line_syntax("''", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "There must be a symbol or list after apostrophe: 0")
        
        #comments
        result = interpreter.verify_line_syntax("#( 1 1#blah", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("'(1 1) #blah", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("(1 1) #blah 'should be ok", 0)
        self.assertTrue(result[0])
        result = interpreter.verify_line_syntax("(1 1 #) not ok", 0)
        self.assertFalse(result[0])
        self.assertEquals(result[1], "Mismatched bracket in line: 0")
        
        
    def test5_eval(self):
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
        #default answer: None
        result = interpreter.eval_line("")
        self.assertEquals(None, result)
        
        #base case: symbol
        result = interpreter.eval_line('1')
        self.assertEquals('1', result)
        result = interpreter.eval_line("'(1 1)")
        self.assertEquals("'(1 1)", result)
        
        #some processing in brackets
        result = interpreter.eval_line('(+ 1 1)')
        self.assertEquals('2', result)
        
        #some nesting
        result = interpreter.eval_line('(+ 1 (- 1 2))')
        self.assertEquals('0', result)
        
        #comments
        result = interpreter.eval_line('(+ 1 1) #hello there \'(1 2)')
        self.assertEquals('2', result)
        result = interpreter.eval_line('#this should result empty')
        self.assertEquals(None, result)
        
        #variables
        result = interpreter.eval_line('a') #uninitiated variable
        self.assertEquals(None, result)
        interpreter.variables['a'] = '1' #initiate variables illegally
        result = interpreter.eval_line('a')
        self.assertEquals('1', result)
        result = interpreter.eval_line('(+ a 1) #a')
        self.assertEquals('2', result)
        
        #variables through "eq"
        