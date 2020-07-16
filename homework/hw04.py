HW_SOURCE_FILE = 'hw04.py'

###############
#  Questions  #
###############

def intersection(st, ave):
    """Represent an intersection using the Cantor pairing function."""
    return (st+ave)*(st+ave+1)//2 + ave

def street(inter):
    return w(inter) - avenue(inter)

def avenue(inter):
    return inter - (w(inter) ** 2 + w(inter)) // 2

w = lambda z: int(((8*z+1)**0.5-1)/2)

def taxicab(a, b):
    """Return the taxicab distance between two intersections.

    >>> times_square = intersection(46, 7)
    >>> ess_a_bagel = intersection(51, 3)
    >>> taxicab(times_square, ess_a_bagel)
    9
    >>> taxicab(ess_a_bagel, times_square)
    9
    """
    "*** YOUR CODE HERE ***"
    
    return abs(street(a)-street(b)) + abs(avenue(a)-avenue(b))

def squares(s):
    """Returns a new list containing square roots of the elements of the
    original list that are perfect squares.

    >>> seq = [8, 49, 8, 9, 2, 1, 100, 102]
    >>> squares(seq)
    [7, 3, 1, 10]
    >>> seq = [500, 30]
    >>> squares(seq)
    []
    """
    "*** YOUR CODE HERE ***"
    return [int(i**0.5) for i in s if round(i**0.5)**2 == i ]

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
#    if n > 3:
#        k = 3
#        predd, pred, curr = 1, 2, 3
#        while k < n:
#            predd, pred, curr = pred, curr, curr+2*pred+3*predd
#            k += 1
#    else:
#        curr = n
#    return curr
    

    if n < 4:
        return n
    else:
        return g(n-1) + 2*g(n-2) + 3*g(n-3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    "*** YOUR CODE HERE ***"
    predd, pred, curr = 1, 2, 3
    if n > 3:
        for k in range(3,n):
            predd, pred, curr = pred, curr, curr+2*pred+3*predd
    else:
        curr = n
    return curr

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    "*** YOUR CODE HERE ***"
#    methode 1: using recursion"""
#    if n == 1:  
#        return 1
#    else:
#        m = 0
#        for i in range(1,n):
#            if has_seven(i) or i%7==0:
#                m += 1 
#            
#            if m%2 ==0:
#                k =1
#            else:
#                k=-1
#        return pingpong(n-1) + k

#    methode 2: using high order function"""
    def f(i, condition, previous_number):
            if i == n:
                return previous_number + condition
            elif has_seven(i) or i%7==0:
                return f(i+1, -condition, previous_number + condition)
            else:
                return f(i+1,condition, previous_number + condition)

    return f(1,1,0)

def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    if k % 10 == 7:
        return True
    elif k < 10:
        return False
    else:
        return has_seven(k // 10)

def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    "*** YOUR CODE HERE ***"
    size, k = 0, amount
    while k > 0 :
        k = k//2
        size += 1

        
    def f(a, s):
        if a == 0:
            return 1
        elif a < 0:
            return 0
        if s == 0:
            return 0
        else:
            return f(a-2**(s-1), s) + f(a, s-1)
            
            
        
    return f(amount, size)



###################
# Extra Questions #
###################

from operator import sub, mul


fact = lambda n: 1 if n == 1 else mul(n, fact(sub(n, 1)))

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return lambda n: 1 if n == 1 else mul(n, fact(sub(n, 1)))
