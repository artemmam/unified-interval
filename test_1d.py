import sympy as sym
import  interval as ival
import numpy as np
from check_box import check_box
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter
from kravchik_operator import krawczyk_eval
from extension_calculator_class import Ext_calcul


def func_1d():
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C
    """
    Vmid = [sym.symbols('v1mid')]
    V = [sym.symbols('v1')]
    U = sym.symbols('u1, u2')
    C = [sym.symbols('c1')]
    f = sym.Matrix([U[0] ** 2 + U[1] ** 2 + V[0] ** 2 - 1])
    return f, U, V, Vmid, C


N = 64 # The number of nodes on uniform grid

##### 1d circle
f, U, V, Vmid, C = func_1d()
v1 = ival.Interval([0, 1])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = 2  # the width of the of the 2-dimensional square
param = []
#unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C)
interval_extension = krawczyk_eval(f, U, V, Vmid, C)
#####

k = 20  # Max number of iterations
coef = 1.5  # Coefficient
size = 2  # The dimension of uniform grid
grid = np.linspace(-L2u, L2u, N)  # The vector to build size-dim. grid
cont1 = Ext_calcul(interval_extension, coef, param)
area_points_uni, border_points_uni = check_box(grid, size, V_ival, classical_checker, cont1, k)
uni_plotter(area_points_uni, border_points_uni, L2u)


