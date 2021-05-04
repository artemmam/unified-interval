import numpy as np
from interval import Interval
PI2 = 2*np.pi


def diam(A):
    s = 0
    for v in A:
        s += v.width()**2
    return np.sqrt(s)


def classical_checker(box, v_init, eps, ext_calcul, log=False, decomposition=False):
    """
    Check box with classical method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param eps: accuracy
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :param log: turn on log info printing
    :param decomposition: turn on decomposition
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    v_iter = v_init.copy()
    n = len(v_init)
    v_prev = v_iter.copy()
    k = 0
    max_width = -np.inf
    new_v_left = np.empty_like(v_init)
    new_v_right = np.empty_like(v_init)
    if log:
        print("box", box)
    while True:
        v_ext = ext_calcul.calculate_extension(box, v_iter).reshape(-1)
        check = True
        if log:
            print("*****")
            print("Number of iteration =", k)
            print("Old V = ", v_iter)
            print("New V = ", v_ext)
        for i in range(n):
            if v_iter[i].isNoIntersec(v_ext[i]):
                if log:
                    print("Outside")
                return 'outside'
            else:
                v_iter[i] = v_iter[i].intersec(v_ext[i])
        for i in range(n):
            if not(v_ext[i].isIn(v_iter[i])):
                check = False
                break
        if abs(diam(v_iter) - diam(v_prev))/(0.5*abs(diam(v_iter) + diam(v_prev))) < eps or k > 20:
            if decomposition:
                v_width = []
                for i in range(n):
                    v_width.append(v_init[i].width()>np.pi/16)
                if np.all(v_width):
                    separ_i = 0
                    for i in range(n):
                        if v_init[i].width()>max_width:
                            max_width = v_init[i].width()
                            separ_i = i
                    for i in range(n):
                        if i == separ_i:
                            v_left = Interval([v_init[i][0], v_init[i].mid()])
                            v_right = Interval([v_init[i].mid(), v_init[i][1]])
                            new_v_left[i] = v_left
                            new_v_right[i] = v_right
                        else:
                            new_v_left[i] = v_init[i]
                            new_v_right[i] = v_init[i]
                    if log:
                        print("Left: ", new_v_left)
                        print("Right:", new_v_right)
                        print("GOING LEFT")
                    left_check = classical_checker(box, new_v_left, eps, ext_calcul, log, decomposition)
                    if left_check == "inside":
                        return "inside"
                        break
                    if log:
                        print("GOING RIGHT")
                    right_check = classical_checker(box, new_v_right, eps, ext_calcul, log, decomposition)
                    if right_check == "inside":
                        return "inside"
                        break
            if log:
                print("Border")
            return "border"
        v_prev = v_iter.copy()
        if check:
            if log:
                print("Inside")
            return 'inside'
        k += 1





