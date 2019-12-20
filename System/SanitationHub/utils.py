from .models import StatsResumed, Dataset
import pandas as pd
import numpy as np
import folium
from folium import plugins


def getCredentials(user, function):
    def Decorator(*args, **kwargs):
        if user.organisation is None:
            return "you don't have permission to do that, contact you company to unlock the functionality"
        elif not user.organisation.isHubMember:
            return function(True, user)
        else:
            return function(False, user)
    return Decorator

def showMaps(limited, user):
    if limited:
        return 'Show premade map (Normally the risk map)'
    else:
        x =  Dataset.objects.filter(organisation_id = user.organisation_id)[0].filename
        df = pd.read_csv(x.path)

        m = folium.Map(location=[np.mean(df['latitude']), np.mean(df['longitude'])],tiles='Stamen Terrain')

        #mc = plugins.MarkerCluster()
        
        for index, location in df.iterrows():
            #mc.add_child(folium.Marker([location['latitude'], location['longitude']])).add_to(m)
            folium.Marker([location['latitude'], location['longitude']], popup=location['Final_Risk']).add_to(m)

        return m._repr_html_()
        

def showStats(limited, user):
    if limited:
        obj = list(StatsResumed.objects.filter(id=1).values())
        for row in obj:
            return row
    else:
        return {'Stats about data' : 'Value about data'}


def showCharts(limited,user):
    if limited:
        return 'Functionality reduced - Funding Partner'
    else:
        return 'Unlimited power! - Hub Manager' 








