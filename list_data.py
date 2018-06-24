# -*- coding: utf-8 -*-


import collections
import json
import os
import sys


dataset = collections.defaultdict(set)
for file in os.listdir('./data'):
    if os.path.splitext(file)[1] != '.json':    continue
    with open(f'./data/{file}', 'r') as file:
        data = json.load(file)
        for item in data:
            for key, value in item.items():
                dataset[key].add(value)


# import pprint
print(dataset['小区介绍'])
# print(list(map(lambda x: x.strip('元/平米'), dataset['均价'])))
# for key, value in dataset.items():
#     if len(value) < 20:
#         print(key, value)
#     else:
#         print(key, f'{len(value)}项')
