import numpy as np
import pandas as pd

import json
import pickle

import warnings
warnings.filterwarnings("ignore")
import config


class PredictionData():
    def __init__(self, age,marital,education,default,balance,housing,loan,contact,day,month,duration,campaign,pdays,previous,job,poutcome):


        self.age	    =	age
        self.education	=	education
        self.default	=	default
        self.balance	=	balance
        self.housing	=	housing
        self.loan	    =	loan
        self.day	    =	day
        self.month	    =	month
        self.duration	=	duration
        self.campaign	=	campaign
        self.pdays	    =	pdays
        self.previous	=	previous
        self.poutcome   =   poutcome

        # # input for one-hot encoding
        self.job = "job_" + job
        self.marital = "marital_" + marital
        self.contact = "contact_" + contact
        

    def load_models(self):
        #fitted model
        with open(config.MODEL_FILE_PATH, "rb") as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH, "r") as f:
            self.json_data = json.load(f)

        with open(config.SCALLING_FILE_PATH, "rb") as f:
            self.StandardScaler = pickle.load(f)


    def get_prediction(self):

        self.load_models()   # Creating instance function of model and json_data

        # # input for label encoding
        self.education  =   self.json_data['education'][self.education]
        self.default    =   self.json_data['default'][self.default]
        self.housing    =   self.json_data['housing'][self.housing]
        self.loan       =   self.json_data['loan'][self.loan]
        self.month      =   self.json_data['month'][self.month]

        # index of one-hot encodded columns
        if self.job in list(self.json_data['best_features']):
            job_index = self.json_data['columns'].index(self.job)

        if self.marital in list(self.json_data['best_features']): 
            marital_index = self.json_data['columns'].index(self.marital)
            
        if self.contact in list(self.json_data['best_features']): 
            contact_index = self.json_data['columns'].index(self.contact)

        # if KNN Model is used
        # conversion of scaled variables
        scale_features_values=[self.age,self.education,self.balance,self.day,self.month,
                               self.duration,self.campaign,self.pdays,self.previous]

        self.age       =self.StandardScaler.transform([scale_features_values])[0][0]
        self.education =self.StandardScaler.transform([scale_features_values])[0][1]
        self.balance   =self.StandardScaler.transform([scale_features_values])[0][2]
        self.day       =self.StandardScaler.transform([scale_features_values])[0][3]
        self.month     =self.StandardScaler.transform([scale_features_values])[0][4]
        self.duration  =self.StandardScaler.transform([scale_features_values])[0][5]
        self.campaign  =self.StandardScaler.transform([scale_features_values])[0][6]
        self.pdays     =self.StandardScaler.transform([scale_features_values])[0][7]
        self.previous  =self.StandardScaler.transform([scale_features_values])[0][8]



        test_array = np.zeros(len(self.json_data['columns']))

        # Note: put feature values in front of correct feature index
        test_array[0] = self.age
        test_array[1] = self.education
        test_array[2] = self.default
        test_array[3] = self.balance
        test_array[4] = self.housing
        test_array[5] = self.loan
        test_array[6] = self.day
        test_array[7] = self.month
        test_array[8] = self.duration
        test_array[9] = self.campaign
        test_array[10] = self.pdays
        test_array[11] = self.previous

        if self.job in list(self.json_data['best_features']):
            test_array[job_index] = 1   # one-hot encodded if present in feature list
        
        if self.marital in list(self.json_data['best_features']):
            test_array[marital_index] = 1   # one-hot encodded if present in feature list
            
        if self.contact in list(self.json_data['best_features']):
            test_array[contact_index] = 1   # one-hot encodded if present in feature list


        best_feature_indices=[]
        for i in self.json_data['best_features']:
            m=self.json_data['columns'].index(i)
            best_feature_indices.append(m)
        best_test_array = test_array[best_feature_indices]


        prediction = self.model.predict([best_test_array])[0]

        if prediction==1:
            return "Client would be subscribed the product (bank term deposit)."
        else:
            return "Client would not be subscribed the product (bank term deposit)."


if __name__ == "__main__":
    age=58
    job='management'
    marital='married'
    education='tertiary'
    default='no'
    balance=2143
    housing='yes'
    loan='no'
    contact='unknown'
    day=5
    month='may'
    duration=261
    campaign=1
    pdays=-1
    previous=0
    poutcome='unknown'

    predict = PredictionData(age,marital,education,default,balance,housing,loan,contact,day,month,duration,campaign,pdays,previous,job,poutcome)
    
    prediction = predict.get_prediction()

    if prediction==1:
        print("Client would be subscribed the product (bank term deposit).")
    else:
        print("Client would not be subscribed the product (bank term deposit).")