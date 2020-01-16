import interval as ival
from box_class import BoxPoints
import numpy as np
#  TODO: add more description for function check_box


def check_box(grid, dim, V, checker, unified_krav_func, coef, p=10, param = []):
    """
    Function for checking boxes on dim-dimensional uniform grid with cheker method
    :param x: 1-d grid
    :param dim: number of the dimensions
    :param V: vector of not fixed variables
    :param checker: interval method function for checking box
    :param unified_krav_func: numerical function from symbolic format for calculating interval extension
    :param p: the max number of iterations
    :param param: list of system parameters
    :return: list of inside boxes, list of border boxes
    """
    area_boxes = []
    border_boxes = []
    q = 0
    U = []
    grid = np.array(grid)
    grid_size = len(grid) - 1
    fix = 0
    for i in range(grid_size**dim):
        for j in range(dim):
            if i % grid_size == 0 and i != 0 and j == 0:
                fix +=1
            if i % grid_size == 0 and i != 0 and j == 0:
                q += 1
            if j == 0:
                U.append(ival.Interval([grid[i % grid_size], grid[i % grid_size + 1]]))
            else:
                U.append(ival.Interval([grid[fix % grid_size], grid[fix % grid_size + 1]]))
    U = np.array(U)
    U = U.reshape(grid_size**dim, dim)
    for i in range(grid_size**dim):
        box = []
        for j in range(dim):
            u1 = ival.valueToInterval(U[i, j])
            box.append(u1)
        if checker(box, V, unified_krav_func, p, param, coef) == 'inside': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
            area_boxes.append(box)
        elif checker(box, V, unified_krav_func, p, param, coef) == 'border': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border:
            border_boxes.append(box)
    return np.array(area_boxes), np.array(border_boxes)