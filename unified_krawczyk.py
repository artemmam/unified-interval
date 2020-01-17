def unified_krav_eval(box, V, unified_krav_func, p = 10, param = [], coef = 1):
    """
    Ckeck box with calculating Krawczyk evalutaion to check if it is the solution of the system, on the border of the
    solution or neigther of none of these.
    :param box: box to check
    :param V: variables for checking
    :param unified_krav_func: function for calculate Krawczyk evalutaion
    :param p: number the the iterations
    :param param: const parameteres of the sustem
    :param coef: coefficeint
    :return: "inside" if it is the solution
             "border" if it is on the border of solution
             "outside" if it doesn't have intersection with solution
    """
    V_iter = V.copy()
    Vmid = []
    for i in range(len(V)):
        Vmid.append(coef*V[i].mid())
    #print('*****')
    #print('Box')
    #print(U)
    # print('*****')
    for k in range(p):
        C = []
        for i in range(len(V_iter)):
            C.append(V_iter[i].mid())
        v_krav = unified_krav_func(box, V_iter, Vmid, C, param)  # Calculate Kravchik evaluation for u1, u2
        #print('-----')
        #print(k)
        #print("New v")
        #print(v_krav)
        #print('-----')
        #print("Old v")
        #print(V)
        # print('-----')
        check = True
        for i in range(len(V)):
            if not(v_krav[i][0].isIn(V[i])):
                check = False
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        for i in range(len(V)):
            if V[i].isNoIntersec(v_krav[i][0]):
                return 'outside'
            else:
                V_iter[i] = V[i].intersec(v_krav[i][0])  # if our evalution not fully inside, then intersect it and repeat


