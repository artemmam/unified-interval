import numpy as np
from check_box import make_boxes_list
from interval_checker import classical_checker
import os
import pyautogui


class Logger:

    def __init__(self, grid, size, v_init, eps, ext_calcul, decomp = False):
        """
        :param grid: grid
        :param size: the size of the grid
        :param v_init: initial value for V
        :param eps: error
        :param ext_calcul: extension calculator class
        """
        self.__grid = grid
        self.__size = size
        self.__v_init = v_init
        self.__eps = eps
        self.__ext_calcul = ext_calcul
        self.__decomp = decomp

    def find_box(self, x, y):
        L = len(self.__v_init)
        print("\n\n\n")
        print("LOGGING")
        all_boxes = make_boxes_list(self.__grid, self.__size)
        if self.__size == 2:
            for box in all_boxes:
                if (x > box[0][0] and x<box[0][1] and y > box[1][0] and y<box[1][1]):
                    print("Box:", box)
                    break
        if self.__size == 1:
            for box in all_boxes:
                if x > box[0][0] and x<box[0][1]:
                    print("Box:", box)
                    break
        print("v_init:", self.__v_init)
        print("Lambda", self.__ext_calcul.calculate_lam(self.__v_init, box).reshape((L, L)))
        classical_checker(box, self.__v_init, self.__eps, self.__ext_calcul, log=True, decomposition=self.__decomp)
        print("-----\n\n\n")


class Neumaier_Logger(Logger):
    def __init__(self, grid, size, V, ini_value, neumaier_solver):
        """
        :param grid: uniform grid
        :param size: size of grid
        :param V: initiial V
        :param ini_value: initial value for zero-finding algorithm
        :param neumaier_solver: Neumaier solver object
        """
        self.__grid = grid
        self.__size = size
        self.__neumaier = neumaier_solver
        self.__V = V
        self.__ini_value = ini_value


    def find_box(self, x, y):
        L = len(self.__V)
        print("\n\n\n")
        print("LOGGING")
        all_boxes = make_boxes_list(self.__grid, self.__size)
        for box in all_boxes:
            if (x > box[0][0] and x<box[0][1] and y > box[1][0] and y<box[1][1]):
                print("Box:", box)
                break
        print("v_init:", self.__V)
        self.__neumaier.check_box(box, self.__ini_value, log = True)
