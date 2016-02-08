"""
This module is used to determine the values that the dimmer
must be set to, in order to achieve various levels of power
dissipation (in this case, the levels 0,10...90,100%).

Because P(t)=V(t)*I(t), it is true that we can determine the
power dissipation in a specific amount of time by integrating
this equation. Here, we integrate for half a period of the
mains supply, because that is the period of the power (the
period of sin squared).

Then, for each value we want to determine, we brute-force the
solution by comparing the desired result to the result of each
iteration (the precision is user-determined). The mean value
is mapped through the MIN and MAX values of the dimmer, thus
providing us with a result - of course with an error.

"""

from numpy import sin, linspace, pi
from scipy.integrate import quad
from scipy.interpolate import interp1d # C's 'map' function
import json


f = 50          # mains frequency
V = 325         # Vrms*sqrt(2)
I = 0.3         # 100/V because we work with percentages
HALF_P = 0.5/f  # half period of the wave
DIM_MAX = 600   # max value dictated by the dimmer..
DIM_MIN = 50    # .. and min value
PREC = 2        # precision for calculations
# Absolute tolerance for comparisons. If one value
# yields no results, we move on to a greater one,
# thus to a larger error.
tolerance = [i/1000.0 for i in xrange(10)]


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    Implementation of the `math.isclose` method
    which is provided in python 3.5, as described
    in the documentation.

    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def integrand(x):
    return V*I*sin(2*pi*f*x)**2

def construct_table():
    """:rtype: list"""
    solutions = []
    MAX, _ = quad(integrand, 0, HALF_P)
    for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        power = MAX*i
        results = []

        for tol in tolerance:
            if len(results) > 0:
                break
            for start in linspace(0, HALF_P, 1000):
                res, _ = quad(integrand, start, HALF_P)
                #print res
                if isclose(res, power, abs_tol=tol):
                    results.append(start)

        mean = sum(results)/len(results)
        solutions.append(mean)

    conv = interp1d([min(solutions), max(solutions)], [DIM_MIN, DIM_MAX])
    mapped_sol = conv(solutions)
    return [int(i) for i in mapped_sol] # = DIM_TABLE


if __name__ == '__main__':
    DIM_TABLE = construct_table()
    print DIM_TABLE

    with open('dim_table.json', 'w') as f:
        f.write(json.dumps(DIM_TABLE))


