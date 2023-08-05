
import sympy
import numbers

from .taylornum import taylornum
from .taylorsym import taylorsym


# Check if f has some element that if symbolic in nature.
# If so, we will let the symbolic side handle it
def is_f_symbolic(f):
    if isinstance(f, (list, tuple)):
        return any(isinstance(fi, tuple(sympy.core.all_classes)) for fi in f)
    else:
        return isinstance(f, tuple(sympy.core.all_classes))


# Function to check if this is a sympy symbol or a number
def is_symbol_or_num(fi):
    return isinstance(fi, (tuple(sympy.core.all_classes), numbers.Number))


# Calculate the taylor series.
# This is the main routing function that determines symbolic or
# numerical Taylor series and where to send the data to
def taylor(f, x0=None, n=None):
    # Does f have something symbolic in it
    fsym = is_f_symbolic(f)

    # If n is None, then we know that this is a numeric
    if n is None:
        if x0 is None:
            if fsym:
                return taylorsym(f)
            else:
                # We need to return a lambda function that takes in
                # dt and calculates the values
                return lambda dt: taylornum(f, dt)
        else:
            if fsym:
                return taylorsym(f, x0)
            else:
                return taylornum(f, x0)
    else:
        if x0 is None:
            if fsym:
                return taylorsym(f, n=n)
            else:
                # We need to return a lambda function that takes in
                # dt and calculates the values
                return lambda dt: taylornum(f, n=n)

    # Symbolic. Check that everything is a symbol
    if isinstance(f, list) or isinstance(f, tuple):
        if all(is_symbol_or_num(fi) for fi in f):
            if isinstance(x0, list) or isinstance(x0, tuple):
                if len(f) == len(x0):
                    return taylorsym(f, x0, n)
                else:
                    error_msg = 'ERROR: Size of f and x0 do not match'
                    raise RuntimeError(error_msg)
            else:
                error_msg = 'x0 is not the same size as f'
                raise RuntimeError(error_msg)
        else:
            emsg = 'ERROR: Expected list to be all symbolic expressions.'
            raise RuntimeError(emsg)
    elif isinstance(f, tuple(sympy.core.all_classes)) \
            or isinstance(f, numbers.Number):
        return taylorsym(f, x0, n)
    else:
        raise RuntimeError('ERROR: Expected symbolic expressions.')
