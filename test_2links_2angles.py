import sympy as sym
from sympy import sin, cos
from numpy import pi
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from results_func import *
#from interval_checker import S_class
from log_functions import Logger, Neumaier_Logger
from neumaier_theorem import Neumaier_solver
from check_box import make_boxes_list
import warnings
warnings.filterwarnings("ignore")

def plot_area(a, b):
    circle = plt.Circle((0, 0), radius=a + b, fc='y', fill=False)
    plt.gca().add_patch(circle)
    circle = plt.Circle((0, 0), radius=abs(a - b), fc='y', fill=False)
    plt.gca().add_patch(circle)


def func_2links_2angles(l_a, l_b):
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
    f = sym.Matrix([[U[0] - l_a*cos(V[0]) - l_b*cos(V[0] + V[1])],
                   [U[1] - l_a*sin(V[0]) - l_b*sin(V[0] + V[1])]]
    )
    return f, U, V


N = 20  # The number of nodes on uniform grid
##### 2-RPR
L1v = 0  # Lower range of row
L2v = 2*pi    # Upper range of row
l_a = 30
l_b = 10
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]

L2u = l_a + l_b + 15   # the width of the 2-dimensional square
f, U, V = func_2links_2angles(l_a, l_b)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
eps = 1e-6  # accuracy
coef = 1.5
print("%%%%%")
print("Neumaier".upper())
print("%%%%%")
neumaier_boxes = []
neumaier_boxes_border = []
D = [v1, v2]
ns_1d = Neumaier_solver(f, U, V, D)
Neumaier_Log = Neumaier_Logger(grid, size, D, np.pi, ns_1d)
box = [ival.Interval([-L2u, L2u]), ival.Interval([-L2u, L2u])]
all_boxes = make_boxes_list(grid, size)
for box in all_boxes:
    ch = ns_1d.check_box(box, np.pi)
    if ch == "in":
        neumaier_boxes.append(box)
    elif ch =="border":
        neumaier_boxes_border.append(box)
uni_plotter(neumaier_boxes, neumaier_boxes_border, L2u, "neumaier", Neumaier_Log)
plot_area(l_a, l_b)
print("%%%%%")
print("Krawczyk".upper())
print("%%%%%")
ext_calcul = ClassicalKrawczykCalcul(f, U, V)
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)
classical_loger = Logger(grid, size, V_ival, eps, ext_calcul)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                              classical_checker, ext_calcul_bicentered, eps)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk", classical_loger)
plot_area(l_a, l_b)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk", classical_loger)
plot_area(l_a, l_b)
plt.show()

