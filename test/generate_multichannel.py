#!/usr/bin/env python3

import csv
import random

channels = 1000
elements = 2

data = dict()
data["x"] = list()
for i in range(elements):
    data["x"].append(i)

for i in range(channels):
    name = "value_" + str(i)
    data[name] = list()
    for j in range(elements):
        data[name].append((2*random.random())-1)

keys = data.keys()
with open('./multichannel.csv', 'w', newline='') as csvfile:
   writer = csv.writer(csvfile, delimiter = ";")
   writer.writerow(keys)
   writer.writerows(zip(*[data[key] for key in keys]))
