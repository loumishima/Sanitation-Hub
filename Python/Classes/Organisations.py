#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:57:50 2019

@author: gather3
"""

from datetime import datetime as dt
from Users import User, SuperUser
from Dataset import Dataset

# =============================================================================
# ---------------------------- Organisation -----------------------------------
# =============================================================================
class Organisation():
    
    def __init__(self, name, idOrg, dateEntrance = dt.now()):
        self.name = name
        self.dateEntrance = dateEntrance
        self.idOrg = idOrg
        self.members = list()
        
    def addMember(self, database, Email):
        if Email is None:
            raise Exception("You need an Email to link the user to the organisation")
            
        result = [user for user in database if user.email == Email]
        for item in result:
            newItem = SuperUser(item, self)
            self.members.append(newItem)
    
    def viewDataStats(self):
        #Load the stats directly from db
        #Load the risk map / Shapefiles from QGIS
        
        return 0
            
    def removeMember(self, database, Email):
        if Email is None:
            raise Exception("You need an Email to link the user to the organisation")
            
        result = [user for user in self.members if user.email == Email]
        for user in result:
            self.members.remove(user)
            #newUser = User(user.firstName, user.lastName, user.email, user.login, user.password, user.phone)

# =============================================================================
# ---------------------------- Partner ----------------------------------------
# =============================================================================  
        
class Partner(Organisation):
    
    def __init__(self, name, idOrg, dateEntrance = dt.now() ):
        super().__init__(name, idOrg, dateEntrance)
        self.datasets = list()
        
        
    def viewDataStats(self, Data = 0):
        super().viewDataStats()
        #Load Specifics datasets
        if not Data: 
            for ds in self.datasets:
                ds.createAnalysis()
                
        if Data:
            try:
                stats = self.datasets[abs(Data) - 1].createAnalysis()
                return stats
            except:
                print("Your Organisation don't have this many datasets, try a lower value")
            
        
