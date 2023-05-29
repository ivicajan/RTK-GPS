import pandas as pd
import matplotlib.pyplot as plt
from math import sin, asin, cos, radians, fabs, sqrt
from scipy.spatial.distance import cdist


# This program is used for draw graphics using the positioning data provided


 
EARTH_RADIUS = 6371.137*10000 # in cm
 
 
def hav(theta):
    s = sin(theta / 2)
    return s * s
 
def get_distance_hav(lat0, lng0, lat1, lng1):
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))      # cm
    return distance

def processMultiToDistance(testSets):
    maxlatList=[]
    maxlngList=[]
    minlatList=[]
    minlngList=[]
    for testSet in testSets:
        maxlatList.append(testSet['lat'].max())
        maxlngList.append(testSet['lng'].max())
        minlatList.append(testSet['lat'].min())
        minlngList.append(testSet['lng'].min())
    minlat=min(minlatList)
    minlng=min(minlngList)
    for testSet in testSets:
        for row_index, row in testSet.iterrows():
            temprowlat=row['lat']
            temprowlng=row['lng']
            row['lat']=get_distance_hav(minlat,minlng,temprowlat,minlng)
            row['lng']=get_distance_hav(minlat,minlng,minlat,temprowlng)



# round: 6, when the board is set as stationary

roundName='13'
gpsTestData=pd.read_csv('./data/rtkOutput'+roundName+'.csv')
rtkTestData=pd.read_csv('./data/gpsOutput'+roundName+'.csv')
roundName='12'
gpsTrainData=pd.read_csv('./data/rtkOutput'+roundName+'.csv')
rtkTrainData=pd.read_csv('./data/gpsOutput'+roundName+'.csv')
roundName='6'
gpsGroundData=pd.read_csv('./data/rtkOutput'+roundName+'.csv')
rtkGroundData=pd.read_csv('./data/gpsOutput'+roundName+'.csv')
#gpsGroundData=gpsGroundData[100:] # drop first 100 rows for dropping warm up procedure
#rtkGroundData=rtkGroundData[100:]


lnrPredictData=pd.read_csv('./data/LinearRegressionPredictLocation.csv')
lnrPredictData=lnrPredictData[['lat','lng']]

knnPredictData=pd.read_csv('./data/KNeighborsRegressorPredictLocation.csv')
knnPredictData=knnPredictData[['lat','lng']]

dtPredictData=pd.read_csv('./data/DecisionTreeRegressorPredictLocation.csv')
dtPredictData=dtPredictData[['lat','lng']]


processMultiToDistance([gpsGroundData,rtkGroundData])


#processMultiToDistance([gpsTestData,rtkTestData,lnrPredictData])
#processMultiToDistance([gpsTestData,rtkTestData,gpsTrainData,rtkTrainData])

processMultiToDistance([gpsTrainData, rtkTrainData, gpsTestData,rtkTestData,lnrPredictData, knnPredictData, dtPredictData])

#plt.scatter(gpsGroundData['lng'],gpsGroundData['lat'], label="gps positioning data")
#plt.scatter(rtkGroundData['lng'],rtkGroundData['lat'], label="rtk positioning data")

#print(rtkGroundData.describe())
#print(gpsGroundData.describe())

plt.scatter(gpsTrainData['lng'],gpsTrainData['lat'], s=10,label="gps train data")
plt.scatter(rtkTrainData['lng'],rtkTrainData['lat'], s=10,alpha=0.5,label="rtk train data")
plt.scatter(gpsTestData['lng'],gpsTestData['lat'], s=10,label="gps validation data")
plt.scatter(rtkTestData['lng'],rtkTestData['lat'], s=10,alpha=0.5,label="rtk validation data")
plt.scatter(lnrPredictData['lng'],lnrPredictData['lat'], s=10,label="linear regressor data")
plt.scatter(knnPredictData['lng'],knnPredictData['lat'], s=10,label="knn regressor data")
plt.scatter(dtPredictData['lng'],dtPredictData['lat'], s=10,label="decision tree regressor data")



#plt.xlabel("lat")
#plt.ylabel("lng")

plt.xlabel("distance - x (cm)")
plt.ylabel("distance - y (cm)")

plt.title("Prediction Result Overview")
plt.legend(loc="best",fontsize=12)

plt.show()

#plt.scatter(testSet['lat'],testSet['lng'])
#plt.show()