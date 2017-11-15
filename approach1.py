import pandas as pd
import seaborn as sns
import numpy
import matplotlib.pyplot as plt
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
	return numpy.array(dataX), numpy.array(dataY)

data = pd.read_csv('finalDataForSampleEdgeSorted.csv')

# Anamoly removal
data = data.drop(data.loc[data['duration'] > 30].index)
data = data.drop(data.loc[data['duration'] < 5].index)
data = data[:1000]

plt.plot(data['duration'][:200])
plt.ylabel('duration')
plt.xlabel('observation number')
plt.show()

# fix random seed for reproducibility
numpy.random.seed(7)

dataset = data['duration'].values.astype('float32').reshape((-1,1))

print "Normalising Data..."
# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))

print "creating Datasets.."
# reshape into X=t and Y=t+1
look_back = 12
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

print "creating Model.."
# create and fit the LSTM network
model = Sequential()
model.add(LSTM(50, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
print "Learning"
model.fit(trainX, trainY, epochs=3, batch_size=1, verbose=1)

print "Predicting..."
# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

print "Inverse transforming..."
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
print "computing error..."
# calculate root mean squared error

trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))



trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0])) / trainY[0].mean()
print('Train Score: %.2f Relative RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0])) / testY[0].mean()
print('Test Score: %.2f Relative RMSE' % (testScore))

trainMAPE = numpy.mean(numpy.abs((trainY[0] - trainPredict[:,0]) / trainY[0])) * 100
print('Train Score: %.2f MAPE' % (trainMAPE))
testMAPE = numpy.mean(numpy.abs((testY[0] - testPredict[:,0]) / testY[0])) * 100
print('Test Score: %.2f MAPE' % (testMAPE))


print("len of testY",len(testY[0]))
plt.plot(testY[0,:400],'r',testPredict[:400,0],'b')
plt.show()

plt.plot(trainY[0,:400],'r',trainPredict[:400,0],'b')
plt.show() 
