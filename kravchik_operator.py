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
    for i in range(g.shape[0]):
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


def recurent_form(f, U, V, Vmid):
    #mysin1 = implemented_function(sym.Function('mysin1'), lambda x: mysin(x))
    #mycos1 = implemented_function(sym.Function('mycos1'), lambda x: mycos(x))
    v = sym.Matrix()
    vmid = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
        vmid = vmid.row_insert(i, sym.Matrix([Vmid[i]]))
    f_v = derive_matrix(f, v)  # Calculate matrix of partial derivatives of kinematic matrix
    lam = f_v
    for i in range(len(v)):
        lam = lam.subs([(V[i], Vmid[i])])  # Calculate lambda function for recurrent transformation
    lam = lam ** (-1)
    # print(lam)
    # lam = 1 * sym.eye(f.shape[0])
    g = v - lam * f  # Equivalent recurrent transformation
    return g

def centered_form(g, U, V, Vmid, C, param = []):
    """
    Centered interval form
    :param g: recurrent form of system
    :param U: fixed parameters
    :param V: spare parameters
    :param C: point from interval V
    :param param: list of const parameters
    :return: function for calculating centered interval form
    """
    #mysin1 = implemented_function(sym.Function('mysin1'), lambda x: mysin(x))
    #mycos1 = implemented_function(sym.Function('mycos1'), lambda x: mycos(x))
    v = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
    g_v = derive_matrix(g, v) # Calculate matrix of partial derivatives of matrix g
    #print(g_v)
    c = sym.Matrix()
    for i in range(len(v)):
        c = c.row_insert(i, sym.Matrix([C[i]]))
    v_c = v - c
    for i in range(len(V)):
        g = g.subs([(V[i], C[i])])
    g_eval = g + g_v * v_c # Calculates classical Krawczyk evaluation
    #g_eval = g_eval.replace(sym.sin, mysin1)
    #g_eval = g_eval.replace(sym.cos, mycos1)
    #print(g_eval)
    print(g_eval)
    return sym.lambdify([U, V, Vmid, C, param], g_eval)


def krawczyk_evalutation(f, U, V, Vmid, C, param = []):
    return centered_form(recurent_form(f, U, V, Vmid), U, V, Vmid, C, param)


def get_unified_krav_eval(f, U, V, Vmid, C, param = []):
    """
    :param f: system of equations
    :param U: fixed parameters
    :param V: spare parameters
    :param Vmid: mids of V
    :param C: new mids of C
    :param param: list of const parameters
    :return: function for calculating Krawczyk evaluation
    """
    mysin1 = implemented_function(sym.Function('mysin1'), lambda x: mysin(x))
    mycos1 = implemented_function(sym.Function('mycos1'), lambda x: mycos(x))
    v = sym.Matrix()
    vmid = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
        vmid = vmid.row_insert(i, sym.Matrix([Vmid[i]]))
    f_v = derive_matrix(f, v) # Calculate matrix of partial derivatives of kinematic matrix
    lam = f_v
    for i in range(len(v)):
        lam = lam.subs([(V[i], Vmid[i])]) # Calculate lambda function for recurrent transformation
    lam = lam ** (-1)
    #print(lam)
    #lam = 1 * sym.eye(f.shape[0])
    g = v - lam * f # Equivalent recurrent transformation
    print(g)
    g_v = derive_matrix(g, v) # Calculate matrix of partial derivatives of matrix g
    #print(g_v)
    c = sym.Matrix()
    for i in range(len(v)):
        c = c.row_insert(i, sym.Matrix([C[i]]))
    v_c = v - c
    for i in range(len(V)):
        g = g.subs([(V[i], C[i])])
    g_eval = g + g_v * v_c # Calculates classical Krawczyk evaluation
    g_eval = g_eval.replace(sym.sin, mysin1)
    g_eval = g_eval.replace(sym.cos, mycos1)
    #print(g_eval)
    print(g_eval)
    return sym.lambdify([U, V, Vmid, C, param], g_eval)
