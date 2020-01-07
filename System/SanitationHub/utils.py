from .models import StatsResumed, Dataset
import pandas as pd
import numpy as np
import folium
from folium import plugins
from random import randint
import functools


def getCredentials(user, function):
    @functools.wraps(function)
    def Decorator(*args, **kwargs):
        if user.organisation is None:
            raise Exception("you don't have permission to do that, contact you company to unlock the functionality")
        elif not user.organisation.isHubMember:
            return function(True, user)
        else:
            return function(False, user)
    return Decorator

def showMaps(limited, user):
    generalMap = 'Show premade map (Normally the risk map)'
    if limited:
        return [generalMap]
    else:
        x =  Dataset.objects.filter(organisation_id = user.organisation_id)[0].filename
        df = pd.read_csv(x.path)

        m = folium.Map(location=[np.mean(df['latitude']), np.mean(df['longitude'])],tiles='Stamen Terrain')

        #mc = plugins.MarkerCluster()
        
        for index, location in df.iterrows():
            #mc.add_child(folium.Marker([location['latitude'], location['longitude']])).add_to(m)
            folium.Marker([location['latitude'], location['longitude']], popup=location['Final_Risk']).add_to(m)

        return [ m._repr_html_(), generalMap]
        

def showStats(limited, user):
    obj = list(StatsResumed.objects.filter(id=1).values())
    for row in obj:
        result = row
    if limited:
        return [result]
    # Add the specific data functionality here
    else:
        return [result, {'//Stats about company data//' : '//Value about company data//'}]


def showCharts(limited,user):
    if limited:
        return 'Functionality reduced - Funding Partner'
    else:
        return 'Unlimited power! - Hub Manager' 


# In case of multiple datasets (Still have to think about it)

def getProviders(limited,user = None):
    if limited:
        return 'General'
    else:
        return ['People using Toilets', 'Last time cleaned']

def getData(limited, user = None):
    data = list()
    partial_data = list()
    for i in range(len(getProviders(limited, None))):
        for i in range(12):
            monthly_info = randint(0,50)
            partial_data.append(monthly_info)
        data.append(partial_data)
        partial_data = list()
    
    if limited:
        return data
    
    else:
        try:
            x =  Dataset.objects.filter(organisation_id = user.organisation_id)[0].filename
            df = pd.read_csv(x.path)
        except expression as identifier:
            #TODO Add the correct exception here
            pass

        df = df.groupby(by='id').mean()
        detailedData = df[['people_usi', 'last_clean']]
        return detailedData.values.T.tolist()
    






