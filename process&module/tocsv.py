#-*-coding:utf-8-*-
import csv
import sys
import pandas as pd
import codecs
from dataset import dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing

#检查属性是否满足要求并过滤离群点
def check(line):
	if ('average' in line.keys() and 'community' in line.keys() and 'decoration' in line.keys() and 'deed' in line.keys()
	   and 'elevator' in line.keys() and 'facility' in line.keys() and 'floor' in line.keys() and 'framework' in line.keys()
	   and 'house_term' in line.keys() and 'ownership' in line.keys() and 'price' in line.keys() and 'purpose' in line.keys()
	   and 'ratio'in line.keys() and 'region' in line.keys()and 'rights' in line.keys()and 'scale' in line.keys() and 'structure' in line.keys()
	   and 'type' in line.keys()):
		if ('coordinate' in line['community'].keys() and 'condition' in line['decoration'].keys() and 
			'level' in line['floor'].keys() and 'total' in line['floor'].keys() and 'apt' in line['ratio'].keys() and 
			'lift' in line['ratio'].keys() and 'district' in line['region'].keys() and 'bath' in line['type'].keys() and 
			'kitchen'in line['type'].keys() and 'room'in line['type'].keys() and 'saloon' in line['type'].keys()):
			if (line['average']>0 and len(line['community']['coordinate'])>0 and len(line['facility'])>0 and 
				line['average']<190000 and line['scale']<3000 and line['ratio']['apt']<50 and line['ratio']['lift']<10 ):
				return 1
			else: return 0
		else: return 0
	else: return 0

#提取数据写入csv文件
def trans(path):
    data = dataset()
    csvfile = open(path+'.csv', 'a+', newline='') 
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    flag = True
    for line in data:
        if flag:
            keys = ['average','coordinate_x',
            	        'coordinate_y', 'decoration_condition','deed',
            	        'elevator', 'facility0', 'facility1', 'facility2',
            	        'facility3', 'facility4', 'facility5','level',
            	        'total', 'framework','house_term',
            	        'ownership','price','purpose','apt','lift','district',
            	        'rights','scale','structure','bath','kitchen', 'room',
            	        'saloon']
            writer.writerow(keys) # 将属性列表写入csv中
            flag = False
        # 将数据一次一行的写入csv中
        if check(line)==1:
        	values = [line['average'],line['community']['coordinate'][0],
            		  line['community']['coordinate'][1],line['decoration']['condition'],line['deed'],
            		  line['elevator'],line['facility'][0],line['facility'][1],line['facility'][2],
            		  line['facility'][3],line['facility'][4],line['facility'][5],line['floor']['level'],
            		  line['floor']['total'],line['framework'],line['house_term'],
            		  line['ownership'],line['price'],line['purpose'],line['ratio']['apt'],line['ratio']['lift'],
            		  line['region']['district'],line['rights'],line['scale'],line['structure'],line['type']['bath'],
            		  line['type']['kitchen'],line['type']['room'],line['type']['saloon']]
        	writer.writerow(values)
    csvfile.close()

#使用随机森林预测补全unknown值
def fill_unknown_with_RS(data):
    #带预测unknown值的属性
    attrs = ['decoration_condition', 'elevator', 'ownership','framework']

    for i in attrs:     
        test_data = data[data[i] == -1]    #测试集
        testX = test_data.drop(attrs, axis=1)     #测试集输入,剔掉待预测属性
        train_data = data[data[i] != -1]   #训练集
        trainY = train_data[i]                    #训练集的输出
        trainX = train_data.drop(attrs, axis=1)   #训练集的输入
        forest = RandomForestClassifier(n_estimators=100)
        forest = forest.fit(trainX, trainY.astype(int))
        predictY = forest.predict(testX).astype(int)
        test_data[i] = pd.DataFrame(predictY,index=testX.index)
        data = pd.concat([train_data, test_data])
    return data

if __name__ == '__main__':

    trans('data_c')
    data = pd.read_csv('data_c.csv')
    data = fill_unknown_with_RS(data)

    data.to_csv('data_r.csv',index=False)
