import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.linear_model._stochastic_gradient import SGDRegressor
from sklearn.ensemble import VotingRegressor
from sklearn import metrics
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import BaggingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
import joblib
import math


# This program trains machine learning model
# Expected Input: original data for training
# Expected Output: Mahcine learning models for each alorightm, and thier prediction location accordingly.



def returnPred(lat,lng,reg):
    sample = [lat,lng]
    sample = np.array(sample).reshape(1, -1)
    sample=pd.DataFrame(sample)
    sample.columns=['gpslat','gpslng']
    return reg.predict(sample)


rtkSet=pd.read_csv('./data/gpsOutput12.csv',nrows = 1000)
rtkSet=rtkSet[1:1000]
rtkSet=rtkSet.rename(columns={"lat":"rtklat","lng":"rtklng"})
rtkSet=rtkSet.dropna()
print(rtkSet.describe())



gpsSet=pd.read_csv('./data/rtkOutput12.csv',nrows = 1000)
gpsSet=gpsSet.rename(columns={"lat":"gpslat","lng":"gpslng"})
gpsSet=gpsSet.dropna()
dataSet=pd.concat([rtkSet,gpsSet],axis=1)
dataSet=dataSet.dropna()
print(dataSet.describe())


# perform train-test set split
# split to 20% testing and 80% training

feature_train=dataSet.drop(['rtklat','rtklng'],axis=1)
label_train=dataSet.drop(['gpslat','gpslng'],axis=1)

################################################################################### 13 or 6
rtkSet=pd.read_csv('./data/gpsOutput13.csv',nrows = 1000)
rtkSet=rtkSet.rename(columns={"lat":"rtklat","lng":"rtklng"})
rtkSet=rtkSet[1:200] #1:200
rtkSet=rtkSet.dropna()
print(rtkSet.describe())



gpsSet=pd.read_csv('./data/rtkOutput13.csv',nrows = 1000)
gpsSet=gpsSet.rename(columns={"lat":"gpslat","lng":"gpslng"})
gpsSet=gpsSet.dropna()
dataSet=pd.concat([rtkSet,gpsSet],axis=1)
dataSet=dataSet.dropna()
print(dataSet.describe())


# perform train-test set split
# split to 20% testing and 80% training

feature_test=dataSet.drop(['rtklat','rtklng'],axis=1)
label_test=dataSet.drop(['gpslat','gpslng'],axis=1)


rf_reg = RandomForestRegressor(n_estimators=500,random_state=0,max_leaf_nodes=600,max_features='sqrt',criterion='absolute_error',min_impurity_decrease=0,n_jobs=-1)


lnr_reg=LinearRegression(fit_intercept=True)
knn_reg=KNeighborsRegressor()
dt_reg=DecisionTreeRegressor()


x_data=[]
y_data=[]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', 'r', 'b']



# train regressors
print('Ground RMSE is: '+str(np.sqrt(metrics.mean_squared_error(label_test, feature_test))))
x_data.append("Ground Val")
y_data.append(np.sqrt(metrics.mean_squared_error(label_test, feature_test)))


for reg in(lnr_reg,dt_reg,knn_reg):
    reg.fit(feature_train,label_train)
    label_pred=reg.predict(feature_test)
    print(reg.__class__.__name__+' RMSE is: '+str(np.sqrt(metrics.mean_squared_error(label_test, label_pred))))
    label_pred = pd.DataFrame(np.squeeze(label_pred),columns =['lat','lng'])
    label_pred.to_csv('./data/'+reg.__class__.__name__+'PredictLocation.csv')

    x_data.append(reg.__class__.__name__)
    y_data.append(np.sqrt(metrics.mean_squared_error(label_test, label_pred)))

    joblib.dump(reg, reg.__class__.__name__+'.model')

print(y_data)
bars=plt.bar(x_data, y_data,color=colors,alpha=0.7)
plt.xlabel("RMSE Type", fontdict={'size': 8})
plt.ylabel("Val", fontdict={'size': 8})
plt.xticks(rotation=-20)
plt.title("RMSE Comparsions")
plt.legend(loc="best",fontsize=12)
plt.show()












#lnr_reg.fit(feature_train,label_train)
#label_pred=lnr_reg.predict(feature_test)
#print(returnPred(-31.976081666666666,115.81476916666666,rf_reg)[0][0])
#print(lnr_reg.__class__.__name__+' RMSE is: '+str(np.sqrt(metrics.mean_squared_error(label_test, label_pred))))
#label_pred = pd.DataFrame(np.squeeze(label_pred),columns =['lat','lng'])
#label_pred=label_pred['lat','lng']
#label_pred.to_csv('./data/predictLocation.csv')
#joblib.dump(lnr_reg, 'rf_reg.model')
#lnr_reg = joblib.load('rf_reg.model')




