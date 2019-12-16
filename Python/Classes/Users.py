#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:58:36 2019

@author: gather3
"""
import re
from datetime import datetime as dt
from Dataset import Dataset

# =============================================================================
# ---------------------------------- User -------------------------------------
# =============================================================================      
        
class User():
    
    def __init__(self, firstName, lastName, email, login, password, phone = 0):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.login = login
        self.password = password
        self.phone = phone
        self.dateCreation = dt.now()
        
    # =============================================================================
    # Name properties 
    # =============================================================================
    @property
    def firstName(self):
        #print('called getter')
        return self._firstName
    
    @firstName.setter
    def firstName(self, value):
        if len(value) < 3:
            raise Exception(f"Your first name can't have less than 3 characters")
        if len(value) > 50:
            raise Exception(f"Your first name is too big, maybe you should break into first and last name")
        if re.search("(?! )(?!')([0-9]|\W|_)", value):
            raise Exception(f"Your name cant have special characters!")
        self._firstName = value

    @property
    def lastName(self):
        #print('called getter')
        return self._lastName
    
    @lastName.setter
    def lastName(self, value):
        if len(value) < 2:
            raise Exception(f"Your last name can't have less than 3 characters")
        if len(value) > 100:
            raise Exception(f"Your first name is too big, maybe you should break into first and last name")
        if re.search("(?! )(?!')([0-9]|\W|_)", value):
            raise Exception(f"Your name cant have special characters!")
        self._lastName = value
            
    # =============================================================================
    # Email properties 
    # =============================================================================
    @property
    def email(self):
        #print('called getter')
        return self._email
    @email.setter
    def email(self, value):
        if not re.search("^.+@\w{3,}\.[^ ]+", value):
            raise Exception("Your email doesn't have the standard format")
        self._email = value
        
    # =============================================================================
    # Login properties
    # =============================================================================
    
    @property
    def login(self):
        #print('called getter')
        return self._login
    @login.setter
    def login(self, value):
        if re.search('^[\W| ]+', value):
            raise Exception('You cant start your Login with a special character')
        if len(value) > 50:
            raise Exception(f"Your Login is too big!")
        self._login = value
        
    # =============================================================================
    # Password properties
    # =============================================================================
    
    @property
    def password(self):
        #print('called getter')
        return self._password
        pass
    @password.setter
    def password(self, value):
        if len(value) < 11:
            raise Exception('Your password is too short, you must have a password with at least 12 characters')
        if value is self.login:
            raise Exception("Don't use you login as password anywhere, please")
        if not re.search('[a-z]', value):
            raise Exception('You must have at least on lowercase character in your password')
        if not re.search('[0-9]', value):
            raise Exception('You must have at least on number in your password')
        if not re.search('[A-Z]', value):
            raise Exception('You must have at least on uppercase character in your password')
        self._password = value
        
    # =============================================================================
    # Phone properties    
    # =============================================================================
    
    @property
    def phone(self):
        #print('called getter')
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = value
        
    # =============================================================================
    # Date properties    
    # =============================================================================
    
    @property
    def dateCreation(self):
        #print('called getter')
        return f'{self._dateCreation.day}' + '/' + \
    f'{self._dateCreation.month}' + '/' + \
    f'{self._dateCreation.year}'
    @dateCreation.setter
    def dateCreation(self, value):
        self._dateCreation = value        
        
        
    def __str__(self):
        return f'Name: {self.firstName} {self.lastName}' + '\n' + f'Email: {self.email}' + '\n' + \
    f'Login: {self.login}' + '\n' + f'Phone: {self.phone}' + '\n' + f'Created on: {self.dateCreation}' 
    
 
# =============================================================================
# ------------------------------ SuperUser ------------------------------------
# =============================================================================          
class SuperUser(User):
    
    def __init__(self, user, organisation):
        super().__init__(user.firstName, user.lastName, user.email, user.login, user.password, user.phone)
        self.organisation = organisation
        
    
    def addDataset(self, filename, dataset, ipAddress = 0, location= 0, latitude = 0, longitude= 0):
        from Organisations import Partner
        if type(self.organisation) is Partner:
            try:
                ds = Dataset(filename, dataset, ipAddress, location, latitude, longitude)
            except Exception:
                print('Your data is not valid! Follow our docs to know how to prepare your data')
            else:
                self.organisation.datasets.append(ds)
        else:
            raise Exception('Your company has no permition to upload datasets! Contact us for more details')

        
    def viewDataStats(self, Data = 0):
        return self.organisation.viewDataStats(Data)
            
    def __str__(self):
        return super().__str__() +'\n'+ f'Organisation type: {type(self.organisation)}'
        