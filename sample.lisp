'addition
(+ 1 1)
(+ 1 2)
(+ 1.0 1.0)
(+ 1.0 1.2)
(+ 1.0 1)
(+ 1 1.2)
(+ -1.0 1.0) #comment
(+ -1 1)

'subtracting
(- 1 1)
(- 1 2)
(- 1.0 1.0)
(- 1.0 1.2)
(- 1.0 1)
(- 1 1.2)
(- -1.0 1.0) #comment
(- -1 1)

'comparisons
(eq? 1 1.0)
(eq? 1 2)
(eq?
    (1 1)
    (1 1))
(eq?
    (1 2)
    (2 1))   #testing order of values
(eq?
    (a 1)
    (a 1))
(eq?
    (1 a b)
    (1 a)) #test to make sure false is returned even though first two elements are equal

'quote
(quote a)
(quote (1 a b))
(quote (+ 1 2))  #testing to make sure (+ 1 2) is not evaluated
(quote a (b c))

'nesting
(+ (- 1 1) 1)

'variables
(define a 2)
(+ a 1)
(define b 3)
(+ a (* b 2))