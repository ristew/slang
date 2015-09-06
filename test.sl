(
(set x 5)
(set x (+ x 1))
(while (> x 1) (
    (print x) 
    (set x (- x 1))
    ))
(set str "he")
(set str (+ str "llo"))
(print str)
(if (< 4 5) 
    (print "the world is okay")
    (print "something is really wrong"))
;functions!
(def cube (x) (* x x x))
(print (cube (4)))
(def factorial (n) (
    if n 
        (* n (factorial((- n 1))))
        1
    )
)
(print (factorial(10)))
(print (+ (1 2) (3 4)))
(print (+ 1.4 2.6))
(set l (1 2 3))
(print (nth l 1))
)
