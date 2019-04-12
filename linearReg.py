import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
file_name = "blank0312_clip.csv"
time_x = []
value_y =[]



with open(file_name,"r") as f:
    content = csv.reader(f)
    

    for data in content:
        x = int(data[2])
        y = float(data[3])
        if (x%5 == 0 and x>10800):
            time_x.append(x)
            value_y.append(y)

        


time_x = np.array(time_x)
value_y=np.array(value_y)

time_x = np.reshape(time_x,(len(time_x),1))
value_y=np.reshape(value_y,(len(value_y),1))

regr = linear_model.LinearRegression(fit_intercept=True)
regr.fit(time_x, value_y)
y_predict = regr.predict(time_x)
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(value_y, y_predict))
# Explained variance score: 1 is perfect prediction
#print('Variance score: %.2f' % r2_score(value_y, y_predict))
print('Variance score: %.2f' % regr.score(time_x, value_y))
print("y intercept:%.2f" %regr.intercept_ )
plt.scatter(time_x,value_y,s=2)
plt.plot(time_x,y_predict,color="red")


plt.axis([0,21600,0,3500])
plt.show()

