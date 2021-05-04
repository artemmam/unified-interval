import numpy as np
import sympy as sym
import interval as ival
from scipy import optimize
global boxes
boxes = []
from kravchik_operator import function_replacer, centered_form
from extension_calculator_class import ExtCalcul

class Neumaier_solver:
    def __init__(self, func, U, V, D):
        self.__func = func
        print("#####")
        print("Input system".upper())
        print("#####")
        for f in func:
            print(f)
        self.__U = U
        self.__V = V
        self.__D = D
        self.__centered_calcul = ExtCalcul(self.__func, self.__U, self.__V)

    def check_box(self, ini_box, ini_value, log = False):
        """
        :param ini_box: checked box
        :param ini_value: starting value for root-finding
        :return: "in" -- the box is inside, "out" -- the box is outside, "border" -- the box is on the border
        """
        N = len(self.__D)
        check_borders = []
        box_mid = []
        for box in ini_box:
            box_mid.append(box.mid())
        subsv = []
        for j in range(len(self.__U)):
            subsv.append((self.__U[j], box_mid[j]))
        f_root_sym = self.__func.subs(subsv)
        f_root = sym.lambdify([self.__V], f_root_sym)
        self.__func = function_replacer(self.__func)
        f_n = sym.lambdify([self.__V, self.__U], self.__func)
        f_n_init = f_n(self.__D, ini_box).reshape(-1)
        C_left = []
        C_right = []
        for i in range(len(self.__D)):
            for j in range(len(self.__D)):
                C_left.append(self.__D[i][0])
                C_right.append(self.__D[i][1])
        if log:
            print("Interval evaluations:")
            print("Natural")
            print(f_n_init)
        for i in range(len(f_n_init)):
            if not ival.Interval([0, 0]).isIn(f_n_init[i]):
                if log:
                    print("Out")
                return "out"
        init = []
        for i in range(N):
            init.append(ini_value)
        result = optimize.root(f_root, init, method='anderson', tol=1e-12)
        X = result.x
        check_in_roots = []
        for i in range(N):
            x = ival.valueToInterval(abs(X[i]))
            if x.isIn(self.__D[i]):
                check_in_roots.append(True)
        if result.success and np.all(check_in_roots):
            check_root = True
        else:
            check_root = False
        if log:
            print("Find root?", check_root)
        if N == 1 and len(self.__U) == 1:
            check_borders.append(self.check_zeros(f_n([self.__D[0][0]], [ini_box])))
            check_borders.append(self.check_zeros(f_n([self.__D[0][1]], [ini_box])))
        elif N == 1:
            check_borders.append(self.check_zeros(f_n([self.__D[0][0]], [ini_box[0], ini_box[1]])))
            check_borders.append(self.check_zeros(f_n([self.__D[0][1]], [ini_box[0], ini_box[1]])))
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
                if log:
                    print(variants)
                for var in variants:
                    var = list(var)
                    check_borders.append(self.check_zeros(f_n(var, [ini_box[0], ini_box[1]])))
        if log:
            print("Check borders?", check_borders)
        if check_root and np.all(check_borders):
            if log:
                print("Inside")
            return "in"
        else:
            if log:
                print("Border")
            return "border"

    def check_zeros(self, a):
        a = a.reshape(-1)
        a = a.reshape(-1)
        tmp = True
        for i in range(len(a)):
            ai = a[i]
            if (0 < ai[0] or 0 > ai[1]):
                tmp = True
                break
            else:
                tmp = False
        return tmp
