import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from interval_checker import S_class
from results_func import *


def func_1d():
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C
    """
    V = [sym.symbols('v1')]
    U = sym.symbols('u1, u2')
    f = sym.Matrix([U[0] ** 2 + U[1] ** 2 + V[0] ** 2 - 1])
    return f, U, V


N = 30  # The number of boxes on uniform grid
##### 1d circle
f, U, V = func_1d()
v1 = ival.Interval([0.1, 1.2])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = 2  # the width of the of the 2-dimensional square

#derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
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

uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
grid_size = [10, 20, 30, 40, 50, 60]

"""
# Precalculated times to decrease execution time
classical_time_mean = [0.032082344999999936, 0.19224768999999986, 0.403666345, 0.7383652150000005,
                       1.6308797099999996, 2.55645095]
bic_time_mean = [0.09698290000000113, 0.3464503200000003, 0.589862325, 0.9749241999999996,
                 1.3536733949999984, 1.9183285950000013]
"""
"""
# Uncomment this to enable coeff variation
coef_test(L2u, ClassicalKrawczykCalcul, interval_extension, V_ival,
          k, "Classical", classical_checker)
coef_test(L2u, BicenteredKrawczykCalcul, interval_extension, V_ival,
          k, "Bicentered", bicentered_checker, derived_reccurent_form)
"""
"""
#Uncomment this to enable time calculation
classical_time_mean = time_calcul(classical_checker, ext_calcul, grid_size, L2u, size, V_ival, k)
bic_time_mean = time_calcul(bicentered_checker, ext_calcul_bicentered, grid_size, L2u, size, V_ival, k)
print(classical_time_mean)
print(bic_time_mean)
"""
#start_interval_test(L2u, ext_calcul, [ival.Interval([0, 1])], "Classical", "circle")
work_with_result("Classical", "circle", [ival.Interval([0, 1])])
#start_interval_test(L2u, ext_calcul_bicentered, [ival.Interval([0, 1])], "Bicentered", "circle")
work_with_result("Bicentered", "circle", [ival.Interval([0, 1])])
#plot_time(grid_size, classical_time_mean, bic_time_mean)
#iter_plot(np.array(S_class), N)
plt.show()



