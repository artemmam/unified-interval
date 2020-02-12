import sympy as sym
import  interval as ival
import numpy as np
from check_box import check_box
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter
from kravchik_operator import krawczyk_eval
from container_class import Container


def func_2rpr():
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
            the list of symbolic parameters of 2-RPR system
    """
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')
    param_sym = sym.symbols('d')
    param_sym = [param_sym]
    f = sym.Matrix([[V[0] ** 2 - (U[0] + 0.5 * param_sym[0]) ** 2 - U[1] ** 2],
         [V[1] ** 2 - (U[0] - 0.5 * param_sym[0]) ** 2 - U[1] ** 2]])
    return f, U, V, Vmid, C, param_sym


N = 64 # The number of nodes on uniform grid
##### 2-RPR
f, U, V, Vmid, C, param_sym = func_2rpr()
L1v = 3  # Lower range of row
L2v = 15  # Upper range of row
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]
L2u = L2v   # the width of the 2-dimensional square

interval_extension = krawczyk_eval(f, U, V, Vmid, C, param_sym)
#####
grid = np.linspace(-L2u, L2u, N)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
k = 10  # Max number of iterations
coef = 1.5
d = 6
param = [d]
checker_param = [coef, k]
cont1 = Container(interval_extension, k, coef, param, checker_param)
print(cont1.iter_num, cont1.func, cont1.checker_param, cont1.coef, cont1.param)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, interval_extension,
                                               checker_param, param)
uni_plotter(area_points_uni, border_points_uni, L2u)

