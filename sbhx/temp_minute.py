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

    cur.execute("select count(*), MINUTE(STR_TO_DATE(TIME,'%Y-%m-%d %H:%i:%s')) as minute from rt \
    where CURVE_NO=2289 and VALUE=25 group by minute")
    result = cur.fetchall()
    conn.close()

    print('data query finish.')
    data=np.array(result)

    plt.plot(data[:,1], data[:,0], 'bo-', lw=2, label='告警次数')
    plt.xlabel(u'分钟', fontsize=15)
    plt.grid(True)
    plt.show()

