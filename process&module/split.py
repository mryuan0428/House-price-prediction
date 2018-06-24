import numpy as np
import pandas as pd


#数据集划分，训练集和测试集，大致各占80%和20%
def split(data):
	data_len = data['price'].count()
	sp = int(data_len*0.8)
	train_data = data[:sp]
	test_data = data[sp:]
	return train_data,test_data

if __name__ == '__main__':
	data = pd.read_csv('data_n.csv')
	train_data,test_data = split(data)
	train_data.to_csv('train_data.csv',index=False)
	test_data.to_csv('test_data.csv',index=False)

