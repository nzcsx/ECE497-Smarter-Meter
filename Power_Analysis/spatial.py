import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
from datetime import datetime, timedelta
from calendar import monthrange
import copy

import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates

import numpy as np
from sympy import *
from sympy.solvers.diophantine import diophantine
from sympy.solvers.diophantine.diophantine import base_solution_linear
from sympy.abc import t
import re

def organize_alphabet(unknown):
    alpha = list(map(chr, range(97, 97 + unknown)))
    labels = ""
    for a in alpha:
        labels += a + ' '
    return alpha, labels

def eqn_to_sol(coeff, alpha, labels, const):
    sym = [None for _ in range(len(labels))]
    sym = symbols(labels)
    exp = ''

    for i in range(len(alpha)):
        exp += str(coeff[i]) + "* sym[" + str(i) + '] + '
    exp += '('+str(const)+')'

    result = str(eval('diophantine('+exp+')'))
    result = result.replace('t_0','t')
    result = result.replace('(', '')
    result = result.replace(')', '')
    result = result.replace('{', '')
    result = result.replace('}', '')
    return result.split(", ")

def find_potential_res(sep):
    all_res, pos_t = [], []
    for t in range(0, 24):
        curr_res = []

        flag = True
        for q in sep:
            q = q.replace("t", str(t))
            curr_res.append(eval(q))
            if curr_res[-1]<0 or curr_res[-1]>24:
                flag = False
                break

        if flag:
            all_res.append(curr_res)
            pos_t.append(t)
    return pos_t, all_res


ap, vv = organize_alphabet(2)
ff = [None for _ in range(2)]
ff = symbols(vv)
sep = eqn_to_sol([2,3], ap, vv, -5)
print(sep)
possible_time, result = find_potential_res(sep)
print(possible_time, result)


# ap, vv = organize_alphabet(4)
# a,b,c,d = symbols(vv)
# ff = [None for _ in range(4)]
# ff = symbols(vv)
# print(ff)
# arg_l = '2*ff[0] + 3*b - 5'
# res = eval('diophantine('+arg_l+')')
# yy = str(res)
# yy = yy.replace("t_0", "f")
# yy = yy.replace("(", "")
# yy = yy.replace(")", "")
# yy = yy.replace("{", "")
# yy = yy.replace("}", "")
# sep = yy.split(", ")
#
# print(yy)
# print(sep)
