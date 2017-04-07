import datetime

import pymysql as db
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# X = np.random.randint(5, size=(5, 10))
# print(X)
#
# y=np.array(['0','1','0','0','1'])
# print(y)
# clf = MultinomialNB()
# clf.fit(X, y)
# MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
# print(clf.predict(X[2:3]))
#x=[[2,-1,0,0,-1,0],[-1,3,-1,0,-1,0],[0,-1,2,-1,0,0],[0,0,-1,3,-1,-1],[-1,-1,0,-1,3,0],[0,0,0,-1,0,1]]
x=np.linspace(0.81,0.82,100)
y=x*x*x+3*x-3
plt.plot(x, y, 'bo-', lw=2)

plt.grid(True)
plt.show()