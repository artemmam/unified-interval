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
        f_root_sym = self.__func.subs([(self.__U[0], box_mid[0]), (self.__U[1], box_mid[1])])
        f_root = sym.lambdify([self.__V], f_root_sym)
        self.__func = function_replacer(self.__func)
        f_n = sym.lambdify([self.__V, self.__U], self.__func)
        ### Finding zero in interval evalutaions
        f_n_init = f_n(self.__D, ini_box).reshape(-1)
        C_left = []
        C_right = []
        for i in range(len(self.__D)):
            for j in range(len(self.__D)):
                C_left.append(self.__D[i][0])
                C_right.append(self.__D[i][1])
        ### Bicentered evaluation
        C_min_bicen, C_max_bicen = self.__centered_calcul.calcul_new_c(self.__D, box)
        C_min_bicen = C_min_bicen.reshape(len(self.__D) * len(self.__D))
        C_max_bicen = C_max_bicen.reshape(len(self.__D) * len(self.__D))
        f_ext_min_bicen, f_ext_max_bicen = self.__centered_calcul.calculated_centered_form(ini_box, self.__D,
                                                                                           C_min_bicen).reshape(-1), \
                                           self.__centered_calcul.calculated_centered_form(ini_box, self.__D,
                                                                                           C_max_bicen).reshape(-1)
        ### Mean-valued evaluation
        f_n_init_centered_right = self.__centered_calcul.calculated_centered_form(ini_box, self.__D, C_right).reshape(
            -1)
        f_n_init_centered_left = self.__centered_calcul.calculated_centered_form(ini_box, self.__D, C_left).reshape(-1)
        f_n_init_centered = []
        f_ext_bicen = []

        for i in range(len(f_n_init_centered_left)):
            f_n_init_centered.append(f_n_init_centered_left[i].intersec(f_n_init_centered_right[i]))
            f_ext_bicen.append(f_ext_min_bicen[i].intersec(f_ext_max_bicen[i]))
        if log:
            print("Interval evaluations:")
            print("Natural")
            print(f_n_init)
            print("Mean-valued form:")
            print(f_n_init_centered)
            print("Bicentered")
            print(f_ext_bicen)
        for i in range(len(f_n_init_centered_left)):
            if not ival.Interval([0, 0]).isIn(
                    f_n_init[i]):  # (f_n_init_centered_left[i].intersec(f_n_init_centered_right[i])):
                if log:
                    print("Out")
                return "out"
        init = []
        for i in range(N):
            init.append(ini_value)
        # Find adn check roots root
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


        ### Check zeros on borders
        if N == 1:
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
                for var in variants:
                    var = list(var)
                    check_borders.append(self.check_zeros(f_n(var, [ini_box[0], ini_box[1]])))
        if log:
            print("Check borders?", np.all(check_borders))
        if np.all(check_borders) and check_root:
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
