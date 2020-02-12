def classical_checker(box, V, interval_extension, checker_param, param = []):
    """
    Ckeck box if it is the solution of the system, on the border of the
    solution or neither of none of these.
    :param box: box to check
    :param V: variables for checking
    :param interval_extension: function for calculating the interval extension
    :param checker_param parameter for checker (p[0] - coefficient for the inverse point, p[1] - max number of iterations)
    :param param: parameters for interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """

    V_iter = V.copy()
    for k in range(checker_param[1]):
        Vmid = []
        for i in range(len(V)):
            Vmid.append(checker_param[0] * V_iter[i].mid())
        param_iter = param.copy()
        param_iter += [box] + [Vmid]
        C = []
        for i in range(len(V_iter)):
            C.append(V_iter[i].mid())
        v_ext = interval_extension(V_iter, C, param_iter)
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
                # V_iter[i] = V[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
                V_iter[i] = V_iter[i].intersec(v_ext[i][0])  # if our evalution not fully inside, then intersect it and repeat
    return 'border'  # if we achieve max of the iterations, then it's border

