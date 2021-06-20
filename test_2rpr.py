import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot, plot_all_methods
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul, ExtCalcul, ModernizedClassicalKrawczykCalcul
from results_func import *
from Hansen_Sengupta import HansenSenguptaSolver
#from interval_checker import S_class
from log_functions import Logger
from neumaier_theorem import Neumaier_solver
from check_box import make_boxes_list
import time
import warnings
warnings.filterwarnings("ignore")
from all_boxes_class import AllBoxes
import sys


def plot_circles(r1, r2, d):
    circle = plt.Circle((-0.5*d, 0), radius=r1, fc='y', fill=False)
    plt.gca().add_patch(circle)
    circle = plt.Circle((0.5*d, 0), radius=r1, fc='y', fill=False)
    plt.gca().add_patch(circle)
    circle = plt.Circle((-0.5*d, 0), radius=r2, fc='y', fill=False)
    plt.gca().add_patch(circle)
    circle = plt.Circle((0.5*d, 0), radius=r2, fc='y', fill=False)
    plt.gca().add_patch(circle)

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
### Modernized Krwczyk
# MK_solver = ModernizedClassicalKrawczykCalcul(f, U, V)
# ModernizedClassicalKrawczyk_loger = Logger(grid, size, V_ival, eps, MK_solver)
# area_points_MK, border_points_MK = check_box(grid, size, V_ival,
#                                                classical_checker, MK_solver, eps= 1e-3, log = False)
# uni_plotter(area_points_MK, border_points_MK, L2u, "ModernizedKrawczyk", logger=ModernizedClassicalKrawczyk_loger, size=2)
# plot_circles(L1v, L2v, d)
# plt.show()
# sys.exit(1)

### Hansen-Sengupta solver
HS_solver = HansenSenguptaSolver(f, U, V)
hansen_sengupta_loger = Logger(grid, size, V_ival, eps, HS_solver, decomp=False)
area_points_HS, border_points_HS = check_box(grid, size, V_ival,
                                               classical_checker, HS_solver, eps= 1e-6, log = False, decomp=False)
uni_plotter(area_points_HS, border_points_HS, L2u, "Hansen-Sengupta", hansen_sengupta_loger, size=2)
plot_circles(L1v, L2v, d)
# plt.show()
# sys.exit(1)

### Neumaier solve
# neumaier_boxes = []
# neumaier_boxes_border = []
# D = [ival.Interval([3, 15]), ival.Interval([3, 15])]
# print("%%%%%")
# print("Neumaier".upper())
# print("%%%%%")
# ns_1d = Neumaier_solver(f, U, V, D)
# all_boxes = make_boxes_list(grid, size)
# start_neumaier = time.time()
# for box in (all_boxes):
#     ch = ns_1d.check_box(box, 5)
#     if ch == "in":
#         neumaier_boxes.append(box)
#     elif ch == "border":
#         neumaier_boxes_border.append(box)
# uni_plotter(neumaier_boxes, neumaier_boxes_border, L2u, "Neumaier")
# plot_circles(L1v, L2v, d)

print("%%%%%")
print("Krawczyk".upper())
print("%%%%%")
ext_calcul = ClassicalKrawczykCalcul(f, U, V)
classical_loger = Logger(grid, size, V_ival, eps, ext_calcul)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk", classical_loger, size = size)
plot_circles(L1v, L2v, d)
plt.show()
sys.exit(1)
print("%%%%%")
print("Bicentered Krawczyk".upper())
print("%%%%%")
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)
bicentered_loger = Logger(grid, size, V_ival, eps, ext_calcul_bicentered)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul_bicentered, eps)

uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk", bicentered_loger, size = size)
plot_circles(L1v, L2v, d)
plt.show()
sys.exit(1)
# print("NUMBER OF INSIDE BOXES")
# print("Classiccal", len(area_points_uni))
# print("Bicentered", len(area_points_uni_bicen))
# print("Neumaier", len(neumaier_boxes))
#
# points = {}
# class_points = AllBoxes("Classical", area_points_uni, border_points_uni)
# bic_points = AllBoxes("Bicentered", area_points_uni_bicen, border_points_uni_bicen)
# neumaier_points = AllBoxes("Neumaier", neumaier_boxes, neumaier_boxes_border)
# points["Classical"] = class_points
# points["Bicentered"] = bic_points
# points["Neumaier"] = neumaier_points
# methods = ["Classical", "Bicentered", "Neumaier"]
# plot_all_methods(methods, points, L2u, "2rpr", size=size, L1v=L1v, L2v=L2v, d=d)
# plt.show()




