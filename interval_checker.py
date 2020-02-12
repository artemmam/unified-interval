def classical_checker(box, V, container):
    """
    Ckeck box if it is the solution of the system, on the border of the
    solution or there is no intersection with solution.
    :param box: box to check
    :param V: variables for checking
    :param container: Container-class object, contains param info and calculate interval extension
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """

    V_iter = V.copy()
    for k in range(container.iter_num):
        #container.calcul_all(box, V)
        #Vmid = []
        #for i in range(len(V)):
        #    Vmid.append(checker_param[0] * V_iter[i].mid())
       # param_iter = param.copy()
        #param_iter += [box] + [Vmid]
        #C = []
        #for i in range(len(V_iter)):
        #    C.append(V_iter[i].mid())
        #v_ext = container.func(V_iter, container.C, container.param_iter)
        v_ext = container.calcul_ext(box, V_iter)
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

