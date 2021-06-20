import numpy as np
from kravchik_operator import krawczyk_eval, derived_f, derived_recurrent_form, centered_form, sym_derived_f, \
    function_replacer
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
        print("Jacobian")
        print(sym_derived_f(self.f, self.v, self.u))
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
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                c.append(sym.symbols("c" + str(i) + str(j)))
        return centered_form(self.f, self.v, c, self.u)

    def calculate_lam(self, V, U, coef=1):
        """
        Function for calculation matrix lambda (L = (mid(F'))**-1)
        :param V: variables
        :param U: box to check
        :return: matrix lambda
        """
        param = [U]
        #print(V, U)
        FV = self.fv(V, param)
        #print(FV)
        M = np.zeros_like(FV)
        for i in range(len(FV)):
            for j in range(len(FV)):
                M[i, j] = coef*ival.valueToInterval(FV[i, j])[1]
        M = M.astype(np.float64)
        if np.linalg.det(M) == 0:
            return np.linalg.inv(M + np.eye(len(FV))).reshape(len(V)*len(V))
        else:
            return np.linalg.inv(M).reshape(len(V)*len(V))

    def calcul_new_c(self, V, box):
        """
        Function for calculation cmin and cmax for bicentered evaluation
        :param V: variables for checking
        :param box: box to check
        :return: intervals c_min and c_max
        """
        param = [box]
        new_v = self.fv(V, param)
        new_v = new_v.reshape(len(V), len(V))
        n = len(new_v)
        c_max = np.zeros_like(new_v)
        c_min = np.zeros_like(new_v)
        for i in range(n):
            for j in range(n):
                new_v[i][j] = ival.valueToInterval(new_v[i][j])
                if new_v[i][j][1] <= 0:
                    c_min[i][j] = V[j][1]
                elif new_v[i][j][0] >= 0:
                    c_min[i][j] = V[j][0]
                else:
                    c_min[i][j] = (new_v[i][j][1] * V[j][0] - new_v[i][j][0] * V[j][1]) / (new_v[i][j][1] - new_v[i][j][0])
        for i in range(n):
            for j in range(n):
                if new_v[i][j][1] <= 0:
                    c_max[i][j] = V[j][0]
                elif new_v[i][j][0] >= 0:
                    c_max[i][j] = V[j][1]
                else:
                    c_max[i][j] = (new_v[i][j][0] * V[j][0] - new_v[i][j][1] * V[j][1]) / (new_v[i][j][0] - new_v[i][j][1])
        return c_min, c_max

    def calculated_centered_form(self, box, V, C = []):
        """
        :param box: box to check
        :param V: variables for checking
        :param C: "centers" for centered form
        :return: centered form for self.func
        """
        param = box
        C = np.array(C).reshape(len(V), len(V)).T.reshape(len(V) * len(V))
        return np.array(self.func(V, C, param))


