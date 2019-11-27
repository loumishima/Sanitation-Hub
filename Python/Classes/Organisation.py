#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:27:10 2019

@author: gather3
"""
from User import User,SuperUser
from datetime import datetime as dt

class Organisation():
    
    def __init__(self, name, idOrg, isHubMember = False ):
        self.name = name
        self.dateEntrance = dt.now()
        self.idOrg = idOrg
        self.isHubMember = isHubMember
        self.members = list()
        
    def addMember(self, database, Email):
        if Email is None:
            raise Exception("You need an Email to link the user to the organisation")
            
        result = [user for user in database if user.email == Email]
        for item in result:
            newItem = SuperUser(item, self)
            self.members.append(newItem)
            database.remove(item)
            
            
    def removeMember(self, database, Email):
        if Email is None:
            raise Exception("You need an Email to link the user to the organisation")
        result = [user for user in self.members if user.email == Email]
        for user in result:
            self.members.remove(user)
            newUser = User(user.firstName, user.lastName, user.email, user.login, user.password, user.phone)
            database.append(newUser)
     
        
        
        
if __name__ == "__main__":
    
    database = [
            User('Luiz', 'Rodrigues', 'luiz.h@abc.com', 'LHRO', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0'),
            User('Lindsey', 'Noakes', 'lindsey.n@abc.com', 'LNNO', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0'),
            User('John', 'Peter Archer', 'john.pa@abc.com', 'JPA', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0'),
            User('Charlie', 'Stubbs', 'charlie.s@abc.com', 'CHST', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0'),
            User('Stephanie', 'Fang', 'steph.f@abc.com', 'STFG', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0'),
            User('Lieven', 'Slenders', 'lieven.s@abc.com', 'LVSL', 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0')
            ]
    print('----------------- Before adding to the organisation -----------------')
    print('Database')
    print([type(user) for user in database])
    print([user.firstName for user in database])
    
    Gather = Organisation('Gather', '000', True)
    
    print('----------------- After adding to the organisation -----------------')
    Gather.addMember( database, Email = 'luiz.h@abc.com')
    print('Members')
    print([type(user) for user in Gather.members])
    print([user.firstName for user in Gather.members])
    print('Database')
    print([user.firstName for user in database])
    
    Gather.removeMember( database, Email = 'luiz.h@abc.com')
    
    print('----------------- After removing from the organisation -----------------')
    print('Members')
    print([user.Name for user in Gather.members])
    print('Database')
    print([type(user) for user in database])
    print([user.firstName for user in database])
    
    