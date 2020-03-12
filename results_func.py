import timeit
import seaborn as sns
import numpy as np
from check_box import check_box
import matplotlib.pyplot as plt

def plot_dist(S1, S2):
    """
    Function for plotting the distribution of the number of the iterations
    :param S1: array of the iterations count (>=2) for every box for Classical method
    :param title: array of the iterations count (>=2) for every box for Bicentered method
    """
    S1 = np.array(S1)
    S2 = np.array(S2)
    nbins_class = len(np.unique(S1))
    nbins_bic = len(np.unique(S2))
    fig, ax = plt.subplots(1, 1, figsize=(6, 8), constrained_layout=True)
    ax.set_title("The distribution of the iteration count")
    sns.set()
    ax = sns.distplot(S1, label="Classical Krawczyk", bins=nbins_class)
    ax = sns.distplot(S2, label="Bicentred Krawczyk", bins=nbins_bic)
    ax.legend(loc="upper right")
    ax.set_xlim(left=min(min(S1), min(S2)) - 1, right=max(max(S1), max(S2)) + 1)

def time_calcul(checker, ext_calcul, grid_size, L2u, size, V_ival, k):
    """
    :param checker:
    :param ext_calcul:
    :param grid_size: array sizes of the grid
    :param L2u: the borders of the grid
    :param size: int dimension of the grid
    :param V_ival: vector of not fixed interval variables
    :param k: error
    :return: array, mean times of check_box function for every grid size
    """
    time_mean = []
    for N in grid_size:
        grid = np.linspace(-L2u, L2u, N)
        t = timeit.Timer(lambda: check_box(grid, size, V_ival,
                                           checker, ext_calcul, k))
        time = []
        for i in range(20):
            time.append(t.timeit(number=1))
        time_mean.append(np.mean(time))
    return time_mean

def plot_time(grid, time, time1):
    """
    Plotting the dependency of classical and bicentered time execution from grid size
    :param grid: array sizes of the grid
    :param time: execution time for Classical method
    :param time1: execution time for Bicentered method
    """
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), constrained_layout=True)
    ax.plot(grid, time, label="Classical Krawczyk")
    ax.scatter(grid, time)
    ax.plot(grid, time1, label="Bicentered Krawczyk")
    ax.scatter(grid, time1)
    ax.grid()
    ax.set_xlabel("Gridsize")
    ax.set_ylabel("Time, s")
    ax.legend(loc='upper left')
    ax.set_title("The dependency of the time from grid size")

def coef_test(L2u, CalculClass, interval_extension, V_ival, k, name, checker, derived_reccurent_form=0):
    """
    :param L2u: the borders of the grid
    :param CalculClass: the class of the used method
    :param interval_extension: using interval extension form
    :param V_ival: vector of not fixed interval variables
    :param k: error
    :param name: name of the method
    :param checker: checker type
    :param derived_reccurent_form: if we use Bicentered method we need to use derived_recurrent_form
    """
    coef_arr = np.linspace(0, 5, 21)
    print(coef_arr)
    grid_size = [10, 30, 60]
    size = 2
    pdf = []
    for i in grid_size:
        for j in coef_arr:
            grid = np.linspace(-L2u, L2u, i)
            if derived_reccurent_form == 0:
                ext_calcul = CalculClass(interval_extension, j)
            else:
                ext_calcul = CalculClass(interval_extension, derived_reccurent_form, j)
            area_points, border_points = check_box(grid, size, V_ival,
                                        checker, ext_calcul, k)
            pdf.append(len(area_points))
    pdf = np.array(pdf).reshape(len(grid_size), len(coef_arr)).T
    for i in range(len(grid_size)):
        print(name + " Krawczyk", pdf[::, i])