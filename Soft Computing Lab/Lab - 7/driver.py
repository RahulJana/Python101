from Perceptron import Perceptron
import pandas as pd
from sklearn.model_selection import train_test_split
#read data from .csv file
data=pd.read_csv("iris.csv")
data.columns=["petal_length","petal_width","sepal_length","sepal_width","class"]
classes=data["class"]
data=data.drop(columns="class")
#splitting test and train data for iris
x_train,x_test,y_train,y_test=train_test_split(data,classes)
model=Perceptron()
model.fit(x_train,y_train,0.5,10)
pred=model.predict(x_test)
print("accuracy: ",model.accuracy(pred,y_test))
print("weights: ",model.getweights())
