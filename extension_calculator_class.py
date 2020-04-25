import numpy as np
from kravchik_operator import krawczyk_eval, derived_F
import sympy as sym
import interval as ival
class ExtCalcul:

    def __init__(self, f, u, v, coef=1):
        """
        :param f: system of equations
        :param u: box to check
        :param v: variables for checking
        :param coef: coefficient for variating recurrent form
        """
        self.__f = f
        self.__u = u
        self.__v = v
        self.__coef = coef

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

class ClassicalKrawczykCalcul(ExtCalcul):
    def calculate_lam(self, V, U):
        """
        Produces the right-hand side of the equivalent recurrent form for the equation f(v) = 0
        :param f: old right-hand side
        :param V: variables
        :param Vmid: variables for a middle point
        :return: the recurrent right-hand side v - L(vmid)^(-1) * f(v)
        """
        param = [U]
        FV = self.__fv(V, param)
        M = np.zeros_like(FV)
        for i in range(len(FV)):
            for j in range(len(FV)):
                M[i, j] = ival.valueToInterval(FV[i, j]).mid()
        M = M.astype(float)
        return np.linalg.inv(M)


    def __init__(self, f, u, v, coef=1):
        """
        :param f: system of equations
        :param u: box to check
        :param v: variables for checking
        :param coef: coefficient for variating recurrent form
        """
        super().__init__(f, u, v, coef)
        self.__func = self.func_calcul()
        self.__fv = derived_F(self.f, self.v, self.u)

    def func_calcul(self):
        """
        Function for initializing Krawczyk evaluation
        :return: Krawczyk operator evaluation
        """
        Vmid = []
        C = []
        lam = []
        for i in range(len(self.v)):
            Vmid.append(sym.symbols("v" + str(i) + "mid"))
            C.append(sym.symbols("c" + str(i)))
            for j in range(len(self.v)):
                lam.append(sym.symbols("lam" + str(i) + str(j)))
        return krawczyk_eval(self.f, self.u, self.v, lam, C)

    def calculate_extension(self, box, V):
        """
        Function for calculation interval Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval extension with method "func" for variables "V" on box "box"
        """
        L = self.calculate_lam(V, box)
        L = L.reshape(len(V)*len(V))
        param = [box] + [L]
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        return np.array(self.__func(V, C, param))


class BicenteredKrawczykCalcul(ExtCalcul):

    def __init__(self, func, g, coef = 1):
        """
        :param func: numerical interval extension function
        :param g: numerical interval extension for derived recurrent form
        :param coef: coefficient for variating recurrent form
        """
        super().__init__(func, coef)
        self.__g = g

    @property
    def g(self):
        return self.__g

    def calcul_new_c(self, V, Vmid, box):
        """
        Function for calculation cmin and cmax for bicentered Krawczyk
        :param V: variables for checking
        :param Vmid: V middles
        :param box: box to check
        :return: intervals c_min and c_max
        """
        param = [box] + [Vmid]
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
        Function for calculation interval Krawczyk extension
        :param box: box to check
        :param V: variables for checking
        :return: interval extension with method "func" for variables "V" on box "box"
        """
        Vmid = []
        for i in range(len(V)):
            Vmid.append(self.coef * V[i].mid())
        param = [box] + [Vmid]
        C_min, C_max = self.calcul_new_c(V, Vmid, box)
        v_ext_min, v_ext_max = self.func(V, C_min, param), self.func(V, C_max, param)
        v_bic = []
        for i in range(len(V)):
            v_bic.append(v_ext_min[i][0].intersec(v_ext_max[i][0]))
        return np.array(v_bic).T
