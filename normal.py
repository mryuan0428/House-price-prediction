#-*-coding:utf-8-*-
import csv
import sys
import pandas as pd
import codecs
from sklearn import preprocessing

if __name__ == '__main__':

    data = pd.read_csv('data_r.csv')

    #待归一化的属性
    numeric_attrs = ['average','coordinate_x',
            	        'coordinate_y', 'decoration_condition','deed',
            	        'elevator', 'facility0', 'facility1', 'facility2',
            	        'facility3', 'facility4', 'facility5','level',
            	        'total', 'framework','house_term',
            	        'ownership','purpose','apt','lift','district',
            	        'rights','scale','structure','bath','kitchen', 'room',
            	        'saloon']
    for i in numeric_attrs: 
        scaler = preprocessing.StandardScaler()
        data[i] = scaler.fit_transform(data[i].as_matrix().reshape(-1, 1))

    data.to_csv('data_n.csv',index=False)