class ClassicalKrawczykCalcul(ExtCalcul):
    def func_calcul(self):
        """
        Function for transformation symbolic Krawczyk operator function into numeric
        :return: numeric Krawczyk operator calculation function
        """
        c = []
        lam = []
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                c.append(sym.symbols("c" + str(i) + str(j)))
                lam.append(sym.symbols("lam" + str(i) + str(j)))
        return krawczyk_eval(self.f, self.u, self.v, lam, c)

    def calculate_extension(self, box, V, log = False):
        """
        Function for calculation interval Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval vector
        """
        L = self.calculate_lam(V, box, self.coef)
        param = [box] + [L]
        C = []
        for i in range(len(V)):
            for j in range(len(V)):
                C.append(V[i].mid())
        C = np.array(C).reshape(len(V), len(V)).T.reshape(len(V)*len(V))
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

    def func_calcul(self):
        """
        Function for transformation symbolic Krawczyk operator function into numeric
        :return: numeric Krawczyk operator calculation function
        """
        c = []
        lam = []
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                c.append(sym.symbols("c" + str(i) + str(j)))
                lam.append(sym.symbols("lam" + str(i) + str(j)))
        return krawczyk_eval(self.f, self.u, self.v, lam, c)

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
        new_v = self.g(V, param)
        new_v = new_v.reshape(len(V), len(V))
        n = len(new_v)
        c_max = np.zeros_like(new_v)
        c_min = np.zeros_like(new_v)
        for i in range(n):
            for j in range(n):
                if new_v[i][j][1] <= 0:
                    c_min[i][j] = V[j][1]
                elif new_v[i][j][0] >= 0:
                    c_min[i][j] = V[j][0]
                else:
                    c_min[i][j] = (new_v[i][j][1] * V[j][0] - new_v[i][j][0] * V[j][1]) / (new_v[i][j][1] - new_v[i][j][0])
        for i in range(n):
            for j in range(n):
                if new_v[i][j][1] <= 0:
                    c_max[i][j] = V[j][0]
                elif new_v[i][j][0] >= 0:
                    c_max[i][j] = V[j][1]
                else:
                    c_max[i][j] = (new_v[i][j][0] * V[j][0] - new_v[i][j][1] * V[j][1]) / (new_v[i][j][0] - new_v[i][j][1])
        return c_min, c_max

    def calculate_extension(self, box, V, log = False):
        """
        Function for calculation interval Bicentered Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval vector
        """
        L = self.calculate_lam(V, box, self.coef)
        param = [box] + [L]
        C_min, C_max = self.calcul_new_c(V, L, box)
        C_min = C_min.reshape(len(V) * len(V))
        C_max = C_max.reshape(len(V) * len(V))
        v_ext_min, v_ext_max = self.func(V, C_min, param), self.func(V, C_max, param)
        v_bic = []
        for i in range(len(V)):
            v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
        return np.array(v_bic).T

class ModernizedClassicalKrawczykCalcul(ExtCalcul):
    def calculate_lam(self, V, U, coef=1):
        """
        Function for calculation matrix lambda (L = (mid(F'))**-1)
        :param V: variables
        :param U: box to check
        :return: matrix lambda
        """
        param = [U]
        #print(V, U)
        FV = self.fv(V, param)
        #print(FV)
        M = np.zeros_like(FV)
        for i in range(len(FV)):
            for j in range(len(FV)):
                M[i, j] = coef*ival.valueToInterval(FV[i, j]).mid()
        M = M.astype(np.float64)
        if np.linalg.det(M) == 0:
            return np.linalg.inv(M + np.eye(len(FV)))
        else:
            return np.linalg.inv(M)

    def sym_R(self, V, box, log = False):
        Lam = np.array(self.calculate_lam(V, box))
        J = sym_derived_f(self.f, self.v)
        if log:
            print(np.dot(-Lam, J))
        return np.eye(len(V)) - np.dot(Lam, J)

    def calculate_extension(self, box, V, log=False):
        N = len(V)
        V = np.array(V)
        Lam = np.array(self.calculate_lam(V, box))
        C = []
        for v in V:
            C.append(v.mid())
        C = np.array(C)
        f_num = sym.lambdify([self.v, self.u], function_replacer(self.f))
        Fc = np.array(f_num(C, box))
        g = np.dot(Lam, Fc)
        J = self.fv(V, [box])
        R = np.eye(len(V)) - np.dot(Lam, J)
        if log:
            print(Lam)
            print(Fc)
            print("g", g)
            print("R", R)
        K = V.copy()
        X = V.copy()
        K_intersec = K.copy()
        for i in range(N):
            s1 = 0
            s2 = 0
            for j in range(i):
                K_intersec[j] = K[j].intersec(X[j])
                s1 += R[i, j]*(K_intersec[j] - C[j])
            for j in range(i, N):
                s2 += R[i, j]*(X[j] - C[j])
            K[i] = (C[i] - g[i] + s1 + s2)[0]
        return K
