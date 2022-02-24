import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import time as t
import itertools

class Appliance():
    def __init__(self, name, domain, wattage):
        self.name = name
        self.domain = domain
        self.wattage = wattage

    def get_domain_size(self):
        return len(self.domain)

plt.style.use('seaborn-poster')

start = t.time()
wattage = np.array([3, 5, 7])
time = np.array([1, 15, 3])
wattage_T = np.transpose(wattage)
sum = np.dot(wattage, time)

timer = [i*0.1 for i in range(240)]
print(timer)

print(np.dot(wattage, time))

appliance_list = []
appliance_list.append(Appliance(name = 'microwave', domain = [i*0.5*3 for i in range(1, 120) if i*0.1*3<=sum], wattage = 3))
appliance_list.append(Appliance(name = 'fridge', domain = [i*0.5*5 for i in range(120, 239) if i*0.1*5<=sum], wattage = 5))
appliance_list.append(Appliance(name = 'laptop', domain = [i*0.5*7 for i in range(1, 120) if i*0.1*7<=sum], wattage = 7))

# Using a Python dictionary to act as an adjacency list
exp = ""
for idx,app in enumerate(appliance_list):
    exp += "appliance_list["+str(idx)+"].domain,"

func = "itertools.product(" + exp +")"
count = 0
for cell in eval(func):
    sum = 0
    for val in cell:
        sum += val

    if sum == np.dot(wattage, time):
        #print(sum)
        count += 1
print(count)

def app_time(appliance_list):
    for ele in appliance_list[0].domain:
        for ele2 in appliance_list[1].domain:
            for ele3 in appliance_list[2].domain:
                if ele + ele2 + ele3 == sum:
                    #print(ele, ele2, ele3)
                    break

#app_time(appliance_list)
def find_least_app(appliance_list):
    min = float("inf")
    appliance = None
    for app in appliance_list:
        if len(app.domain) < min:
            min = len(app.domain)
            appliance = app
    appliance_list.remove(appliance)
    return appliance, appliance_list

# print(appliance_list)
# app, app_l = find_least_app(appliance_list)
# print(app_l)


end = t.time()
print("Elapsed time:", end-start)