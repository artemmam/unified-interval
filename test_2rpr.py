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
import timeit

def time_calcul(checker, ext_calcul):
    classical_time_mean = []
    for N in grid_size:
        grid = np.linspace(-L2u, L2u, N)
        t = timeit.Timer(lambda: check_box(grid, size, V_ival,
                                           checker, ext_calcul, k))
        classical_time = []
        for i in range(20):
            classical_time.append(t.timeit(number=1))
        classical_time_mean.append(np.mean(classical_time))
    return classical_time_mean

def plot_time(grid, time, title):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), constrained_layout=True)
    ax.plot(grid, time)
    ax.scatter(grid, time)
    ax.grid()
    ax.set_xlabel("Grid")
    ax.set_ylabel("Time, s")
    ax.set_xticks(grid)
    ax.set_yticks(time)
    ax.set_title("The dependency of the time from grid size"+"("+title+" method)")

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


N = 60  # The number of nodes on uniform grid
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
area_points_uni, border_points_uni = check_box(grid, size, V_ival,
                                               classical_checker, ext_calcul, k)
area_points_uni_bicen, border_points_uni_bicen = check_box(grid, size, V_ival,
                                               bicentered_checker, ext_calcul_bicentered, k)
grid_size = [10, 20, 30, 40, 50, 60]
classical_time_mean = [0.16201975499999993, 0.35754429499999973, 0.6507252499999998, 1.0159106799999997, 1.3666825800000002, 1.8148902950000014] #= time_calcul(classical_checker, ext_calcul)
bic_time_mean = [0.16068296000000187, 0.4340462399999986, 0.792084169999999, 1.2371301550000027, 1.6865018449999993, 2.2618362799999985] #= time_calcul(bicentered_checker, ext_calcul_bicentered)
print(grid_size)
print(classical_time_mean)
print(bic_time_mean)
plot_time(grid_size, classical_time_mean, "Classical")
plot_time(grid_size, bic_time_mean, "Krawczyk")
#print(classical_time_std)
"""
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
        pdf.append(len(area_points_uni))
        pdf_b.append(len(area_points_uni_bicen))
pdf = np.array(pdf).reshape(len(grid_size), len(coef_arr)).T
pdf_b = np.array(pdf_b).reshape(len(grid_size), len(coef_arr)).T
for i in range(len(grid_size)):
    print("Classical Krawczyk", pdf[::, i])
    print("Bicentered Krawczyk", pdf_b[::, i])
"""
#uni_plotter(area_points_uni, border_points_uni, L2u, "Classical Krawczyk")
#uni_plotter(area_points_uni_bicen, border_points_uni_bicen, L2u, "Bicentered Krawczyk")
#plot_dist(S_class, "Classical Krawczyk")
#plot_dist(S_bic, "Bicentered Krawczyk")
plt.show()

