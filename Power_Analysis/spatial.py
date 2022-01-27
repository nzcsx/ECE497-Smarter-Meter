import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
from datetime import datetime, timedelta
from calendar import monthrange
import copy

import numpy as np
from sympy import *

# create the unknowns in the equation
def organize_alphabet(unknown):
    alpha = list(map(chr, range(97, 97 + unknown)))
    labels = ""
    for a in alpha:
        labels += a + ' '

    # alpha are the ascii characters while the labels are the unknowns in the equation
    return alpha, labels

# solve the equation with given amount of unknowns
def eqn_to_sol(coeff, alpha, labels, const):
    sym = [None for _ in range(len(labels))]
    sym = symbols(labels)
    exp = ''

    for i in range(len(alpha)):
        exp += str(coeff[i]) + " * sym[" + str(i) + '] + '
    exp += '('+str(const)+')'

    result = str(eval('diophantine('+exp+')'))
    result = result.replace('t_0','t')
    result = result.replace('(', '')
    result = result.replace(')', '')
    result = result.replace('{', '')
    result = result.replace('}', '')
    return result.split(", ")

# find out the possible hours in integer
def find_potential_res(sep, max_hrs):
    all_res, pos_t = [], []
    for t in range(-max_hrs, max_hrs):
        curr_res = []

        flag = True
        for q in sep:
            q = q.replace("t", str(t))
            curr_res.append(eval(q))
            if curr_res[-1]<0 or curr_res[-1]>max_hrs:
                flag = False
                break

        if flag:
            all_res.append(curr_res)
            pos_t.append(t)
    return pos_t, all_res

# calculate the number of hours in a period
def hrs_in_period(date_1, date_2):
    time_delta = (date_2 - date_1)
    total_seconds = time_delta.total_seconds()
    return round(total_seconds / 3600)

# estimate the amount of power each of the appliances used
def power_allocation(db, collection, usr_id, min_date, max_date):
    search.print_appliance_info(db = db, collection = collection, usr_id = usr_id)

    # get the appliance list
    app_list = search.search_appliance_list(db = db, collection = collection, usr_id = usr_id)

    # get power meter readings within the list
    power_readings, dates = search.search_power_reading_date(collection,
                                                             usr_id, min_date, max_date, return_string=False)
    # print(power_readings, dates)

    # find the number of hours in the period
    # max_hrs = hrs_in_period(datetime.strptime(min_date, "%b-%d-%Y %H:%M:%S"),
    #                         datetime.strptime(max_date, "%b-%d-%Y %H:%M:%S"))
    max_hrs = hrs_in_period(dates[0], dates[-1])
    # print(max_hrs)

    # find the total power consumed during the period
    power_consumed = int(float(power_readings[-1]) - float(power_readings[0])) * 1000

    hrs, unknowns = [0 for _ in range(len(app_list))], len(app_list)
    idx_incomplete, watt, app_name, consumption = [], [], [], [0 for _ in range(len(app_list))]
    for idx, app in enumerate(app_list):
        app_name.append(app[0])
        if app[-1] == 'all day':
            hrs[idx] = max_hrs
            consumption[idx] = max_hrs * app[1] * app[2]
            power_consumed -= max_hrs * app[1] * app[2] # time * wattage * number of appliances
            unknowns -= 1
        elif app[-1] == 'not in use':
            consumption[idx] = 0
            hrs[idx] = 0
            unknowns -= 1
        else:
            consumption[idx] = app[1] * app[2]
            idx_incomplete.append(idx)
            watt.append(int(app[1] * app[2]))

    #print(app_list, power_consumed)
    if power_consumed < 0:
        print("unknown power consumption")
        return []
    # special circumstances where none or only one appliance is left
    if unknowns == 0:
        return hrs
    elif unknowns == 1:
        hrs[idx_incomplete[0]] = power_consumed / (app_list[idx_incomplete[0]][1] * app_list[idx_incomplete[0]][2])
        return hrs

    # need to solve the functions
    # print(watt)
    ascii, label = organize_alphabet(unknown = unknowns)
    res_eqn = eqn_to_sol(coeff=watt, alpha=ascii, labels=label, const=-int(power_consumed))
    # print(res_eqn)

    possible_time, result = find_potential_res(res_eqn, max_hrs=max_hrs)
    # print(possible_time, result)

    # check if anything is wrong with the given information (time(often) > time(rare))
    # lazy looping through all indices
    for ii, res in enumerate(result):
        for idx, pointed_idx in enumerate(idx_incomplete):
            for idx_2 in range(idx+1, len(idx_incomplete)):
                pointed_idx_2 = idx_incomplete[idx_2]
                if app_list[pointed_idx][-1] == 'often' and app_list[pointed_idx_2][-1] == 'rare':
                    if res[idx] < res[idx_2]:
                        result[ii] = None

                if app_list[pointed_idx][-1] == 'rare' and app_list[pointed_idx_2][-1] == 'often':
                    if res[idx] > res[idx_2]:
                        result[ii] = None

    # no solution found
    result = list(filter(None, result))
    if len(result) == 0:
        print("unknown power consumption")
        return []
    else:
        # even if the more than one result is found, we leave the middle one
        # can be changed to other options
        final_sol = result[len(result)//2]

    for idx, pointed_idx in enumerate(idx_incomplete):
        hrs[pointed_idx] = final_sol[idx]
        consumption[pointed_idx] *= final_sol[idx]

    return app_name, hrs, consumption


# ap, vv = organize_alphabet(2)
# ff = [None for _ in range(2)]
# ff = symbols(vv)
# sep = eqn_to_sol([2,3], ap, vv, -5)
# print(sep)
# possible_time, result = find_potential_res(sep, max_hrs=24)
# print(possible_time, result)
