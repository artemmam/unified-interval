class Container:

    def __init__(self, func, iter_num, coef=1, param=[]):
        """
        :param func: numerical interval extension function
        :param iter_num: max number of the iteration for checker
        :param coef: coefficient for variating recurrent form
        :param param: the list of params for interval extension function
        """
        self.__iter_num = iter_num
        self.__func = func
        self.__coef = coef
        self.__param = param

    def calcul_ext(self, box, V):
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
    def iter_num(self):
        return self.__iter_num

    @property
    def func(self):
        return self.__func

    @property
    def coef(self):
        return self.__coef

    @property
    def param(self):
        return self.__param
