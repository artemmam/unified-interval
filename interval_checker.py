import numpy as np
from interval import Interval
S_class = []
S_bic = []

def classical_checker(box, v_init, eps, ext_calcul):
    """
    Check box with classical method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param eps: error
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    v_iter = v_init.copy()
    n = len(v_init)
    ch = True
    v_prev = ext_calcul.calculate_extension(box, v_iter).reshape(-1) + Interval([0, 1])
    s = 0
    while ch:
        s += 1
        v_ext = ext_calcul.calculate_extension(box, v_iter).reshape(-1)
        for i in range(n):
            if abs(v_ext[i].width() - v_prev[i].width()) < eps:
                ch = False
                S_class.append(s)
                break
        v_prev = v_ext
        check = True
        for i in range(n):
            if not(v_ext[i].isIn(v_iter[i])):
                check = False
                break
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        for i in range(n):
            if v_iter[i].isNoIntersec(v_ext[i]):
                return 'outside'
            else:
                v_iter[i] = v_iter[i].intersec(v_ext[i])  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border


def bicentered_checker(box, v_init, eps, ext_calcul):
    """
    Check box with bicentered method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param eps: error
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    v_iter = v_init.copy()
    n = len(v_init)
    v_prev = np.full((2, 1), Interval([0, 1])).reshape(-1)
    ch = True
    s = 0
    while ch:
        s += 1
        v_ext_min, v_ext_max = ext_calcul.calculate_extension(box, v_iter)
        check = True
        v_bic = []
        for i in range(n):
            v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
        for i in range(n):
            if abs(v_bic[i].width() - v_prev[i].width()) < eps:
                ch = False
                S_bic.append(s)
                break
        v_prev = v_bic
        for i in range(n):
            if not (v_bic[i].isIn(v_iter[i])):
                check = False
                break
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        for i in range(n):
            if v_iter[i].isNoIntersec(v_bic[i]):
                return 'outside'
            else:
                v_iter[i] = v_iter[i].intersec(v_bic[i])  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border




