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


def func_2rpr(d):
    """
    Creating symbol variables for 2-RPR eq. system
    :return: symbolic 2-RPR eq. system,
            symbolic U (fixed boxes),
            symbolic V (checking boxes),
            symbolic Vmid,
            symbolic C,
    """
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')

    f = sym.Matrix([[V[0] ** 2 - (U[0] + 0.5 * d) ** 2 - U[1] ** 2],
         [V[1] ** 2 - (U[0] - 0.5 * d) ** 2 - U[1] ** 2]])
    return f, U, V, Vmid, C


N = 10  # The number of nodes on uniform grid
##### 2-RPR

L1v = 3  # Lower range of row
L2v = 15  # Upper range of row
d = 8  # Distance between actuators
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]
L2u = L2v   # the width of the 2-dimensional square
f, U, V, Vmid, C = func_2rpr(d)

interval_extension = krawczyk_eval(f, U, V, Vmid, C)
derived_reccurent_form = derived_reccurent_form(f, V, U, Vmid)
grid = np.linspace(-L2u, L2u, N)  # The vector to build size-dim. grid
size = 2  # The dimension of uniform grid
k = 1e-6  # error
coef = 1.5
ext_calcul = ClassicalKrawczykCalcul(interval_extension, coef)
ext_calcul_bicentered = BicenteredKrawczykCalcul(interval_extension, derived_reccurent_form, coef)
#area_points_uni, border_points_uni = check_box(grid, size, V_ival,
#                                               classical_checker, ext_calcul, k)
#area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
#                                               bicentered_checker, ext_calcul_bicentered, k)
coef_arr = np.linspace(0, 5, 20)
grid_size = [10, 20, 30, 40, 50, 60]
pdf = []
pdf_b = []
for i in grid_size:
    for j in coef_arr:
        grid = np.linspace(-L2u, L2u, i)
        ext_calcul = ClassicalKrawczykCalcul(interval_extension, j)
        area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                                       classical_checker, ext_calcul, k)
        ext_calcul_bicentered = BicenteredKrawczykCalcul(interval_extension, derived_reccurent_form, coef)
        area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                                       bicentered_checker, ext_calcul_bicentered, k)
        #print("KRAWCZYK/")
        #print("GRID SIZE", i)
        #print("COEFF", j)
        #print("App. ex", len(area_points_uni)/i**2)
        pdf.append(len(area_points_uni))
        pdf_b.append(len(area_points_uni_bicen))
pdf = np.array(pdf).reshape(len(grid_size), len(coef_arr)).T
pdf_b = np.array(pdf_b).reshape(len(grid_size), len(coef_arr)).T
#print("Classical Krawczyk")
#print(np.array(pdf).reshape(3, 10).T)
#print("Bicentered Krawczyk")
#print(np.array(pdf_b).reshape(3, 10).T)
for i in range(len(grid_size)):
    print("Classical Krawczyk", pdf[::, i])
    print("Bicentered Krawczyk", pdf_b[::, i])
#uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
#uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
#plot_dist(S_class, "Classical Krawczyk")
#plot_dist(S_bic, "Bicentered Krawczyk")
plt.show()

