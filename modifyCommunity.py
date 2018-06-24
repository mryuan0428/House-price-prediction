import os, json


path = "POI_COMMUNITY_SH/"
files = [path+x for x in os.listdir(path)]
output = open(path+"community0.txt", 'w')
communities = {}
for file in files:
    tmp = open(file, 'r')
    t = tmp.readline()
    while t:
        name, lan, lng, high = t.split(',')
        communities[name] = (float(lan), float(lng))
        t = tmp.readline()
    tmp.close()
json.dump(communities, output)
output.close()
