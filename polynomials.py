
"""
Functions and APIs: Polynomials
-------------------------------

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""
import re

SIMPLIFICATION_RULES = {
                    r'(\d+)\s\*\sx\*{2}0':r'\1', # a * (x^0) = a
                    r'(x)\*{2}1\b':r'\1',# x^1 = x 
                    r'\b1\s\*\s(x\*{2}\d)':r'\1', # 1 * (x^2) = x^2
                    r'x\*{2}0':'1' # x^0 = 1
                }

def simplify(expression):
    for pattern in SIMPLIFICATION_RULES:
        if(re.search(pattern,expression)):
            expression = re.sub(pattern,r'%s'%(SIMPLIFICATION_RULES[pattern]),expression)
    return expression

# redefine enumerate that supports reverse
def enumerate(sequence,reverse=False):
    n = len(sequence)-1 if reverse else 0
    for _ in range(len(sequence)):
        yield n,sequence[n]
        n = (n-1) if reverse else (n+1)

# returns an uncompiled/canonical polynomial string (10,20,30) => '30 * x**2 + 20 * x + 10'
def canonical_poly(coefs):
    terms = [simplify('{0} * x**{1}'.format(coef,position)) for position,coef in enumerate(coefs,reverse=True) if coef != 0]
    expression = ' + '.join(terms)
    return expression 

def poly(coefs):
    poly_st = canonical_poly(coefs)
    poly_fn = eval('lambda x: {0}'.format(poly_st))
    def fn(x):
        return  poly_fn(x)
    fn.__name__ = poly_st
    fn.coefs = coefs
    return fn

def canonical_name(name): 
    return name.replace(' ', '').replace('+-', '-')

def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    return canonical_name(name1) == canonical_name(name2)

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    if not (hasattr(x,'__call__')): # x should be a function
        return False
    if not (hasattr(x,'__name__')): # x should have name attr. 
        return False
    poly = canonical_name(x.__name__) # strip and return in standard form
    poly_pattern = r'(\b\d+\*x\*{2}\d+\b)|(\bx\*{2}\d+\b)|(\b\d+\*x\b)|(\bx\b)|(\b\d+\b)'
    for p in poly.split('+'):
        if not re.search(poly_pattern,p):
            return False
    return True
# For all functions below, just manipulate the coefs and use poly() function.
def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    summed_coefs = add_coefs(p1.coefs,p2.coefs)
    return poly(summed_coefs)

def add_coefs(p1,p2):
    diff = len(p1) - len(p2)
    if diff > 0 : # standardize by making coefs the same length
        p2 = p2 + (0,) * abs(diff) 
    else:
        p1 = p1 + (0,) * abs(diff)
    return tuple([p1[i] + p2[i] for i,_ in enumerate(p1)])

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    p2.coefs = tuple([-e for e in p2.coefs])
    return add(p1,p2)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    p1_coefs = p1.coefs
    p2_coefs = p2.coefs
    list_coefs = list()
    for index,p1_coef in enumerate(p1_coefs):
        list_coefs.append([0]*index + [p1_coef*p2_coef for p2_coef in p2_coefs])
    mul_coefs = list() 
    for coefs in list_coefs:
        mul_coefs = add_coefs(tuple(coefs),tuple(mul_coefs)) # cumulative addition of coefs is the multiplication coef.
    return poly(mul_coefs)


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    power_poly = poly((1,))
    for _ in range(0,n): #cumulative multiplication is the power fn.
        power_poly = mul(power_poly,p)
    return power_poly
   
def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    coefs = p.coefs
    derivative_coefs = list()
    for index,coef in enumerate(coefs):
        if index != 0:
            derivative_coefs.append(coef * index)
    return poly(tuple(derivative_coefs))

def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    coefs = p.coefs
    integral_coefs = [C]
    for index,coef in enumerate(coefs):
        integral_coefs.append(coef/(index+1))
    return poly(tuple(integral_coefs))

def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 =  add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')
    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27) 
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)
    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573
    print 'tests pass'

if __name__ == '__main__':
    test_poly()
