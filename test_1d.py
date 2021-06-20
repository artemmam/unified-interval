import sympy as sym
import interval as ival
from interval_checker import classical_checker
from plot_workspace_area import uni_plotter, iter_plot, plot_all_methods
from extension_calculator_class import ClassicalKrawczykCalcul, BicenteredKrawczykCalcul, ModernizedClassicalKrawczykCalcul
from log_functions import Logger
#from interval_checker import S_class
from results_func import *
from neumaier_theorem import Neumaier_solver
from check_box import make_boxes_list
import time
import warnings
import sys
from Hansen_Sengupta import HansenSenguptaSolver
from all_boxes_class import AllBoxes
warnings.filterwarnings("ignore")

def circle_func(x, t):
    return x**2 + t[0]**2 + t[1]**2

def func_1d():
    """
    Creating symbol variables for circle eq. system
    :return: symbolic eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C
    """
    V = [sym.symbols('v1')]
    U = sym.symbols('u1, u2')
    f = sym.Matrix([(U[0]) ** 2 +
                    (U[1]) ** 2 + V[0] ** 2 - 1])
    return f, U, V



N = 30  # The number of boxes on uniform grid
##### 1d circle
f, U, V = func_1d()
v1 = ival.Interval([0., 1.2])  # Set the interval for v1
V_ival = [v1]  # interval vector V
L2u = 1.5  # the width of the of the 2-dimensional square
#derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N + 1)  # The vector to build size-dim. grid
#print(grid)
size = 2  # The dimension of uniform grid
eps = 1e-3  # accuracy
coef = 2  # Coefficient

### Modernized Krwczyk
# MK_solver = ModernizedClassicalKrawczykCalcul(f, U, V)
# ModernizedClassicalKrawczyk_loger = Logger(grid, size, V_ival, eps, MK_solver)
# area_points_MK, border_points_MK = check_box(grid, size, V_ival,
#                                                classical_checker, MK_solver, eps= 1e-3, log = False)
# uni_plotter(area_points_MK, border_points_MK, L2u, "ModernizedKrawczyk", logger=ModernizedClassicalKrawczyk_loger, size=2)
# circle1 = plt.Circle((0, 0), 1, fc="y", fill = False)
# plt.gca().add_patch(circle1)
# plt.show()
# sys.exit(1)


### Hansen-Sengupta solve
HS_solver = HansenSenguptaSolver(f, U, V)
hansen_sengupta_loger = Logger(grid, size, V_ival, eps, HS_solver)
area_points_HS, border_points_HS = check_box(grid, size, V_ival,
                                               classical_checker, HS_solver, eps= 1e-15, log = False)
uni_plotter(area_points_HS, border_points_HS, L2u, "Hansen-Sengupta", hansen_sengupta_loger, size=size)
circle1 = plt.Circle((0, 0), 1, fc="y", fill = False)
plt.gca().add_patch(circle1)
#plot_circles(L1v, L2v, d)
# plt.show()
# sys.exit(1)
# neumaier_boxes = []
# neumaier_boxes_border = []
# D = [ival.Interval([0, 1.2])]
# print("%%%%%")
# print("Neumaier".upper())
# print("%%%%%")
# ns_1d = Neumaier_solver(f, U, V, D)
# box = [ival.Interval([-1, 1]), ival.Interval([-1, 1])]
# #neumaier_boxes = ns_1d.solve(box)
# all_boxes = make_boxes_list(grid, size)
# #print(all_boxes)
# start_neumaier = time.time()
# for box in (all_boxes):
#     ch = ns_1d.check_box(box, 1)
#     if ch == "in":
#         neumaier_boxes.append(box)
#     elif ch == "border":
#         neumaier_boxes_border.append(box)
# end_neumaier = time.time()
# neumaier_time = end_neumaier - start_neumaier

print("%%%%%")
print("Krawczyk".upper())
print("%%%%%")
ext_calcul = ClassicalKrawczykCalcul(f, U, V)
classical_loger = Logger(grid, size, V_ival, eps, ext_calcul)
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, eps)
uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk", classical_loger, size = size)
circle2 = plt.Circle((0, 0), 1, fc="y", fill = False)
plt.gca().add_patch(circle2)
print("%%%%%")
print("Bicentered Krawczyk".upper())
print("%%%%%")
ext_calcul_bicentered = BicenteredKrawczykCalcul(f, U, V, coef)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul_bicentered, eps)
uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk", size = size)
circle3 = plt.Circle((0, 0), 1, fc="y", fill = False)
plt.gca().add_patch(circle3)
plt.show()
# print("NUMBER OF INSIDE BOXES")
# print("Classiccal", len(area_points_uni))
# print("Bicentered", len(area_points_uni_bicen))
# print("Neumaier", len(neumaier_boxes))
# points = {}
# class_points = AllBoxes("Classical", area_points_uni, border_points_uni)
# bic_points = AllBoxes("Bicentered", area_points_uni_bicen, border_points_uni_bicen)
# neumaier_points = AllBoxes("Neumaier", neumaier_boxes, neumaier_boxes_border)
# points["Classical"] = class_points
# points["Bicentered"] = bic_points
# points["Neumaier"] = neumaier_points
# methods = ["Classical", "Bicentered", "Neumaier"]
# plot_all_methods(methods, points, L2u, "circle", size=size)
# plt.show()



