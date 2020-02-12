class Container:

    def __init__(self, func, iter_num, coef=1, param=[], checker_param = [] ):
        self.__iter_num = iter_num
        self.__func = func
        self.__coef = coef
        self.__param = param
        self.__checker_param = checker_param

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

    @property
    def checker_param(self):
        return self.__checker_param
