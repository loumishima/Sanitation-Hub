#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:57:03 2019

@author: gather3
"""

from Organisations import Organisation, Partner
from Users import User

import pandas as pd

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

Gather = Partner('Gather', '000')

print('----------------- After adding to the organisation -----------------')
Gather.addMember( database, Email = 'luiz.h@abc.com')
print('Members')
print([type(user) for user in Gather.members])
print(Gather.members[0])
print([user.firstName for user in Gather.members])
print('Database')
print([user.firstName for user in database])

Gather.removeMember( database, Email = 'luiz.h@abc.com')

print('----------------- After removing from the organisation -----------------')
print('Members')
print([user.firstName for user in Gather.members])
print('Database')
print([type(user) for user in database])
print([user.firstName for user in database])

for users in database:
    Gather.addMember(database, users.email)

print('----------------- Members -----------------')
print([user.firstName for user in Gather.members])

file = pd.read_csv("Risk_Toilets_Final.csv")
Gather.members[0].addDataset("teste", file)

x = Gather.members[0].viewDataStats(1)
print(x)