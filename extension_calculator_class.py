class Ext_calcul:

    def __init__(self, func, coef=1, param=[]):
        """
        :param func: numerical interval extension function
        :param coef: coefficient for variating recurrent form
        :param param: the list of params for interval extension function
        """
        self.__func = func
        self.__coef = coef
        self.__param = param

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

    @property
    def param(self):
        return self.__param

class Classical_Krawczyk_calcul(Ext_calcul):
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
        param_iter = self.param.copy()
        param_iter += [box] + [Vmid]
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        return self.func(V, C, param_iter)
