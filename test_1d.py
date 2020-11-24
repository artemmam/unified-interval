import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from interval_checker import S_class
from results_func import *
from neumaier_theorem import Neumaier_solver
from check_box import make_boxes_list
import time
import warnings
warnings.filterwarnings("ignore")

def circle_func(x, t):
    return x**2 + t[0]**2 + t[1]**2

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
    f = sym.Matrix([(U[0] )** 2 + (U[1])** 2 + V[0] ** 2 - 1])
    return f, U, V



N = 10  # The number of boxes on uniform grid
##### 1d circle
f, U, V = func_1d()
v1 = ival.Interval([0., 1.2])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = 1.1  # the width of the of the 2-dimensional square
#derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
eps = 1e-3  # accuracy
coef = 2  # Coefficient

### Neumaier solve

neumaier_boxes = []
D = [ival.Interval([0, 1.2])]
ns_1d = Neumaier_solver(f, U, V, D)
box = [ival.Interval([-1, 1]), ival.Interval([-1, 1])]
#neumaier_boxes = ns_1d.solve(box)
all_boxes = make_boxes_list(grid, size)
start_neumaier = time.time()
for box in (all_boxes):
    if ns_1d.check_box(box):
        neumaier_boxes.append(box)
end_neumaier = time.time()
neumaier_time = end_neumaier - start_neumaier

start_classical = time.time()
ext_calcul = ClassicalKrawczykCalcul(f, U, V)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
end_classiccal = time.time()
classical_time = end_classiccal - start_classical
start_bic = time.time()
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul_bicentered, eps)
end_bic =  time.time()
bic_time = end_bic - start_bic
print("NUMBER OF INSIDE BOXES")
print("Classiccal", len(area_points_uni))
print("Bicentered", len(area_points_uni_bicen))
print("Neumaier", len(neumaier_boxes))

print("TIME")
print("Classiccal", classical_time)
print("Bicentered", bic_time)
print("Neumaier", neumaier_time)
uni_plotter(neumaier_boxes, [], L2u, "Neumaier")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
circle = plt.Circle((0, 0), radius=1, fc='y', fill=False)
plt.gca().add_patch(circle)
#coef_test(f, U, V, L2u, V_ival, eps, "Classical", "circle", ch = "c")
#coef_test(f, U, V, L2u, V_ival, eps, "Bicentered", "circle", ch = "b")
#work_with_result_coef("Classical", "circle")
#work_with_result_coef("Bicentered", "circle")
iter_plot(np.array(S_class), N)

plt.show()



