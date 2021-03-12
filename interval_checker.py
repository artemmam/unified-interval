import numpy as np
from interval import Interval
S_class = []
PI2 = 2*np.pi


def interval_radian(x):
    l = []
    for a in x:
        l.append(a%PI2)
    return Interval([min(l), max(l)])


def diam(A):
    s = 0
    for v in A:
        s += v.width()**2
    return np.sqrt(s)


def classical_checker(box, v_init, eps, ext_calcul, log = False):
    """
    Check box with classical method if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param v_init: variables for checking
    :param eps: accuracy
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    v_iter = v_init.copy()
    n = len(v_init)
    ch = True
    v_prev = ext_calcul.calculate_extension(box, v_iter).reshape(-1) + Interval([0, 0.1])
    s = 0
    while ch:
        s += 1
        v_ext = ext_calcul.calculate_extension(box, v_iter).reshape(-1)
        check = True
        if log:
            print("*****")
            print("Number of iteration =", s)
            print("Old V = ", v_iter)
            print("New V = ", v_ext)
        for i in range(n):
            if v_iter[i].isNoIntersec(v_ext[i]):
                S_class.append(s)
                if log:
                    print("Outside")
                return 'outside'
            else:
                v_iter[i] = v_iter[i].intersec(v_ext[i])  # if our evalution not fully inside, then intersect it and repeat
        for i in range(n):
            if not(v_ext[i].isIn(v_iter[i])):
                check = False
                break
        if abs(diam(v_ext) - diam(v_prev))/(0.5*abs(diam(v_ext) + diam(v_prev))) < eps:
            ch = False
            break
        v_prev = v_ext
        if check:
            S_class.append(s)
            if log:
                print("Inside")
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
    S_class.append(s)
    if log:
        print("Border")
    return 'border'  # if we achieve max of the iterations, then it's border





