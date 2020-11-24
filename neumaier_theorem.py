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

    def check_box(self, ini_box):
        N = len(self.__D)
        #print("Ini box", ini_box)
        check2 = []
        check1 = []
        box_mid = []
        for box in ini_box:
            box_mid.append(box.mid())
        #print(box_mid)
        f_root_sym = self.__func.subs([(self.__U[0], box_mid[0]), (self.__U[1], box_mid[1])])
        #print(f_root)
        f_root = sym.lambdify([self.__V], f_root_sym)
        #print(self.__V)
        #print(f_root([0, 0]))
        self.__func = function_replacer(self.__func)
        f_n = sym.lambdify([self.__V, self.__U], self.__func)
        init = []
        for i in range(N):
            init.append(np.pi)
        # print(f_root_sym)
        # sym_solv = sym.nonlinsolve(f_root_sym, self.__V)
        # x, y, z = sym.symbols('x, y, z')
        # sym_solv1 = sym.nonlinsolve([sym.sin(x) - 1, sym.cos(y)], [x, y])
        # print(sym_solv1)
        result = optimize.root(f_root, init, method='anderson', tol=1e-12)
        X = -result.x
        #print(X)
        for i in range(N):
            x = ival.valueToInterval(X[i])
            if x.isIn(self.__D[i]):
                check2.append(True)
        if result.success and np.all(check2):
            check = True
        else:
            check = False
        # try:
        #     #optimize.bisect(f_root, self.__D[0], self.__D[1])
        #     optimize.fsolve(f_root,  [0, 0])
        # except:
        #     check = False
        # check1.append(self.check_zeros(f_n([self.__D[0][0]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][0]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0], self.__D[1][1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][0], self.__D[1]], [ini_box[0], ini_box[1]])))
        # check1.append(self.check_zeros(f_n([self.__D[0][1], self.__D[1]], [ini_box[0], ini_box[1]])))

        import itertools as it

        for j in range(N):
            arrays = []
            fixed = j
            for i in range(N):
                if i!=fixed:
                    arrays.append([self.__D[fixed][0], self.__D[fixed][1]])
                else:
                    arrays.append([self.__D[fixed]])
            variants = list(it.product(*arrays))
            for var in variants:
                var = list(var)
                #print(var)
                check1.append(self.check_zeros(f_n(var, [ini_box[0], ini_box[1]])))
        #print(f_root_sym)
        #if not(np.all(check1)):
            #print(ini_box)
        #print(ini_box)
        #print(check, check1)
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