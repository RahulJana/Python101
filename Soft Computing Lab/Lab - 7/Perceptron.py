import numpy as np
class Perceptron:
    def __init__(self):
        self.weights=[]

    #activation function
    def activation(self,data):
        #initializing with threshold value
        activation_val=self.weights[0]
        activation_val+=np.dot(self.weights[1:],data)
        return 1 if activation_val>=0 else 0

    def fit(self,X,y,lrate,epochs):
        #initializing weight vector
        self.weights=[0.0 for i in range(len(X.columns)+1)]
        #no.of iterations to train the neural network
        for epoch in range(epochs):
            print(str(epoch+1),"epoch has started...")
            for index in range(len(X)):
                x=X.iloc[index]
                predicted=self.activation(x)
                #check for misclassification
                if(y.iloc[index]==predicted):
                    pass
                else:
                    #calculate the error value
                    error=y.iloc[index]-predicted
                    #updation of threshold
                    self.weights[0]=self.weights[0]+lrate*error
                    #updation of associated self.weights acccording to Perceptron training rule
                    for j in range(len(x)):
                        self.weights[j+1]=self.weights[j+1]+lrate*error*x[j]

    #training perceptron for the given data
    def predict(self,x_test):
        predicted=[]
        for i in range(len(x_test)):
            #prediction for test set using obtained weights
            predicted.append(self.activation(x_test.iloc[i]))
        return predicted
    
    def accuracy(self,predicted,original):
        correct=0
        lent=len(predicted)
        for i in range(lent):
            if(predicted[i]==original.iloc[i]):
                correct+=1
        return (correct/lent)*100

    def getweights(self):
        return self.weights