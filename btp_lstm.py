import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.dates as md
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics.regression import r2_score, mean_squared_error
from datetime import datetime,time,date 
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)


 #read the dataset
data = pd.read_csv('finalDataForSampleEdgeSorted.csv')

 #eliminate data points having duration > 100 and duration < 5

data = data.drop(data.loc[data['duration']>100].index)
data = data.drop(data.loc[data['duration']<5].index)

print(data['duration'].describe())

fmt = '%Y-%m-%d %H:%M:%S.%f'

res = []
X = []
i = 0
j = 0
while i < len(data):
	lastTime = datetime.strptime(data['timestamp'][data.index[i]], fmt)
	j = i 
	temp = []
	temp.append(data['duration'][data.index[j]])
	j = j+1
	while j < len(data):
		tstamp1 = datetime.strptime(data['timestamp'][data.index[j]], fmt)
		if math.floor(((tstamp1 - lastTime).seconds) / 60) <= 15:
			temp.append(data['duration'][data.index[j]])
			j = j + 1
		else:
			break
	i = j
	s = 0.0
	for k in range(len(temp)):
		s = s + temp[k]
	res.append(s/(1.0*len(temp)))

res = [i for i in res if i <= 50]

# plt.plot(res[:200])
# plt.show()
print(len(res))


res = np.array(res)
res = res.reshape((-1,1))



scaler = MinMaxScaler(feature_range=(0,1))
res = scaler.fit_transform(res)



train_size = int(len(res) * 0.80) #80% of dataset is taken as training set
test_size = len(res) - train_size

print(res.shape)
print(train_size)

train,test = res[0:train_size,:],res[train_size:,:]

trainX,trainY = create_dataset(train,12)
testX,testY = create_dataset(test,12)

print(trainX.shape,trainY.shape)
print(testX.shape,testY.shape)



trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], 1))
testX = testX.reshape((testX.shape[0], testX.shape[1], 1))
look_back = 12

batch_size = 1
model = Sequential()
model.add(LSTM(50, return_sequences=True, batch_input_shape=(batch_size, look_back, 1), stateful=True))
model.add(LSTM(100, stateful=True))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
for i in range(1):
	model.fit(trainX, trainY, epochs=1, batch_size=batch_size, verbose=1, shuffle=False)
	model.reset_states()


trainPredict = model.predict(trainX, batch_size=batch_size)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])

testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

print("len of testY",len(testY[0]))
plt.plot(testY[0,:400],'r',testPredict[:400,0],'b')
plt.show()

testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print("Test Score:",testScore)

trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print("Train Score:",trainScore)

plt.plot(trainY[0,:400],'r',trainPredict[:400,0],'b')
plt.show() 
