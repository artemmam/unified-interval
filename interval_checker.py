def classical_checker(box, V, iter_nums, ext_calcul):
    """
    Ckeck box if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param V: variables for checking
    :param iter_nums: max number of the iterations
    :param ext_calcul: Extension calculator-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """

    V_iter = V.copy()
    for k in range(iter_nums):
        v_ext = ext_calcul.calcul_ext(box, V_iter)
        check = True
        for i in range(len(V)):
            if not(v_ext[i][0].isIn(V_iter[i])):
                check = False
                break
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        for i in range(len(V)):
            if V_iter[i].isNoIntersec(v_ext[i][0]):
                return 'outside'
            else:
                V_iter[i] = V_iter[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border

