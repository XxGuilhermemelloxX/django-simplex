# simplex_app/simplex.py
from scipy.optimize import linprog

def simplex(c, A_ub, b_ub, A_eq=None, b_eq=None, maximize=False):
    if maximize:
        c = [-ci for ci in c]  # Inverte os coeficientes da função objetivo para maximização
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
    if maximize:
        res.fun = -res.fun  # Reverte o valor da função objetivo após a otimização
    return res
