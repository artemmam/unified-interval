import sympy as sym
import  interval as ival
import numpy as np
import matplotlib.pyplot as plt

from check_box import check_box
from interval_checker import classical_checker, bicentered_checker
from plot_workspace_area import uni_plotter, plot_dist
from kravchik_operator import krawczyk_eval, derived_reccurent_form
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from interval_checker import S_bic, S_class


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


N = 30  # The number of boxes on uniform grid
##### 1d circle
f, U, V, Vmid, C = func_1d()
v1 = ival.Interval([0, 1.2])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = 2  # the width of the of the 2-dimensional square

interval_extension = krawczyk_eval(f, U, V, Vmid, C)
derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
# grid = np.linspace(0, 0.5, 2)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
k = 1e-6  # error
coef = 1.5  # Coefficient

ext_calcul = ClassicalKrawczykCalcul(interval_extension, coef)
ext_calcul_bicentered = BicenteredKrawczykCalcul(interval_extension, derived_reccurent_form, coef)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, k)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               bicentered_checker, ext_calcul_bicentered, k)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
plot_dist(S_bic, "Classical Krawczyk")
plot_dist(S_class, "Bicentered Krawczyk")
plt.show()



