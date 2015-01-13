import unittest
import lisp_interpret
import lisp_verifications
import lisp_functions

class ParserTest(unittest.TestCase):
    def test1_parse_line(self):
        interpreter = lisp_interpret.Interpreter({}, {})
        
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
        result = interpreter.parse_line("(def a 'something)")
        self.assertEquals([['def', 'a', ["'", 'something']]], result)
        result = interpreter.parse_line("(def a '(1 2))")
        self.assertEquals([['def', 'a', ["'", ['1', '2']]]], result)

    def test2_functions_verifications(self):
        func = lisp_functions.funcs.FUNCTIONS
        veri = lisp.verifications.veris.VERIFICATIONS

    def test3_is_symbol(self):
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
        parsed_text = interpreter.parse_line('1')
        self.assertFalse(interpreter.is_symbol(parsed_text))
        self.assertTrue(interpreter.is_symbol(parsed_text[0]))

    def test4_verify(self):
        #TODO:
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
    def test5_evaluate(self):
        interpreter = lisp_interpret.Interpreter(lisp_functions.FUNCTIONS, lisp_verifications.VERIFICATIONS)
        
        #operation +
        result = interpreter.eval_line('(+ 1 1)')
        self.assertEquals(2, result)
        self.assertIsInstance(result, int)
        
        result = interpreter.eval_line('(+ 1 1.0)')
        self.assertEquals(2, result)
        self.assertIsInstance(result, float)