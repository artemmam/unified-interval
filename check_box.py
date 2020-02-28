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
    return np.reshape(U, (grid_size ** dim, dim))


def check_box(grid, dim, V, checker, ext_calcul, k=10):
    """
    Function for checking boxes on dim-dimensional uniform grid with checker method
    :param grid: 1-d grid
    :param dim: number of the dimensions
    :param V: vector of not fixed interval variables
    :param checker: interval method function for checking box
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :param k: max number of the iterations for checker
    :return: list of inside boxes, list of border boxes
    """
    area_boxes = []
    border_boxes = []
    grid = np.array(grid)
    grid_size = len(grid) - 1
    all_boxes = make_boxes_list(grid, dim)
    for i in range(grid_size**dim):
        temp = checker(all_boxes[i], V, k, ext_calcul)
        if temp == 'inside': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
            area_boxes.append(all_boxes[i])
        elif temp == 'border': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border:
            border_boxes.append(all_boxes[i])
    return area_boxes, border_boxes
