import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


time_x = []
value_y =[]
x_data=[]
y_data=[]
#set file name
filename="圓椒照光0318"
# set title 
title = "circleL 0318"
file_ = filename+".csv"
# set lower and upper boundary
lower_bound = 120 # minute unit
upper_bound = 360



#read csv file 
with open(file_,"r") as f:
    content = csv.reader(f)
    count = 1 
    for data in content:
        x = int(data[2])/60 # x is second, tranform data to minute
        y = float(data[3]) # y is sensor value
        # reduce data points
        if (count%5 == 0):
            time_x.append(x)
            value_y.append(y)
        count+=1
        # time_x.append(x)
        # value_y.append(y)
        # get range for analysis
    for x,y in zip(time_x,value_y):
        if (lower_bound<x<upper_bound):
            x_data.append(x)
            y_data.append(y)
        


   

# convert x_data and y_data into array type.
x_data = np.array(x_data)
y_data=np.array(y_data)
x_data = np.reshape(x_data,(len(x_data),1))
y_data=np.reshape(y_data,(len(y_data),1))

# create regr object for analysis
regr = linear_model.LinearRegression(fit_intercept=True)
regr.fit(x_data, y_data)
y_predict = regr.predict(x_data) # produce predicted y data

# output csv file for figure in report
''''
with open('output.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  for tt, vv, time, pp in zip(time_x, value_y, x_data, y_predict):
      writer.writerow([tt,vv," ",time,pp])
'''

# show parameter results
plt.text(280,3000,'Mean squared error: %.2f '  % mean_squared_error(y_data, y_predict) )
plt.text(280,2800,'Variance score: %.2f' % regr.score(x_data, y_data) )
plt.text(280,2600,"Total data points: %d" % len(time_x) )
plt.text(280,2400,"Analyzed points: %d" % len(x_data))
plt.text(280,2000,"y = %.2f -  %.2f X Time" %(regr.intercept_,-regr.coef_[0]))

#draw scatter plot of whole data and draw a regressin line 
plt.scatter(time_x,value_y,s=2)
plt.plot(x_data,y_predict,color="red")

# set x , y axis range and interval
plt.xticks(range(0,500,60))
plt.yticks(range(0,4000,500))
plt.xlabel("Time(minute)")
plt.ylabel('Sensor value')
plt.xlim((0,480))
plt.ylim((0,3500))
plt.title(title)


plt.show()

