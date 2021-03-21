import numpy as np
from check_box import make_boxes_list
from interval_checker import classical_checker
import os
import pyautogui


class Logger:

    def __init__(self, dim, size, v_init, eps, ext_calcul):
        """
        :param f: system of equations
        :param u: box to check
        :param v: variables for checking
        :param coef: coefficient for varying lambda matrix
        """
        self.__dim = dim
        self.__size = size
        self.__v_init = v_init
        self.__eps = eps
        self.__ext_calcul = ext_calcul

    def find_box(self, x, y):
        L = len(self.__v_init)
        print("\n\n\n")
        print("LOGGING")
        all_boxes = make_boxes_list(self.__dim, self.__size)
        for box in all_boxes:
            if (x > box[0][0] and x<box[0][1] and y > box[1][0] and y<box[1][1]):
                print("Box:", box)
                break
        print("v_init:", self.__v_init)
        print("Lambda", self.__ext_calcul.calculate_lam(self.__v_init, box).reshape((L, L)))
        classical_checker(box, self.__v_init, self.__eps, self.__ext_calcul, log=True)
        print("-----\n\n\n")


class Neumaier_Logger(Logger):
    def __init__(self, dim, grid, size, V, ini_value, neumaier_solver):

        self.__dim = dim
        self.__grid = grid
        self.__size = size
        self.__neumaier = neumaier_solver
        self.__V = V
        self.__ini_value = ini_value


    def find_box(self, x, y):
        L = len(self.__V)
        print("\n\n\n")
        print("LOGGING")
        all_boxes = make_boxes_list(self.__grid, self.__dim)
        for box in all_boxes:
            if (x > box[0][0] and x<box[0][1] and y > box[1][0] and y<box[1][1]):
                print("Box:", box)
                break
        print("v_init:", self.__V)
        self.__neumaier.check_box(box, self.__ini_value, log = True)


