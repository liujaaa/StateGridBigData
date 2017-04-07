import pymysql as db
import numpy as np
from sklearn.model_selection import train_test_split

import matplotlib as mpl

from sklearn.naive_bayes import MultinomialNB



if __name__ == "__main__":
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    conn = db.connect(host='localhost', user='root', passwd='liujie', db='StateGrid', port=3306, charset='utf8')
    cur = conn.cursor()

    cur.execute("select RES_OBJ_ID,PRODUCER_ID,DEV_TYPE_ID,RES_TYPE,ALARM_CAUSE,ALARM_LEVEL,IS_DAMAGE,ROOT_STATUS,(PROCESS_STATE = 8) as remark from history_alarm_random where PROCESS_STATE>0")
    result = cur.fetchall()
    # conn.close()
    data=np.array(result)
    print(data.shape)
    x, y = np.split(data, (8,), axis=1)
    dicArr=[]
    for i in range(8):
        dic={}
        xdic = x[:,i].reshape(1,-1)
        for j in range(xdic.shape[1]):
            if(xdic[0,j] not in dic):
                dic[xdic[0,j]]=dic.__len__()
        dicArr.append(dic)
    xp = np.random.randint(5, size=(x.shape[0], 8))
    for i in range(8):
        for j in range(x.shape[0]):
            xp[j,i]=int(dicArr[i][x[j,i]])
    y=y[:,0]
    x_train, x_test, y_train, y_test = train_test_split(xp, y, test_size=0.1, random_state=1)
    # x=x[:,4:]
    # l=int(0.0*x.shape[0])
    # r = int(0.5 * x.shape[0])
    # m = int(0.7 * x.shape[0])
    # x_train=xp[:r,:]
    # x_test=xp[m:,:]
    # y_train=y[:r,0]
    # y_test=y[m:,0]
    MNB = MultinomialNB(alpha=1.0)

    print(x_train)
    model = MNB.fit(x_train, y_train)
    y_test_hat = model.predict_log_proba(x_test)[:,1]     # 测试数据
    y_test = y_test.reshape(-1)
    # print(y_test_hat[:100])
    # print(y_test[:100])
    decision = np.log2(0.5)
    result = (y_test=='0')&(y_test_hat < decision)   # True则预测正确，False则预测错误
    result1 = y_test=='0'
    result2 = (y_test == '1') & (y_test_hat >= decision)  # True则预测正确，False则预测错误
    result3 = y_test == '1'
    #result0 =  (y_test_hat == y_test)
    acc = np.mean(result)/np.mean(result1)
    acc2 = np.mean(result2) / np.mean(result3)
    print('无故障准确度: %.2f%%' % (100 * acc),'\n',np.sum(result),'/',np.sum(result1))
    print('故障准确度: %.2f%%' % (100 * acc2),'\n',np.sum(result2),'/',np.sum(result3))
    #print('总准确度: %.2f%%' % (100 * np.mean(result0)))