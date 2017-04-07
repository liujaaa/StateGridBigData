import pymysql as db
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import datetime



if __name__ == "__main__":
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    conn = db.connect(host='localhost', user='root', passwd='liujie', db='StateGrid', port=3306, charset='utf8')
    cur = conn.cursor()

    cur.execute("select TIME,VALUE from rt where CURVE_NO=2553 ")
    tempResult = cur.fetchall()
    conn.close()
    conn2 = db.connect(host='localhost', user='root', passwd='liujie', db='StateGrid', port=3306, charset='utf8')
    cur2 = conn2.cursor()
    cur2.execute("select FROM_UNIXTIME(ALARM_EMS_TIME/1000) as time from history_alarm \
    where PAR_ROOM='894EDEC2-E87B-42E9-A82E-8C24B3320FE1-84123' and \
    ALARM_EMS_TIME>1000*UNIX_TIMESTAMP('2016-09-26 00:00:00') and ALARM_EMS_TIME<1000*UNIX_TIMESTAMP('2016-11-19 23:50:00') \
    and ALARM_CAUSE in ('Underlying Resource Unavailable' ,'Communications Subsystem Failure' ,'Replaceable Unit Problem' ,\
    'Node Isolation' ,'TEMP_OVER' ,'HARD_BAD' ,'coolingSystemFailure' ,'PORT_REMOVED' ,'BUS_ERR' ,'PKG_FAIL' ,'Battery Failure' \
    ,'coolingFanFailure' ,'POWER_FAIL' ,'Replaceable Unit Missing','FAN_FAIL','SYSBUS_FAIL')")
    alarmResult = cur2.fetchall()
    conn2.close()
    print('data query finish.')
    tempData=np.array(tempResult)
    alarmData = np.array(alarmResult)
    x, y = np.split(tempData, (1,), axis=1)
    begintime = datetime.datetime.strptime('2016-09-26 00:00:00', '%Y-%m-%d %H:%M:%S')
    endtime = datetime.datetime.strptime('2016-11-19 23:50:00', '%Y-%m-%d %H:%M:%S')
    arrlenth = int((endtime-begintime).total_seconds()/60/10)
    tem = []
    alarm = []
    delta = 0
    for i in range(arrlenth):
        tem.append(0)
        alarm.append(0)
    for i in range(x.shape[0]):
        time = x[i,0]
        index = int(((time-begintime).total_seconds()/60)//10)
        if(index>=0 and index<arrlenth and int(y[i,0])>0):
            if(tem[index] != 0):
                delta += abs(tem[index]-int(y[i,0]))
                if(abs(tem[index]-int(y[i,0]))>0):
                    print(tem[index],'->',int(y[i,0]))
            tem[index] = int(y[i,0])
    tempMin=30
    tempMax=0
    numOfZero = 0
    for i in range(tem.__len__()):
        if(tem[i]<=0):
            numOfZero += 1
            tem[i]=tem[i-1]
        else:
            if(tem[i] < tempMin):
                tempMin = tem[i]
            elif(tem[i] > tempMax):
                tempMax = tem[i]
    for i in range(alarmData.shape[0]):
        time = alarmData[i, 0]
        if(type(time) is datetime.datetime):
            index = int(((time - begintime).total_seconds() / 60) // 10)
            if (index >= 0 and index < arrlenth):
                alarm[index]+=1
    # timeCount=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # alarmCount=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    timeCount=[]
    alarmCount=[]
    tempIndex = range(tempMin, tempMax+1)
    for i in tempIndex:
        timeCount.append(0)
        alarmCount.append(0)
    for i in range(arrlenth):
        temp = tem[i]
        # if(temp==0):
        #     timeCount[0]+=1
        #     alarmCount[0]+=alarm[i]
        # else:
        if(temp>0):
            index=temp-tempMin
            timeCount[index] += 1
            alarmCount[index] += alarm[i]
    print(timeCount)
    print(alarmCount)

    print(numOfZero)
    print(delta)
    timeSum=np.sum(timeCount)
    alarmSum=np.sum(alarmCount)
    timeCountNorm = np.array(timeCount)*alarmSum/timeSum
    fig=plt.figure(facecolor='w')
    ax1 = fig.add_subplot(111)
    ax1.plot(tempIndex, timeCountNorm, 'bo-', lw=2, label='时间次数')
    ax1.plot(tempIndex, alarmCount, 'ro-', lw=2, label='故障次数')
    ax1.set_xlabel(u'温度', fontsize=15)
    ax1.set_ylabel(u'次数', fontsize=15)
    # ax2 = ax1.twinx()
    # ax2.set_ylabel(u'频率', fontsize=15)
    # ax2.plot(tempIndex, (np.array(alarmCount)+10*np.ones_like(timeCountNorm))/(timeCountNorm+10*np.ones_like(timeCountNorm)), 'co--', lw=2, label='告警频率')
    # ax2.plot(tempIndex,np.ones_like(tempIndex),'k--',lw=2)
    plt.title(u'马回岭变1660SM机房温度与设备故障次数')
    ax1.legend(loc='best')
    # ax2.legend(loc='upper right')
    # num10min = []
    # for i in range(timeCount.__len__()):
    #     num10min.append((alarmCount[i]+1*alarmSum/timeSum)/(timeCount[i]+1*alarmSum/timeSum))
    # plt.plot(tempIndex, num10min, 'bo-', lw=2, label='告警次数')
    # plt.xlabel(u'温度', fontsize=15)
    plt.grid(True)
    plt.show()
