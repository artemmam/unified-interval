import sympy as sym
import  interval as ival
import numpy as np
import matplotlib.pyplot as plt
from check_box import check_box
from interval_checker import classical_checker, bicentered_checker
from plot_workspace_area import uni_plotter
from kravchik_operator import krawczyk_eval, derived_reccurent_form
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul


def func_2rpr(d):
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
    """
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')

    f = sym.Matrix([[V[0] ** 2 - (U[0] + 0.5 * d) ** 2 - U[1] ** 2],
         [V[1] ** 2 - (U[0] - 0.5 * d) ** 2 - U[1] ** 2]])
    return f, U, V, Vmid, C


N = 26  # The number of nodes on uniform grid
##### 2-RPR

L1v = 3  # Lower range of row
L2v = 15  # Upper range of row
d = 8 # Distance between actuators
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]
L2u = L2v   # the width of the 2-dimensional square
f, U, V, Vmid, C = func_2rpr(d)

interval_extension = krawczyk_eval(f, U, V, Vmid, C)
derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
k = 10  # Max number of iterations
coef = 1
ext_calcul = ClassicalKrawczykCalcul(interval_extension, coef)
ext_calcul_bicentered = BicenteredKrawczykCalcul(interval_extension, derived_reccurent_form, coef)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, k)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               bicentered_checker, ext_calcul_bicentered, k)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
plt.show()

