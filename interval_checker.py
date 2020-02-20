def classical_checker(box, v_init, iter_nums, ext_calcul):
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
    for k in range(iter_nums):
        v_ext = ext_calcul.calculate_extension(box, v_iter)
        check = True
        for i in range(n):
            if not(v_ext[i][0].isIn(v_iter[i])):
                check = False
                break
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        for i in range(n):
            if v_iter[i].isNoIntersec(v_ext[i][0]):
                return 'outside'
            else:
                v_iter[i] = v_iter[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
                # v_iter[i] = v_init[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
                # v_ext[i][0].scale(1.01)
                # v_iter[i] = v_ext[i][0]  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border


def bicentered_checker(box, v_init, iter_nums, ext_calcul):
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
    for k in range(iter_nums):
        v_ext_min, v_ext_max = ext_calcul.calculate_extension(box, v_iter)
        check = True
        v_bic = []
        for i in range(n):
            v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
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




