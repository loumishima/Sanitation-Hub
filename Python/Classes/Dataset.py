#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:39:42 2019

@author: gather3
"""
import pandas as pd
from datetime import datetime as dt
import random
import string
from Analysis import Map, Statistics, Plot

class Dataset():
    def __init__(self,filename, file, ipAddress = 0, location = 0, latitude = 0, longitude = 0):
        self.idDs = None
        self.filename = filename
        self.file = file
        self.date = dt.now()
        self.ipAddress = ipAddress
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.ready = False
        
    # =============================================================================
    # Latitude    
    # =============================================================================
    @property
    def latitude(self):
        #print('called getter')
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value is not None:
            self._latitude = float(round(value, 3))
        else:
            self._latitude = 0
 
    # =============================================================================
    # Longitude   
    # =============================================================================
    
    @property
    def longitude(self):
        #print('called getter')
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value is not None:
            self._longitude = float(round(value, 3))
        else:
            self._longitude = 0
    
    # =============================================================================
    # Ip Address   
    # =============================================================================
    @property
    def ipAddress(self):
        #print('called getter')
        return self._ipAddress

    @ipAddress.setter
    def ipAddress(self, value):
        lettersAndDigits = string.ascii_letters + string.digits
        self._ipAddress = ''.join(random.choice(lettersAndDigits) for i in range(8))
        
    # =============================================================================
    # IDs
    # =============================================================================
    @property
    def idDs(self):
        #print('called getter')
        return self._idDs

    @idDs.setter
    def idDs(self, value):
        lettersAndDigits = string.ascii_letters + string.digits
        self._idDs = ''.join(random.choice(lettersAndDigits) for i in range(8))

    # =============================================================================
    # !!!! Data validation !!!!  
    # =============================================================================
           
    @property
    def file(self):
        #print('called getter')
        return self._file
    
    
    @file.setter
    def file(self, value):
        self.verifyEssentialColumns(value)
        self._file = self.typeValidation(value) 
            
                
    #Check if the dataset has all the columns required for the stats and plots            
    def verifyEssentialColumns(self, df ):
        columns = ['latitude','longitude','capacity','people_usi','last_clean','storage_ty']
        for col in df.columns:
            if col in columns:
                columns.remove(col)
                
        if columns:
            raise Exception(f"Your dataset don't have all the required columns {columns}")
    
    #Validation to check if the columns are floats integers or in the adequate category
    def typeValidation(self,df):
        floats = ['latitude','longitude','capacity']
        integer = ['people_usi','last_clean']
        category = ['storage_ty']
        for i,j in df.iteritems():
            if i in floats:
                df[i] = self.verifyFloat(j)
            elif i in integer:
                df[i] = self.verifyInteger(j)
            elif i in category:
                self.verifyCategory(j)
                pass       
        return df
    
    # =============================================================================
    # !!!! Aux validation funcitions !!!!  
    # =============================================================================
     
    
    def verifyFloat(self, df):
        if(df.dtype != 'object'):
            return df.astype(float)
        else:
            raise Exception('Not the correct type')
    
    def verifyInteger(self,df):
        if(df.dtype != 'object'):
            pass
        else:
            raise Exception('Not the correct type')
        if(df.dtype != 'int'):
            return df.astype(int)
         
    def verifyCategory(self,df):
        pass
    
    # =============================================================================
    # !!!! Other functionalities !!!!  
    # =============================================================================
    
    def __str__(self):
        
        return f'Filename: {self.filename}' + \
    f'\n' + f'Data types: \n {self.file.dtypes}' + '\n' + f'Posted in: {self.date}'
        
    def cleanData(self):
        
        #Removing any Nulls in the essential columns from the dataset
        print(self.file.size)
        self.file.dropna(axis = 'index',
                         how = 'any',
                         subset = ['latitude','longitude','capacity','people_usi','last_clean','storage_ty'],
                         inplace = True)
        
        # Remove row if the Latitude's absolute value is bigger than 90 degrees
        # Remove row if the Longitude's absolute value is bigger than 180 degrees
        self.file = self.file[(abs(self.file.latitude) < 90) | (abs(self.file.longitude) < 90)]
        pass
    
    def sendToAnalyst(self):
        #Send dataset to an FTP server for the analyst's deep cleaning and analysis 
        #STILL TO DEVELOP
        pass
    
    def loadFromDatabase(self):
        #update the dataset with the cleaned data by the analyst
        #Load from the database based on the ID
        #STILL TO DEVELOP
        fileFromDB = pd.read_csv("Risk_Toilets_Final.csv") #Sub it from the db load
        self.file = fileFromDB
        pass
    
    def createAnalysis(self):
        dsMap = Map(self.file)
        dsStats = Statistics(self.file, columns = ['latitude','longitude','capacity','people_usi','last_clean','storage_ty'])
        #dsPlots = Plot()
        
        return (dsStats.generateStats(), dsMap.createMap())
        
    
if __name__ == "__main__":
    
    file = pd.read_csv("Risk_Toilets_Final.csv")
    ds = Dataset('a', file)
    print(ds)
    ds.cleanData()
    