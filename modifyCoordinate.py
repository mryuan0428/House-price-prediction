import csv
import json
import os

path = "dataset2/"
files = [path+x for x in os.listdir(path)]
output = csv.writer(open('coordinate.csv', 'w', newline=''))

for file in files:
    with open(file, 'r') as f:
        print('reading', file)
        houses = json.load(f)
        writeList = []
        for house in houses:
            name = house['community']['name']
            lan, lng = house['community']['coordinate']
            average = house['average']
            count = 1
            flag = True
            for i in writeList:
                if i[0] == name:
                    i[3] = (i[3]*i[4]+average)/(i[4]+1)
                    i[4] += 1
                    flag = False
            if flag:
                writeList.append([name, lan, lng, average, count])
        output.writerows(writeList)


