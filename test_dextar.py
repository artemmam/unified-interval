import sympy as sym
from sympy import sin, cos
from numpy import pi
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul
from results_func import *
from interval_checker import S_class
from log_functions import Logger
from neumaier_theorem import Neumaier_solver
from check_box import make_boxes_list
import warnings
warnings.filterwarnings("ignore")



def func_dextar(l_a, l_b, l_c, l_d, d):
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
    """
    V = sym.symbols('v1, v2, v3, v4')
    U = sym.symbols('u1, u2')
    f = sym.Matrix([[-U[0] + l_b*cos(V[2]) + l_a*cos(V[0]) + d/2],
                   [-U[0] - d/2 + l_d*cos(V[1]) + l_c*cos(V[3])],
                   [-U[1] + l_a*sin(V[0]) + l_b*sin(V[2])],
                   [-U[1] + l_d*sin(V[1]) + l_c*sin(V[3])]]
    )
    return f, U, V


N = 20  # The number of nodes on uniform grid
##### 2-RPR
L1v = 0  # Lower range of row
L2v = 2*pi   # Upper range of row
d = 60  # Distance between actuators
l_a = l_d = 72
l_b = l_c = 87
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
v3 = ival.Interval([L1v, L2v])
v4 = ival.Interval([L1v, L2v])
V_ival = [v1, v2, v3, v4]

L2u = l_a + l_b + d+20   # the width of the 2-dimensional square
f, U, V = func_dextar(l_a, l_b, l_c, l_d, d)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
eps = 1e-6  # accuracy
coef = 1.5
neumaier_boxes = []
neumaier_boxes_border = []
D = [v1, v2, v3, v4]
ns_1d = Neumaier_solver(f, U, V, D)
box = [ival.Interval([-L2u, L2u]), ival.Interval([-L2u, L2u])]
all_boxes = make_boxes_list(grid, size)
for box in (all_boxes):
    ch = ns_1d.check_box(box, np.pi)
    if ch == "in":
        neumaier_boxes.append(box)
    elif ch =="border":
        #print("border ", box)
        neumaier_boxes_border.append(box)
    #else:
        #print("out", box)
#uni_plotter(neumaier_boxes, [], L2u, "neumaier", 0)
# from neumaier_theorem import boxes
# ns_1d.find_box(box, 0, np.pi)
uni_plotter(neumaier_boxes, neumaier_boxes_border, L2u, "neumaier", 0)

# ext_calcul = ClassicalKrawczykCalcul(f, U, V)
# ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)
# classical_loger = Logger(grid, size, V_ival, eps, ext_calcul)
# area_points_uni, border_points_uni = check_box(grid, size, V_ival,
#                                                classical_checker, ext_calcul, eps)
# area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
#                                               classical_checker, ext_calcul_bicentered, eps)
# uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk", classical_loger)
# uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk", classical_loger)
#
# #iter_plot(np.array(S_class), N)
plt.show()

