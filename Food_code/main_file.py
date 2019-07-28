from dht11 import *
from dht11_example import *
from mq135 import *
from mq7 import *
from mq2 import *
from mq4 import *
import sys, time
from array import *
from RPi import GPIO
from array import *
import numpy as np
from NeuralNetwork import NeuralNetwork
import utils as utils
import pandas as pd
from sklearn import preprocessing

csv_filename = "food.csv"
hidden_layers = [5] # number of nodes in hidden layers i.e. [layer1, layer2, ...]
eta = 0.1 # learning rate
n_epochs = 100 # number of training epochs
n_folds = 2 # number of folds for cross-validation
seed_crossval = 1 # seed for cross-validation
seed_weights = 1 # seed for NN weight initialization

    # ===================================
    # Read csv data + normalize features
    # ===================================
print("Reading '{}'...".format(csv_filename))
X, y, n_classes = utils.read_csv(csv_filename, target_name="class", normalize=True)
N, d = X.shape
print(" -> X.shape = {}, y.shape = {}, n_classes = {}\n".format(X.shape, y.shape, n_classes))

print("Neural network model:")
print(" input_dim = {}".format(d))
print(" hidden_layers = {}".format(hidden_layers))
print(" output_dim = {}".format(n_classes))
print(" eta = {}".format(eta))
print(" n_epochs = {}".format(n_epochs))
print(" n_folds = {}".format(n_folds))
print(" seed_crossval = {}".format(seed_crossval))
print(" seed_weights = {}\n".format(seed_weights))

    # ===================================
    # Create cross-validation folds
    # ===================================
idx_all = np.arange(0, N)
idx_folds = utils.crossval_folds(N, n_folds, seed=seed_crossval) # list of list of fold indices

    # ===================================
    # Train/evaluate the model on each fold
    # ===================================
acc_train, acc_valid = list(), list()  # training/test accuracy score
print("Cross-validating with {} folds...".format(len(idx_folds)))
for i, idx_valid in enumerate(idx_folds):

        # Collect training and test data from folds
    idx_train = np.delete(idx_all, idx_valid)
    X_train, y_train = X[idx_train], y[idx_train]
    X_valid, y_valid = X[idx_valid], y[idx_valid]

        # Build neural network classifier model and train
    model = NeuralNetwork(input_dim=d, output_dim=n_classes,
                              hidden_layers=hidden_layers, seed=seed_weights)
    model.train(X_train, y_train, eta=eta, n_epochs=n_epochs)

        # Make predictions for training and test data
    ypred_train = model.predict(X_train)
    ypred_valid = model.predict(X_valid)

        # Compute training/test accuracy score from predicted values
    acc_train.append(100*np.sum(y_train==ypred_train)/len(y_train))
    acc_valid.append(100*np.sum(y_valid==ypred_valid)/len(y_valid))

        # Print cross-validation result
    print(" Fold {}/{}: acc_train = {:.2f}%, acc_valid = {:.2f}% (n_train = {}, n_valid = {})".format(i+1, n_folds, acc_train[-1], acc_valid[-1], len(X_train), len(X_valid)))

    # ===================================
    # Print results
    # ===================================
print("  -> acc_train_avg = {:.2f}%, acc_valid_avg = {:.2f}%".format(sum(acc_train)/float(len(acc_train)), sum(acc_valid)/float(len(acc_valid))))

print("Press CTRL+C to abort.")

my_file = open('food_test.csv','a')
my_file.write("MQ2,MQ4,MQ7,MQ135,Temperature,Humidity\n")
my_file.close()
while True:
    myfile = open('food_test.csv','a')
    for i in range(0,1):
      mq = MQ();
      perc = mq.MQPercentage()
      print("MQ2 sensor's resistance Rs = "+str(perc))
      myfile.write("%5f"%perc)
      myfile.write(",")
      mq4 = MQ4()
      perc_2 = mq4.MQPercentage()
      print("MQ4 sensor's resistance Rs = "+str(perc_2))
      myfile.write("%5f"%perc_2)
      myfile.write(",")
      mq7 = MQ7()
      perc_3 = mq7.MQPercentage()
      print("MQ7 sensor's resistance Rs = "+str(perc_3))
      myfile.write("%5f"%perc_3)
      myfile.write(",")
      mq135 = MQ135()
      perc_4 = mq7.MQPercentage()
      print("MQ135 sensor's resistance Rs = "+str(perc_4))
      myfile.write("%5f"%perc_4)
      myfile.write(",")
      a = A()
      perc_5=a.demo()     
      print("Temperature: "+str(perc_5[0]))
      myfile.write("%d"%(perc_5[0]))
      myfile.write(",")
      print("Humidity: "+str(perc_5[1]))
      myfile.write("%d"%(perc_5[1]))
      myfile.write("\n")
	  
      print("_ _ _ _ _ _ _ _ _ _ _ _ _")
    myfile.close()
    csv_file_2 = pd.read_csv("food_test.csv")
    X_test = csv_file_2.iloc[:,:]
    X_test = preprocessing.normalize(X_test)
    ypred_test = model.predict(X_test)
    print(ypred_test)
'''    for i in range(0,len(ypred_test)):
      if (ypred_test==0):
        print("excellent food quality")
        time.sleep(5)
      elif (ypred_test==1):
        print("food quality is good")
        time.sleep(5)
      elif (ypred_test==2):
        print("food is acceptable")
        time.sleep(5)
      elif (ypred_test==3):
        print("food is spoiled")
        time.sleep(5)'''
          
