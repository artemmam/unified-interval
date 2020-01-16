import sympy as sym
import  interval as ival
import numpy as np
from kravchik_operator import get_unified_krav_eval
from box_class import BoxPoints
from check_box import check_box
from unified_krawczyk import unified_krav_eval
from plot_workspace_area import uni_plotter


def func_1d():
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
            the list of symbolic parameters of 2-RPR system
    """
    Vmid = [sym.symbols('v1mid')]
    V = [sym.symbols('v1')]
    U = sym.symbols('u1, u2')
    C = [sym.symbols('c1')]
    #param_sym = sym.symbols('d')
    #param_sym = [param_sym]
    f = sym.Matrix([U[0] ** 2 + U[1] ** 2 + V[0] ** 2 - 1])
    return f, U, V, Vmid, C#, param_sym


### Setting params
def set_param(L, N):
    """
    Setting size of uniform grid
    :param L: the length of 1/2 of uniform grid
    :param N: number of nodes
    :return: the lists of X and Y coordinates of boxes
    """
    l1 = -L  # Left and lower border of uniform grid
    l2 = L  # Right and upper border of uniform grid
    X1 = np.linspace(l1, l2, N)
    Y1 = np.linspace(l1, l2, N)
    X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
    return (X, Y)

N = 51  # The number of nodes on uniform grid

##### 1d circle
f, U, V, Vmid, C = func_1d()
L1v = -2 # Lower range of row
L2v = 2 # Upper range of row
v1 = ival.Interval([0, 1])
V_ival = [v1]
L2u = L2v
X, Y = set_param(L2u, N)
param = []
unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C)
#####

k = 10  # Max number of iterations
coef = 1.5
coef_list = np.linspace(0.0, 5.0, num = 10)
area_points = BoxPoints()
border_points = BoxPoints()
"""
for c in coef_list:
    print('***')
    print('COEF = ', c)
    area_points_uni, border_points_uni = check_box(X, Y, N, V_ival, unified_krav_eval, unified_krav_func, c, k,
                                                   param)
    uni_plotter(area_points_uni, border_points_uni, L2u)
"""
area_points_uni, border_points_uni = check_box(X, Y, N, V_ival, unified_krav_eval, unified_krav_func, coef, k, param)
uni_plotter(area_points_uni, border_points_uni, L2u)


