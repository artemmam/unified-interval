import numpy as np
import sympy as sym
import interval as ival
from scipy import optimize
global boxes
boxes = []

class Neumaier_solver:
    def __init__(self, func, U, V, D):
        self.__func = func
        self.__U = U
        self.__V = V
        self.__D = D

    def check_box(self, ini_box):
        #print("Ini box", ini_box)
        N = len(self.__D)
        check = True
        check1 = []
        box_mid = []
        for box in ini_box:
            box_mid.append(box.mid())
        f_root_sym = self.__func.subs([(self.__U[0], box_mid[0]), (self.__U[1], box_mid[1])])
        #print(f_root)
        f_root = sym.lambdify([self.__V], f_root_sym)
        #print(self.__V)
        #print(f_root([0, 0]))
        f_n = sym.lambdify([self.__V, self.__U], self.__func)
        init = []
        for i in range(N):
            init.append(5)
        result = optimize.root(f_root, init, method='anderson', tol=1e-12)
        X = result.x
        #print(X)
        X1 = ival.valueToInterval(X[0])
        X2 = ival.valueToInterval(X[1])
        if result.success and X1.isIn(self.__D[0]) and X2.isIn(self.__D[1]):
            check = True
        else:
            check = False
        # try:
        #     #optimize.bisect(f_root, self.__D[0], self.__D[1])
        #     optimize.fsolve(f_root,  [0, 0])
        # except:
        #     check = False
        # check1.append(self.check_zeros(f_n([self.__D[0][0], self.__D[1][0]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][1], self.__D[1][1]], [ini_box[0], ini_box[1]])))
        check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][0]], [ini_box[0], ini_box[1]])))
        check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][1]], [ini_box[0], ini_box[1]])))
        check1.append(self.check_zeros(f_n([self.__D[0][0], self.__D[1]], [ini_box[0], ini_box[1]])))
        check1.append(self.check_zeros(f_n([self.__D[0][1], self.__D[1]], [ini_box[0], ini_box[1]])))
        #print(f_root_sym)
        #print(check1, check)
        if np.all(check1) and check:
            return True
        else:
            return False

    def find_box(self, ini_box, i):
        check = True
        # print(i)
        for box in ini_box:
            if (box[1] - box[0]) < 0.01:
                check = False
        if check:
            if not (self.check_box(ini_box)):
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
                self.find_box(box1, i)
                # print("Enter box2")
                self.find_box(box2, i)
            else:
                # print("Find")
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