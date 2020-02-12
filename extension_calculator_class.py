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

    def calcul_ext(self, box, V):
        """
        Function for calculation interval extension
        :param box: box to check
        :param V: variables for checking
        :return: interval extension with method "func" for variables "V" on box "box"
        """
        Vmid = []
        for i in range(len(V)):
            Vmid.append(self.__coef * V[i].mid())
        param_iter = self.__param.copy()
        param_iter += [box] + [Vmid]
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        return self.__func(V, C, param_iter)

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
    def calcul_ext(self, box, V):
        """
        Function for calculation interval extension
        :param box: box to check
        :param V: variables for checking
        :return: interval extension with method "func" for variables "V" on box "box"
        """
        Vmid = []
        for i in range(len(V)):
            Vmid.append(self.__coef * V[i].mid())
        param_iter = self.__param.copy()
        param_iter += [box] + [Vmid]
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        return self.__func(V, C, param_iter)