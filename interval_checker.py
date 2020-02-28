import numpy as np
from interval import Interval

def classical_checker(box, v_init, eps, ext_calcul):
    """
    Check box with classical method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param iter_nums: max number of the iterations
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """

    v_iter = v_init.copy()
    n = len(v_init)
    #print(v_init)
    #print(v_ext.reshape(-1))
    #print(v_ext.reshape(-1) - v_init)

    ch = True
    #print(abs(A))
    #v_ext =
    #print(v_ext[1][0])
    #print((np.array(v_ext[0]) - np.array(v_iter)))
    #print(np.squeeze(np.array(v_ext) - np.array(v_iter)).reshape(1))
    #[print(i) for i in (np.array(v_ext) - np.array(v_iter))[0]]
    #print([i for i in ((np.array(v_ext) - np.array(v_iter))[0])])
    v_prev = ext_calcul.calculate_extension(box, v_iter).reshape(-1) + Interval([0, 1])
    while ch:
        v_ext = ext_calcul.calculate_extension(box, v_iter).reshape(-1)
        for i in range(n):
            if abs(v_ext[i].width() - v_prev[i].width()) < eps:
                ch = False
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
                # v_iter[i] = v_init[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
                # v_ext[i][0].scale(1.01)
                # v_iter[i] = v_ext[i][0]  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border


def bicentered_checker(box, v_init, eps, ext_calcul):
    """
    Check box with bicentered method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param iter_nums: max number of the iterations
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    v_iter = v_init.copy()
    n = len(v_init)
    v_prev = np.full((2, 1), Interval([0, 1])).reshape(-1)
    ch = True
    while ch:
        #v_ext = ext_calcul.calculate_extension(box, v_iter).reshape(-1)
        v_ext_min, v_ext_max = ext_calcul.calculate_extension(box, v_iter)
        check = True
        v_bic = []
        for i in range(n):
            v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
        for i in range(n):
            if abs(v_bic[i].width() - v_prev[i].width()) < eps:
                ch = False
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
                # v_iter[i] = v_init[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
                # v_ext[i][0].scale(1.01)
                # v_iter[i] = v_ext[i][0]  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border




