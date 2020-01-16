import interval as ival
from box_class import BoxPoints
import numpy as np
#  TODO: add more description for function check_box


def check_box(x, size, n, V, checker, unified_krav_func, coef, p=10, param = []):
    """
    Function for checking intervals rectangles on uniform grid to approximate workspace area of 2-RPR robot
    :param x: X-coordinates of elements of uniform grid
    :param y: Y-coordinates of elements of uniform grid
    :param n: number of nodes of uniform grid
    :param V: vector of not fixed variables
    :param param: list of system parameters
    :param checker: interval method function for checking box
    :param unified_krav_func: numerical function from symbolic format for calculating interval extension
    :param p: the max number of iterations
    :return: 4 arrays of calculated boxes: X-coordinates of workspace area, Y-coordinates of workspace area,
             X-coordinates of border of workspace area, Y-coordinates of border of workspace area
    """
    area_points = BoxPoints()
    border_points = BoxPoints()
    q = 0
    U = []
    x = np.array(x)
    h = len(x) -1
   # print((h - 1)**size)
   # print(h)
    fix = 0
    for i in range((h)**size):
        for j in range(size):
            print('Check', i%(h))
            if i % h  == 0 and i!=0 and j == 0:
                fix +=1
                print('Fix', fix)
            if i % h == 0 and i!=0 and j == 0:
                q+=1
                print('kuku')
            if j == 0:
                print(i % h, j % h)
                print(x[i % h], x[i % h + 1])
                U.append(ival.Interval([x[i % h], x[i % h  + 1]]))
            else:
                print(i, j)
                print(fix)
                print(x[fix], x[fix + 1])
                U.append(ival.Interval([x[fix], x[fix + 1]]))
    U = np.array(U)
    print(U.reshape(h**size, size))
    U = U.reshape(h**size, size)
    print(U.shape)
    for i in range(n - 1):
        for j in range(n - 1):
            u1 = ival.Interval([x[i, j], x[i, j + 1]])  # Interval form of X-coordinate of rectangle of uniform grid
            u2 = ival.Interval([y[i, j], y[i + 1, j]])  # Interval form of Y-coordinate of rectangle of uniform grid
            U = [u1, u2]
            if checker(U, V, unified_krav_func, p, param, coef) == 'inside': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
                area_points.add_point(u1[0], 'xleft')
                area_points.add_point(u1[1], 'xright')         # inside the workspace area
                area_points.add_point(u2[0], 'yleft')
                area_points.add_point(u2[1], 'yright')
            elif checker(U, V, unified_krav_func, p, param, coef) == 'border': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border':
                border_points.add_point(u1[0], 'xleft')  # if it is inside previous interval, then it's
                border_points.add_point(u1[1], 'xright')  # inside the workspace area
                border_points.add_point(u2[0], 'yleft')
                border_points.add_point(u2[1], 'yright')
    return area_points, border_points