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
    gv = gv.reshape(g.shape[0], g.shape[0]).T
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


def recurrent_form(f, V, Vmid):
    """
    Produces the right-hand side of the equivalent recurrent form for the equation f(v) = 0
    :param f: old right-hand side
    :param V: variables
    :param Vmid: variables for a middle point
    :return: the recurrent right-hand side v - L(vmid)^(-1) * f(v)
    """
    v = sym.Matrix()
    vmid = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
        vmid = vmid.row_insert(i, sym.Matrix([Vmid[i]]))
    lam = derive_matrix(f, v)  # Calculate matrix of partial derivatives of kinematic matrix
    subsv = []
    for i in range(len(v)):
        subsv.append((V[i], Vmid[i]))
    lam = lam.subs(subsv)
    lam = lam ** (-1)
    return v - lam * f  # Equivalent recurrent transformation


def centered_form(f, V, C, param):
    """
    Centered interval form
    :param f: old right-hand side
    :param V: list of checking intervals
    :param C: point from interval V
    :param param: parameters
    :return: function for calculating centered interval form
    """
    v = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
    g_v = derive_matrix(f, v) # Calculate matrix of partial derivatives of matrix g
    c = sym.Matrix()
    for i in range(len(v)):
        c = c.row_insert(i, sym.Matrix([C[i]]))
    v_c = v - c
    subsv = []
    for i in range(len(V)):
        subsv.append((V[i], C[i]))
    f = f.subs(subsv)
    g_eval = f + g_v * v_c # Classical central form
    return sym.lambdify([V, C, param], g_eval)


def krawczyk_eval(f, U, V, Vmid, C):

    """
    Krawczyk_evalutation function (centered form of the recurrent form of the system of the equations)
    :param f: old right-hand side
    :param U: list of fixed intervals
    :param V: list of checking intervals
    :param Vmid: list of mids of the V (to compute the recurrent form)
    :param C: list of point in V (mids in our case)
    :return: function of centered form from recurrent form
    """
    param = [U] + [Vmid]
    return centered_form(recurrent_form(f, V, Vmid), V, C, param)

