#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


data = pd.read_csv('C:\\Users\\SRIRAM\\Desktop\\ce889assignment\\ce889_dataCollection.csv')


# In[3]:


data_cols = ['X_distance to target', 'Y_distance to target', 'New Vel_Y', 'New Vel_X']
data.columns = data_cols


# In[4]:


data.head()


# In[5]:


data.set_index('X_distance to target')


# In[6]:


data.head()


# In[7]:


#Checking for missing values
data.isnull().sum()


# In[8]:


# Checking for missing values
# Visualizing the missing values
sns.heatmap(data.isnull(), cbar = False)


# In[9]:


# Detecting outliers in 1st input variable
f, ax = plt.subplots(figsize = (10, 8))
x = data['X_distance to target']
ax = sns.boxplot(x)
ax.set_title("visualizing outliers in X_distance to target")
plt.show()


# In[10]:


# Detecting outliers in 2nd input variable
f, ax = plt.subplots(figsize = (10, 8))
x = data['Y_distance to target']
ax = sns.boxplot(x)
ax.set_title("visualizing outliers in Y_distance to target")
plt.show()


# In[11]:


# Detecting outliers in 1st output variable
f, ax = plt.subplots(figsize = (10, 8))
x = data['New Vel_Y']
ax = sns.boxplot(x)
ax.set_title("visualizing outliers in New Vel_Y")
plt.show()


# In[12]:


# Detecting outliers in 2nd output variable
f, ax = plt.subplots(figsize = (10, 8))
x = data['New Vel_X']
ax = sns.boxplot(x)
ax.set_title("visualizing outliers in New Vel_X")
plt.show()


# In[13]:


# Removing Outlier
import scipy.stats as stats
Q1 = data.quantile(q=.25)
Q3 = data.quantile(q=.75)
IQR = data.apply(stats.iqr)

data_clean = data[~((data < (Q1-1.5*IQR)) | (data > (Q3+1.5*IQR))).any(axis=1)]


# In[14]:


data_clean.shape


# In[15]:


data_clean.drop_duplicates()


# In[16]:


data_clean.duplicated()


# In[17]:


data_clean.drop_duplicates(keep = False)


# In[18]:


x = data_clean.iloc[:, 0:2].values
y = data_clean.iloc[:, 2:4].values


# In[19]:


x


# In[20]:


y


# In[21]:


# Data Splitting
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)


# In[22]:


print("Shape of X_train:", x_train.shape)
print("Shape of X_test:", x_test.shape)
print("Shape of y_train:", y_train.shape)
print("Shape of y_test:", y_test.shape)


# In[23]:


x_train


# In[24]:


# Normalization
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)


# In[25]:


from math import exp 
from random import seed
from random import random

def init_network(inputs, hid, outputs):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(inputs + 1)]} for i in range(hid)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(hid + 1)]} for i in range(outputs)]
    network.append(output_layer)
    return network

seed(1)


def activate(weights, inputs):
    activation = weights[-1]   
    for i in range(len(weights)-1):  
        activation += weights[i]*inputs[i]  
    return activation

def transfer(activation):
    return 1.0/(1.0+exp(-activation))         
def forward_prop(network,row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

network = init_network(2,4,2)
row = [1,0,None]
output = forward_prop(network, row)
#print(output)

def transfer_der(output):
    return output*(1-output)

def backward_prop_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)) :
                error = 0.0
                for neuron in network[i+1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j]-neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j]	* transfer_der(neuron['output'])

def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i-1]]            
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]   
            neuron['weights'][-1] += l_rate * neuron['delta']            

def train_network(network,train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_prop(network,row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backward_prop_error(network, expected)
            update_weights(network, row, l_rate)
        print('epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))

seed(1)
weight = [[2.7810836,2.550537003,0],         
    [1.465489372,2.362125076,0],
    [3.396561688,4.400293529,0],
    [1.38807019,1.850220317,0],
    [3.06407232,3.005305973,0],
    [7.627531214,2.759262235,1],
    [5.332441248,2.088626775,1],
    [6.922596716,1.77106367,1],
    [8.675418651,-0.242068655,1],
    [7.673756466,3.508563011,1]]
n_inputs = 2                    
n_outputs = 2 # 
#print(n_inputs)
network = init_network(n_inputs,4,n_outputs)
train_network(network, weight, 0.1, 100, n_outputs)
for layer in network:
 print(layer)


# In[ ]:




