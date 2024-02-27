import numpy as np
import pandas as pd

data = pd.read_csv('C:\\Users\\SRIRAM\\Desktop\\ce889assignment\\ce889_dataCollection.csv')

data_cols = ['X_distance to target', 'Y_distance to target', 'New_Vel_Y', 'New_Vel_X']
data.columns = data_cols

#Checking for missing values
data.isnull().sum()

# Removing Outlier
import scipy.stats as stats
Q1 = data.quantile(q=.25)
Q3 = data.quantile(q=.75)
IQR = data.apply(stats.iqr)

data_clean = data[~((data < (Q1-1.5*IQR)) | (data > (Q3+1.5*IQR))).any(axis=1)]

data_clean.drop_duplicates()

data_clean.drop_duplicates(keep = False)

x = data_clean.iloc[:, 0:2].values
y = data_clean.iloc[:, 2:4].values


from math import exp 
from random import seed
from random import random


weights  =  [0.050027590860284646, 0.7734933169803079, 0.7361689021579728]
class NeuralNetHolder:

    def __init__(self):
        super().__init__()
        
    def init_network(self, inputs, hid, outputs):
        network = list()
        hidden_layer = [{'weights':[random() for i in range(inputs + 1)]} for i in range(hid)]
        network.append(hidden_layer)
        output_layer = [{'weights':[random() for i in range(hid + 1)]} for i in range(outputs)]
        network.append(output_layer)
        return network
    
    def activate(self, weights, inputs):
        activation = weights[-1]
        for i in range(len(weights)-1):
            activation += weights[i]*inputs[i]
        return activation
    
    def transfer(self, activation):
        return 1.0/(1.0+exp(-activation))
    
    def forward_prop(self, network, row):
        inputs = row
        for layer in network:
            new_inputs = []
            for neuron in layer:
                activation = nn.activate(neuron['weights'], inputs)
                neuron['output'] = nn.transfer(activation)
                new_inputs.append(neuron['output'])
            inputs = new_inputs
        return inputs


    def predict(self, dataset):
        dataset = x
       
        def minmax(dataset):
            minmax = list()
            for i in range(len(dataset[0])):
                col_values = [row[i] for row in dataset]
                value_min = min(col_values)
                value_max = max(col_values)
                minmax.append([value_min, value_max])
                return minmax
          
            def normalize_dataset(dataset, minmax):
                for row in dataset:
                    for i in range(len(row)):
                        row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
                     
                        minmax(dataset)
                        normalize_dataset(dataset, minmax)

    
        nn.forward_prop(dataset, row)
    
        return y
        pass

nn = NeuralNetHolder()
network = nn.init_network(2, 4, 2)
row = [1, 0, None]
output = nn.forward_prop(network, row)        
        