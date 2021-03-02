import numpy as np
import sympy as sym
import interval as ival
from scipy import optimize
global boxes
boxes = []
from kravchik_operator import function_replacer

class Neumaier_solver:
    def __init__(self, func, U, V, D):
        self.__func = func
        self.__U = U
        self.__V = V
        self.__D = D

    def check_box(self, ini_box, ini_value):
        #print("Ini box", ini_box)
        N = len(self.__D)
        check = True
        check1 = []
        box_mid = []
        for box in ini_box:
            box_mid.append(box.mid())
        f_root_sym = self.__func.subs([(self.__U[0], box_mid[0]), (self.__U[1], box_mid[1])])
        f_root = sym.lambdify([self.__V], f_root_sym)
        self.__func = function_replacer(self.__func)
        f_n = sym.lambdify([self.__V, self.__U], self.__func)
        init = []
        for i in range(N):
            init.append(ini_value)
        result = optimize.root(f_root, init, method='anderson', tol=1e-12)
        X = result.x
        circle_ival = f_n(self.__D, ini_box).reshape(-1)
        #print(ini_box, circle_ival)
        for i in range(len(circle_ival)):
            if ival.Interval([0, 0]).isIn(circle_ival[i]):
                pass
                # return "border"
            else:
                #pass
                return "border"
        #print(X)
        # X1 = ival.valueToInterval(X[0])
        # X2 = ival.valueToInterval(X[1])
        # if result.success and X1.isIn(self.__D[0]) and X2.isIn(self.__D[1]):
        #     check = True
        # else:
        #     check = False
        check2 = np.full(N, False) #2-RPR
        for i in range(N):
            x = ival.valueToInterval(X[i])
            #print(x, x.isIn(self.__D[i]))
            if x.isIn(self.__D[i]):
                #check2.append(True)
                check2[i] = True
            # else:
            #     check2.append(False)
        #print(check2)
        if result.success and np.all(check2):
            check = True
        else:
            check = False
        # try:
        #     #optimize.bisect(f_root, self.__D[0], self.__D[1])
        #     optimize.fsolve(f_root,  [0, 0])
        # except:
        #     check = False
        if N ==1:
            check1.append(self.check_zeros(f_n([self.__D[0][0]], [ini_box[0], ini_box[1]])))
            check1.append(self.check_zeros(f_n([self.__D[0][1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][0], self.__D[1][0]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][1], self.__D[1][1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][0]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][0], self.__D[1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][1], self.__D[1]], [ini_box[0], ini_box[1]])))
        else:
            import itertools as it
            for j in range(N):
                arrays = []
                fixed = j
                for i in range(N):
                    if i != fixed:
                        arrays.append([self.__D[fixed][0], self.__D[fixed][1]])
                    else:
                        arrays.append([self.__D[fixed]])
                variants = list(it.product(*arrays))
                for var in variants:
                    var = list(var)
                    check1.append(self.check_zeros(f_n(var, [ini_box[0], ini_box[1]])))
        if np.all(check1) and check:
            return True
        else:
            return False

    def find_box(self, ini_box, i, ini_value):
        check = True
        # print(i)
        for box in ini_box:
            if (box[1] - box[0]) < 3:
                check = False
        if check:
            if not (self.check_box(ini_box, ini_value)):
                if i == 0:
                    box1 = [ival.Interval([ini_box[0][0], (ini_box[0][1] + ini_box[0][0]) / 2]), ini_box[1]]
                    box2 = [ival.Interval([(ini_box[0][0] + ini_box[0][1]) / 2, ini_box[0][1]]), ini_box[1]]
                    i = 1
                else:
                    # TO DO HERE
                    box1 = [ini_box[0], ival.Interval([ini_box[1][0], (ini_box[1][1] + ini_box[1][0]) / 2])]
                    box2 = [ini_box[0], ival.Interval([(ini_box[1][1] + ini_box[1][0]) / 2, ini_box[1][1]])]
                    i = 0
                # print("Enter box1")
                self.find_box(box1, i, ini_value)
                # print("Enter box2")
                self.find_box(box2, i, ini_value)
            else:
                print("Find")
                print(ini_box)
                boxes.append(ini_box)



    def check_zeros(self, a):
        a = a.reshape(-1)
        a = a.reshape(-1)
        #print("a", a)
        #a = a[0]
        tmp = True
        for i in range(len(a)):
            ai = a[i]
            #print("ai", ai)
            if (0 < ai[0] or 0 > ai[1]):
                tmp = True
                break
            else:
                tmp = False
        return tmp