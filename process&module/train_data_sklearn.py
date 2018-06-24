import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
#sklearn库中的普通线性模型、岭回归模型、lasso模型
from sklearn.linear_model import LinearRegression,Ridge,Lasso
#模型效果评估
from sklearn.metrics import r2_score,mean_absolute_error


if __name__ == '__main__':

	train_data=pd.read_csv('train_data.csv')
	test_data=pd.read_csv('test_data.csv')

	#划分训练集和测试集的输入输出	
	train_X = train_data.drop('average',axis=1)
	train_X = train_X.drop('price',axis=1)
	train_y = train_data['price']
	test_X = test_data.drop('average', axis=1)
	test_X = test_X.drop('price', axis=1)
	test_y = test_data['price']

	#线性模型
	line = LinearRegression()
	line.fit(train_X,train_y)
	line_y_pre=line.predict(test_X)
	plt.plot(test_y,label='True')
	plt.plot(line_y_pre,label='Line')
	plt.legend()
	plt.show() 
	line_score=r2_score(test_y,line_y_pre)
	line_error=mean_absolute_error(test_y,line_y_pre)
	print(line_score)
	print(line_error)
	print('\n')

	#岭回归模型
	ridge = Ridge()
	ridge.fit(train_X,train_y)
	ridge_y_pre=ridge.predict(test_X)
	plt.plot(test_y,label='True')
	plt.plot(ridge_y_pre,label='Ridge')
	plt.legend()
	plt.show() 
	ridge_score=r2_score(test_y,ridge_y_pre)
	ridge_error=mean_absolute_error(test_y,ridge_y_pre)
	print(ridge_score)
	print(ridge_error)
	print('\n')

	#lasso模型
	lasso = Lasso()
	lasso.fit(train_X,train_y)
	lasso_y_pre=lasso.predict(test_X)
	plt.plot(test_y,label='True')
	plt.plot(lasso_y_pre,label='Lasso')
	plt.legend()
	plt.show() 
	lasso_score=r2_score(test_y,lasso_y_pre)
	lasso_error=mean_absolute_error(test_y,lasso_y_pre)
	print(lasso_score)
	print(lasso_error)
	print('\n')


''' n
0.6969752140223003

0.6969801503067232

0.6969752635975008

'''