from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso, Ridge
import pymysql as db
import numpy as np

import matplotlib as mpl

if __name__ == "__main__":
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    conn = db.connect(host='localhost', user='root', passwd='liujie', db='StateGrid', port=3306, charset='utf8')
    cur = conn.cursor()

    #cur.execute("select RES_OBJ_ID,STATION_ID,SYS_OBJ_ID,PRODUCER_ID,DEV_TYPE_ID,ALARM_EMS_TIME,ALARM_EMS_TIME from restype_NE")
    cur.execute("select NE_NAME,STATION_ID,SYS_OBJ_ID,PRODUCER_ID,FROM_UNIXTIME(ALARM_EMS_TIME/1000,'%c') as month,FROM_UNIXTIME(ALARM_EMS_TIME/1000,'%H') as hour from history_alarm where PROCESS_STATE = 8 limit 1000000")
    result = cur.fetchall()
    # conn.close()
    data=np.array(result)
    dicArr=[]
    for i in range(4):
        dic={}
        xdic = data[:,i].reshape(1,-1)
        for j in range(xdic.shape[1]):
            if(xdic[0,j] not in dic):
                dic[xdic[0,j]]=dic.__len__()
        dicArr.append(dic)
    dicNeTo = []
    for i in range(1,4):
        dic={}
        xdic = data[:,:4]
        for j in range(xdic.shape[0]):
            if(dicArr[0].get(xdic[j,0]) not in dic):
                dic[dicArr[0].get(xdic[j,0])]=dicArr[i].get(xdic[j,i])
        dicNeTo.append(dic)
    numofRes = dicArr[0].__len__()
    initMatrix = np.zeros([numofRes*12*24,7])

    #print(initMatrix.shape)
    for i in range(initMatrix.shape[0]):
        initMatrix[i,0]=i%numofRes
        for j in range(1,4):
            initMatrix[i,j]=dicNeTo[j-1].get(initMatrix[i,0])
    for i in range(initMatrix.shape[0]):
        initMatrix[i, -3] = i // numofRes % 12
    for i in range(initMatrix.shape[0]):
        initMatrix[i, -2] = i // (numofRes * 12) % 24
    for k in range(data.shape[0]):
        index = dicArr[0].get(data[k,0])+(int(data[k,-2])-1)*numofRes+int(data[k,-1])*numofRes*12
        initMatrix[index,-1] = initMatrix[index,-1]+1
    # num=0
    # for i in range(initMatrix.shape[0]):
    #     if(initMatrix[i,3]!=0):
    #         num+=1
    # print(num)
    x, y = np.split(initMatrix, (6,), axis=1)
    # y_lg = np.log2(y+1)
    # num=0
    # for i in range(x.shape[0]):
    #     if(x[i,1]):
    #         num+=1
    # print(num)
    # x=x[:,(0,2,3,4,5)]
    enc = OneHotEncoder()
    x=enc.fit_transform(x)
    print(x.shape)
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    model = Ridge(alpha=5)
    # alpha_can = np.logspace(-1, 2, 5)
    # cv_model = GridSearchCV(model, param_grid={'alpha': alpha_can}, cv=5)
    print('begin train...')
    model.fit(x_train, y_train)
    #model.fit(x_train, y_train)
    # print('验证参数：\n', model.get_params())
    print("预测结果--实际结果")
    for i in range(500):
        xi=int(round(model.predict(x_test[i,:])[0,0]))
        yi=int(y_test[i,0])
        xi=0 if xi<0 else xi
        if(yi>0 or np.random.random()>0.6):
            print("  ",xi,"  --  ",yi)
    print(model.score(x_test, y_test))
    # print(model.intercept_)
    print('序号   影响系数     类型     名称或ID')
    for i in range(model.coef_.shape[1]):
        if (model.coef_[0, i] > 10 or model.coef_[0, i] < -5):
            if(i<dicArr[0].__len__()):
                print(i, model.coef_[0, i],"设备",{value: key for key, value in dicArr[0].items()}[i])
            elif(i<dicArr[0].__len__()+dicArr[1].__len__()):
                print(i, model.coef_[0, i], "站点" ,{value: key for key, value in dicArr[1].items()}[i-dicArr[0].__len__()])
            elif (i < dicArr[0].__len__() + dicArr[1].__len__()+ dicArr[2].__len__()):
                print(i, model.coef_[0, i], "系统",
                      {value: key for key, value in dicArr[2].items()}[i - dicArr[0].__len__()- dicArr[1].__len__()])
            elif (i < dicArr[0].__len__() + dicArr[1].__len__()+ dicArr[2].__len__()+ dicArr[3].__len__()):
                print(i, model.coef_[0, i], "厂家",
                      {value: key for key, value in dicArr[3].items()}[i - dicArr[0].__len__()- dicArr[1].__len__()- dicArr[2].__len__()])
            else:
                print(i,model.coef_[0, i])