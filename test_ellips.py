import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from kravchik_operator import krawczyk_eval, derived_reccurent_form
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from interval_checker import S_class
from results_func import *
from matplotlib.patches import Ellipse
a = 2
b = 1

def func_ellips():
    """
    Creating symbol variables for ellipsoid eq. system
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
    f = sym.Matrix([(U[0] ** 2)/(a**2) + (U[1] ** 2)/(b**2) + V[0] ** 2 - 1])
    return f, U, V, Vmid, C


N = 10  # The number of boxes on uniform grid
##### 1d circle
f, U, V, Vmid, C = func_ellips()
v1 = ival.Interval([0, 1.5])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = max(a, b)  # the width of the of the 2-dimensional square

interval_extension = krawczyk_eval(f, U, V, Vmid, C)
derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
k = 1e-6  # error
coef = 1.5  # Coefficient

ext_calcul = ClassicalKrawczykCalcul(interval_extension, coef)
ext_calcul_bicentered = BicenteredKrawczykCalcul(interval_extension, derived_reccurent_form, coef)

area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, k)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul_bicentered, k)
#"""
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
ellipse = Ellipse((0, 0), 2*a, 2*b, fc='y', fill=False)
plt.gca().add_patch(ellipse)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
ellipse = Ellipse((0, 0), 2*a, 2*b, fc='y', fill=False)
plt.gca().add_patch(ellipse)
#"""
grid_size = [10, 20, 30, 40, 50, 60]

"""
# Uncomment this to enable coeff variation
coef_test(L2u, ClassicalKrawczykCalcul, interval_extension, V_ival,
          k, "Classical", classical_checker)
coef_test(L2u, BicenteredKrawczykCalcul, interval_extension, V_ival,
          k, "Bicentered", bicentered_checker, derived_reccurent_form)
"""
#plot_time(grid_size, classical_time_mean, bic_time_mean)
iter_plot(np.array(S_class), N)
plt.show()



