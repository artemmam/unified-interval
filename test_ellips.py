import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
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
    V= [sym.symbols('v1')]
    U = sym.symbols('u1, u2')
    f = sym.Matrix([(U[0] ** 2)/(a**2) + (U[1] ** 2)/(b**2) + V[0] ** 2 - 1])
    return f, U, V


N = 12  # The number of boxes on uniform grid
##### 1d circle
f, U, V = func_ellips()
v1 = ival.Interval([0., 1.5])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = max(a, b)  # the width of the of the 2-dimensional square
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
eps = 1e-3  # accuracy
coef = 1.5  # Coefficient

ext_calcul = ClassicalKrawczykCalcul(f, U, V)
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)

area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                              classical_checker, ext_calcul_bicentered, eps)
#"""
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
ellipse = Ellipse((0, 0), 2*a, 2*b, fc='y', fill=False)
plt.gca().add_patch(ellipse)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
ellipse = Ellipse((0, 0), 2*a, 2*b, fc='y', fill=False)
plt.gca().add_patch(ellipse)
#"""
iter_plot(np.array(S_class), N)
plt.show()



