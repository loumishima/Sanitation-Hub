#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:39:42 2019

@author: gather3
"""
import pandas as pd
from datetime import datetime as dt

class Dataset():
    def __init__(self,filename, file, ipAddress, location, latitude, longitude):
        self.filename = filename
        self.file = file
        self.date = dt.now()
        self.ipAddress = ipAddress
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        
        

    # =============================================================================
    # !!!! Data validation Here !!!!  
    # =============================================================================
    
    @property
    def file(self):
        #print('called getter')
        return self._file
    @filename.setter
    def file(self, value):
        self._file = value
        