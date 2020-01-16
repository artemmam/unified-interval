import interval as ival
import inspect


def unified_krav_eval(U, Vin, unified_krav_func, p=10, param = [], coef = 1):
    V = []
    for i in range(len(Vin)):
        V.append(ival.Interval([Vin[i][0], Vin[i][1]]))
    Vmid = []
    for i in range(len(V)):
        Vmid.append(coef*V[i].mid())
    #print('Box')
    #print(U)
    for k in range(p):
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        v_krav = unified_krav_func(U, V, Vmid, C, param)  # Calculate Kravchik evaluation for u1, u2
        #print(k)
        #print('-----')
        #print("New v")
        #print(v_krav)
        #print('-----')
        #print("Old v")
        #print(V)
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
                V[i].intersec(v_krav[i][0])  # if our evalution not fully inside, then intersect it and repeat


