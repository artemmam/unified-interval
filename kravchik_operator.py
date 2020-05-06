import sympy as sym
from sympy.utilities.lambdify import implemented_function
import interval as ival
v1, v2, u1, u2, d = sym.symbols('v1, v2, u1, u2, d')


def derive_matrix(g, v):
    """
    Function for calculating partial derivative of matrix g
    :param g : array to be derived
    :param v : variables for derivative
    :return gv: derived matrix
    """
    g_v_all = []
    for i in range(len(v)):
        g_v_all.append(sym.diff(g, v[i]))  # Calculate derivative of G with respect to v
    gv = sym.Matrix()
    for i in range(len(g_v_all)):
        gv = sym.Matrix([gv, g_v_all[i]])
    gv = gv.reshape(g.shape[0], len(v)).T
    return gv


def mysin(x):
    """
    Interval sin
    :param x: interval
    :return: interval sin(x)
    """
    return ival.sin(x)


def mycos(x):
    """
    Interval cos
    :param x: interval
    :return: interval cos(x)
    """
    return ival.cos(x)


def derived_f(f, v, u):
    """
    Produce numerical derived function
    :param f: old right-hand side
    :param v: list of checking intervals
    :param u: list of fixed intervals
    :return: function of numerical derived form
    """
    param = [u]
    fv = derive_matrix(f, v)
    return sym.lambdify([v, param], fv)


def recurrent_form(f, V, lam):
    """
    Produces the right-hand side of the equivalent recurrent form for the equation f(v) = 0
    :param f: old right-hand side
    :param V: variables
    :param lam: lamda matrix
    :return: the recurrent right-hand side v - lam * f(v)
    """
    v = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
    lam = sym.Matrix([lam]).reshape(len(V), len(V))
    return v - lam * f  # Equivalent recurrent transformation


def derived_recurrent_form(f, v, u, l):
    """
    Produce derived recurrent function
    :param f: old right-hand side
    :param v: list of checking intervals
    :param u: list of fixed intervals
    :param l: lamda matrix
    :return: function of derived recurrent form
    """
    param = [u] + [l]
    g = sym.Matrix()
    f_rec = recurrent_form(f, v, l)
    for j in range(len(v)):
        g_v = derive_matrix(sym.Matrix([f_rec[j]]), v)
        g = sym.Matrix([g, g_v])
    return sym.lambdify([v, param], g)


def centered_form(f, V, C, param):
    """
    Centered interval form
    :param f: old right-hand side
    :param V: list of checking intervals
    :param C: point from interval V
    :param param: parameters
    :return: function for calculating centered interval form
    """
    g_fin = sym.Matrix()
    C = sym.Matrix([C]).reshape(len(V), len(V))
    for i in range(len(V)):
        v = sym.Matrix()
        for j in range(len(V)):
            v = v.row_insert(j, sym.Matrix([V[j]]))
        g_v = derive_matrix(sym.Matrix([f[i]]), v)
        c = C[i, ::].T
        v_c = v - c
        subsv = []
        for j in range(len(V)):
            subsv.append((V[j], c[j]))
        f_s = f.subs(subsv)
        g_eval = sym.Matrix([f_s[i]]) + g_v.T * v_c  # Classical central form
        g_fin = sym.Matrix([g_fin, g_eval])
    return sym.lambdify([V, C, param], g_fin)


def krawczyk_eval(f, u, v, l, c):

    """
    Krawczyk_evalutation function (centered form of the recurrent form of the system of the equations)
    :param f: old right-hand side
    :param u: list of fixed intervals
    :param v: list of checking intervals
    :param l: lamda matrix
    :param c: list of points in v
    :return: function of centered form from recurrent form
    """
    param = [u] + [l]
    return centered_form(recurrent_form(f, v, l), v, c, param)

