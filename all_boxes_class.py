class AllBoxes:
    def __init__(self, method, area_points, border_points):
        self.__area_points = area_points
        self.__method = method
        self.__border_points = border_points

    @property
    def area_points(self):
        return self.__area_points

    @property
    def method(self):
        return self.__method

    @property
    def border_points(self):
        return self.__border_points