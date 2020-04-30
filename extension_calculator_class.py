import numpy as np
from kravchik_operator import krawczyk_eval, derived_f, derived_recurrent_form
import sympy as sym
import interval as ival


class ExtCalcul:

    def __init__(self, f, u, v, coef=1):
        """
        :param f: system of equations
        :param u: box to check
        :param v: variables for checking
        :param coef: coefficient for varying lambda matrix
        """
        self.__f = f
        self.__u = u
        self.__v = v
        self.__coef = coef
        self.__fv = derived_f(self.f, self.v, self.u)
        self.__func = self.func_calcul()

    def calculate_extension(self):
        """
        Function for calculation interval extension
        """
        print("Not defined")

    @property
    def f(self):
        return self.__f

    @property
    def v(self):
        return self.__v

    @property
    def u(self):
        return self.__u

    @property
    def coef(self):
        return self.__coef

    @property
    def fv(self):
        return self.__fv

    @property
    def func(self):
        return self.__func

    def func_calcul(self):
        """
        Function for transformation symbolic Krawczyk operator function into numeric
        :return: numeric Krawczyk operator calculation function
        """
        c = []
        lam = []
        for i in range(len(self.v)):
            c.append(sym.symbols("c" + str(i)))
            for j in range(len(self.v)):
                lam.append(sym.symbols("lam" + str(i) + str(j)))
        return krawczyk_eval(self.f, self.u, self.v, lam, c)

    def calculate_lam(self, V, U, coef=1):
        """
        Function for calculation matrix lambda (L = (mid(F'))**-1)
        :param V: variables
        :param U: box to check
        :param coef: coefficient for varying lambda
        :return: matrix lambda
        """
        param = [U]
        FV = self.fv(V, param)
        M = np.zeros_like(FV)
        for i in range(len(FV)):
            for j in range(len(FV)):
                M[i, j] = coef*ival.valueToInterval(FV[i, j]).mid()
        M = M.astype(float)
        print(M)
        if M == 0:
            print("box", U)
            return "sing"
        else:
            return np.linalg.inv(M).reshape(len(V)*len(V))


class ClassicalKrawczykCalcul(ExtCalcul):

    def calculate_extension(self, box, V):
        """
        Function for calculation interval Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval vector
        """
        L = self.calculate_lam(V, box)
        if L == "sing":
            return "sing"
        else:
            param = [box] + [L]
            C = []
            for i in range(len(V)):
                C.append(V[i].mid())
            return np.array(self.func(V, C, param))


class BicenteredKrawczykCalcul(ExtCalcul):

    def __init__(self, f, u, v, coef = 1):
        """
        :param f: system of equations
        :param u: box to check
        :param v: variables for checking
        """
        super().__init__(f, u, v, coef)
        self.__g = self.derived_recurrent_form_calcul()

    @property
    def g(self):
        return self.__g

    def derived_recurrent_form_calcul(self):
        """
        Function for transformation symbolic derived recurrent function into numeric
        :return: numeric derived recurrent function
        """
        lam = []
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                lam.append(sym.symbols("lam" + str(i) + str(j)))
        return derived_recurrent_form(self.f, self.v, self.u, lam)

    def calcul_new_c(self, V, L, box):
        """
        Function for calculation cmin and cmax for bicentered Krawczyk
        :param V: variables for checking
        :param L: lambda-matrix
        :param box: box to check
        :return: intervals c_min and c_max
        """
        param = [box] + [L]
        new_v_matrix = self.g(V, param)
        new_v = []
        c_min = []
        c_max = []
        n = len(new_v_matrix)
        for i in range(n):
            new_v.append(new_v_matrix[i][i])
            c_min.append(0)
            c_max.append(0)
        for i in range(n):
            if new_v[i][1] <= 0:
                c_min[i] = V[i][1]
            elif new_v[i][0] >= 0:
                c_min[i] = V[i][0]
            else:
                c_min[i] = (new_v[i][1] * V[i][0] - new_v[i][0] * V[i][1]) / (new_v[i][1] - new_v[i][0])
        for i in range(n):

            if new_v[i][1] <= 0:
                c_max[i] = V[i][0]
            elif new_v[i][0] >= 0:
                c_max[i] = V[i][1]
            else:
                c_max[i] = (new_v[i][0] * V[i][0] - new_v[i][1] * V[i][1]) / (new_v[i][0] - new_v[i][1])
        return c_min, c_max

    def calculate_extension(self, box, V):
        """
        Function for calculation interval Bicentered Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval vector
        """
        L = self.calculate_lam(V, box, self.coef)
        if L == "sing":
            return "sing"
        else:
            param = [box] + [L]
            C_min, C_max = self.calcul_new_c(V, L, box)
            v_ext_min, v_ext_max = self.func(V, C_min, param), self.func(V, C_max, param)
            v_bic = []
            for i in range(len(V)):
                v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
            return np.array(v_bic).T
