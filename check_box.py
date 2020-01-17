import interval as ival
import numpy as np


def make_boxes_list(grid, dim):
    """
    Make list of boxes in dim dimension from vector grid
    :param grid: vector on which grid is constructed
    :param dim:  the dimensional of grid
    :return: the list of boxes in dim
    """
    U = []
    grid_size = len(grid) - 1
    fix = 0
    for i in range(grid_size ** dim):
        for j in range(dim):
            if i % grid_size == 0 and i != 0 and j == 0:
                fix += 1
            if j == 0:
                U.append(ival.Interval([grid[i % grid_size], grid[i % grid_size + 1]]))
            else:
                U.append(ival.Interval([grid[fix % grid_size], grid[fix % grid_size + 1]]))
    U = np.array(U)
    U = U.reshape(grid_size ** dim, dim)
    return(U)


def check_box(grid, dim, V, checker, unified_krav_func, coef, p=10, param = []):
    """
    Function for checking boxes on dim-dimensional uniform grid with checker method
    :param grid: 1-d grid
    :param dim: number of the dimensions
    :param V: vector of not fixed interval variables
    :param checker: interval method function for checking box
    :param unified_krav_func: numerical function from symbolic format for calculating interval extension
    :param the coefficient
    :param p: the max number of iterations
    :param param: list of system parameters
    :return: list of inside boxes, list of border boxes
    """
    area_boxes = []
    border_boxes = []
    grid = np.array(grid)
    grid_size = len(grid) - 1
    all_boxes = make_boxes_list(grid, dim)
    for i in range(grid_size**dim):
        box = []
        for j in range(dim):
            box.append(ival.valueToInterval(all_boxes[i, j]))
        if checker(box, V, unified_krav_func, p, param, coef) == 'inside': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
            area_boxes.append(box)
        elif checker(box, V, unified_krav_func, p, param, coef) == 'border': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border:
            border_boxes.append(box)
    return np.array(area_boxes), np.array(border_boxes)