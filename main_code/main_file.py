import os
import numpy as np
from NeuralNetwork import NeuralNetwork
import utils as utils
import pandas as pd
from sklearn import preprocessing
from dht11 import *
from mq135 import *
from mq_7 import *
from mq_2 import *
from dht11_example import *
import sys, time
from array import *
from RPi import GPIO
from array import *
from RPLCD.gpio import CharLCD
GPIO.setwarnings(False)
csv_filename = "mq_dataset.csv"	
hidden_layers = [5] # number of nodes in hidden layers i.e. [layer1, layer2, ...]
eta = 0.1 # learning rate
n_epochs = 300 # number of training epochs
n_folds = 2
 # number of folds for cross-validation
seed_crossval = 1 # seed for cross-validation
seed_weights = 1 # seed for NN weight initialization

    # ===================================
    # Read csv data + normalize features
    # ===================================
print("Reading '{}'...".format(csv_filename))
X, y, n_classes = utils.read_csv(csv_filename, target_name="Dangerous Degree", normalize=True)
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
  print(X_train)
        #print(y_train)
        # Build neural network classifier model and train
  model = NeuralNetwork(input_dim=d, output_dim=n_classes,
                              hidden_layers=hidden_layers, seed=seed_weights)
  model.train(X_train, y_train, eta=eta, n_epochs=n_epochs)

        # Make predictions for training and test data
  ypred_train = model.predict(X_train)
        #print(ypred_train)
  ypred_valid = model.predict(X_valid)
        #print(ypred_valid)
        
        
        # Compute training/test accuracy score from predicted values
  acc_train.append(100*np.sum(y_train==ypred_train)/len(y_train))
  acc_valid.append(100*np.sum(y_valid==ypred_valid)/len(y_valid))

        # Print cross-validation result
  print(" Fold {}/{}: acc_train = {:.2f}%, acc_valid = {:.2f}% (n_train = {}, n_valid = {})".format(i+1, n_folds, acc_train[-1], acc_valid[-1], len(X_train), len(X_valid)))

    # ===================================
    # Print results
    # ===================================
print("  -> acc_train_avg = {:.2f}%, acc_valid_avg = {:.2f}%".format(sum(acc_train)/float(len(acc_train)), sum(acc_valid)/float(len(acc_valid))))


lcd = CharLCD(pin_rs=15, pin_rw=18,pin_e=16,pins_data=[31,32,33,35],numbering_mode=GPIO.BOARD,cols=16,rows=2)

my_file=open('mq_test.csv','a')
my_file.write("Temperature,Humidity,LPG,Smoke,CH4,Butane,CO,NH3,CO2,Alcohol,Acetone,Toluene,Benzene\n")
my_file.close()

print("Press CTRL+C to abort.")
mq = MQ();
mq7 = MQ7()
mq135 = MQ135()
a=A()
while True:
  myfile = open('mq_test.csv','w+')
  for i in range(0,20):
      perc_4=a.demo()     
      lcd.write_string("Temperature: "+str(perc_4[0])+" C")
      time.sleep(2)
      lcd.clear()
      myfile.write("%d"%(perc_4[0]))
      myfile.write(",")
      lcd.write_string("Humidity: "+str(perc_4[1]))
      time.sleep(2)
      lcd.clear()
      myfile.write("%d"%(perc_4[1]))
      myfile.write(",")
      perc = mq.MQPercentage()
      lcd.write_string("LPG: "+str(perc[0])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc[0]))
      myfile.write(",")
      lcd.write_string("SMOKE: "+str(perc[1])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc[1]))
      myfile.write(",")
      lcd.write_string("METHANE: "+str(perc[2])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc[2]))
      myfile.write(",")	
      lcd.write_string("BUTANE: "+str(perc[3])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc[3]))
      myfile.write(",")
      perc_2 = mq7.MQPercentage()
      lcd.write_string("CO: "+str(perc_2)+" ppm")	
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_2))
      myfile.write(",")
      perc_3 = mq135.MQPercentage()
      lcd.write_string("NH3: "+str(perc_3[0])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[0]))
      myfile.write(",")
      lcd.write_string("CO2: "+str(perc_3[1])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[1]))
      myfile.write(",")
      lcd.write_string("ALCOHOL: "+str(perc_3[2])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[2]))
      myfile.write(",")
      lcd.write_string("ACETONE: "+str(perc_3[3])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[3]))
      myfile.write(",")
      lcd.write_string("TOLUENE: "+str(perc_3[4])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[4]))
      myfile.write(",")
      lcd.write_string("BENZENE: "+str(perc_3[5])+" ppm")
      time.sleep(2)
      lcd.clear()
      myfile.write("%5f"%(perc_3[5]))
      myfile.write("\n")
      print("_________________________________________")
  myfile.close()
  start_time = time.time()

  csv_file_2 = pd.read_csv("mq_test.csv")
  X_test = csv_file_2.iloc[:,:]
  X_test = preprocessing.normalize(X_test)
  ypred_test = model.predict(X_test)
  print(ypred_test)
  print("---%s seconds--" %(time.time()-start_time))
  for j in range(len(ypred_test)):
      if (ypred_test[j]==2):
	  print("Dangerous gas")
          lcd.write_string("Dangerous gas")
          os.system('echo "' + 'Dangerous gas' + '" | festival --tts')
          time.sleep(5)
      	  from twilio.rest import Client
          account_sid = "AC8fac226e310b4358097fc803c3942ffd"
          auth_token = "0a0a98ca64383dc0283fcf47d7adeaac"
          client = Client(account_sid,auth_token)
          message = client.api.account.messages.create(to="+919958784884",from_="+13304731363",body="Khatra Bhaago:(....")
          import time
          import RPi.GPIO as gpio
          gpio.setwarnings(False)
          gpio.setmode(gpio.BOARD)
          gpio.setup(7,gpio.OUT)
          try:
		while True:	
			gpio.output(7,0)
			time.sleep(.2)
			gpio.output(7,1)
			time.sleep(.2)
	  except KeyboardInterrupt:
		gpio.cleanup()
	  	exit
      else:
          print("Optimal")
	  lcd.write_string("Optimal !!")
          os.system('echo "' + 'Not dangerous for health' + '" | festival --tts')
          time.sleep(5)  


