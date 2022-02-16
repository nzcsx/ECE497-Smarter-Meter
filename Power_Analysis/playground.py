import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

class Appliance():
    def __init__(self, name, domain, wattage):
        self.name = name
        self.domain = domain
        self.wattage = wattage

    def get_domain_size(self):
        return len(self.domain)

plt.style.use('seaborn-poster')

wattage = np.array([3, 5, 7])
time = np.array([1, 15, 3])
wattage_T = np.transpose(wattage)
sum = np.dot(wattage, time)

timer = [i*0.1 for i in range(240)]
print(timer)

print(np.dot(wattage, time))

appliance_list = []
appliance_list.append(Appliance(name = 'microwave', domain = [i*0.1 for i in range(120)], wattage = 3))
appliance_list.append(Appliance(name = 'fridge', domain = [i*0.1 for i in range(120, 240)], wattage = 5))
appliance_list.append(Appliance(name = 'laptop', domain = [i*0.1 for i in range(120)], wattage = 7))

for ele in appliance_list[0].domain:
    if ele * appliance_list[0].wattage > sum:
        continue

    for ele2 in appliance_list[1].domain:
        if ele * appliance_list[0].wattage + ele2 * appliance_list[1].wattage > sum:
            continue

        for ele3 in appliance_list[2].domain:
            if ele * appliance_list[0].wattage + ele2 * appliance_list[1].wattage + ele3 * appliance_list[2].wattage == sum:
                print(ele, ele2, ele3)
