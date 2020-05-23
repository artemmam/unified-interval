import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from results_func import *
from interval_checker import S_class

def func_2rpr(d):
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
    """
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    f = sym.Matrix([[V[0] ** 2 - (U[0] + 0.5 * d) ** 2 - U[1] ** 2],
         [V[1] ** 2 - (U[0] - 0.5 * d) ** 2 - U[1] ** 2]])
    return f, U, V


N = 30  # The number of nodes on uniform grid
##### 2-RPR
L1v = 3  # Lower range of row
L2v = 15  # Upper range of row
d = 8  # Distance between actuators
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]
L2u = L2v   # the width of the 2-dimensional square
f, U, V = func_2rpr(d)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
eps = 1e-3  # accuracy
coef = 1.5
ext_calcul = ClassicalKrawczykCalcul(f, U, V)
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)

area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul_bicentered, eps)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")

iter_plot(np.array(S_class), N)
plt.show()

