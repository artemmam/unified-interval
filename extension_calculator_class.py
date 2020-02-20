class ExtCalcul:

    def __init__(self, func, coef=1):
        """
        :param func: numerical interval extension function
        :param coef: coefficient for variating recurrent form
        """
        self.__func = func
        self.__coef = coef

    def calculate_extension(self):
        """
        Function for calculation interval extension
        """
        print("Not defined")

    @property
    def func(self):
        return self.__func

    @property
    def coef(self):
        return self.__coef


class ClassicalKrawczykCalcul(ExtCalcul):

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
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        return self.func(V, C, param)


class BicenteredKrawczykCalcul(ExtCalcul):

    def __init__(self, func, g, coef=1):
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
        return self.func(V, C_min, param), self.func(V, C_max, param)
