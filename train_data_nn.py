import pandas as pd
from sklearn.datasets import load_boston
from keras.layers import Dense,Dropout,Activation,Input
from keras.models import Sequential,Model
from numpy import *
from keras import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score,mean_absolute_error

#神经网络模型构建
def make_model(InputSize):
    model=Sequential()
    model.add(Dense(units=100,activation='relu',input_shape=(InputSize,)))
    model.add(Dropout(0.05))
    model.add(Dense(units=80,activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(units=1,activation=None))
    model.compile(loss='mean_squared_error',optimizer='adam',metrics=[metrics.mae])
    print(model.summary())
    return model

if __name__ == '__main__':

    #划分训练集和测试集的输入输出 
    df_train=pd.read_csv('train_data.csv')
    df_test=pd.read_csv('test_data.csv')
    X_train = df_train.drop('average',axis=1)
    X_train = X_train.drop('price',axis=1)
    y_train = df_train['price']
    X_test = df_test.drop('average', axis=1)
    X_test = X_test.drop('price', axis=1)
    y_test = df_test['price']

    model=make_model(27)

    #训练模型并保存为module.h5
    #model.fit(X_train,y_train,batch_size=150,epochs=200,verbose=1,validation_data=(X_test,y_test),shuffle=True)
    #model.save_weights('module.h5')

    #加载已保存的模型
    model.load_weights('module.h5',by_name=False)

    #预测并评估结果
    pred=model.predict(X_test)
    plt.plot(y_test,label='True')
    plt.plot(pred,label='NN')
    plt.legend()
    plt.show() 
    score=r2_score(y_test,pred)
    error=mean_absolute_error(y_test,pred)
    print(score)
    print(error)

'''
R^2

0.728964325027

数据归一化-->

0.748450522912

添加dropout层-->

best
0.75180572067

'''