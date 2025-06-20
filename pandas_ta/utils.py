# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

from functools import reduce
from operator import mul
from sys import float_info as sflt



def combination(**kwargs):
    """https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python"""
    n = int(math.fabs(kwargs.pop('n', 1)))
    r = int(math.fabs(kwargs.pop('r', 0)))

    if kwargs.pop('repetition', False) or kwargs.pop('multichoose', False):
        n = n + r - 1

    # if r < 0: return None
    r = min(n, n - r)
    if r == 0:
        return 1
    
    # Use math.prod for Python 3.8+
    numerator = math.prod(range(n, n - r, -1))
    denominator = math.prod(range(1, r + 1))
    return numerator // denominator


def df_error_analysis(dfA, dfB, **kwargs):
    """ """
    col = kwargs.pop('col', None)
    corr_method = kwargs.pop('corr_method', 'pearson')

    # Find their differences
    diff = dfA - dfB
    
    # Calculate descriptive statistics for the difference
    desc_stats = diff.describe()
    
    # Calculate additional statistics
    var_val = diff.var()
    mad_val = (diff - diff.mean()).abs().mean() # Replaced diff.mad()
    sem_val = diff.sem()
    corr_val = dfA.corr(dfB, method=corr_method) # Assuming dfA and dfB are Series for correlation
    
    extra_stats = pd.Series([var_val, mad_val, sem_val, corr_val], index=['var', 'mad', 'sem', 'corr'])
    
    # Concatenate descriptive statistics with extra statistics
    df = pd.concat([desc_stats, extra_stats])

    # For plotting
    # diff.hist()
    # if diff[diff > 0].any():
    #     diff.plot(kind='kde')
    
    if col is not None:
        return df[col]
    else:
        return df

def fibonacci(**kwargs):
    """Fibonacci Sequence as a numpy array"""
    n = int(math.fabs(kwargs.pop('n', 2)))
    zero = kwargs.pop('zero', False)
    weighted = kwargs.pop('weighted', False)

    if zero:
        a, b = 0, 1
    else:
        n -= 1
        a, b = 1, 1

    result = np.array([a])
    for i in range(0, n):
        a, b = b, a + b
        result = np.append(result, a)

    if weighted:
        fib_sum = np.sum(result)
        if fib_sum > 0:
            return result / fib_sum
        else:
            return result
    else:
        return result


def get_drift(x:int):
    """Returns an int if not zero, otherwise defaults to one."""
    return int(x) if x and x != 0 else 1


def get_offset(x:int):
    """Returns an int, otherwise defaults to zero."""
    return int(x) if x else 0


def pascals_triangle(**kwargs):
    """Pascal's Triangle

    Returns a numpy array of the nth row of Pascal's Triangle.
    n=4  => triangle: [1, 4, 6, 4, 1]
         => weighted: [0.0625, 0.25, 0.375, 0.25, 0.0625
         => inverse weighted: [0.9375, 0.75, 0.625, 0.75, 0.9375]
    """
    n = int(math.fabs(kwargs.pop('n', 0)))
    weighted = kwargs.pop('weighted', False)
    inverse = kwargs.pop('inverse', False)

    # Calculation
    triangle = np.array([combination(n=n, r=i) for i in range(0, n + 1)])
    triangle_sum = np.sum(triangle)
    triangle_weights = triangle / triangle_sum
    inverse_weights = 1 - triangle_weights

    if weighted and inverse:
        return inverse_weights
    if weighted:
        return triangle_weights
    if inverse:
        return None

    return triangle


def signed_series(series:pd.Series, initial:int = None):
    """Returns a Signed Series with or without an initial value"""
    series = verify_series(series)
    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial
    return sign


def verify_series(series:pd.Series):
    """If a Pandas Series return it."""
    if series is not None and isinstance(series, pd.Series): # Changed to pd.Series
        return series


def weights(w):
    def _dot(x):
        return np.dot(w, x)
    return _dot


def zero(x):
    """If the value is close to zero, then return zero.  Otherwise return the value."""
    return 0 if -sflt.epsilon < x and x < sflt.epsilon else x