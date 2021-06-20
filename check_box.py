import interval as ival
import numpy as np
import itertools as it

def make_boxes_list(grid, dim):
    """
    Make list of boxes in dim dimension from vector grid
    :param grid: vector on which grid is constructed
    :param dim:  the dimensional of grid
    :return: the list of boxes in dim
    """
    grid_size = len(grid) - 1
    f = []
    array = []
    for i in range(grid_size):
        f.append(ival.Interval([grid[i], grid[i + 1]]))
    for i in range(dim):
        array.append(f)
    A = list(it.product(*array))
    return A


def check_box(grid, dim, V, checker, ext_calcul, eps, log = False, decomp = False):
    """
    Function for checking boxes on dim-dimensional uniform grid with checker method
    :param grid: 1-d grid
    :param dim: number of the dimensions
    :param V: vector of not fixed interval variables
    :param checker: interval method function for checking box
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :param eps: error
    :param log: turn on log info printing
    :param decomp: turn on decomposition
    :return: list of inside boxes, list of border boxes
    """
    area_boxes = []
    border_boxes = []
    grid = np.array(grid)
    grid_size = len(grid) - 1
    all_boxes = make_boxes_list(grid, dim)
    for i in range(grid_size**dim):
        temp = checker(all_boxes[i], V, eps, ext_calcul, log=log, decomposition=decomp)
        if temp == 'inside':
            area_boxes.append(all_boxes[i])
        elif temp == 'border':
            border_boxes.append(all_boxes[i])
    return area_boxes, border_boxes
