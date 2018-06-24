import json
import os

path = "dataset/"
newPath = "dataset2/"
files = os.listdir(path)
communities = json.load(open("POI_COMMUNITY_SH/community0.txt", 'r'))
keys = communities.keys()

count = 0
total = 0

for file in files:
    f = open(path+file, 'r')
    print(f)
    houses = json.load(f)
    newHouses = []

    for house in houses:
        total += 1
        try:
            name = house['community']['name'].split('(')[0]
        except:
            continue
        key = ''
        for i in keys:
            if name in i:
                key = i
                break
        if key:
            print(name)
            print(communities[key])
            house['community']['coordinate'] = communities[key]
            newHouses.append(house)
            count += 1
        else:
            print(name, 'doesn\'t match')
    f.close()
    newF = open(newPath+file, 'w')
    json.dump(newHouses, newF)
    print(count, total)
