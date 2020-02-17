class Ext_calcul:

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


class Classical_krawczyk_calcul(Ext_calcul):
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
