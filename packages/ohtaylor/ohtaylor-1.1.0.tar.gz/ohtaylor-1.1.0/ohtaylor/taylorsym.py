
import sympy
import numbers
import itertools

from ohtaylor.taylorutils import ktuples_nsum, factorial_tuple, \
    create_symbol_point_list, sort_symbols
from ohtaylor.diffcalc import DiffCalcCached


# Find the Taylor series when f:R^1 -> R^1
def taylorsym_1_1(x, f, x0):
    # If the input is given as a list or tuple of one variable,
    # change it to be a number
    if isinstance(x0, (list, tuple)):
        x0 = x0[0]

    # Initialize the iteration
    fi_1x = f
    fix = f

    for i in itertools.count():
        # Calculate the Taylor series term
        px_i = fix.subs(x, x0) / sympy.factorial(i) * (x - x0)**i
        yield px_i

        # Calculate the next derivative
        fix = sympy.diff(fi_1x, x)
        fi_1x = fix


# Find the Taylor series for f:R^N -> R
def taylorsym_N_1(x, f, x0):
    # Number of input variables
    k = len(x)
    vars = create_symbol_point_list(x, x0)
    d = DiffCalcCached()
    syms, ivs = zip(*vars)

    # Generate the Taylor series
    for i in itertools.count():
        tuples = ktuples_nsum(k, i)
        px_i = 0
        for t in tuples:
            fix = d.diff(f, syms, t)
            fix = fix.subs(vars)
            for j in range(0, k):
                fix *= (syms[j] - ivs[j])**t[j]
            px_i += fix / factorial_tuple(t)
        yield px_i


# Send to R^1 or R^n
def taylorsym_d(f, x0, n):
    if isinstance(f, numbers.Number):
        return f

    # Get the independent variables
    symbols = f.free_symbols

    if x0 is None:
        x0_syms = []
        for symbol in sort_symbols(symbols):
            x0_syms.append(sympy.Symbol(symbol.name + '0'))
        x0 = x0_syms

    # Dispatch to the right place
    if len(symbols) == 1:
        [x] = symbols
        gen = taylorsym_1_1(x, f, x0)
    else:
        gen = taylorsym_N_1(symbols, f, x0)

    # User wants the generator
    if n is None:
        return gen

    # Use the generator to create the requested polynomial
    px = 0
    for i in range(0, n+1):
        px += next(gen)
    return px


# Send each of the dimensions of R^M output to be evaluated independently
def taylorsym_l(f, x0, n):
    px = [None]*len(f)
    for i in range(0, len(f)):
        if x0 is None:
            px[i] = taylorsym_d(f[i], x0, n=n)
        else:
            px[i] = taylorsym_d(f[i], x0[i], n)
    return px


# Figure out the dimensions and dispatch to the right Taylor series evaluation
# Check that the inputs are valid and match up
def taylorsym(f, x0=None, n=None):
    if isinstance(f, list) or isinstance(f, tuple):
        return taylorsym_l(f, x0, n)
    else:
        return taylorsym_d(f, x0, n)
