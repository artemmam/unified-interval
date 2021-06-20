import numpy as np
import interval as ival
from kravchik_operator import derived_f, function_replacer
import sympy as sym

class HansenSenguptaSolver:
    def __init__(self, func, u, v):
        self.__func = func
        print("#####")
        print("Input system".upper())
        print("#####")
        for f in func:
            print(f)
        self.__u = u
        self.__v = v
        self.__fv = derived_f(self.func, self.v, self.u)
        self.__f_num = sym.lambdify([self.__v, self.__u], function_replacer(self.__func))

    @property
    def f(self):
        return self.__func

    @property
    def v(self):
        return self.__v

    @property
    def u(self):
        return self.__u

    @property
    def fv(self):
        return self.__fv

    @property
    def func(self):
        return self.__func

    def calculate_lam(self, V, U, coef=1):
        """
        Function for calculation matrix lambda (L = (mid(F'))**-1)
        :param V: variables
        :param U: box to check
        :return: matrix lambda
        """
        param = [U]
        FV = self.fv(V, param)
        M = np.zeros_like(FV)
        for i in range(len(FV)):
            for j in range(len(FV)):
                M[i, j] = coef*ival.valueToInterval(FV[i, j]).mid()
        M = M.astype(np.float64)
        if np.linalg.det(M) == 0:
            return np.linalg.inv(M + np.eye(len(FV)))
        else:
            return np.linalg.inv(M)

    def calculate_extension(self, box, V, log = False):
        """
        Function for calculation interval Hansen-Sengupta extension
        :param box: input box, box
        :param V: initial V, box
        :param log: turn on logging
        :return: interval vector
        """
        N = len(V)
        V = np.array(V)
        Lam = np.array(self.calculate_lam(V, box))
        C = []
        for v in V:
            C.append(v.mid())
        C = np.array(C)
        L = np.array(self.fv(V, [box]))
        f_num = sym.lambdify([self.v, self.u], function_replacer(self.f))
        for ans in self.__f_num(V, box).reshape(-1):
            if not(ival.Interval([0, 0]).isIn(ans)):
                return "out"
        Fc = np.array(f_num(C, box))
        g = np.dot(Lam, Fc).reshape(-1)
        P = np.dot(Lam, L)
        if log:
            print("P", P)
            print("g", g)
        HS = V.copy()
        Y_intersec = V.copy()
        for i in range(N):
            if log:
                print("i", i)
                print("Pii", P[i, i])
            s1 = 0
            s2 = 0
            for j in range(i):
                Y_intersec[j] = HS[j].intersec(V[j])
                s1 += P[i, j] * (Y_intersec[j] - C[j])
                if log:
                    print("j", j)
                    print(Y_intersec[j] - C[j])
                    print(s1)
            for j in range(i + 1, N):
                s2 += P[i, j] * (V[j] - C[j])
                if log:
                    print("j", j)
                    print(V[j] - C[j])
                    print(s2)
            if log:
                print("Up", g[i] + s1 + s2)
                print("Down", P[i, i])
            HS[i] = C[i] - (g[i] + s1 + s2)/P[i, i]
        return HS