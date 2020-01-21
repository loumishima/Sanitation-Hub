from .models import StatsResumed, Dataset
import pandas as pd
import numpy as np
import folium
from folium import plugins
from random import randint
import functools


def getCredentials(user, function):
    ''' 
    Verify what type of user is trying to access, 
    and depending on that, has the access
    granted or denied

    if the user is not linked to an organisation,
    an exception is raised, else, the user executes
    a function with a boolean value.
    '''
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
    '''
    Render a map with the folium library

    if the user is not a hub member the user should see only the general risk map
    (function still to be developed), else, the user can see both general and specific
    maps (the user can only sees the specific map if he/she has a dataset uploaded).
    '''
    generalMap = 'Show premade map (Normally the risk map)'
    if limited:
        # TODO: Load the ArcGis model here with folium and something similar to RGDAL.
        return [generalMap]
    else:
        # Find the first dataset uploaded by the user
        x =  Dataset.objects.filter(organisation_id = user.organisation_id)[0].filename
        df = pd.read_csv(x.path)

        m = folium.Map(location=[np.mean(df['latitude']), np.mean(df['longitude'])],tiles='Stamen Terrain')

        # If you want the markers grouped by place, 
        #mc = plugins.MarkerCluster()
        
        for index, location in df.iterrows():
            #mc.add_child(folium.Marker([location['latitude'], location['longitude']])).add_to(m)
            folium.Marker([location['latitude'], location['longitude']], popup=location['Final_Risk']).add_to(m)
        return [ m._repr_html_(), generalMap]
        

def showStats(limited, user):
    '''
    Load general statistics uploaded by the data analyst and dataset statistics
    (function still to be developped).

    The data analyst is responsible to determinate what statistics are going to be available,
    and add that pattern to the specific stats as well.
    '''
    obj = list(StatsResumed.objects.filter(id=1).values())
    for row in obj:
        result = row
    if limited:
        return [result]
    # TODO: Add the specific data functionality here, normally pandas summarise function.
    else:
        return [result, {'//Stats about company data//' : '//Value about company data//'}]

def getProviders(limited,user = None):
    if limited:
        return 'General'
    else:
        return ['People using Toilets', 'Last time cleaned']

def getData(limited, user = None):
    '''
    Return a chart with the user data statistics and general statistics (still to be developed).

    For now, the only specific statistic available is the average value.
    '''

    #TODO: Change the random distribution to a statistic about all data.
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
            # TODO: Add the correct exception here in case of not finding any dataset
            pass
        # TODO: Add more complex statistics
        df = df.groupby(by='id').mean()
        detailedData = df[['people_usi', 'last_clean']]
        return detailedData.values.T.tolist()
    






